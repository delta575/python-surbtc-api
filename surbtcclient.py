import requests
import json
import base64
import hmac
import hashlib
import time
from urllib.parse import urlparse, urlencode


PROTOCOL = 'https'
HOST = 'www.surbtc.com/api'
TEST_HOST = 'stg.surbtc.com/api'
VERSION = 'v1'

PATH_MARKETS = 'markets'
PATH_MARKET_DETAILS = 'markets/%s'
PATH_ORDER_BOOK = 'markets/%s/order_book'
PATH_QUOTATION = 'markets/%s/quotations'
PATH_FEE_PERCENTAGE = 'markets/%s/fee_percentage'
PATH_BALANCES = 'balances/%s'
PATH_BALANCES_EVENTS = 'balance_events'
PATH_ORDERS = 'markets/%s/orders'
PATH_SINGLE_ORDER = 'orders/%s'
PATH_WITHDRAWAL = 'withdrawals'

TEST_KEY = 'XXXX'  # Use stg api key
TEST_SECRET = 'XXXX'  # Use stg api secret

TIMEOUT = 30.0


class SURBTC(object):

    def __init__(self, testing=True, key=TEST_KEY, secret=TEST_SECRET, timeout=TIMEOUT):
        self.host = TEST_HOST if testing else HOST
        self.api_key = key
        self.api_secret = secret
        self.timeout = timeout

    def server_url(self):
        return '%s://%s/%s' % (PROTOCOL, self.host, VERSION)

    def url_path_for(self, path, path_arg=None):
        url = '%s/%s' % (self.server_url(), path)

        if path_arg:
            url = url % path_arg

        return url, urlparse(url).path

    # MARKETS

    def markets(self):
        url, path = self.url_path_for(PATH_MARKETS)
        signed_payload = self._payload_packer(method='GET', path=path)
        return self._get(url, signed_payload)

    def market_details(self, market_id):
        url, path = self.url_path_for(PATH_MARKET_DETAILS, path_arg=market_id)
        signed_payload = self._payload_packer(method='GET', path=path)
        return self._get(url, signed_payload)

    def order_book(self, market_id):
        url, path = self.url_path_for(PATH_ORDER_BOOK, path_arg=market_id)
        signed_payload = self._payload_packer(method='GET', path=path)
        return self._get(url, signed_payload)

    def quotation(self, market_id, quotation_type, reverse, amount):
        payload = {
            'quotation': {
                'type': quotation_type,
                'reverse': reverse,
                'amount': str(amount)
            }
        }
        url, path = self.url_path_for(PATH_QUOTATION, path_arg=market_id)
        signed_payload = self._payload_packer(method='POST', path=path, payload=payload)
        return self._post(url, signed_payload, payload)

    # NOT WORKING
    def fee_percentage(self, market_id, order_type, market_order=None):
        parameters = {
            'type': order_type,
            'market_order': market_order
        }
        url, path = self.url_path_for(PATH_FEE_PERCENTAGE, path_arg=market_id)
        signed_payload = self._payload_packer(method='GET', path=path)
        return self._get(url, signed_payload, parameters)

    # BALANCES

    def balances(self, currency):
        url, path = self.url_path_for(PATH_BALANCES, path_arg=currency)
        signed_payload = self._payload_packer(method='GET', path=path)
        return self._get(url, signed_payload)

    # NOT WORKING
    def balances_events(self, currencies_list, event_names_list):
        parameters = {
            'currencies[]': currencies_list,
            'event_names[]': event_names_list,
        }
        url, path = self.url_path_for(PATH_BALANCES_EVENTS)
        signed_payload = self._payload_packer(method='GET', path=path)
        return self._get(url, signed_payload, parameters)

    # ORDERS

    def new_order(self, market, order_type, limit, amount, original_amount, price_type):
        payload = {
            'type': order_type,
            'limit': limit,
            'amount': amount,
            'original_amount': original_amount,
            'price_type': price_type,
        }
        return self.new_order_payload(market, payload)

    def new_order_payload(self, market, payload):
        url, path = self.url_path_for(PATH_ORDERS, path_arg=market)
        signed_payload = self._payload_packer(method='POST', path=path, payload=payload)
        return self._post(url, signed_payload, payload)

    def orders(self, market_id, orders_per_page=None, page=None, state=None):
        parameters = {
            'per': orders_per_page,
            'page': page,
            'state': state,
        }
        url, path = self.url_path_for(PATH_ORDERS, path_arg=market_id)
        signed_payload = self._payload_packer(method='GET', path=path, params=parameters)
        return self._get(url, signed_payload=signed_payload, params=parameters)

    def single_order(self, order_id):
        url, path = self.url_path_for(PATH_SINGLE_ORDER, path_arg=order_id)
        signed_payload = self._payload_packer(method='GET', path=path)
        return self._get(url, signed_payload)

    def cancel_order(self, order_id):
        payload = {
            'state': 'canceling'
        }
        url, path = self.url_path_for(PATH_SINGLE_ORDER, path_arg=order_id)
        signed_payload = self._payload_packer(method='PUT', path=path, payload=payload)
        return self._put(url, signed_payload, payload)

    # PAYMENTS

    def withdraw(self, address, amount):
        payload = {
            'withdrawal_data': {
                'target_address': address
            },
            'amount': str(amount),
            'currency': 'BTC',
        }
        url, path = self.url_path_for(PATH_WITHDRAWAL)
        signed_payload = self._payload_packer(method='POST', path=path, payload=payload)
        return self._post(url, signed_payload, payload)

    # PRIVATE METHODS

    def _get(self, url, signed_payload, params=None):
        response = requests.get(url, headers=signed_payload, params=params, verify=True, timeout=self.timeout)
        return response.url, response.json()

    def _put(self, url, signed_payload, data):
        response = requests.put(url, headers=signed_payload, data=json.dumps(data), verify=True, timeout=self.timeout)
        return response.json()

    def _post(self, url, signed_payload, data):
        response = requests.post(url, headers=signed_payload, data=json.dumps(data), verify=True, timeout=self.timeout)
        return response.json()

    def _build_parameters(self, parameters):
        if parameters:
            p = {k: v for k, v in parameters.items() if v is not None}
            return urlencode(p, True)
        else:
            return None

    def _build_route(self, path, params=None):
        built_params = self._build_parameters(params)
        if built_params:
            return '%s?%s' % (path, built_params)
        else:
            return path

    def _gen_nonce(self):
        time.sleep(0.2)
        return str(int((time.time() * 1000)))

    def _payload_packer(self, method, path, params=None, payload=None):
        nonce = self._gen_nonce()
        route = self._build_route(path, params)

        if payload:
            j = json.dumps(payload).encode('utf-8')
            body = base64.standard_b64encode(j).decode('utf-8')
            string = method + ' ' + route + ' ' + body + ' ' + nonce
        else:
            string = method + ' ' + route + ' ' + nonce

        h = hmac.new(self.api_secret.encode('utf-8'), string.encode('utf-8'), hashlib.sha384)
        signature = h.hexdigest()

        return {
            'X-SBTC-APIKEY': self.api_key,
            'X-SBTC-NONCE': nonce,
            'X-SBTC-SIGNATURE': signature,
            'Content-Type': 'application/json'
        }
