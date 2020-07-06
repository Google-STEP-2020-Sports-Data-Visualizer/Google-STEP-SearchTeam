from firebase_admin import db
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def dict_to_database(db_dict):
    db_ref = db.reference("/")

    schema_names = list(db_dict.keys())
    for schema_name in schema_names:
        schema_ref = db_ref.child(schema_name)

        schema_ref.set(db_dict[schema_name])
        schema_ref.update(db_dict[schema_name])

        logging.info("Successfully pushed {schema} to database!".format(schema=schema_name))
