from abc import ABC, abstractmethod


class HttpBrokerRequest(ABC):
    """Request Object detailing information on how to build the HTTP Request
    todo
    """
    def __init__(
            self,
            method
    ):
        """
        :param method : str, required
            The HTTPMethod (see broker_api.http.method.py) corresponding with this request
        """
        super().__init__()
        self._method = method
