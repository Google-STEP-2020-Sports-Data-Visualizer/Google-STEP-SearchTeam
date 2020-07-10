import json

def dict_to_json_file(db_dict, file_name):
    """
    Converts dictionary to json file

    Parameters
    ----------

    db_dict: dict
        Dictionary containing all the schemas to be added to/updated in the database.

    file_name: str
        Name of the json file to be created; should be same as the name of the
        corresponding schema.
    """

    out_file = open("json_output/{file_name}.json".format(file_name=file_name), "w")
    json.dump(db_dict, out_file, indent=2)
