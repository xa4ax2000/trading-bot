from .broker_factory import BrokerFactory


class Client:

    def __init__(self, broker=None):
        self.broker = BrokerFactory.get_broker(broker)
