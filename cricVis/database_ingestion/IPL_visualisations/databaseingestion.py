import pandas as pd
from time import time

from utils.InitialDataframes import InitialDataframes
from utils.FinalDataframes import FinalDataframes
#from utils.manipulate_dataframes import *
from utils.dataframes_to_json import *

# Paths to required CSV files
deliveries_csv = "csv_files/deliveries.csv"
matches_csv = "csv_files/matches.csv"

# List of columns required from deliveries.csv
del_cols_orig = ['match_id',
'inning',
'batting_team',
'bowling_team',
'over',
'ball',
'batsman',
'non_striker',
'bowler',
'wide_runs',
'bye_runs',
'legbye_runs',
'noball_runs',
'penalty_runs',
'batsman_runs',
'extra_runs',
'total_runs',
'player_dismissed',
'dismissal_kind',
'fielder']

# List of columns required from matches.csv
match_cols_orig = ['id',
'season',
'city',
'date',
'team1',
'team2',
'toss_winner',
'toss_decision',
'winner',
'win_by_runs',
'win_by_wickets',
'player_of_match',
'venue']

# Initialise the deliveries and matches dataframes
t1 = time()
initial_dataframes = InitialDataframes(deliveries_csv, matches_csv, del_cols_orig, match_cols_orig)
print("Finished reading csv files in {duration} seconds...".format(duration=(time() - t1)))

# Initialise the following dataframes in accordance with schema:
# 1. match_stats
# 2. match_dismissal
# 3. player_desc
# 4. player_match
# 5. match_desc
# 6. season_wise
# 7. team_wise
# 8. venue_wise
t2 = time()
final_dataframes = FinalDataframes(initial_dataframes)
print("Finished initialising final dataframes in {duration} seconds...".format(duration=(time() - t2)))

# Nest each dataframe to resemble the design of each collection in database design
t3 = time()
final_dataframes_grouped = group_final_dataframes(final_dataframes)
print("Finished grouping final dataframes in {duration} seconds...".format(duration=(time() - t3)))

# Convert nested dataframes to json
dfs_to_json = dataframes_to_json(final_dataframes_grouped)
dfs_to_json.all_dfs_to_json()
# Import the saved .json file into an instance of Realtime Database
# Warning: Doing so will erase previously stored data from the database.
# In case the current database needs to be expanded, write PUSH functions using firebase-admin library
