from .client import Client
from .broker_factory import BrokerFactory
import requests


class ClientImpl(Client):

    def __init__(
            self,
            broker=None,
            key_id=None,
            secret_key=None,
            api_version=None,
            oauth=None
    ):
        self._broker = BrokerFactory.get_broker(broker)
        self._key_id = key_id
        self._secret_key = secret_key
        self._api_version = api_version
        self._oauth = oauth
        self._session = requests.Session()
