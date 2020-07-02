import pandas as pd
import json

from utils.nested_dict import nested_dict

############# Final Collection
class DataframesToDict:
    def __init__(self, final_dataframes_grouped):
        self.match_stats_grouped = final_dataframes_grouped.match_stats_grouped
        self.match_dismissal_grouped = final_dataframes_grouped.match_dismissal_grouped
        self.player_desc_grouped = final_dataframes_grouped.player_desc_grouped
        self.player_match_grouped = final_dataframes_grouped.player_match_grouped
        self.match_desc_grouped = final_dataframes_grouped.match_desc_grouped
        self.season_wise_grouped = final_dataframes_grouped.season_wise_grouped
        self.team_wise_grouped = final_dataframes_grouped.team_wise_grouped
        self.venue_wise_grouped = final_dataframes_grouped.venue_wise_grouped
        self.stadium_city = final_dataframes_grouped.stadium_city

        self.db_dict = nested_dict()

        self.to_dict()

    ###### Define all utility functions

    # Function for setting the keys and values of db_dict dictionaary
    def fill_db_dict(self, row, attribute, fields_list, field_as_key=True):
        if not field_as_key:
            self.db_dict[attribute][row.Index] = fields_list[0]
        elif type(row.Index) == tuple:
            if len(row.Index) == 2:
                for field in fields_list:
                    self.db_dict[attribute][row.Index[0]][row.Index[1]][field] = getattr(row, field)
            elif len(row.Index) == 3:
                for field in fields_list:
                    self.db_dict[attribute][row.Index[0]][row.Index[1]][row.Index[2]][field] = getattr(row, field)
            elif len(row.Index) == 4:
                for field in fields_list:
                    self.db_dict[attribute][row.Index[0]][row.Index[1]][row.Index[2]][row.Index[3]][field] = getattr(row, field)

        else:   # Index is a single int/string instead of being a tuple
            for field in fields_list:
                self.db_dict[attribute][row.Index][field] = getattr(row, field)


    def match_stats_to_dict(self):
        for row in self.match_stats_grouped.itertuples():
            self.fill_db_dict(row, "MatchStats", ["runs", "breakdownRuns"])


    def match_dismissal_to_dict(self):
        for row in self.match_dismissal_grouped.itertuples():
            self.fill_db_dict(row, "MatchDismissal", ["playerDismissed", "nonStriker", "type", "bowler", "fielder"])


    def player_desc_to_dict(self):
        for row in self.player_desc_grouped.itertuples():
            self.fill_db_dict(row, "PlayerDescription", ["team"])


    def player_match_to_dict(self):
        player_index = 1

        for row in self.player_match_grouped.itertuples():
            self.fill_db_dict(row, "PlayerMatch", ["player{number}".format(number=player_index)], field_as_key=False)


    def match_desc_to_dict(self):
        for row in self.match_desc_grouped.itertuples():
            self.fill_db_dict(row, "MatchDescription", ["matchDate", "season", "venue", "team1", "team2", "tossDecision", "result", "playerOfMatch", "winByRuns", "winByWickets"])


    def season_wise_to_dict(self):
        for row in self.season_wise_grouped.itertuples():
            self.fill_db_dict(row, "SeasonWise", ["finalMatchScoreBatting", "lowestScore", "highestScore"])


    def team_wise_to_dict(self):
        for row in self.team_wise_grouped.itertuples():
            self.fill_db_dict(row, "TeamWise", ["matchWins", "seasonWins", "runnerUps", "tossWins", "averageScore"])


    def venue_wise_to_dict(self):
        for row in self.venue_wise_grouped.itertuples():
            self.fill_db_dict(row, "VenueWise", ["numberOfMatches", "averageScore"])


    def stadium_city_to_dict(self):
        for row in self.stadium_city.itertuples():
            self.fill_db_dict(row, "StadiumCity", ["city"], field_as_key=False)


    def to_dict(self):
        # Created dictionaries of same name inside db_dict
        self.match_stats_to_dict()
        self.match_dismissal_to_dict()
        self.player_desc_to_dict()
        self.player_match_to_dict()
        self.match_desc_to_dict()
        self.season_wise_to_dict()
        self.team_wise_to_dict()
        self.venue_wise_to_dict()
        self.stadium_city_to_dict()
