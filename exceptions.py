class TMSException(Exception):
    """
    All the raised exceptions within thTMS
    """
    pass

class TMSValueError(TMSException):
    """
    All Value errors
    """
    pass

class PsqlDataSourceException(TMSException):
    """
    Exceptions related to Postgres DataBase
    """
    pass