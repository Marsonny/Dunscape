from .exceptions import InvalidClassAttrType, NegativeStat


def validate_if_string(value, attrName, fromClass):
    if not isinstance(value, str):
        raise InvalidClassAttrType(f"{fromClass} '{attrName}' must be a string, but got {type(value)}.")
    return value

def validate_if_number(value, attrName, fromClass):
    if not isinstance(value, (int, float)):
        raise InvalidClassAttrType(f"{fromClass} '{attrName}' must be a string, but got {type(value)}.")
    elif value <= 0:
        raise NegativeStat(f"{fromClass} '{attrName}' must either be a positive non-zero integer or float")
    return value  