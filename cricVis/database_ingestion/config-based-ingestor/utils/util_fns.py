import pandas as pd

from dateutil.parser import parse
from dateutil.parser  import _parser

def extract_date(date_str):
    try:
        date_str = '{dd}-{mm}-{yyyy}'.format(dd=parse(date_str, fuzzy=True).day,
                                             mm=parse(date_str, fuzzy=True).month,
                                             yyyy=parse(date_str, fuzzy=True).year)

    except(_parser.ParserError):
        date_str = "unavailable"

def remove_invalid_chars(df_column):
    df_column = df_column.map(lambda x: x.replace(".", ""))
    df_column = df_column.map(lambda x: x.replace("$", ""))
    df_column = df_column.map(lambda x: x.replace("[", ""))
    df_column = df_column.map(lambda x: x.replace("]", ""))
    df_column = df_column.map(lambda x: x.replace("#", ""))
    df_column = df_column.map(lambda x: x.replace("/", ""))
