from abc import ABC, abstractmethod
import requests
from .broker_factory import BrokerFactory


class BrokerClientApiInterface(ABC):
    """General client that will be able to connect and communicate to the broker APIs.

    This client will expose methods to allow interaction with the broker - whether it be to
    obtain market data, conduct trades with securities, or get account specific information.
    Flexibility is dependent on the broker and its supported APIs. This client requires the
    `requests` module to be installed -- as listed in the requirements.txt.
    """
    def __init__(self):
        super().__init__()


class BrokerClient(BrokerClientApiInterface):
    """Implementation of BrokerClientApiInterface

    """

    def __init__(
            self,
            broker_input=None,
            key_id=None,
            secret_key=None,
            username=None,
            password=None
    ):
        """
        Parameters
        ----------
        :param broker_input : str, required
            string containing the broker to connect with
        :param key_id : str, optional
            (if supported) the API Key
        :param secret_key : str, optional
            (if supported) the API Secret Key
        :param username : str, optional
            (if supported) the credentials used to login
        :param password : str, optional
            (if supported) the password used to login
        """
        super().__init__()
        # required broker
        self._broker = BrokerFactory.get_broker(broker_input)
        # obtain http session
        self.__http_session = requests.session()
        # optional additional information to build api request
        self.__key_id = key_id
        self.__secret_key = secret_key
        self.__username = username
        self.__password = password
