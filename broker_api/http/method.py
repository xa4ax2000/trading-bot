from enum import Enum


class HttpMethod(Enum):
    """HTTPMethod enumerated

    Attributes
    ----------
    GET : str
        Enum represented GET Http Method
    PUT : str
        Enum represented PUT Http Method
    POST : str
        Enum represented POST Http Method
    DELETE : str
        Enum represented DELETE Http Method
    """
    GET = 'GET'
    PUT = 'PUT'
    POST = 'POST'
    DELETE = 'DELETE'
