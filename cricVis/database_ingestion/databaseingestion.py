import pandas as pd
import numpy as np
import json
from collections import defaultdict

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

df_deliveries = pd.read_csv("csv_files/deliveries.csv", usecols=del_cols_orig)
df_matches = pd.read_csv("csv_files/matches.csv", usecols=match_cols_orig)
df_matches.rename(columns={"id": "matchID"}, inplace=True)

df_deliveries.rename(columns={"match_id": "matchID"}, inplace=True)

"""
Table 1 : MatchStatsTable

(matchID, #over, team), breakdownRuns, runs

Table  2 : DismissalTable

(matchID, #over, #ball, team), playerDismissed, nonStriker, bowler, fielder, type

Table 3: Player Description

(playerName, season), team

Table 4: Match Description

(matchID), matchDate, season, venue (combine venue and city fields of matches.csv), team1, team2, tossWinner, tossDecision, result, playerOfMatch, winByRuns, winByWickets

Table 5: Player_Match Relation (Many - Many Relation: one match -> multiple players, one player -> multiple matches)

(playerName, matchID)

Table 6: Season-wise

(season, team), finalMatchScoreBatting, lowestScore, highestScore

Table 7: Team-wise

(team), matchWins, seasonWins, runnerUps, tossWins, averageScore

Table 8: Venue-wise

(city, stadium), numberOfMatches, averageScore

Table 9: Stadium-City (Many - One Relation)

(stadium, city)


"""

################ MatchStats initial dataframe
match_stats = df_deliveries[["matchID",
"over",
"batting_team",
'wide_runs',
'bye_runs',
'legbye_runs',
'noball_runs',
'penalty_runs',
'batsman_runs',
'extra_runs',
'total_runs']].copy();

match_stats.rename(columns={"batting_team": "team",
                            "total_runs": "runs"}, inplace=True)



############# DismissalTable initial dataframe
match_dismissal = df_deliveries.filter(["matchID",
"over",
"ball",
"batting_team",
"player_dismissed",
"non_striker",
"bowler",
"fielder",
"dismissal_kind"
], axis=1)

match_dismissal.dropna(axis=0, subset=["player_dismissed"], inplace=True)
match_dismissal = match_dismissal.reset_index(drop=True)

match_dismissal.rename(columns={"batting_team": "team",
                                "player_dismissed": "playerDismissed",
                                "non_striker": "nonStriker",
                                "dismissal_kind": "type"}, inplace=True)

# Some rows have NaN in the "fielder" column
match_dismissal.fillna("-", inplace=True)

############ Player Description & Player Match initial dataframes

df_players_seasons = pd.merge(df_deliveries[['matchID',
                                            'batting_team',
                                            'bowling_team',
                                            'batsman',
                                            'non_striker',
                                            'bowler',
                                            'fielder']].copy(),
                              df_matches[['matchID',
                                          'season']].copy(),
                              how='inner', on='matchID')

# Batsmen
player_desc = df_players_seasons.filter(["matchID","season", "batting_team", "batsman"], axis=1)
player_desc.rename(columns={"batsman": "player",
                            "batting_team": "team"},
                            inplace=True)

# Non-strikers
player_desc2 = df_players_seasons.filter(["matchID","season", "batting_team", "non_striker"], axis=1)
player_desc2.rename(columns={"non_striker": "player",
                            "batting_team": "team"},
                            inplace=True)

# Bowlers
player_desc3 = df_players_seasons.filter(["matchID","season", "bowling_team", "bowler"], axis=1)
player_desc3.rename(columns={"bowler": "player",
                            "bowling_team": "team"},
                            inplace=True)

# Fielders
player_desc4 = df_players_seasons.filter(["matchID","season", "bowling_team", "fielder"], axis=1)
player_desc4.rename(columns={"fielder": "player",
                            "bowling_team": "team"},
                            inplace=True)

# Append all of them
player_desc = player_desc.append(player_desc2, ignore_index=True)
player_desc = player_desc.append(player_desc3, ignore_index=True)
player_desc = player_desc.append(player_desc4, ignore_index=True)

# Remove all rows with NaN values
player_desc.dropna(axis=0, subset=["player"], inplace=True)

# To remove the " (sub)" substring that was there in the original data
# to signify that the player came in as a substitute
player_desc.player = player_desc.player.map(lambda x: x.rstrip(" (sub)"))

