from collections import defaultdict


def nested_dict():
    """Recursive function to return a new instance of defaultdict"""

    return defaultdict(nested_dict)
