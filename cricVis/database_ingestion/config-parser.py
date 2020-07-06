import argparse
import json
import firebase_admin
from firebase_admin import credentials
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

from utils.InitialDataframes import InitialDataframes
from utils.FinalDataframes import FinalDataframes
from utils.GroupedDataframes import GroupedDataframes
from utils.dataframe_to_database import dataframe_to_database

def ingest(configs):
    initial_dataframes = InitialDataframes(configs["InitialDataframes"])
    logging.info("Finished parsing datasets")

    final_dataframes = FinalDataframes(initial_dataframes.final_matches, initial_dataframes.dfs, configs["FinalDataframes"])
    logging.info("Finished creating dataframes")

    final_dataframes_grouped = GroupedDataframes(final_dataframes.dfs, configs["GroupedDataframes"])
    logging.info("Finished grouping dataframes\n")

    dataframe_to_database(final_dataframes_grouped.dfs, configs["DataFrameToDatabase"])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Get the paths to config settings and database instance")

    parser.add_argument('--config_path', '-cp',
                        help="Path to config file from pwd", required=True)

    parser.add_argument(
        '--db_url', '-d', help="URL of Realtime Database", default="https://playercomparison-6dde2.firebaseio.com/")
    parser.add_argument(
        '--cred_path', '-cr', help="Path to secure .json private key from pwd", default="firebase-sdk.json")

    args = parser.parse_args()

    with open(args.config_path) as f:
      configs = json.load(f)

    cred = credentials.Certificate(args.cred_path)

    firebase_admin.initialize_app(cred, {
        'databaseURL': args.db_url
    })


    ingest(configs)
