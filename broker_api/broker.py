from abc import ABC, abstractmethod
from decorators.abstract_class_attributes import abstract_class_attributes


@abstract_class_attributes('_api_base_url')
class BrokerInterface(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_api(self, action=None):
        pass


class Alpaca(BrokerInterface):

    _api_base_url = 'https://api.alpaca.markets'.rstrip('/')

    def __init__(self):
        super().__init__()

    def get_api(self, action=None):
        return self._api_base_url
