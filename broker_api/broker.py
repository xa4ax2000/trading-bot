from abc import ABC, abstractmethod
import requests
import time
from requests.exceptions import HTTPError


class BrokerInterface(ABC):
    """Interface exposing all broker interactions possible.

    If a particular interaction is not supported by a particular broker, a
    TypeError will be raised. Interactions could include anything from
    obtaining market data, conducting trades with securities, or getting account specific
    information. This client requires the `requests` module to be installed -- as listed in the requirements.txt.

    Methods
    -------
    get_account_information()
        returns account information such as user's buying power, account status, margin (if any), etc.

    """

    def __init__(self, **kwargs):
        """
        Parameters
        ----------
        :keyword key_id : str, optional
            (if supported) the API Key
        :keyword secret_key : str, optional
            (if supported) the API Secret Key
        :keyword username : str, optional
            (if supported) the credentials used to login
        :keyword password : str, optional
            (if supported) the password used to login
        """

        super().__init__()
        self._key_id = kwargs.get('key_id')
        self._secret_key = kwargs.get('secret_key')
        self._username = kwargs.get('username')
        self._password = kwargs.get('password')
        self._http_session = requests.session()
        self._default_timeout = 15
        self._retry_count = 3
        self._retry_wait = 3
        self._retry_codes = []

    def _request(self, method, url, opts):
        """ Will wrap Http Request call with a custom retry implementation

        :param method : str
            The HttpMethod - GET, PUT, POST, DELETE
        :param url : str
            The url endpoint to make Http Request to
        :param opts:
            Additional optional keyword arguments to pass to request.request() method such as
            headers, data, allow_redirects, timeout, etc.
        :return:
        """
        retry = self._retry_count
        if retry < 0:
            retry = 0
        while retry >= 0:
            try:
                return self.__make_request(method, url, opts, retry)
            except Retry:
                retry_wait = self._retry_wait
                print(
                    'sleep {} seconds and retrying {} '
                    '{} more time(s)...'.format(
                        retry_wait, url, retry)
                )
                time.sleep(retry_wait)
                retry -= 1
                continue

    def __make_request(self, method, url, opts, retry):
        """Perform one request and returns response on success

        Parameters
        ----------
        :param method : str
            The HttpMethod - GET, PUT, POST, DELETE
        :param url : str
            The url endpoint to make Http Request to
        :param opts : dict
            The list of optional arguments to pass to requests.request() method
        :param retry : num
            The number of retries
        Raise
        -----
        :raise Retry
            If the Http Code in response matches retry_codes, this exception will be raised to retry the request
        :raise APIError
            Any other Http Error Code
        :raise HTTPError
            Uncaught errors

        Return
        ------
        :return: JSON Response if available or None if empty
            The response from the Http Request made
        """
        retry_codes = self._retry_codes
        resp = self._http_session.request(method, url, **opts)
        try:
            resp.raise_for_status()
        except HTTPError as http_error:
            # retry if we hit Rate Limit
            if resp.status_code in retry_codes and retry > 0:
                raise Retry()
            if 'code' in resp.text:
                error = resp.json()
                if 'code' in error:
                    raise APIError(error, http_error)
            else:
                raise http_error
        if resp.text != '':
            return resp.json()
        return None

    @abstractmethod
    def acct_info(self):
        """Get the account information from brokerage account

        This method will connect to the broker and obtain account information
        """
        pass


class Retry(Exception):
    """Raised when an HTTP Request fails and we want to retry it based off the response status"""
    pass


class APIError(Exception):
    """Represent API related error.
    error.status_code will have http status code.
    """
    pass


class Account(ABC):
    """
    The Account Information API Response Abstract Class

    Parameters
    ----------
    :param equity : num
        Cash + long_market_value + short_market_value
    :param cash : num
        Cash balance
    :param pattern_day_trader : boolean
        Whether or not the account has been flagged as a pattern day trader
    :param trading_blocked : boolean
        If true, the account is not allowed to place orders.
    """

    def __init__(self, resp):
        """
        Parameters
        ----------
        :param resp : HttpResponse object
            The response returned from the Http Request
        """
        if resp is None:
            raise EmptyResponse()

    @property
    @abstractmethod
    def equity(self):
        pass

    @property
    @abstractmethod
    def cash(self):
        pass

    @property
    @abstractmethod
    def pattern_day_trader(self):
        pass

    @property
    @abstractmethod
    def trading_blocked(self):
        pass


class EmptyResponse(Exception):
    """Raised when an empty response is returned"""
    pass
