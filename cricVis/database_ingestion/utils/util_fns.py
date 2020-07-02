import pandas as pd

from dateutil.parser import parse
from dateutil.parser._parser import ParserError
from datetime import datetime

def extract_date(date_str):
    try:
        if(parse(born, fuzzy=True, default=datetime(1,1,1)) != parse(born, fuzzy=True, default=datetime(2,2,2))):
            raise ValueError

        else:
            return '{dd}-{mm}-{yyyy}'.format(dd=parse(born, fuzzy=True).day, mm=parse(born, fuzzy=True).month, yyyy=parse(born, fuzzy=True).year)

    except (ValueError, ParserError):
        return "unavailable"


def remove_invalid_chars(df_column):
    df_column = df_column.map(lambda x: x.replace(".", ""))
    df_column = df_column.map(lambda x: x.replace("$", ""))
    df_column = df_column.map(lambda x: x.replace("[", ""))
    df_column = df_column.map(lambda x: x.replace("]", ""))
    df_column = df_column.map(lambda x: x.replace("#", ""))
    df_column = df_column.map(lambda x: x.replace("/", ""))
