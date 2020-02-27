from .broker import BrokerInterface
import uuid


class Robinhood(BrokerInterface):

    api_base_url = 'https://api.robinhood.com'.rstrip('/')
    client_id = 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS'

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def acct_info(self):
        pass
