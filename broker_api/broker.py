from abc import ABC, abstractmethod
from decorators.abstract_class_attributes import abstract_class_attributes


@abstract_class_attributes('api_base_url', 'action_path')
class BrokerInterface(ABC):
    """Interface exposing all broker interactions possible.

    If a particular interaction is not supported by a particular broker, a
    NotSupportedException will be raised. Interactions could include anything from
    obtaining market data, conducting trades with securities, or getting account specific
    information. The methods of this interface should build and return a corresponding
    BrokerRequest object detailing the HTTP Request details.

    Attributes
    ----------
    api_base_url : str, required
        The base url is required as all of the broker APIs follow REST-ful practices
    action_path : dict


    Methods
    -------
    get_base_url()
        Returns api_base_url for given Broker
    """
    def __init__(self):
        super().__init__()

    @classmethod
    @abstractmethod
    def get_base_url(cls):
        """Gets the Broker's API endpoint's base url

        Returns
        -------
        :return: A string of the Broker's API endpoint's base url (stripped of any trailing forward-slashes)
        """
        pass


class Alpaca(BrokerInterface):

    action_path = {

    }
    api_base_url = 'https://api.alpaca.markets'.rstrip('/')

    def __init__(self):
        super().__init__()

    @classmethod
    def get_base_url(cls):
        return cls.api_base_url


class NotSupportedException(Exception):
    """Raised if the method or action is unknown or not supported by a particular Broker"""
    pass
