from abc import ABC, abstractmethod
import getpass


class LoginDecorator(ABC):
    """
    Interface to use the login_required decorator
    """

    @property
    @abstractmethod
    def refresh_token(self):
        """The refresh token obtained from login response"""
        pass

    @property
    @abstractmethod
    def auth_token(self):
        """The auth token obtained from login response"""
        pass

    @abstractmethod
    def _login(self, username, password, mfa_code=None):
        """Required method to use login_required decorator"""
        pass


def login_required(function):
    """ Decorator function that prompts user for login if they are not logged in already.

    Can be applied to any function using the @ notation.
    """

    def wrapper(self, *args, **kwargs):
        if self._auth_token is None:
            """Prompts user for username and password and calls login()"""
            username = input("Username: ")
            password = getpass.getpass()
            self._login(username=username, password=password)
        return function(self, *args, **kwargs)
    return wrapper
