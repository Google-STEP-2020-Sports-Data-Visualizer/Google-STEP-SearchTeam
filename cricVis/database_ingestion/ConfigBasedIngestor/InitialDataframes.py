import pandas as pd
import utils.util_fns as util_fns


class InitialDataframes:
    """Parses each raw dataset into dataframes."""

    def __init__(self, configs):
        """
        Parameters
        ----------

        configs: dict
            Dictionary containing the config settings for initialising each dataframe.

        Attributes
        ----------

        __dfnames_list: list
            List of names of dataframes.

        dfs: dict
            Dictionary of the dataframes created.
        """

        __dfnames_list = list(configs.keys())
        self.dfs = {}

        for dfname in __dfnames_list:
            self.__file_to_dataframe(dfname, configs[dfname])

    def __file_to_dataframe(self, dfname, df_config):
        """
        Reads a dataset into a Pandas dataframe.

        Parameters
        ----------

        dfname: str
            Name of the dataframe to be initialised.

        df_config: dict
            Dictionary containing the following configs needed to create the dataframe:
                -file type of dataset
                -path to dataset
                -columns to be used
                -how to rename the columns (optional)
                -data type of each column (optional)
        """
        if(df_config["file_type"] == "csv"):
            df = pd.read_csv(**df_config["params"])

        elif(df_config["file_type"] == "excel"):
            df = pd.read_excel(**df_config["params"])

        elif(df_config["file_type"] == "json"):
            df = pd.read_json(**df_config["params"])

        if "renamed_columns" in df_config.keys():
            df.rename(columns=df_config["renamed_columns"], inplace=True)

        if "find_final_matches" in df_config.keys():
            self.final_matches = util_fns.find_final_matches(df)

        self.dfs[dfname] = df
