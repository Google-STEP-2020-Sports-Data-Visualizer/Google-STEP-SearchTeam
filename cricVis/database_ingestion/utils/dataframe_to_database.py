import pandas as pd
import json

from utils.nested_dict import nested_dict
from utils.dict_to_database import dict_to_database

############# Final Collection
def dataframe_to_database(dfs_dict, configs):
    db_dict = nested_dict()
    db_ref_path_length = None

    # Function for setting the keys and values of db_dict dictionaary
    def fill_db_dict(row, schema_name, fields_list, field_as_key=True):
        if not field_as_key:
            db_dict[schema_name][row.Index] = fields_list[0]

            db_ref_path_length = 2

        else:
            for field in fields_list:
                if type(row.Index) == tuple:
                    if len(row.Index) == 2:
                        db_dict[schema_name][row.Index[0]][row.Index[1]][field] = getattr(row, field)

                        db_ref_path_length = 3
                    elif len(row.Index) == 3:
                            db_dict[schema_name][row.Index[0]][row.Index[1]][row.Index[2]][field] = getattr(row, field)

                            db_ref_path_length = 4
                    elif len(row.Index) == 4:
                        db_dict[schema_name][row.Index[0]][row.Index[1]][row.Index[2]][row.Index[3]][field] = getattr(row, field)

                        db_ref_path_length = 5
                else:   # Index is a single int/string instead of being a tuple
                    db_dict[schema_name][row.Index][field] = getattr(row, field)

                    db_ref_path_length = 2

    # Fill the dictionary
    for (dfname, df) in dfs_dict.items():
        for row in df.itertuples():
            fill_db_dict(row, **configs[dfname])

    # Push dictionary to database
    dict_to_database(db_dict, db_ref_path_length)
