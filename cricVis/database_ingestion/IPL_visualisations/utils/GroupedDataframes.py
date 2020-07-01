import pandas as pd
import numpy as np

########## Modifying the dataframes to become nested like the above design

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
		breakdownRuns = ['wide_runs',
						 'bye_runs',
						 'legbye_runs',
						 'noball_runs',
						 'penalty_runs',
						 'batsman_runs',
						 'extra_runs']

	    # Summing the runs over all balls per over
		self.match_stats_grouped = match_stats.groupby(["matchID", "over", "team"])[["runs"] + breakdownRuns].sum()

	    # Grouping different types of runs into a breakdownRuns dictionary
		self.match_stats_grouped["breakdownRuns"] = self.match_stats_grouped.apply(lambda x: x[breakdownRuns].to_dict(), axis=1)

		self.match_stats_grouped.drop(columns=breakdownRuns, inplace=True)


	# Nesting the match_dismissal df
	def group_match_dismissal(self, match_dismissal):
		self.match_dismissal_grouped = match_dismissal.groupby(["matchID", "over", "ball", "team"])[[\
				                                                'playerDismissed',\
				                                                'nonStriker',\
				                                                'type',\
				                                                'bowler',\
				                                                'fielder']]\
				                                                .sum()


	# Nesting the player_desc df
	def group_player_desc(self, player_desc):
	    self.player_desc_grouped = player_desc.groupby(["player", "season"])[['team']].sum()


	# Nesting the player_match df
	def group_player_match(self, player_match):
	    self.player_match_grouped = player_match.groupby("matchID")[['player']]


	# Nesting the match_desc df
	def group_match_desc(self, match_desc):
	    self.match_desc_grouped = match_desc.groupby("matchID")


	# Nesting season_wise df
	def group_season_wise(self, season_wise):
	    # Calculations to find finalMatchScoreBatting,
	    # lowestScore, highestScore in SeasonWise table
		self.season_wise_grouped = season_wise.groupby(["season",
		                                        	 "team"])\
													.agg(highestScore=pd.NamedAgg(column='runs', aggfunc='max'),\
													 lowestScore=pd.NamedAgg(column="runs", aggfunc="min"),\
													 finalMatchScoreBatting=pd.NamedAgg(column="finalMatchScoreBatting", aggfunc="max"))


	# Team Wise calculations
	def group_team_wise(self, team_wise):
	    team_wise_grouped = team_wise.groupby("team")[["runs"]]\
													 .mean()\
													 .rename(columns={"runs": "averageScore"})

	    team_wise_tossWins = team_wise_grouped_initial[["matchID", "tossWinner"]]\
														.drop_duplicates()\
														.groupby("tossWinner")["tossWinner"]\
														.count()
	    team_wise_tossWins.index.name = "team"
	    team_wise_grouped["tossWins"] = team_wise_tossWins

	    team_wise_grouped["matchWins"] = team_wise_grouped_initial[team_wise_grouped_initial["team"]\
													== team_wise_grouped_initial["result"]]\
													.dropna(axis=0)\
													.groupby("team")["team"]\
													.count()


	    team_wise_grouped["seasonWins"] = team_wise_grouped_initial[team_wise_grouped_initial["team"]\
													== team_wise_grouped_initial["result"]]\
													.dropna(axis=0)\
													.groupby(["team"])["team"]\
													.count()
	    team_wise_grouped["runnerUps"] = team_wise_grouped_initial[team_wise_grouped_initial["team"]\
													!= team_wise_grouped_initial["result"]]\
													.dropna(axis=0)\
													.groupby("team")["team"]\
													.count()


	    team_wise_grouped.replace(np.nan, 0, inplace=True)

	    return team_wise_grouped

	# VenueWise calculations
	def group_venue_wise(self, venue_wise):
	    venue_wise_grouped_initial = venue_wise.groupby(["city", "stadium", "matchID"],\
	                                                    as_index=False)[["runs"]].sum()
	    venue_wise_grouped_initial.city = venue_wise_grouped_initial.city\
	                                                                .map(lambda x:\
	                                                                 x.replace(".", ""))
	    venue_wise_grouped_initial.stadium = venue_wise_grouped_initial.stadium\
	                                                                   .map(lambda x:\
	                                                                    x.replace(".", ""))

	    venue_wise_grouped = venue_wise_grouped_initial.groupby(["city", "stadium"])\
	                                                            [["matchID"]]\
																.count()\
	                                                            .rename(columns=\
	                                                            {"matchID": "numberOfMatches"})
	    venue_wise_grouped["averageScore"] = venue_wise_grouped_initial\
	                                                            .groupby(["city", "stadium"])\
	                                                            [["runs"]].mean()


	# StadiumCity
	def group_stadium_city(self, venue_wise):
	    self.stadium_city_grouped_initial = venue_wise.groupby(["city", "stadium", "matchID"],\
	                                                    as_index=False)[["runs"]].sum()

	    self.stadium_city = stadium_city_grouped_initial.groupby("stadium")[["city"]]