# Player Match dataframe
player_match = player_desc.filter(["matchID", "player"], axis=1)
player_match = player_match.reset_index(drop=True)

# Player Description dataframe
player_desc = player_desc.filter(["season", "team", "player"], axis=1)
player_desc = player_desc.reset_index(drop=True)

# Remove all duplicate rows
player_desc.drop_duplicates(inplace=True)
player_desc.fillna("-", inplace=True)

player_match.drop_duplicates(inplace=True)
player_match.fillna("-", inplace=True)


############# Match Description initial dataframe

match_desc = df_matches.copy()
match_desc.venue = match_desc.venue.astype(str) + ", " + match_desc.city
match_desc.drop(columns=["city"], axis=1, inplace=True)

match_desc.rename(columns={"date": "matchDate",
                            "win_by_runs": "winByRuns",
                            "win_by_wickets": "winByWickets",
                            "winner": "result",
                            "player_of_match": "playerOfMatch",
                            "toss_winner": "tossWinner",
                            "toss_decision": "tossDecision"},
                  inplace=True)

# Venue isn't avaliable for all matches i.e. some rows have NaN under "venue"
match_desc.fillna("-", inplace=True)


################ SeasonWise Initial Table
season_wise = pd.merge(df_deliveries[['matchID',
                                      'total_runs',
                                      'batting_team']].copy(),
                       df_matches[['matchID',
                                   'season']].copy(),
                       how='inner', on='matchID')

season_wise.rename(columns={"batting_team": "team",
                            "total_runs": "runs"}, inplace=True)


############### TeamWise Initial Table
team_wise = pd.merge(df_deliveries[['matchID',
                                    'total_runs',
                                    'batting_team']].copy(),
                       df_matches[['matchID',
                                   'season',
                                   'toss_winner',
                                   'winner']].copy(),
                       how='inner', on='matchID')\
                       .rename(columns={"batting_team": "team",
                                        "total_runs": "runs",
                                        "toss_winner": "tossWinner",
                                        "winner": "result"})


############## VenueWise initial Table
venue_wise = pd.merge(df_deliveries[['matchID',
                                    'total_runs']].copy(),
                       df_matches[['matchID',
                                   'city',
                                   'venue']].copy(),
                       how='inner', on='matchID')\
                       .rename(columns={"venue": "stadium",
                                        "total_runs": "runs"})

venue_wise.fillna("Dubai", inplace=True)


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

