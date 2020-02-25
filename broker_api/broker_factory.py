from .broker import *


class BrokerFactory:
    """
    Factory to obtain singleton instance of Broker classes.
    ...
    Attributes
    ----------
    broker_input_to_class : dict
        dictionary containing reference to particular Broker implementation classes given a key from input
    active_brokers : dict
        dictionary containing reference to object instances that may have already been created -- this map is
        to ensure single creation of a particular Broker object.

    Methods
    -------
    get_broker(broker_input=None)
        Gets or creates a particular broker from the input. Raises an error if the input is empty or unresolvable.
    """

    broker_input_to_class = {
        'alpaca': Alpaca
    }
    active_brokers = {}

    @classmethod
    def get_broker(cls, broker_input=None):
        """Resolves the input to a particular broker instance.

        If the input cannot be resolved, a MissingOrUnknownBrokerError is raised.

        Paramaeters
        -----------
        :param broker_input : str, required
            The broker to obtain instance of

        Raises
        -----------
        MissingOrUnknownBrokerError
            If the input cannot be resolved to an object instance

        Returns
        -------
        :return: Associated Broker instance
        """
        if broker_input is None:
            raise MissingOrUnknownBrokerError
        broker_input_lower = broker_input.lower()
        active_broker = cls.active_brokers.get(broker_input_lower)
        if active_broker is not None:
            return active_broker
        active_broker_class = cls.broker_input_to_class[broker_input_lower]
        if active_broker_class is None:
            raise MissingOrUnknownBrokerError
        active_broker = active_broker_class()
        cls.active_brokers[broker_input_lower] = active_broker
        return active_broker


class MissingOrUnknownBrokerError(Exception):
    """Raised when either no broker or an unknown broker is passed to the factory"""
    pass
