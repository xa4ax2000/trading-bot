import getpass
import requests


def login_required(function):
    """ Decorator function that prompts user for login if they are not logged in already.

    Can be applied to any function using the @ notation.
    """

    def wrapper(self, *args, **kwargs):
        if self._broker.requires_login_credentials and self._auth_token is None:
            __login_prompt(self)
        return function(self, *args, **kwargs)  # pylint: disable=E1102

    return wrapper


def __login_prompt(self):
    """Prompts user for username and password and calls login() """

    username = input("Username: ")
    password = getpass.getpass()

    return login(self, username=username, password=password)


def login(self, username, password):
    """Login Logic

    :param self: BrokerClient
        the BrokerClient object containing attributes
    :param username: str
        the username to login with
    :param password: str
        the password to login with
    """
    broker_request = self.__broker.build_login_broker_request(username, password)
    try:
        res = self.__http_session.request(
            method=broker_request.method.name,
            url=broker_request.endpoint,
            data=broker_request.request_body,
            headers=broker_request.headers,
            timeout=15
        )
        res.raise_for_status()
        data = res.json()
    except requests.exceptions.HTTPError:
        raise LoginFailedError

    if 'access_token' in data.keys() and 'refresh_token' in data.keys():
        self.__auth_token = data['access_token']
        self.__refresh_token = data['refresh_token']


class LoginFailedError(Exception):
    """Raised when Login Fails"""
    pass
