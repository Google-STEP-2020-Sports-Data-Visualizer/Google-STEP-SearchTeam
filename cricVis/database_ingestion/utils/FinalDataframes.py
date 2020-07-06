import pandas as pd
import numpy as np

import utils.util_fns as util_fns

class FinalDataframes:
    def __init__(self, final_matches, initial_dfs, configs):
        __dfnames_list = list(configs.keys())

        self.final_matches = final_matches

        self.initial_dfs = initial_dfs
        self.dfs = {}

        for dfname in __dfnames_list:
            self.__create_df(dfname, configs[dfname])

    def __create_df(self, dfname, df_config):
        df = None

        for fn in df_config["functions"]:
            df = self.__execute(df, dfname, fn, df_config["functions"][fn])
            self.dfs[dfname] = df

    # TODO: Write a switcher to replace if-elifs
    def __execute(self, df, dfname, fn, fn_config):
        if fn == "copy":
            df_orig = self.__assign_based_on_class(fn_config)
            df = df_orig.copy()

        elif fn == "filter_rows":
            df[fn_config["column"]] = df[fn_config["column"]].apply(lambda x: util_fns.filter_rows(x, fn_config["values_allowed"]))

        elif fn == "replace":
            df = df.replace(fn_config["to_replace"], eval(fn_config["value"]))

        elif fn == "astype":
            df = df.astype(fn_config)

        elif fn == "apply" or fn == "map":
            for column in fn_config["columns"]:
                df[column] = df[column].apply(lambda x: eval(fn_config["lambda"]))

        elif fn == "filter":
            df_orig = self.__assign_based_on_class(fn_config)
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

        elif fn == "validate_keys":
            if "fillna" in fn_config.keys():
                self.__execute(df, dfname, "fillna", fn_config["fillna"])

            for col in fn_config["remove_invalid_chars"]:
                df[col] = util_fns.remove_invalid_chars(df[col])

        elif fn == "concat":
            dfs_subset_list = self.__assign_based_on_class(fn_config)
            df = pd.concat(tuple(dfs_subset_list), ignore_index=True)

        elif fn == "merge":
            # Left table for making the join
            left = self.__assign_based_on_class(fn_config["left"])
            left_cols = fn_config["left"]["columns"]

            # Right table for making the join
            right = self.__assign_based_on_class(fn_config["right"])
            right_cols = fn_config["right"]["columns"]

            df = pd.merge(left[left_cols].copy(),
                          right[right_cols].copy(),
                          how=fn_config["how"], on=fn_config["on"])

        elif fn == "groupby":
            df_orig = self.__assign_based_on_class(fn_config)
            df = df_orig.groupby(**fn_config["params"])

        elif fn == "agg":
            df = df.agg(fn_config)

        elif fn == "drop":
            df = df.drop(**fn_config)

        return df

    def __assign_based_on_class(self, fn_config):
        if(fn_config["class"] == "FinalDataframes"):
            df_orig = self.final_dfs[fn_config["dataframe"]]
        else:
            df_orig = self.dfs[fn_config["dataframe"]]
