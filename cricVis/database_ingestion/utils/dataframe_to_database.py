import pandas as pd
import json

from utils.nested_dict import nested_dict
from utils.dict_to_database import dict_to_database

############# Final Collection
def dataframe_to_database(df, configs):
    schema_dict = nested_dict()

    # Function for setting the keys and values of schema_dict dictionaary
    def fill_schema_dict(row, schema_name, fields_list, field_as_key=True):
        if not field_as_key:
            schema_dict[schema_name][row.Index] = fields_list[0]

        else:
            for field in fields_list:
                if type(row.Index) == tuple:
                    if len(row.Index) == 2:
                        schema_dict[schema_name][row.Index[0]][row.Index[1]][field] = getattr(row, field)
                    elif len(row.Index) == 3:
                            schema_dict[schema_name][row.Index[0]][row.Index[1]][row.Index[2]][field] = getattr(row, field)
                    elif len(row.Index) == 4:
                        schema_dict[schema_name][row.Index[0]][row.Index[1]][row.Index[2]][row.Index[3]][field] = getattr(row, field)

                else:   # Index is a single int/string instead of being a tuple
                    schema_dict[schema_name][row.Index][field] = getattr(row, field)

    # Fill the dictionary
    for row in df.itertuples():
        fill_schema_dict(row, **configs)

    # Push dictionary to database
    dict_to_database(schema_dict)
