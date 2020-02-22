from .broker import *


class BrokerFactory:

    broker_map = {}

    @classmethod
    def get_broker(cls, typ=None, **kwargs):
        if typ is None:
            raise BrokerMissingException(typ)
        target_broker = typ.capitalize()
        if typ in cls.broker_map:
            return cls.broker_map.get(typ)
        broker = globals()[target_broker](kwargs)
        if broker is None:
            raise BrokerMissingException(typ)
        cls.broker_map[target_broker] = broker
        return broker


class BrokerMissingException(Exception):

    def __init__(self, typ):
        self.message='Broker Type: {}, cannot be identified. Failed to initialize client.'.format(typ)
        super(BrokerMissingException, self).__init__(self.message)
