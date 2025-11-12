#custom errors
class GameError(Exception):
    """Generic error"""
    pass

class InvalidClassAttrType(GameError):
    """Raise an error if a class attribute received an invalid attr type"""
    pass

class NegativeStat(GameError):
    """Raise an error if a player stat receives a non positive integer"""
    pass

class SaveDataError(GameError):
    pass