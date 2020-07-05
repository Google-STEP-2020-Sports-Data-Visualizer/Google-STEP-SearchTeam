from firebase_admin import db

def dict_to_database(db_dict):
    db_ref = db.reference("/")

    schema_names = list(db_dict.keys())
    for schema_name in schema_names:
        schema_ref = db_ref.child(schema_name)

        schema_ref.set(db_dict[schema_name])
        schema_ref.update(db_dict[schema_name])

        print("Successfully pushed {schema} to database!".format(schema=schema_name))
