import argparse
import json
import firebase_admin
from firebase_admin import credentials

from utils.InitialDataframes import InitialDataframes
from utils.FinalDataframes import FinalDataframes
from utils.GroupedDataframes import GroupedDataframes
from utils.dataframe_to_database import dataframe_to_database

def ingest(configs):
    initial_dataframes = InitialDataframes(configs["InitialDataframes"])
    print("\nFinished parsing datasets...\n")
    final_dataframes = FinalDataframes(initial_dataframes.final_matches, initial_dataframes.dfs, configs["FinalDataframes"])
    print("\nFinished creating dataframes...\n")
    final_dataframes_grouped = GroupedDataframes(final_dataframes.dfs, configs["GroupedDataframes"])
    print("\nFinished grouping dataframes...\n")

    db_configs = configs["DataFrameToDatabase"]

    for dfname, df in final_dataframes_grouped.dfs.items():
        schema_configs = db_configs[dfname]
        dataframe_to_database(df, schema_configs)

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
