#python
import re

def clamp(value, lower=None, upper=None):
    """ Returns value no lower than lower and no greater than upper.
        Use None to clamp in one direction only. """
    if lower is not None:
        value = max(value, lower)
    if upper is not None:
        value = min(value, upper)
    return value

def StrToInt(s, default=None):
    """ Returns first valid integer in input string. """
    try:
        number = re.search(r"[-+]?\d*\d+|\d+", s).group(0)
        return int(number)
    except AttributeError:
        if default is not None:
            return default
        else:
            raise ValueError("no valid numbers found")

def StrToFlt(s, default=None):
    """ Returns first valid float in input string. """
    try:
        number = re.search(r"[-+]?\d*\.\d+|\d+", s).group(0)
        return float(number)
    except AttributeError:
        if default is not None:
            return default
        else:
            raise ValueError("no valid numbers found")

