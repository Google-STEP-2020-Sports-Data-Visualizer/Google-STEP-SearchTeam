import pandas as pd

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

        if "renamed_columns" in df_config.keys():
            df.rename(columns=df_config["renamed_columns"], inplace=True)

        self.dfs[dfname] = df
