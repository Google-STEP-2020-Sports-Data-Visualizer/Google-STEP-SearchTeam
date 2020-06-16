import pandas as pd
import numpy as np

"""
MatchStats {
	matchID_value: {
		over_value: {
			team: {
				breakdownRuns: {
							4s:
							6s:
							Extras:

							}
				runs:
}
team: {
}
}
over_value: {
}
}
}

MatchDismissal {
	matchID_value:{
		over_value:{
			ball_value:{
				team: {
					playerDismissed:
					nonStriker:
					type:
					bowler:
					fielder:
				}
			}
		}
	}
	matchID_value:{

	}
}


PlayerDescription {

	playerName: {
		season_value: { team: }
		season_value: { team: }
	}
	playerName: {

	}

}

PlayerMatch {

	matchID_value: {
		player1: “”
		player2: “” ...
	}
	matchID_value: {
	}

}

MatchDescription {
	matchID_value: {
		matchDate:
		season:
		venue:
        team1:
        team2:
        innings:
        result:
        playerOfMatch:
        winByRuns:
        winByWickets:
    }
    matchID_value: {
    }
}

SeasonWise

season:{
	team: {

		finalMatchScoreBatting:  //default 0 if that team wasn’t in the final
		lowestScore:
		highestScore:

    }
    team: {

		finalMatchScoreBatting:
		lowestScore:
		highestScore:
    }
}

}

TeamWise

team: {

	matchWins:
	seasonWins:
	runnerUps:
	tossWins:
	averageScore:

}

VenueWise

city: {
stadium: {

	numberOfMatches:
	averageScore:

}

}

StadiumCity

stadium: city,
stadium: city,
….


"""

########## Modifying the dataframes to become nested like the above design
def group_final_dataframes(final_dataframes):
    match_stats = final_dataframes["match_stats"]
    match_dismissal = final_dataframes["match_dismissal"]
    player_desc = final_dataframes["player_desc"]
    player_match = final_dataframes["player_match"]
    match_desc = final_dataframes["match_desc"]
    season_wise = final_dataframes["season_wise"]
    team_wise = final_dataframes["team_wise"]
    venue_wise = final_dataframes["venue_wise"]

    # Modifying column values so that they match the format of
    # the keys in the final database design
    match_stats.matchID = "matchID_" + match_stats.matchID.astype(str)
    match_stats.over = "over_" + match_stats.over.astype(str)

    match_dismissal.matchID = "matchID_" + match_dismissal.matchID.astype(str)
    match_dismissal.over = "over_" + match_dismissal.over.astype(str)
    match_dismissal.ball = "ball_" + match_dismissal.ball.astype(str)

    player_desc.season = "season_" + player_desc.season.astype(str)

    player_match.matchID = "matchID_" + player_match.matchID.astype(str)

    match_desc.matchID = "matchID_" + match_desc.matchID.astype(str)

    final_dataframes_grouped = {}
    final_dataframes_grouped["match_stats_grouped"] = group_match_stats(match_stats)
    final_dataframes_grouped["match_dismissal_grouped"] = group_match_dismissal(match_dismissal)
    final_dataframes_grouped["player_desc_grouped"] = group_player_desc(player_desc)
    final_dataframes_grouped["player_match_grouped"] = group_player_match(player_match)
    final_dataframes_grouped["match_desc_grouped"] = group_match_desc(match_desc)
    final_dataframes_grouped["season_wise_grouped"] = group_season_wise(season_wise)
    final_dataframes_grouped["team_wise_grouped"] = group_team_wise(team_wise)
    final_dataframes_grouped["venue_wise_grouped"] = group_venue_wise(venue_wise)
    final_dataframes_grouped["stadium_city"] = group_stadium_city(venue_wise)

    return final_dataframes_grouped


