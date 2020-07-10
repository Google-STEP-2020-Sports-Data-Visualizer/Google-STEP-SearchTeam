import pandas as pd
import numpy as np

# Modifying the dataframes to become nested like the above design


class GroupedDataframes:
    def __init__(self, final_dataframes):
        # Enlists matchID of the final match of each season
        self.final_matches = final_dataframes.final_matches

        self.group_match_stats(final_dataframes.match_stats)
        self.group_match_dismissal(final_dataframes.match_dismissal)
        self.group_player_desc(final_dataframes.player_desc)
        self.group_player_match(final_dataframes.player_match)
        self.group_match_desc(final_dataframes.match_desc)
        self.group_season_wise(final_dataframes.season_wise)
        self.group_team_wise(final_dataframes.team_wise)
        self.group_venue_wise(final_dataframes.venue_wise)
        self.group_stadium_city(final_dataframes.venue_wise)

    # Nesting the match_stats df
    def group_match_stats(self, match_stats):
        breakdownRuns_list = ['wide_runs',
                         'bye_runs',
                         'legbye_runs',
                         'noball_runs',
                         'penalty_runs',
                         'batsman_runs',
                         'extra_runs']

    # Summing the runs over all balls per over
        self.match_stats_grouped = match_stats.groupby(["matchID", "over", "team"])[
            ["runs"] + breakdownRuns_list].sum()

    # Grouping different types of runs into a breakdownRuns dictionary
        self.match_stats_grouped["breakdownRuns"] = self.match_stats_grouped.apply(
            lambda x: x[breakdownRuns_list].to_dict(), axis=1)

        self.match_stats_grouped.drop(columns=breakdownRuns_list, inplace=True)

    # Nesting the match_dismissal df

    def group_match_dismissal(self, match_dismissal):
        self.match_dismissal_grouped = match_dismissal.groupby(["matchID", "over", "ball", "team"])[[
            'playerDismissed',
            'nonStriker',
            'type',
            'bowler',
            'fielder']]\
            .sum()

    # Nesting the player_desc df

    def group_player_desc(self, player_desc):
        self.player_desc_grouped = player_desc.groupby(["player", "season"])[['team']].sum()

    # Resetting the index of the player_match df

    def group_player_match(self, player_match):
        self.player_match_grouped = player_match.set_index("matchID")

    # Resetting the index of the match_desc df
    def group_match_desc(self, match_desc):
        self.match_desc_grouped = match_desc.set_index("matchID")

    # Nesting season_wise df

    def group_season_wise(self, season_wise):
        # Calculations to find finalMatchScoreBatting,
        # lowestScore, highestScore in SeasonWise table
        self.season_wise_grouped = season_wise.groupby(["season",
                                                        "team"])\
            .agg(highestScore=pd.NamedAgg(column='runs', aggfunc='max'),
                 lowestScore=pd.NamedAgg(column="runs", aggfunc="min"),
                 finalMatchScoreBatting=pd.NamedAgg(column="finalMatchScoreBatting", aggfunc="max"))

    # Team Wise calculations

    def group_team_wise(self, team_wise):
        self.team_wise_grouped = team_wise.groupby("team").agg({"total_runs": "mean",
                                                                "matchWins": "sum",
                                                                "tossWins": "sum",
                                                                "seasonWins": "sum",
                                                                "runnerUps": "sum"})

        self.team_wise_grouped.rename(columns={"total_runs": "averageScore"}, inplace=True)

        self.team_wise_grouped.replace(np.nan, 0, inplace=True)


    # VenueWise calculations

    def group_venue_wise(self, venue_wise):
		self.venue_wise_grouped = venue_wise.groupby(["city", "stadium"], as_index=False).agg({"matchID": "count", "total_runs": "mean"})

		self.venue_wise_grouped["matchID"] = self.venue_wise_grouped["matchID"] / 2
		self.venue_wise_grouped.rename({"matchID": "noOfMatches"}, inplace=True)

		print(self.venue_wise_grouped)

    # StadiumCity

    def group_stadium_city(self, venue_wise):
        self.stadium_city_grouped_initial = venue_wise.groupby(["city", "stadium", "matchID"],
                                                               as_index=False)[["runs"]].sum()

        self.stadium_city = stadium_city_grouped_initial.groupby("stadium")[["city"]]
