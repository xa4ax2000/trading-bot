from .broker import *


class BrokerFactory:

    broker_input_to_class = {
        'alpaca': Alpaca
    }
    active_brokers = {}

    @classmethod
    def get_broker(cls, broker_input=None):
        if broker_input is None:
            raise MissingOrUnknownBrokerException
        broker_input_lower = broker_input.lower()
        active_broker = cls.active_brokers.get(broker_input_lower)
        if active_broker is not None:
            return active_broker
        active_broker_class = cls.broker_input_to_class[broker_input_lower]
        if active_broker_class is None:
            raise MissingOrUnknownBrokerException
        active_broker = active_broker_class()
        cls.active_brokers[broker_input_lower] = active_broker
        return active_broker


class MissingOrUnknownBrokerException(Exception):
    """Raised when unknown or no broker is passed to the factory"""
    pass
