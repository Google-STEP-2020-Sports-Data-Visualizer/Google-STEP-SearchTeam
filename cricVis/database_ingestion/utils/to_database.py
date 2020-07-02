import pandas as pd
from collections import defaultdict
import json

def nested_dict():
    return defaultdict(nested_dict)


############# Final Collection
class dataframes_to_json:
    def __init__(self, final_dataframes_grouped):
        self.match_stats_grouped = final_dataframes_grouped["match_stats_grouped"]
        self.match_dismissal_grouped = final_dataframes_grouped["match_dismissal_grouped"]
        self.player_desc_grouped = final_dataframes_grouped["player_desc_grouped"]
        self.player_match_grouped = final_dataframes_grouped["player_match_grouped"]
        self.match_desc_grouped = final_dataframes_grouped["match_desc_grouped"]
        self.season_wise_grouped = final_dataframes_grouped["season_wise_grouped"]
        self.team_wise_grouped = final_dataframes_grouped["team_wise_grouped"]
        self.venue_wise_grouped = final_dataframes_grouped["venue_wise_grouped"]
        self.stadium_city = final_dataframes_grouped["stadium_city"]

        self.results = nested_dict()

    ###### Define all utility functions
    def fill_result(self, row, attribute, fields_list, field_as_key=True):
        if not field_as_key:
            self.results[attribute][row.Index] = fields_list[0]
        elif type(row.Index) == tuple:
            if len(row.Index) == 2:
                for field in fields_list:
                    self.results[attribute][row.Index[0]][row.Index[1]][field] = getattr(row, field)
            elif len(row.Index) == 3:
                for field in fields_list:
                    self.results[attribute][row.Index[0]][row.Index[1]][row.Index[2]][field] = getattr(row, field)
            elif len(row.Index) == 4:
                for field in fields_list:
                    self.results[attribute][row.Index[0]][row.Index[1]][row.Index[2]][row.Index[3]][field] = getattr(row, field)

        else:   # Index is an int/string
            for field in fields_list:
                self.results[attribute][row.Index][field] = getattr(row, field)


    def match_stats_to_json(self):
        for row in self.match_stats_grouped.itertuples():
            self.fill_result(row, "MatchStats", ["runs", "breakdownRuns"])

        r = json.dumps(self.results["MatchStats"])
        r = json.loads(r)
        out_file = open("json_output/MatchStats.json", "w")
        json.dump(r, out_file, indent=2)

    def match_dismissal_to_json(self):
        for row in self.match_dismissal_grouped.itertuples():
            self.fill_result(row, "MatchDismissal", ["playerDismissed", "nonStriker", "type", "bowler", "fielder"])

        r = json.dumps(self.results["MatchDismissal"])
        r = json.loads(r)
        out_file = open("json_output/MatchDismissal.json", "w")
        json.dump(r, out_file, indent=2)

    def player_desc_to_json(self):
        for row in self.player_desc_grouped.itertuples():
            self.fill_result(row, "PlayerDescription", ["team"])

        r = json.dumps(self.results["PlayerDescription"])
        r = json.loads(r)
        out_file = open("json_output/PlayerDescription.json", "w")
        json.dump(r, out_file, indent=2)

    def player_match_to_json(self):
        for name, df_group in self.player_match_grouped:
            player_index = 1

            for row in df_group.itertuples():
                self.fill_result(row, "PlayerMatch", ["player{number}".format(number=player_index)], field_as_key=False)

        r = json.dumps(self.results["PlayerMatch"])
        r = json.loads(r)
        out_file = open("json_output/PlayerMatch.json", "w")
        json.dump(r, out_file, indent=2)

    def match_desc_to_json(self):
        for name, df_group in self.match_desc_grouped:
            for row in df_group.itertuples():
                self.fill_result(row, "MatchDescription", ["matchDate", "season", "venue", "team1", "team2", "tossDecision", "results", "playerOfMatch", "winByRuns", "winByWickets"])

        r = json.dumps(self.results["MatchDescription"])
        r = json.loads(r)
        out_file = open("json_output/MatchDescription.json", "w")
        json.dump(r, out_file, indent=2)

    def season_wise_to_json(self):
        for row in self.season_wise_grouped.itertuples():
            self.fill_result(row, "SeasonWise", ["finalMatchScoreBatting", "lowestScore", "highestScore"])

        r = json.dumps(self.results["SeasonWise"])
        r = json.loads(r)
        out_file = open("json_output/SeasonWise.json", "w")
        json.dump(r, out_file, indent=2)

    def team_wise_to_json(self):
        for row in self.team_wise_grouped.itertuples():
            self.fill_result(row, "TeamWise", ["matchWins", "seasonWins", "runnerUps", "tossWins", "averageScore"])

        r = json.dumps(self.results["TeamWise"])
        r = json.loads(r)
        out_file = open("json_output/TeamWise.json", "w")
        json.dump(r, out_file, indent=2)

    def venue_wise_to_json(self):
        for row in self.venue_wise_grouped.itertuples():
            self.fill_result(row, "VenueWise", ["numberOfMatches", "averageScore"])

        r = json.dumps(self.results["VenueWise"])
        r = json.loads(r)
        out_file = open("json_output/VenueWise.json", "w")
        json.dump(r, out_file, indent=2)

    def stadium_city_to_json(self):
        for name, df_group in self.stadium_city:
            for row in df_group.itertuples():
                self.fill_result(row, "StadiumCity", ["city"])

        r = json.dumps(self.results["StadiumCity"])
        r = json.loads(r)
        out_file = open("json_output/StadiumCity.json", "w")
        json.dump(r, out_file, indent=2)

    def all_dfs_to_json(self):
        # Created dictionaries of same name inside results
        self.match_stats_to_json()
        self.match_dismissal_to_json()
        self.player_desc_to_json()
        self.player_match_to_json()
        self.match_desc_to_json()
        self.season_wise_to_json()
        self.team_wise_to_json()
        self.venue_wise_to_json()
        self.stadium_city_to_json()

        # results dictionary is converted to json
        self.final_collection_json = json.dumps(self.results)
        self.final_collection_json = json.loads(self.final_collection_json)
        out_file = open("json_output/cricVisDatabase.json", "w")
        json.dump(self.final_collection_json, out_file, indent=2)
