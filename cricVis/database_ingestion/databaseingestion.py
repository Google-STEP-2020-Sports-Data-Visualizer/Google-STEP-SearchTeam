from utils.initialise_dataframes import *
from utils.initialise_final_dataframes import *
from utils.manipulate_dataframes import *
from utils.dataframes_to_json import *

# Initialise the deliveries and matches dataframes
df_deliveries, df_matches = initialise_dataframes()

# Initialise the following dataframes in accordance with schema:
# 1. match_stats
# 2. match_dismissal
# 3. player_desc
# 4. player_match
# 5. match_desc
# 6. season_wise
# 7. team_wise
# 8. venue_wise
final_dataframes = initialise_final_dataframes(df_deliveries, df_matches)

# Nest each dataframe to resemble the design of each collection in database design
final_dataframes_grouped = group_final_dataframes(final_dataframes)

# Convert nested dataframes to json
dataframes_to_json(final_dataframes_grouped)
# Import the saved .json file into an instance of Realtime Database
# Warning: Doing so will erase previously stored data from the database.
# In case the current database needs to be expanded, write PUSH functions using firebase-admin library
