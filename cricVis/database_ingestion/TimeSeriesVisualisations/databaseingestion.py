from utils.CricketStats import BattingStats, BowlingStats
from utils.nested_dict import nested_dict
from utils.dict_to_json_file import dict_to_json_file
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

########## Initialise the tables

batsman_odi_men = BattingStats("BatsmanPerformanceODIMen",
                               "csv_files/Men ODI Player Innings Stats - 20th Century.csv",
                               "csv_files/Men ODI Player Innings Stats - 21st Century.csv")
batsman_test_men = BattingStats("BatsmanPerformanceTestMen",
                                "csv_files/Men Test Player Innings Stats - 19th Century.csv",
                                "csv_files/Men Test Player Innings Stats - 20th Century.csv",
                                "csv_files/Men Test Player Innings Stats - 21st Century.csv")
batsman_t20_men = BattingStats("BatsmanPerformanceT20Men",
                               "csv_files/Men T20I Player Innings Stats - 21st Century.csv")
batsman_odi_women = BattingStats("BatsmanPerformanceODIWomen",
                                 "csv_files/Women ODI Player Innings Stats - 20th Century.csv",
                                 "csv_files/Women ODI Player Innings Stats - 21st Century.csv")
batsman_test_women = BattingStats("BatsmanPerformanceTestWomen",
                                  "csv_files/Women Test Player Innings Stats - 20th Century.csv",
                                  "csv_files/Women Test Player Innings Stats - 21st Century.csv")
batsman_t20_women = BattingStats("BatsmanPerformanceT20Women",
                                 "csv_files/Women T20I Player Innings Stats - 21st Century.csv")

bowler_odi_men = BowlingStats("BowlerPerformanceODIMen",
                               "csv_files/Men ODI Player Innings Stats - 20th Century.csv",
                               "csv_files/Men ODI Player Innings Stats - 21st Century.csv")
bowler_test_men = BowlingStats("BowlerPerformanceTestMen",
                                "csv_files/Men Test Player Innings Stats - 19th Century.csv",
                                "csv_files/Men Test Player Innings Stats - 20th Century.csv",
                                "csv_files/Men Test Player Innings Stats - 21st Century.csv")
bowler_t20_men = BowlingStats("BowlerPerformanceT20Men",
                               "csv_files/Men T20I Player Innings Stats - 21st Century.csv")
bowler_odi_women = BowlingStats("BowlerPerformanceODIWomen",
                                 "csv_files/Women ODI Player Innings Stats - 20th Century.csv",
                                 "csv_files/Women ODI Player Innings Stats - 21st Century.csv")
bowler_test_women = BowlingStats("BowlerPerformanceTestWomen",
                                  "csv_files/Women Test Player Innings Stats - 20th Century.csv",
                                  "csv_files/Women Test Player Innings Stats - 21st Century.csv")
bowler_t20_women = BowlingStats("BowlerPerformanceT20Women",
                                 "csv_files/Women T20I Player Innings Stats - 21st Century.csv")

batsman_tables = [batsman_odi_men, batsman_odi_women,\
                  batsman_test_men, batsman_test_women,\
                  batsman_t20_men, batsman_t20_women]

bowler_tables = [bowler_odi_men, bowler_odi_women,\
                  bowler_test_men, bowler_test_women,\
                  bowler_t20_men, bowler_t20_women]

########## Initialise database_dictionary, rules_dictionary

db_dict = nested_dict()
db_rules_dict = nested_dict()

# To prevent any unuthorised user from accessing the database
db_rules_dict[".write"] = False
db_rules_dict[".read"] = False


for table in batsman_tables:
    table.manipulate()
    table.group_df()
    table.df_to_dict(db_dict, db_rules_dict)
    logging.info("{table_name} dictionary successfully created...".format(table_name=table.table_name))

for table in bowler_tables:
    table.manipulate()
    table.group_df()
    table.df_to_dict(db_dict, db_rules_dict)
    logging.info("{table_name} dictionary successfully created...".format(table_name=table.table_name))

dict_to_json_file(db_dict, "cricketTimeSeriesVisDatabase")
dict_to_json_file(db_rules_dict, "cricketTimeSeriesVisDatabaseRules")
logging.info("Final json outputs of the database and its rules successfully created.\n")
