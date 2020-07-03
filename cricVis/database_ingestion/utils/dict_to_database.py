from firebase_admin import db

def dict_to_database(schema_dict):
    db_ref = db.reference("/")

    schema_name = list(schema_dict.keys())[0]
    schema_ref = db_ref.child(schema_name)

    schema_ref.set(schema_dict[schema_name])

    print("Successfully pushed {schema} to database!".format(schema=schema_name))
