import pandas as pd
import numpy as np

import utils.util_fns as util_fns

class GroupedDataframes:
    def __init__(self, final_dfs, configs):
        dfnames_list = list(configs.keys())

        self.final_dfs = final_dfs
        self.dfs = {}

        for dfname in dfnames_list:
            self.group_df(dfname, configs[dfname])

    def group_df(self, dfname, df_config):
        df = None

        for fn in df_config:
            df = self.execute(df, dfname, fn, df_config[fn])
            self.dfs[dfname] = df



    def execute(self, df, dfname, fn, fn_config):
        if fn == "copy":
            if(fn_config["class"] == "FinalDataframes"):
                df_orig = self.final_dfs[fn_config["dataframe"]]
            else:
                df_orig = self.dfs[fn_config["dataframe"]]
            df = df_orig.copy()

        elif fn == "filter_rows":
            df = df.loc[df[fn_config["column"]].isin(fn_config["isin"])]

        elif fn == "replace":
            df = df.replace(util_fns.str_eval(fn_config["to_replace"]), util_fns.str_eval(fn_config["value"]))

        elif fn == "astype":
            df = df.astype(fn_config)

        elif fn == "apply":
            df[fn_config["column"]] = df[fn_config["column"]].apply(lambda x: eval(fn_config["lambda"]))

        elif fn == "filter":
            if(fn_config["class"] == "FinalDataframes"):
                df_orig = self.final_dfs[fn_config["dataframe"]]
            else:
                df_orig = self.dfs[fn_config["dataframe"]]
            df = df_orig.filter(**fn_config["params"])

        elif fn == "rename":
            df = df.rename(columns=fn_config["columns"])

        elif fn == "dropna":
            df = df.dropna(**fn_config)

        elif fn == "fillna":
            df[fn_config["columns"]] = df[fn_config["columns"]].fillna(fn_config["value"])

        elif fn == "concat":
            if fn_config["class"] == "FinalDataframes":
                dfs_subset_list = [self.final_dfs[subset_name] for subset_name in fn_config["dataframes"]]
            else:
                dfs_subset_list = [self.dfs[subset_name] for subset_name in fn_config["dataframes"]]

            df = pd.concat(tuple(dfs_subset_list), ignore_index=True)

        elif fn == "groupby":
            if fn_config["class"] == "FinalDataframes":
                df_orig = self.final_dfs[fn_config["dataframe"]]
            else:
                df_orig = self.dfs[fn_config["dataframe"]]

            df = df_orig.groupby(**fn_config["params"])

        elif fn == "set_index":
            df = df.set_index(fn_config)

        elif fn == "agg":
            df = df.agg(fn_config)

        elif fn == "drop":
            df = df.drop(**fn_config)

        return df
