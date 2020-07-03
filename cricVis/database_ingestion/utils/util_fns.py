import pandas as pd
import numpy as np
from queue import LifoQueue as stack

from dateutil.parser import parse
from dateutil.parser._parser import ParserError
from datetime import datetime

def find_final_matches(df):
    # Enlists matchID of the final match of each season
    return df.groupby("season")[["match_id"]].max()["match_id"].to_list()

def extract_date(date_str):
    try:
        if(parse(date_str, fuzzy=True, default=datetime(1,1,1)) != parse(date_str, fuzzy=True, default=datetime(2,2,2))):
            raise ValueError

        else:
            return '{dd}-{mm}-{yyyy}'.format(dd=parse(date_str, fuzzy=True).day, mm=parse(date_str, fuzzy=True).month, yyyy=parse(date_str, fuzzy=True).year)

    except (ValueError, ParserError):
        return "unavailable"


def remove_invalid_chars(df_column):
    df_column = df_column.map(lambda x: x.replace(".", ""))
    df_column = df_column.map(lambda x: x.replace("$", ""))
    df_column = df_column.map(lambda x: x.replace("[", ""))
    df_column = df_column.map(lambda x: x.replace("]", ""))
    df_column = df_column.map(lambda x: x.replace("#", ""))
    df_column = df_column.map(lambda x: x.replace("/", ""))

    return df_column

# Takes a postfix expression to create a new column after
# conditionally combining the columns passed as arguments
def boolean_logic(*args, on_true=1, on_false=0):
    def is_operator(x):
        return x in ["&", "|", "==", "!=", "isin"]

    def operate(operand1, operand2, op):
        if op == "==":
            return np.where(operand1 == operand2, on_true, on_false)

        elif op == "!=":
            return np.where(operand1 != operand2, on_true, on_false)

        elif op == "&":
            return np.where(operand1 & operand2, on_true, on_false)

        elif op == "|":
            return np.where(operand1 | operand2, on_true, on_false)

        elif op == "isin":
            return operand1.isin(operand2)

    operands = stack()

    for arg in args:
        if type(arg) == str and is_operator(arg):
            operand2 = operands.get()
            operand1 = operands.get()

            result = operate(operand1, operand2, arg)
            operands.put(result)

        else:
            operands.put(arg)

    return operands.get()
