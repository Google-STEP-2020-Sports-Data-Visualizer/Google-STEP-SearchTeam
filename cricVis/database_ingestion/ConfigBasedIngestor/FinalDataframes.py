import pandas as pd
import numpy as np

import utils.util_fns as util_fns

class FinalDataframes:
    """Creates the dataframes corresponding to each schema in database."""

    def __init__(self, final_matches, initial_dfs, configs):
        """
        Parameters
        ----------

        final_matches: list
            List of the match IDs of the final matches across different years
            of a sports tournament/league.

        configs: dict
            Dictionary containing the config settings for creating each dataframe.

        initial_dfs: dict
            Dictionary of the dataframes created by the InitialDataframes module.

        Attributes
        ----------

        __dfnames_list: list
            List of names of dataframes.

        final_matches: list
            List of the match IDs of the final matches across different years
            of a sports tournament/league.

        initial_dfs: dict
            Dictionary of initial dataframes.

        dfs: dict
            Dictionary of dataframes created.
        """

        __dfnames_list = list(configs.keys())

        self.final_matches = final_matches

        self.initial_dfs = initial_dfs
        self.dfs = {}

        for dfname in __dfnames_list:
            self.__create_df(dfname, configs[dfname])

    def __create_df(self, dfname, df_config):
        """
        Creates the dataframes and saves it in the dfs dictionary.

        Parameters
        ----------

        dfname: str
            Name of the dataframe to be created.

        df_config: dict
            Dictionary containing the following configs needed to create the dataframe:
                -initial dataframe(s) needed
                -functions to be applied and their parameters
        """
        df = None

        for fn in df_config["functions"]:
            df = self.__execute(df, dfname, fn, df_config["functions"][fn])
            self.dfs[dfname] = df

    def __execute(self, df, dfname, fn, fn_config):
        """
        Executes a function on the dataframe(s).

        Parameters
        ----------

        df: Pandas.DataFrame
            Dataframe on which the function is to be applied.

        dfname: str
            Name of the dataframe on which the function is being applied.

        fn: str
            Name of the function to be applied.

        fn_config: dict
            Parameters of the function.

        Returns
        -------

        df: Pandas.DataFrame
            Modified dataframe.
        """
        if fn == "copy":
            df_orig = self.__assign_based_on_class(fn_config["class"], fn_config["dataframe"])
            df = df_orig.copy()

        elif fn == "filter_rows":
            df[fn_config["column"]] = df[fn_config["column"]].apply(lambda x: util_fns.filter_rows(x, fn_config["values_allowed"]))

        elif fn == "replace":
            try:
                df = df.replace(fn_config["to_replace"], eval(fn_config["value"]))
            except TypeError:
                df = df.replace(fn_config["to_replace"], fn_config["value"])

        elif fn == "astype":
            df = df.astype(fn_config)

        elif fn == "apply" or fn == "map":
            for column in fn_config["columns"]:
                df[column] = df[column].apply(lambda x: eval(fn_config["lambda"]))

        elif fn == "filter":
            df_orig = self.__assign_based_on_class(fn_config["class"], fn_config["dataframe"])
            df = df_orig.filter(**fn_config["params"])

        elif fn == "rename":
            df = df.rename(columns=fn_config["columns"])

        elif fn == "dropna":
            df = df.dropna(**fn_config)

        elif fn == "fillna":
            if "columns" in list(fn_config.keys()):
                df[fn_config["columns"]] = df[fn_config["columns"]].fillna(fn_config["value"])

            else:
                df.fillna(fn_config["value"], inplace=True)

        elif fn == "add_columns":
            for col in fn_config.keys():
                df[col] = fn_config[col]

        elif fn == "add_columns_using_boolean_logic":
            for col in fn_config.keys():
                df[col] = util_fns.boolean_logic(*eval(fn_config[col]))

        elif fn == "remove_invalid_chars":
            df = util_fns.remove_invalid_chars(df, **fn_config)

        elif fn == "concat":
            dfs_subset_list = [self.__assign_based_on_class(fn_config["class"], subset_name) for subset_name in fn_config["dataframes"]]
            df = pd.concat(tuple(dfs_subset_list), ignore_index=True)

        elif fn == "merge":
            # Left table for making the join
            left = self.__assign_based_on_class(fn_config["left"]["class"], fn_config["left"]["dataframe"])
            left_cols = fn_config["left"]["columns"]

            # Right table for making the join
            right = self.__assign_based_on_class(fn_config["right"]["class"], fn_config["right"]["dataframe"])
            right_cols = fn_config["right"]["columns"]

            df = pd.merge(left[left_cols].copy(),
                          right[right_cols].copy(),
                          how=fn_config["how"], on=fn_config["on"])

        elif fn == "groupby":
            df_orig = self.__assign_based_on_class(fn_config["class"], fn_config["dataframe"])
            df = df_orig.groupby(**fn_config["params"])

        elif fn == "agg":
            df = df.agg(fn_config)

        elif fn == "drop":
            df = df.drop(**fn_config)

        return df

    def __assign_based_on_class(self, class_name, dataframe_name):
        """
        Returns dataframe from the class provided.

        Parameters
        ----------

        class_name: str
            Name of the class.

        dataframe_name: str
            Name of the dataframe to be read.

        Returns
        -------

        df_orig: Pandas.DataFrame
            The required dataframe from the required class.
        """
        
        if(class_name == "FinalDataframes"):
            df_orig = self.dfs[dataframe_name]
        else:
            df_orig = self.initial_dfs[dataframe_name]

        return df_orig