############ Nesting the match_stats df
def group_match_stats(match_stats):
    # Summing the runs over all balls per over
    match_stats_grouped = match_stats.groupby(["matchID", "over", "team"])[["runs",\
                                                'wide_runs',\
                                                'bye_runs',\
                                                'legbye_runs',\
                                                'noball_runs',\
                                                'penalty_runs',\
                                                'batsman_runs',\
                                                'extra_runs']].sum()

    # Grouping different types of runs into a breakdownRuns dictionary
    match_stats_grouped["breakdownRuns"] = match_stats_grouped.apply(\
                                            lambda x: x[['wide_runs',\
                                            'bye_runs',\
                                            'legbye_runs',\
                                            'noball_runs',\
                                            'penalty_runs',\
                                            'batsman_runs',\
                                            'extra_runs']].to_dict(), axis=1)

    match_stats_grouped.drop(columns=['wide_runs',\
                            'bye_runs',\
                            'legbye_runs',\
                            'noball_runs',\
                            'penalty_runs',\
                            'batsman_runs',\
                            'extra_runs'], inplace=True)

    return match_stats_grouped

############ Nesting the match_dismissal df
def group_match_dismissal(match_dismissal):
    match_dismissal_grouped = match_dismissal.groupby(["matchID", "over", "ball", "team"])[[\
                                                'playerDismissed',\
                                                'nonStriker',\
                                                'type',\
                                                'bowler',\
                                                'fielder']]\
                                                .sum()

    return match_dismissal_grouped

############ Nesting the player_desc df
def group_player_desc(player_desc):
    player_desc_grouped = player_desc.groupby(["player", "season"])\
                                             [['team']].sum()

    return player_desc_grouped

############ Nesting the player_match df
def group_player_match(player_match):
    player_match_grouped = player_match.groupby("matchID")[['player']]

    return player_match_grouped


############ Nesting the match_desc df
def group_match_desc(match_desc):
    match_desc_grouped = match_desc.groupby("matchID")

    return match_desc_grouped


########## Nesting season_wise df
def group_season_wise(season_wise):
    # Calculations to find finalMatchScoreBatting,
    # lowestScore, highestScore in SeasonWise table

    season_wise_grouped_initial = season_wise.groupby(["season",
                                                "team",
                                                "matchID"], as_index=False)\
                                                [["runs"]].sum()

    # Enlists matchID of the final match of each season
    final_matches = season_wise_grouped_initial.groupby("season")\
                                                [["matchID"]]\
                                                .max()["matchID"]\
                                                .to_list()

    final_scores = season_wise_grouped_initial.copy()
    final_scores["runs"] = final_scores["runs"]\
                                        .mask(~final_scores["matchID"]\
                                        .isin(final_matches), \
                                        0)

    season_wise_grouped = final_scores.groupby(["season",
                                                "team"])\
                                                [["runs"]].max()\
                                                .rename(columns=\
                                                {"runs": "finalMatchScoreBatting"})

    season_wise_grouped["lowestScore"] = season_wise_grouped_initial\
                                                .groupby(["season",
                                                "team"])\
                                                [["runs"]].min()

    season_wise_grouped["highestScore"] = season_wise_grouped_initial\
                                                .groupby(["season",
                                                "team"])\
                                                [["runs"]].max()

    return season_wise_grouped


########## Team Wise calculations
def group_team_wise(team_wise):
    team_wise_grouped_initial = team_wise.groupby(["team",\
                                                "season",
                                                "matchID",
                                                "result",
                                                "tossWinner"], as_index=False)\
                                                [["runs"]].sum()

    # Enlists matchID of the final match of each season
    final_matches = team_wise_grouped_initial.groupby("season")\
                                                [["matchID"]].max()\
												["matchID"].to_list()


    team_wise_grouped = team_wise_grouped_initial.groupby("team")[["runs"]]\
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

    team_wise_grouped_initial = team_wise_grouped_initial\
                        .mask(~(team_wise_grouped_initial["matchID"]\
                        .isin(final_matches)))\
                        .dropna(axis=0)
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

########## VenueWise calculations
def group_venue_wise(venue_wise):
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

    return venue_wise_grouped

########## StadiumCity
def group_stadium_city(venue_wise):
    stadium_city_grouped_initial = venue_wise.groupby(["city", "stadium", "matchID"],\
                                                    as_index=False)[["runs"]].sum()

    stadium_city = stadium_city_grouped_initial.groupby("stadium")[["city"]]

    return stadium_city
