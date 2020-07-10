import pandas as pd

class InitialDataframes:
    def __init__(self, deliveries_csv, matches_csv, del_cols_orig, match_cols_orig):
        self.df_deliveries = pd.read_csv(deliveries_csv, usecols=del_cols_orig)
        self.df_matches = pd.read_csv(matches_csv, usecols=match_cols_orig)

        # Rename the match IDs columns in both dataframes to a uniform name
        self.df_matches.rename(columns={"id": "matchID"}, inplace=True)
        self.df_deliveries.rename(columns={"match_id": "matchID"}, inplace=True)
