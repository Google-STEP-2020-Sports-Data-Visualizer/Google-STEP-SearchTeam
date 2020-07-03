import argparse
import json

from utils.InitialDataframes import InitialDataframes
from utils.FinalDataframes import FinalDataframes
#from utils.GroupedDataframes import GroupedDataframes
#from utils.to_database import to_database

def ingest(configs, db_url, cred_path):
    initial_dataframes = InitialDataframes(configs["InitialDataframes"])
    print("\nFinished initialising...\n")
    final_dataframes = FinalDataframes(initial_dataframes.final_matches, initial_dataframes.dfs, configs["FinalDataframes"])
    print("\nFinished final dfs...\n")
    final_dataframes_grouped = GroupedDataframes(final_dataframes.dfs, configs["GroupedDataframes"])
    to_database(final_dataframes_grouped)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Get the paths to config settings and database instance")

    parser.add_argument('--config_path', '-cp',
                        help="Path to config file from pwd", required=True)

    parser.add_argument(
        '--db_url', '-d', help="URL of Realtime Database", required=True)
    parser.add_argument(
        '--cred_path', '-cr', help="Path to secure .json private key from pwd", required=True)

    args = parser.parse_args()

    with open(args.config_path) as f:
      configs = json.load(f)

    ingest(configs,  args.db_url, args.cred_path)
