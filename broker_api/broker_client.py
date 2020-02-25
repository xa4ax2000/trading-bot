import requests
from .broker_factory import BrokerFactory
from .broker_api_interface import BrokerApiInterface


class BrokerClient(BrokerApiInterface):
    def __init__(
            self,
            broker_input=None,
            key_id=None,
            secret_key=None,
            username=None,
            password=None
    ):
        super().__init__()
        # required broker
        self._broker = BrokerFactory.get_broker(broker_input)
        # obtain http session
        self._http_session = requests.session()
        # optional additional information to build api request
        self._key_id = key_id
        self._secret_key = secret_key
        self._username = username
        self._password = password
