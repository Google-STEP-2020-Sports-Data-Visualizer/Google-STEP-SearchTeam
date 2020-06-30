import pandas as pd

class CricketStats:
    def __init__(self, table_name, *csv_files):
        #Name of table as per schema design
        self.table_name = table_name

        self.subset_dfs = (pd.read_csv(csv_file,\
                                       dtype=self.column_types,\
                                       usecols=list(self.column_types.keys()),\
                                       na_values=['-', 'NA'],\
                                       parse_dates=["Innings Date"])\
                           for csv_file in csv_files)

        # The csv_files is an args tuple containing paths to csv files of the
        # data for the required match type over different centuries
        # eg. there are separate datasets for 20th and 21st century Men's ODI
        # Since there is no direct function to read all these csv files into a
        # dataframe, they're read into separate dataframes and then concatenated
        self.df = pd.concat(self.subset_dfs, ignore_index=True)


    def manipulate(self):
        # The year value is extracted from the date of innings
        self.df["year"] = self.df["Innings Date"].apply(lambda date: date.year)

        # Rename columns as per schema design
        self.df = self.df.rename(columns=self.renamed_columns)

        # Drop all entries that don't have the flag (bat/bowl) column set to 1
        self.df = self.df.loc[self.df[self.flag_column] == 1]

        # Drop columns that are no longer needed
        self.df.drop(["Innings Date", self.flag_column], axis=1, inplace=True)

        # Remove "." character as it is an invalid character for a Firebase key
        self.df.player = self.df.player.map(lambda x: x.replace(".", ""))

    def group_df(self):
        # Group by year and player and apply the required aggregate functions
        self.grouped_df = (self.df.groupby(["year", "player"],\
                                          as_index=False)\
                           .agg(self.cols_agg_fn))

        # Creates a generic field attribute to hold the names of the different
        # stats to be visualised, and a value attribute to hold the value for that stat.
        # id_vars: identifier variables
        # value_vars: columns(s) to unpivot
        # var_name: name for the ‘variable’ column
        # value_name: name for the ‘value’ column.
        self.grouped_df = self.grouped_df.melt(id_vars=["year", "player"],\
                                               value_vars=list(self.cols_agg_fn.keys()),\
                                               var_name="field",\
                                               value_name="value")

        self.grouped_df.dropna(inplace=True)

        self.grouped_df = self.grouped_df.groupby(["year", "field"])

    def df_to_dict(self, db_dict, db_rules_dict):
        for name, df_group in self.grouped_df:
            for row in df_group.itertuples():
                db_dict[self.table_name][row.year][row.field][row.player] = row.value
                db_rules_dict[self.table_name][row.year][row.field][".indexOn"] = ".value"


class BattingStats(CricketStats):
    # A mapping of column names to the data type to be enforced on them
    column_types = {"Innings Player": "object",
                    "Innings Runs Scored Num": "float64",
                    "Innings Batted Flag": "float64",
                    "Innings Boundary Fours": "float64",
                    "Innings Boundary Sixes": "float64",
                    "Innings Batting Strike Rate": "float64",
                    "Innings Date": "object",
                    "50's": "float64",
                    "Innings Balls Faced": "float64",
                    "100's": "float64"}

    # A mapping of original column names to new ones
    renamed_columns = {"Innings Runs Scored Num": "runsScored",\
                       "Innings Boundary Fours": "fours",\
                       "Innings Boundary Sixes": "sixes",\
                       "Innings Batting Strike Rate": "strikeRate",\
                       "50's": "fifties",\
                       "100's": "hundreds",\
                       "Innings Player": "player"}

    #To filter out the non-batting entries
    flag_column = "Innings Batted Flag"

    # A mapping of columns names to the aggregate functions to be applied to
    # each of them on grouping the table
    cols_agg_fn = {"runsScored": "sum",
                   "fours": "sum",
                   "sixes": "sum",
                   "strikeRate": "mean",
                   "fifties": "sum",
                   "hundreds": "sum"}

    def __init__(self, table_name, *csv_files):
        super().__init__(table_name, *csv_files)


class BowlingStats(CricketStats):
    # A mapping of column names to the data type to be enforced on them
    column_types = {"Innings Player": "object",
                    "Innings Bowled Flag": "float64",
                    "Innings Maidens Bowled": "float64",
                    "Innings Runs Conceded": "float64",
                    "Innings Wickets Taken": "float64",
                    "Innings Economy Rate": "float64",
                    "Innings Date": "object"}

    # A mapping of original column names to new ones
    renamed_columns = {"Innings Maidens Bowled": "maidens",\
                       "Innings Runs Conceded": "runsConceded",\
                       "Innings Wickets Taken": "wickets",\
                       "Innings Economy Rate": "economyRate",\
                       "Innings Player": "player"}

    #To filter out the non-batting entries
    flag_column = "Innings Bowled Flag"

    # A mapping of columns names to the aggregate functions to be applied to
    # each of them on grouping the table
    cols_agg_fn = {"maidens": "sum",
                   "runsConceded": "sum",
                   "wickets": "sum",
                   "economyRate": "mean"}

    def __init__(self, table_name, *csv_files):
        super().__init__(table_name, *csv_files)
