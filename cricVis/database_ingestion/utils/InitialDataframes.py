import pandas as pd
import utils.util_fns as util_fns

class InitialDataframes:
    def __init__(self, configs):
        dfnames_list = list(configs.keys())
        self.dfs = {}

        for dfname in dfnames_list:
            self.file_to_dataframe(dfname, configs[dfname])

    def file_to_dataframe(self, dfname, df_config):
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
