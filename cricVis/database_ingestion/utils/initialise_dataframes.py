import pandas as pd

def initialise_dataframes():
    # List of columns required from deliveries.csv
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

    # List of columns required from matches.csv
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

    # Rename the match IDs columns in both dataframes to a uniform name
    df_matches.rename(columns={"id": "matchID"}, inplace=True)
    df_deliveries.rename(columns={"match_id": "matchID"}, inplace=True)

    return df_deliveries, df_matches
