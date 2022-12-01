import json


def build_dict(dict_template, res):
    """
    It takes a list of tuples and a dictionary as input, and returns a list of dictionaries

    :param dict_template: the template of the dictionary we want to build
    :param res: the result of the query
    :return: A list of dictionaries.
    """

    data = [dict(zip(dict_template.keys(), i)) for i in res]

    data = [
        dict(
            (k, v.replace('\n', '').replace('  ', '').replace(',', ', ')) if isinstance(v, str) else (k, v)
            for k, v in i.items()) for i in data.copy()
    ]

    return data


def build_json(return_value, res):
    """
    It takes a list of dictionaries, and returns a list of dictionaries, where the values of the original
    dictionaries are converted from strings to dictionaries

    :param return_value: the return value of the query
    :param res: the list of columns to exclude from the json
    :return: A list of dictionaries.
    """
    data = [json.loads(i[k]) for i in return_value for k, v in i.items() if k not in res]
    return data


def build_index(lists, value1, value2):
    """
    "Return a list of values from the list 'lists' that are between the values 'value1' and 'value2' (inclusive)."

    The function takes three arguments:

    lists: a list of values
    value1: a value in the list
    value2: a value in the list
    The function returns a list of values from the list 'lists' that are between the values 'value1' and 'value2'
    (inclusive)

    :param lists: the list of values you want to search through
    :param value1: The first value to search for in the list
    :param value2: The value that you want to stop at
    :return: the index of the list between the two values.
    """

    data = lists[lists.index(value1) + 1:lists.index(value2)]
    return data


def build_field(res):
    """
    It takes a string and returns a list of strings

    :param res: the result of the query -> sql query statement
    :return: The data is being returned as a list of strings.
    """
    data = res[res.find('select') + 6:res.find('from')].strip().split(',')
    return data
