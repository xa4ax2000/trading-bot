from broker_api.alpaca import Alpaca
from broker_api.robinhood import Robinhood


class BrokerFactory:
    """
    Factory to obtain a new instance of a particular Broker class.
    ...
    Attributes
    ----------
    broker_input_to_class : dict
        dictionary containing reference to particular Broker implementation classes given a key from input

    Methods
    -------
    get_broker(broker_input=None)
        Gets or creates a particular broker from the input. Raises an error if the input is empty or unresolvable.
    """

    broker_input_to_class = {
        'alpaca': Alpaca,
        'robinhood': Robinhood
    }

    @classmethod
    def get_broker(cls, broker_input, **kwargs):
        """Resolves the input to a particular broker instance.

        If the input cannot be resolved, a MissingOrUnknownBrokerError is raised.

        Paramaeters
        -----------
        :param broker_input : str, required
            The broker to obtain instance of
        :param kwargs : list(str), optional
            Additional keyword arguments that detail necessary account specific information such as:
            key-id, secret-key, username, password

        Raise
        -----------
        :raise: UnknownBrokerError
            If the input cannot be resolved to an object instance

        Return
        -------
        :return: Associated Broker instance
        """
        broker_input_lower = broker_input.lower()
        active_broker_class = cls.broker_input_to_class[broker_input_lower]
        if active_broker_class is None:
            raise UnknownBroker
        active_broker = active_broker_class(**kwargs)
        return active_broker


class UnknownBroker(Exception):
    """Raised when either an unknown broker input is passed to the factory"""
    pass
