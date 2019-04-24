import re

line = 'asdf fjdk; afed, fjek,asdf, foo'

def split_using_multi(pattern, line):
    """

    :param pattern: regex
    :param line: text to be splitted
    :return: list of splitted strings
    """
    return re.split(pattern, line)