from abc import ABC, abstractmethod


class Broker(ABC):
    def __init__(self):
        super().__init__()

    @property
    @abstractmethod
    def get_url(self, action=None):
        pass


class Alpaca(Broker):
    def __init__(self, kwargs):
        super().__init__()

    def get_url(self, action=None):
        return 'https://api.alpaca.markets'.rstrip('/')
