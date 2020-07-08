from ConfigBasedIngestor.InitialDataframes import InitialDataframes
from ConfigBasedIngestor.FinalDataframes import FinalDataframes
from ConfigBasedIngestor.GroupedDataframes import GroupedDataframes
from ConfigBasedIngestor.dataframe_to_database import dataframe_to_database

import argparse
import json
import firebase_admin
from firebase_admin import credentials
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def initialise_firebase(cred, db_url):
    """
    Initializes a returns a new FireBase app instance in order to gain access
    to the database.

    Parameters
    ----------

    cred: str
        Path to the private key file

    db_url: str
        URL of the database
    """

    # A credential initialized from the JSON certificate private key file.
    cred = credentials.Certificate(cred)

    # Initializes the app
    firebase_admin.initialize_app(cred, {
        'databaseURL': db_url
    })


def ingest(configs):
    """
    Ingests data from plain-text dataset(s) into the database.

    Parameters
    ----------

    configs: dict
        Dictionary of config settings to be passed into the modules of
        ConfigBasedIngestor package in order to ingest data.
    """
    initial_dataframes = InitialDataframes(configs["InitialDataframes"])
    logging.info("Finished parsing datasets")

    final_dataframes = FinalDataframes(initial_dataframes.final_matches,
                                       initial_dataframes.dfs,
                                       configs["FinalDataframes"])
    logging.info("Finished creating dataframes")

    final_dataframes_grouped = GroupedDataframes(final_dataframes.dfs,
                                                 configs["GroupedDataframes"])
    logging.info("Finished grouping dataframes\n")

    dataframe_to_database(final_dataframes_grouped.dfs,
                          configs["DataFrameToDatabase"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Get the paths to config settings and database instance")

    parser.add_argument('--config_path', '-cp',
                        help="Path to config file from pwd", required=True)

    parser.add_argument('--db_url', '-d',
                        help="URL of Realtime Database", required=True)
    parser.add_argument('--cred_path', '-cr',
                        help="Path to secure .json private key from pwd", default="firebase-sdk.json")

    args = parser.parse_args()

    with open(args.config_path) as f:
        configs = json.load(f)

    initialise_firebase(args.cred_path, args.db_url)
    ingest(configs)
