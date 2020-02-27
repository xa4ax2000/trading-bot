from .broker import BrokerInterface, Account
from .login_decorator import LoginDecorator, login_required
import json
import uuid


class Robinhood(BrokerInterface, LoginDecorator):

    client_id = 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._headers = {}
        self._retry_codes.clear()
        self._retry_codes += ['429', '504']
        self._refresh_token = None
        self._auth_token = None

    @property
    def refresh_token(self):
        return self._refresh_token

    @property
    def auth_token(self):
        return self._auth_token

    def _login(self, username, password, mfa_code=None):
        rand_uuid = uuid.uuid1()
        opts = {
            'data': {
                'password': password,
                'username': username,
                'scope': 'internal',
                'expires_in': 86400,
                'grant_type': 'password',
                'client_id': self.client_id,
                'device_token': rand_uuid
            },
            'timeout': self._default_timeout
        }
        if mfa_code:
            opts['data']['mfa_code'] = mfa_code
        data = self._request('POST', _Endpoints.login(), opts)
        if 'mfa_required' in data.keys():
            mfa_code = input('MFA: ')
            return self._login(username, password, mfa_code)
        if 'access_token' in data.keys() and 'refresh_token' in data.keys():
            self._auth_token = data['access_token']
            self._refresh_token = data['refresh_token']
            self._headers['Authorization'] = 'Bearer ' + self._auth_token

    @login_required
    def acct_info(self):
        opts = {
            'timeout': self._default_timeout,
            'headers': self._headers
        }
        acct_resp = self._request('GET', _Endpoints.acct_info(), opts)
        portfolio_resp = self._request('GET', _Endpoints.portfolio(), opts)
        return RobinhoodAccount(acct_resp, portfolio_resp)


class _Endpoints:

    api_base_url = 'https://api.robinhood.com'.rstrip('/')

    @classmethod
    def login(cls):
        return cls.api_base_url + '/oauth2/token/'

    @classmethod
    def acct_info(cls):
        return cls.api_base_url + '/accounts/'

    @classmethod
    def portfolio(cls):
        return cls.api_base_url + '/portfolios/'


class RobinhoodAccount(Account):

    def __init__(self, acct_resp, portfolio_resp):
        super().__init__(acct_resp, portfolio_resp)
        self._acct_resp = acct_resp['results'][0]
        self._portfolio_resp = portfolio_resp['results'][0]
        self._equity = portfolio_resp['results'][0]['equity']
        self._cash = acct_resp['results'][0]['portfolio_cash']
        self._pattern_day_trader \
            = acct_resp['results'][0]['margin_balances']['marked_pattern_day_trader_date'] is not None
        self._trading_blocked = acct_resp['results'][0]['locked']

    def __repr__(self):
        acct_resp_str = json.dumps(self._acct_resp)
        portfolio_resp_str = json.dumps(self._portfolio_resp)
        return 'RobinhoodAccount<AccountResponse<{}>,PortfolioResponse<{}>>'.format(acct_resp_str, portfolio_resp_str)

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
