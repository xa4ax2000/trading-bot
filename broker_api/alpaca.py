from .broker import BrokerInterface, Account
import json


class Alpaca(BrokerInterface):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._headers = {
            'APCA-API-KEY-ID': self._key_id,
            'APCA-API-SECRET-KEY': self._secret_key
        }
        self._retry_codes.clear()
        self._retry_codes += ['429', '504']

    def acct_info(self):
        opts = {
            'headers': self._headers.copy(),
            'timeout': self._default_timeout
        }
        resp = self._request('GET', _Endpoints.acct_info(), opts)
        return AlpacaAccount(resp)


class _Endpoints:

    api_base_url = 'https://paper-api.alpaca.markets'.rstrip('/')
    version = '/v2'

    @classmethod
    def acct_info(cls):
        return cls.api_base_url + cls.version + '/account'


class AlpacaAccount(Account):

    def __init__(self, resp):
        super().__init__(resp)
        self._resp = resp
        self._equity = resp['equity']
        self._cash = resp['cash']
        self._pattern_day_trader = resp['pattern_day_trader']
        self._trading_blocked = resp['trading_blocked']

    def __repr__(self):
        resp_str = json.dumps(self._resp)
        return 'AlpacaAccount<{}>'.format(resp_str)

    @property
    def equity(self):
        return self._equity

    @property
    def cash(self):
        return self._cash

    @property
    def pattern_day_trader(self):
        return self._pattern_day_trader

    @property
    def trading_blocked(self):
        return self._trading_blocked
