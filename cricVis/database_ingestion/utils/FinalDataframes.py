import pandas as pd
import numpy as np

import utils.util_fns as util_fns

class FinalDataframes:
    def __init__(self, final_matches, initial_dfs, configs):
        dfnames_list = list(configs.keys())

        self.final_matches = final_matches

        self.initial_dfs = initial_dfs
        self.dfs = {}

        for dfname in dfnames_list:
            self.create_df(dfname, configs[dfname])

    def create_df(self, dfname, df_config):
        df = pd.DataFrame
        for fn in df_config["functions"]:
            df = self.execute(df, dfname, fn, df_config["functions"][fn])
            self.dfs[dfname] = df

<<<<<<< HEAD
=======
        print(self.dfs[dfname])

>>>>>>> bd12b18dc957d5d8e14358dad32395e1714346ec

    def execute(self, df, dfname, fn, fn_config):
        if fn == "copy":
            if(fn_config["class"] == "InitialDataframes"):
                df_orig = self.initial_dfs[fn_config["dataframe"]]
            else:
                df_orig = self.dfs[fn_config["dataframe"]]
            df = df_orig.copy()

        elif fn == "filter_rows":
            df = df.loc[df[fn_config["column"]].isin(fn_config["isin"])]

        elif fn == "replace":
            df = df.replace(fn_config["to_replace"], eval(fn_config["value"]))

        elif fn == "astype":
            df = df.astype(fn_config)

        elif fn == "apply":
            df[fn_config["column"]] = df[fn_config["column"]].apply(lambda x: eval(fn_config["lambda"]))

        elif fn == "filter":
            if(fn_config["class"] == "InitialDataframes"):
                df_orig = self.initial_dfs[fn_config["dataframe"]]
            else:
                df_orig = self.dfs[fn_config["dataframe"]]
            df = df_orig.filter(**fn_config["params"])

        elif fn == "rename":
            df = df.rename(columns=fn_config["columns"])

        elif fn == "dropna":
            df = df.dropna(**fn_config)

        elif fn == "fillna":
            df[fn_config["columns"]] = df[fn_config["columns"]].fillna(fn_config["value"])

        elif fn == "add_columns":
            for col in fn_config.keys():
                df[col] = fn_config[col]

        elif fn == "add_columns_using_boolean_logic":
            for col in fn_config.keys():
                df[col] = util_fns.boolean_logic(*eval(fn_config[col]))

        elif fn == "validate_keys":
            if "fillna" in fn_config.keys():
                self.execute(df, dfname, "fillna", fn_config["fillna"])

            for col in fn_config["remove_invalid_chars"]:
                df[col] = util_fns.remove_invalid_chars(df[col])

        elif fn == "concat":
            if fn_config["class"] == "InitialDataframes":
                dfs_subset_list = [self.initial_dfs[subset_name] for subset_name in fn_config["dataframes"]]
            else:
                dfs_subset_list = [self.dfs[subset_name] for subset_name in fn_config["dataframes"]]

            df = pd.concat(tuple(dfs_subset_list), ignore_index=True)

        elif fn == "merge":
            # Left table for making the join
            if fn_config["left"]["class"] == "InitialDataframes":
                left = self.initial_dfs[fn_config["left"]["dataframe"]]
            else:
                left = self.dfs[fn_config["left"]["dataframe"]]

            left_cols = fn_config["left"]["columns"]

            # Right table for making the join
            if fn_config["right"]["class"] == "InitialDataframes":
                right = self.initial_dfs[fn_config["right"]["dataframe"]]
            else:
                right = self.dfs[fn_config["right"]["dataframe"]]

            right_cols = fn_config["right"]["columns"]

            df = pd.merge(left[left_cols].copy(),
                          right[right_cols].copy(),
                          how=fn_config["how"], on=fn_config["on"])

        elif fn == "groupby":
            if fn_config["class"] == "InitialDataframes":
                df_orig = self.initial_dfs[fn_config["dataframe"]]
            else:
                df_orig = self.dfs[fn_config["dataframe"]]

            df = df_orig.groupby(**fn_config["params"])

        elif fn == "agg":
            df = df.agg(fn_config)

        elif fn == "drop":
            df = df.drop(**fn_config)

        return df
