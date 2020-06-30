import pandas as pd

class FinalDataframes:
    def __init__(self, initial_dataframes):
        self.df_deliveries = initial_dataframes.df_deliveries
        self.df_matches = initial_dataframes.df_matches

        self.initialise_match_stats()
        self.initialise_match_dismissal()
        self.initialise_player_dataframes()
        self.initialise_match_desc()
        self.initialise_season_wise()
        self.initialise_team_wise()
        self.initialise_venue_wise()

        self.modify_primarykey_values()

    ################ MatchStats initial dataframe
    def initialise_match_stats(self):
        # Filter out the columns needed from df_deliveries
        self.match_stats = self.df_deliveries[["matchID",
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
        self.match_stats.rename(columns={"batting_team": "team",
                                         "total_runs": "runs"},
                                inplace=True)


    ############# DismissalTable initial dataframe
    def initialise_match_dismissal(self):
        # Filter out the columns needed from df_deliveries
        self.match_dismissal = self.df_deliveries.filter(["matchID",
                                                          "over",
                                                          "ball",
                                                          "batting_team",
                                                          "player_dismissed",
                                                          "non_striker",
                                                          "bowler",
                                                          "fielder",
                                                          "dismissal_kind"],
                                                         axis=1)

        # Drop entries in which no player was dismissed
        self.match_dismissal.dropna(axis=0,
                                    subset=["player_dismissed"],
                                    inplace=True)
        self.match_dismissal = self.match_dismissal.reset_index(drop=True)

        # Rename columns as per the schema naming conventions
        self.match_dismissal.rename(columns={"batting_team": "team",
                                             "player_dismissed": "playerDismissed",
                                             "non_striker": "nonStriker",
                                             "dismissal_kind": "type"},
                                    inplace=True)

        # Some rows have NaN in the "fielder" column, which is not a supported
        # data type in firebase. Replace with "-" to show absence of fielder.
        self.match_dismissal.fillna("-", inplace=True)


    ############ Player Description & Player Match initial dataframes
    def initialise_player_dataframes(self):
        # Initialise the dataframe by taking the inner join of
        # the desired columns from df_deliveries and df_matches
        self.players_seasons = pd.merge(self.df_deliveries[['matchID',
                                                            'batting_team',
                                                            'bowling_team',
                                                            'batsman',
                                                            'non_striker',
                                                            'bowler',
                                                            'fielder']].copy(),
                                        self.df_matches[['matchID',
                                                    'season']].copy(),
                                        how='inner', on='matchID')

        self.batsmen = self.players_seasons.filter(["matchID","season", "batting_team", "batsman"], axis=1)
        self.batsmen.rename(columns={"batsman": "player",
                                     "batting_team": "team"},
                            inplace=True)

        self.non_strikers = self.players_seasons.filter(["matchID","season", "batting_team", "non_striker"], axis=1)
        self.non_strikers.rename(columns={"non_striker": "player",
                                          "batting_team": "team"},
                                 inplace=True)

        self.bowlers = self.players_seasons.filter(["matchID","season", "bowling_team", "bowler"], axis=1)
        self.bowlers.rename(columns={"bowler": "player",
                                     "bowling_team": "team"},
                            inplace=True)

        self.fielders = self.players_seasons.filter(["matchID","season", "bowling_team", "fielder"], axis=1)
        self.fielders.rename(columns={"fielder": "player",
                                      "bowling_team": "team"},
                             inplace=True)

        # Concatenate all of them
        self.players_subsets = (self.batsmen, self.non_strikers,
                                self.bowlers, self.fielders)
        self.players = pd.concat(self.players_subsets, ignore_index=True)

        # Remove all rows with NaN values
        self.players.dropna(axis=0, subset=["player"], inplace=True)

        # To remove the " (sub)" substring that was there in the original data
        # to signify that the player came in as a substitute
        self.players.player = self.players.player.map(lambda x: x.rstrip(" (sub)"))

        # Player Match dataframe
        self.player_match = self.players.filter(["matchID", "player"], axis=1)
        self.player_match = self.player_match.reset_index(drop=True)

        # Player Description dataframe
        self.player_desc = self.players.filter(["season", "team", "player"], axis=1)
        self.player_desc = self.player_desc.reset_index(drop=True)

        # Remove all duplicate rows
        self.player_desc.drop_duplicates(inplace=True)
        self.player_desc.fillna("-", inplace=True)

        self.player_match.drop_duplicates(inplace=True)
        self.player_match.fillna("-", inplace=True)


    ############# Match Description initial dataframe
    def initialise_match_desc(self):
        # Filter out the columns needed from df_matches
        self.match_desc = self.df_matches.copy()
        self.match_desc.venue = "{stadium}, {city}".format(stadium=self.match_desc.venue,\
                                                           city=self.match_desc.city)
        self.match_desc.drop(columns=["city"], axis=1, inplace=True)

        # Rename columns as per the schema naming conventions
        self.match_desc.rename(columns={"date": "matchDate",
                                        "win_by_runs": "winByRuns",
                                        "win_by_wickets": "winByWickets",
                                        "winner": "result",
                                        "player_of_match": "playerOfMatch",
                                        "toss_winner": "tossWinner",
                                        "toss_decision": "tossDecision"},
                               inplace=True)

        # Venue isn't avaliable for all matches i.e. some rows have NaN under "venue"
        self.match_desc.fillna("-", inplace=True)


    ################ SeasonWise Initial Table
    def initialise_season_wise(self):
        # Initialise the dataframe by taking the inner join of
        # the desired columns from df_deliveries and df_matches
        # and rename columns as per the schema naming conventions
        season_wise = (pd.merge(self.df_deliveries[['matchID',
                                                    'total_runs',
                                                    'batting_team']].copy(),
                                self.df_matches[['matchID',
                                                 'season']].copy(),
                                how='inner', on='matchID')\
                       .rename(columns={"batting_team": "team",
                                        "total_runs": "runs"}))


    ############### TeamWise Initial Table
    def initialise_team_wise(self):
        # Initialise the dataframe by taking the inner join of
        # the desired columns from df_deliveries and df_matches
        # and rename columns as per the schema naming conventions
        self.team_wise = (pd.merge(self.df_deliveries[['matchID',
                                                       'total_runs',
                                                       'batting_team']].copy(),
                                   self.df_matches[['matchID',
                                                    'season',
                                                    'toss_winner',
                                                    'winner']].copy(),
                                   how='inner', on='matchID')\
                          .rename(columns={"batting_team": "team",
                                           "total_runs": "runs",
                                           "toss_winner": "tossWinner",
                                           "winner": "result"}))


    ############## VenueWise initial Table
    def initialise_venue_wise(self):
        # Initialise the dataframe by taking the inner join of
        # the desired columns from df_deliveries and df_matches
        # and rename columns as per the schema naming conventions
        self.venue_wise = (pd.merge(self.df_deliveries[['matchID',
                                                        'total_runs']].copy(),
                                    self.df_matches[['matchID',
                                                     'city',
                                                     'venue']].copy(),
                                    how='inner', on='matchID')\
                           .rename(columns={"venue": "stadium",
                                            "total_runs": "runs"}))

        # The Dubai International Cricket Stadium has a NaN value
        # for city in the original table
        self.venue_wise.fillna("Dubai", inplace=True)


    # Modifying column values of P.K. so that they match the format of
    # the keys in the final database design
    def modify_primarykey_values(self):
        self.match_stats.matchID = "matchID_{value}".format(value=self.match_stats.matchID)
        self.match_stats.over = "over_{value}".format(value=self.match_stats.over)

        self.match_dismissal.matchID = "matchID_{value}".format(value=self.match_dismissal.matchID)
        self.match_dismissal.over = "over_{value}".format(value=self.match_dismissal.over)
        self.match_dismissal.ball = "ball_{value}".format(value=self.match_dismissal.ball)

        self.player_desc.season = "season_{value}".format(value=self.player_desc.season)

        self.player_match.matchID = "matchID_{value}".format(value=self.player_match.matchID)

        self.match_desc.matchID = "matchID_{value}".format(value=self.match_desc.matchID)