"""

########## Modifying the dataframes to become nested like the above schemas

match_stats.matchID = "matchID_" + match_stats.matchID.astype(str)
match_stats.over = "over_" + match_stats.over.astype(str)

match_dismissal.matchID = "matchID_" + match_dismissal.matchID.astype(str)
match_dismissal.over = "over_" + match_dismissal.over.astype(str)
match_dismissal.ball = "ball_" + match_dismissal.ball.astype(str)

player_desc.season = "season_" + player_desc.season.astype(str)

player_match.matchID = "matchID_" + player_match.matchID.astype(str)

match_desc.matchID = "matchID_" + match_desc.matchID.astype(str)

############# Final Collection
def nested_dict():
    return defaultdict(nested_dict)

results = nested_dict()

############ Nesting the match_stats df to MatchStats dictionary
match_stats_grouped = match_stats.groupby(["matchID", "over", "team"])[["runs",\
                                            'wide_runs',\
                                            'bye_runs',\
                                            'legbye_runs',\
                                            'noball_runs',\
                                            'penalty_runs',\
                                            'batsman_runs',\
                                            'extra_runs']].sum()

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

for row in match_stats_grouped.itertuples():
    matchID = getattr(row, 'Index')[0]
    over = getattr(row, 'Index')[1]
    team = getattr(row, 'Index')[2]
    results["MatchStats"][matchID][over][team]['runs'] = row.runs
    results["MatchStats"][matchID][over][team]['breakdownRuns'] = row.breakdownRuns

"""
r = json.dumps(results["MatchStats"])
r = json.loads(r)
out_file = open("MatchStats.json", "w")
json.dump(r, out_file, indent=2)
"""

############ Nesting the match_dismissal df to MatchDismissal dictionary
match_dismissal_grouped = match_dismissal.groupby(["matchID", "over", "ball", "team"])[[\
                                            'playerDismissed',\
                                            'nonStriker',\
                                            'type',\
                                            'bowler',\
                                            'fielder']]\
                                            .sum()

for row in match_dismissal_grouped.itertuples():
    matchID = getattr(row, 'Index')[0]
    over = getattr(row, 'Index')[1]
    ball = getattr(row, 'Index')[2]
    team = getattr(row, 'Index')[3]
    results["MatchDismissal"][matchID][over][ball][team]['playerDismissed'] = row.playerDismissed
    results["MatchDismissal"][matchID][over][ball][team]['nonStriker'] = row.nonStriker
    results["MatchDismissal"][matchID][over][ball][team]['type'] = row.type
    results["MatchDismissal"][matchID][over][ball][team]['bowler'] = row.bowler
    results["MatchDismissal"][matchID][over][ball][team]['fielder'] = row.fielder

"""
r = json.dumps(results["MatchDismissal"])
r = json.loads(r)
out_file = open("MatchDismissal.json", "w")
json.dump(r, out_file, indent=2)
"""

############ Nesting the player_desc df to PlayerDescription dictionary
player_desc_grouped = player_desc.groupby(["player", "season"])[['team']].sum()

for row in player_desc_grouped.itertuples():
    player = getattr(row, 'Index')[0]
    season = getattr(row, 'Index')[1]
    results["PlayerDescription"][player][season]['team'] = row.team

"""
r = json.dumps(results["PlayerDescription"])
r = json.loads(r)
out_file = open("PlayerDescription.json", "w")
json.dump(r, out_file, indent=2)
"""


############ Nesting the player_match df to PlayerMatch dictionary
player_match_grouped = player_match.groupby("matchID")[['player']]

for name, df_group in player_match_grouped:
    player_index = 1

    for row in df_group.itertuples():
        matchID = row.matchID
        results["PlayerMatch"][matchID]["player" + str(player_index)] = row.player
        player_index = player_index + 1

"""
r = json.dumps(results["PlayerMatch"])
r = json.loads(r)
out_file = open("PlayerMatch.json", "w")
json.dump(r, out_file, indent=2)
"""

############ Nesting the match_desc df to MatchDescription dictionary
match_desc_grouped = match_desc.groupby("matchID")

for name, df_group in match_desc_grouped:
    for row in df_group.itertuples():
        matchID = row.matchID
        results["MatchDescription"][matchID]['matchDate'] = row.matchDate
        results["MatchDescription"][matchID]['season'] = row.season
        results["MatchDescription"][matchID]['venue'] = row.venue
        results["MatchDescription"][matchID]['team1'] = row.team1
        results["MatchDescription"][matchID]['team2'] = row.team2
        results["MatchDescription"][matchID]['tossWinner'] = row.tossWinner
        results["MatchDescription"][matchID]['tossDecision'] = row.tossDecision
        results["MatchDescription"][matchID]['result'] = row.result
        results["MatchDescription"][matchID]['playerOfMatch'] = row.playerOfMatch
        results["MatchDescription"][matchID]['winByRuns'] = row.winByRuns
        results["MatchDescription"][matchID]['winByWickets'] = row.winByWickets

"""
r = json.dumps(results["MatchDescription"])
r = json.loads(r)
out_file = open("MatchDescription.json", "w")
json.dump(r, out_file, indent=2)
"""


########## Calculations to find finalMatchScoreBatting,
########## lowestScore, highestScore in SeasonWise table

season_wise_grouped_initial = season_wise.groupby(["season",
                                            "team",
                                            "matchID"], as_index=False)\
                                            [["runs"]].sum()

# Enlists matchID of the final match of each season
final_matches = season_wise_grouped_initial.groupby("season")\
                                            [["matchID"]].max()["matchID"].to_list()

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

season_wise_grouped["lowestScore"] = season_wise_grouped_initial.groupby(["season",
                                            "team"])\
                                            [["runs"]].min()

season_wise_grouped["highestScore"] = season_wise_grouped_initial.groupby(["season",
                                            "team"])\
                                            [["runs"]].max()


for row in season_wise_grouped.itertuples():
    season = getattr(row, 'Index')[0]
    team = getattr(row, 'Index')[1]
    results["SeasonWise"][season][team]['finalMatchScoreBatting'] = row.finalMatchScoreBatting
    results["SeasonWise"][season][team]['lowestScore'] = row.lowestScore
    results["SeasonWise"][season][team]['highestScore'] = row.highestScore

"""
r = json.dumps(results["SeasonWise"])
r = json.loads(r)
out_file = open("json_output/SeasonWise.json", "w")
json.dump(r, out_file, indent=2)
"""

########## Team Wise calculations
#(team), matchWins, seasonWins, runnerUps, tossWins, averageScore
team_wise_grouped_initial = team_wise.groupby(["team",
                                            "season",
                                            "matchID",
                                            "result",
                                            "tossWinner"], as_index=False)\
                                            [["runs"]].sum()

team_wise_grouped = team_wise_grouped_initial.groupby(["team"])[["runs"]].mean().rename(columns={"runs": "averageScore"})
team_wise_tossWins = team_wise_grouped_initial[["matchID", "tossWinner"]].drop_duplicates().groupby("tossWinner")["tossWinner"].count()
team_wise_tossWins.index.name = "team"
team_wise_matchWins = team_wise_grouped_initial[team_wise_grouped_initial["team"] == team_wise_grouped_initial["result"]].dropna(axis=0).groupby("team")["team"].count()

team_wise_grouped_initial = team_wise_grouped_initial\
                    .mask(~(team_wise_grouped_initial["matchID"]\
                    .isin(final_matches)))\
                    .dropna(axis=0)
team_wise_seasonWins = team_wise_grouped_initial[team_wise_grouped_initial["team"] == team_wise_grouped_initial["result"]].dropna(axis=0).groupby(["team"])["team"].count()
team_wise_runnerUps = team_wise_grouped_initial[team_wise_grouped_initial["team"] != team_wise_grouped_initial["result"]].dropna(axis=0).groupby("team")["team"].count()

team_wise_grouped["matchWins"] = team_wise_matchWins
team_wise_grouped["seasonWins"] = team_wise_seasonWins
team_wise_grouped["runnerUps"] = team_wise_runnerUps
team_wise_grouped["tossWins"] = team_wise_tossWins

team_wise_grouped.replace(np.nan, 0, inplace=True)

for row in team_wise_grouped.itertuples():
    team = row.Index
    results["TeamWise"][team]['matchWins'] = int(row.matchWins)
    results["TeamWise"][team]['seasonWins'] = int(row.seasonWins)
    results["TeamWise"][team]['runnerUps'] = int(row.runnerUps)
    results["TeamWise"][team]['tossWins'] = int(row.tossWins)
    results["TeamWise"][team]['averageScore'] = row.averageScore


"""
r = json.dumps(results["TeamWise"])
r = json.loads(r)
out_file = open("json_output/TeamWise.json", "w")
json.dump(r, out_file, indent=2)
"""

########## VenueWise calculations
#(city, stadium), numberOfMatches, averageScore

venue_wise_grouped_initial = venue_wise.groupby(["city", "stadium", "matchID"], as_index=False)[["runs"]].sum()
venue_wise_grouped_initial.city = venue_wise_grouped_initial.city.map(lambda x: x.replace(".", ""))
venue_wise_grouped_initial.stadium = venue_wise_grouped_initial.stadium.map(lambda x: x.replace(".", ""))

venue_wise_grouped = venue_wise_grouped_initial.groupby(["city", "stadium"])[["matchID"]].count().rename(columns={"matchID": "numberOfMatches"})
venue_wise_grouped["averageScore"] = venue_wise_grouped_initial.groupby(["city", "stadium"])[["runs"]].mean()

for row in venue_wise_grouped.itertuples():
    city = getattr(row, 'Index')[0]
    stadium = getattr(row, 'Index')[1]
    results["VenueWise"][city][stadium]['numberOfMatches'] = row.numberOfMatches
    results["VenueWise"][city][stadium]['averageScore'] = row.averageScore


"""
r = json.dumps(results["VenueWise"])
r = json.loads(r)
out_file = open("json_output/VenueWise.json", "w")
json.dump(r, out_file, indent=2)
"""


########## StadiumCity
stadium_city = venue_wise_grouped_initial.groupby("stadium")[["city"]]

for name, df_group in stadium_city:
    for row in df_group.itertuples():
        stadium = row.stadium
        results["StadiumCity"][stadium] = row.city

"""
r = json.dumps(results["StadiumCity"])
r = json.loads(r)
out_file = open("json_output/StadiumCity.json", "w")
json.dump(r, out_file, indent=2)
"""



final_collection_json = json.dumps(results)
final_collection_json = json.loads(final_collection_json)
out_file = open("json_output/cricVisDatabase.json", "w")
json.dump(final_collection_json, out_file, indent=2)
