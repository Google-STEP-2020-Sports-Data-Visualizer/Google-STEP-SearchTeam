import pandas as pd
import numpy as np
from queue import LifoQueue as stack

from dateutil.parser import parse
from dateutil.parser._parser import ParserError
from datetime import datetime


def is_list(x):
    """Returns True if x is a string of a list."""

    x = x.strip()
    return x[0] == '[' and x[-1] == ']'


def filter_rows(x, values_allowed):
    """
    Filters out rows based on whether a particular column has the desired values.

    Parameters
    ----------

    x: str
        Value of column in a particular row

    values_allowed: list
        List of values based on which the filtering is done

    Returns
    -------

    desired value
        if it is present in x
    np.nan
        otherwise
    """

    if(is_list(x)):
        set_x = set(eval(x))
        values_allowed_set = set(values_allowed)
        required_val = list(set_x & values_allowed_set)

        # Return NaN if the intersection is an empty set
        return np.nan if not required_val else required_val[0].replace(",", "")

    else:
        return x if x in values_allowed else np.nan


def find_final_matches(df):
    """Returns a lists of match IDs of the final match of each year of a sports league/tournament."""

    return df.groupby("season")[["match_id"]].max()["match_id"].to_list()


def extract_date(date_str):
    """
    Extract date from the given string.

    Parameters
    ----------

    date_str: str
        A string possibly containing a date within it.

    Raises
    ------

    ValueError
        If the string contains an incomplete date (for e.g. only the year).

    ParserError:
        If the string does not contain any date.

    Returns
    -------

    date in the format "dd-mm-yyy"
        if the string contains a complete date
    "unavailable"
        otherwise

    Example
    -------

    date_str = "July 8, 2001, Birmingham, Warwickshire" would return "08-07-2001"
    """

    try:
        if(parse(date_str,
                 fuzzy=True,
                 default=datetime(1, 1, 1))
            != parse(date_str,
                     fuzzy=True,
                     default=datetime(2, 2, 2))):
            raise ValueError

        else:
            return '{dd}-{mm}-{yyyy}'.format(dd=parse(date_str, fuzzy=True).day,
                                             mm=parse(date_str, fuzzy=True).month,
                                             yyyy=parse(date_str, fuzzy=True).year)

    except (ValueError, ParserError):
        return "unavailable"


def remove_invalid_chars(df, columns, invalid_chars=[".", "$", "[", "]", "#", "/"]):
    """
    Removes all characters mentioned in invalid_chars from the dataframe columns.

    Parameters
    ----------

    df: Pandas.DataFrame
        The dataframe to be modified

    columns: list
        List of columns from which the invalid characters need to be removed.

    invalid_chars: list
        List of invalid characters.

    Returns
    -------

    df: Pandas.DataFrame
        Modified dataframe.
    """
    for col in columns:
        for invalid_char in invalid_chars:
            df[col] = df[col].map(lambda x: str(x).replace(invalid_char, ""))

    return df

# Takes a postfix expression to create a new column after
# conditionally combining the columns passed as arguments


def boolean_logic(*args, on_true=1, on_false=0):
    """
    Creates new dataframe column by operating on existing column(s).

    Parameters
    ----------

    args: list
        Ordered list of operands and operators constituting a postifix expression.

    on_true: int or str
        Value to be assigned if the result of an operation is true.

    on_true: int or str
        Value to be assigned if the result of an operation is false.

    Returns
    -------

    Pandas.Series object
        Result of evaluating the postfix expression.
    """

    def is_operator(x):
        """Returns True if the character x is in this operators list."""

        return x in ["&", "|", "==", "!=", "isin"]

    def operate(operand1, operand2, op):
        """Returns result of applying operation op to operand1 and operand2."""

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
