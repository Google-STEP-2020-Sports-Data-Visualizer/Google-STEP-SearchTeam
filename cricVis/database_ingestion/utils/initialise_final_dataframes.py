import pandas as pd

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

Note: Table 9 is not initialised here

"""

def initialise_final_dataframes(df_deliveries, df_matches):
    final_dataframes = {}
    final_dataframes["match_stats"] = initialise_match_stats(df_deliveries, df_matches)
    final_dataframes["match_dismissal"] = initialise_match_dismissal(df_deliveries, df_matches)
    player_dataframes = initialise_player_dataframes(df_deliveries, df_matches)
    final_dataframes["player_desc"], final_dataframes["player_match"] = player_dataframes["player_desc"], player_dataframes["player_match"]
    final_dataframes["match_desc"] = initialise_match_desc(df_deliveries, df_matches)
    final_dataframes["season_wise"] = initialise_season_wise(df_deliveries, df_matches)
    final_dataframes["team_wise"] = initialise_team_wise(df_deliveries, df_matches)
    final_dataframes["venue_wise"] = initialise_venue_wise(df_deliveries, df_matches)

    return final_dataframes

################ MatchStats initial dataframe
def initialise_match_stats(df_deliveries, df_matches):
    # Filter out the columns needed from df_deliveries
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

    # Rename columns as per the schema naming conventions
    match_stats.rename(columns={"batting_team": "team",
                                "total_runs": "runs"}, inplace=True)

    return match_stats


############# DismissalTable initial dataframe
def initialise_match_dismissal(df_deliveries, df_matches):
    # Filter out the columns needed from df_deliveries
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

    # Drop entries in which no player was dismissed
    match_dismissal.dropna(axis=0, subset=["player_dismissed"], inplace=True)
    match_dismissal = match_dismissal.reset_index(drop=True)

    # Rename columns as per the schema naming conventions
    match_dismissal.rename(columns={"batting_team": "team",
                                    "player_dismissed": "playerDismissed",
                                    "non_striker": "nonStriker",
                                    "dismissal_kind": "type"}, inplace=True)

    # Some rows have NaN in the "fielder" column, which is not a supported
    # data type in firebase. Replace with "-" to show absence of fielder.
    match_dismissal.fillna("-", inplace=True)

    return match_dismissal


############ Player Description & Player Match initial dataframes
def initialise_player_dataframes(df_deliveries, df_matches):
    # Initialise the dataframe by taking the inner join of
    # the desired columns from df_deliveries and df_matches
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

    player_dataframes = {"player_desc": player_desc,
                          "player_match": player_match}
    return player_dataframes


############# Match Description initial dataframe
def initialise_match_desc(df_deliveries, df_matches):
    # Filter out the columns needed from df_matches
    match_desc = df_matches.copy()
    match_desc.venue = "{stadium}, {city}".format(stadium=match_desc.venue, city=match_desc.city)
    match_desc.drop(columns=["city"], axis=1, inplace=True)

    # Rename columns as per the schema naming conventions
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

    return match_desc

################ SeasonWise Initial Table
def initialise_season_wise(df_deliveries, df_matches):
    # Initialise the dataframe by taking the inner join of
    # the desired columns from df_deliveries and df_matches
    # and rename columns as per the schema naming conventions
    season_wise = pd.merge(df_deliveries[['matchID',
                                          'total_runs',
                                          'batting_team']].copy(),
                           df_matches[['matchID',
                                       'season']].copy(),
                           how='inner', on='matchID')\
                           .rename(columns={"batting_team": "team",
                                            "total_runs": "runs"})

    return season_wise


############### TeamWise Initial Table
def initialise_team_wise(df_deliveries, df_matches):
    # Initialise the dataframe by taking the inner join of
    # the desired columns from df_deliveries and df_matches
    # and rename columns as per the schema naming conventions
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

    return team_wise


############## VenueWise initial Table
def initialise_venue_wise(df_deliveries, df_matches):
    # Initialise the dataframe by taking the inner join of
    # the desired columns from df_deliveries and df_matches
    # and rename columns as per the schema naming conventions
    venue_wise = pd.merge(df_deliveries[['matchID',
                                        'total_runs']].copy(),
                           df_matches[['matchID',
                                       'city',
                                       'venue']].copy(),
                           how='inner', on='matchID')\
                           .rename(columns={"venue": "stadium",
                                            "total_runs": "runs"})

    # The Dubai International Cricket Stadium has a NaN value
    # for city in the original table
    venue_wise.fillna("Dubai", inplace=True)

    return venue_wise
