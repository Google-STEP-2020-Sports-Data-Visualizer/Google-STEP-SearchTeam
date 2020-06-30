import json

def dict_to_json_file(dict, file_name):
    out_file = open("json_output/{file_name}.json".format(file_name=file_name), "w")
    json.dump(dict, out_file, indent=2)
