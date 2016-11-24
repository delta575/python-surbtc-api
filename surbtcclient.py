import requests
import json
import base64
import hmac
import hashlib
import time

PROTOCOL = "https"
HOST = "www.surbtc.com/api"
TEST_HOST = "stg.surbtc.com/api"
VERSION = "v1"

PATH_MARKETS = "markets"
PATH_MARKET_DETAILS = "markets/%s"
PATH_ORDER_BOOK = "markets/%s/order_book"
PATH_QUOTATION = "markets/%s/quotations"
PATH_FEE_PERCENTAGE = "markets/%s/fee_percentage"
PATH_BALANCES = "balances/%s"
PATH_ORDERS = "markets/%s/orders"
PATH_SINGLE_ORDER = "orders/%s"
PATH_WITHDRAWAL = "withdrawals"

TEST_KEY = 'XXXX'  # Use stg api key
TEST_SECRET = 'XXXX'  # Use stg api secret


class SURBTC(object):
    def __init__(self, testing=True, key=TEST_KEY, secret=TEST_SECRET, timeout=30):
        self.host = TEST_HOST if testing else HOST
        self.api_key = key
        self.api_secret = secret
        self.timeout = timeout

    def server(self):
        return "%s://%s/%s" % (PROTOCOL, self.host, VERSION)

    def url_for(self, path, path_arg=None, parameters=None):
        url = "%s/%s" % (self.server(), path)
        route = '/api/%s/%s' % (VERSION, path)

        if path_arg:
            url = url % path_arg
            route = route % path_arg

        if parameters:
            url = "%s?%s" % (url, self._build_parameters(parameters))
            route = "%s?%s" % (route, self._build_parameters(parameters))

        return url, route

    def markets(self):
        url, route = self.url_for(PATH_MARKETS)
        signed_payload = self.payload_packer(proto='GET', route=route)
        return self._get(url, signed_payload)

    def marketdetails(self, market):
        url, route = self.url_for(PATH_MARKET_DETAILS, path_arg=market)
        signed_payload = self.payload_packer(proto='GET', route=route)
        return self._get(url, signed_payload)

    def orderbook(self, market):
        url, route = self.url_for(PATH_ORDER_BOOK, path_arg=market)
        signed_payload = self.payload_packer(proto='GET', route=route)
        return self._get(url, signed_payload)

    def quotation(self, market, qtype, reverse, amount):
        url, route = self.url_for(PATH_QUOTATION, path_arg=market)
        payload = {"quotation": {"type": qtype, "reverse": reverse, "amount": str(amount)}}
        print('Payload:', payload)
        signed_payload = self.payload_packer(proto='POST', route=route, payload=payload)
        return self._post(url, signed_payload, payload)

    def feepercent(self, market, otype, market_order):
        url, route = self.url_for(PATH_FEE_PERCENTAGE, path_arg=market, parameters={'type': otype, 'market_order': market_order})
        signed_payload = self.payload_packer(proto='GET', route=route)
        return self._get(url, signed_payload)

    def balances(self, currency):
        url, route = self.url_for(PATH_BALANCES, path_arg=currency)
        signed_payload = self.payload_packer(proto='GET', route=route)
        return self._get(url, signed_payload)

    def neworder(self, market, payload):
        url, route = self.url_for(PATH_ORDERS, path_arg=market)
        signed_payload = self.payload_packer(proto='POST', route=route, payload=payload)
        return self._post(url, signed_payload, payload)

    def orders(self, market, params=None):
        url, route = self.url_for(PATH_ORDERS, path_arg=market, parameters=params)
        signed_payload = self.payload_packer(proto='GET', route=route)
        return self._get(url, signed_payload)

    def singleorder(self, order_id):
        url, route = self.url_for(PATH_SINGLE_ORDER, path_arg=order_id)
        signed_payload = self.payload_packer(proto='GET', route=route)
        return self._get(url, signed_payload)

    def cancelorder(self, order_id):
        url, route = self.url_for(PATH_SINGLE_ORDER, path_arg=order_id)
        payload = {'state': 'canceling'}
        signed_payload = self.payload_packer(proto='PUT', route=route, payload=payload)
        return self._put(url, signed_payload, payload)

    def withdraw(self, address, amount):
        url, route = self.url_for(PATH_WITHDRAWAL)
        payload = {"withdrawal_data": {"target_address": address}, "amount": str(amount), "currency": "BTC"}
        signed_payload = self.payload_packer(proto='POST', route=route, payload=payload)
        return self._post(url, signed_payload, payload)

    def _get(self, url, signed_payload):
        return requests.get(url, headers=signed_payload, verify=True, timeout=self.timeout).json()

    def _put(self, url, signed_payload, data):
        return requests.put(url, headers=signed_payload, data=json.dumps(data), verify=True, timeout=self.timeout).json()

    def _post(self, url, signed_payload, data):
        return requests.post(url, headers=signed_payload, data=json.dumps(data), verify=True, timeout=self.timeout).json()

    def _build_parameters(self, parameters):
        keys = list(parameters.keys())
        keys.sort()
        return '&'.join(["%s=%s" % (k, parameters[k]) for k in keys])

    def _gen_nonce(self):
        time.sleep(0.2)
        return str(int((time.time() * 1000)))

    def payload_packer(self, proto, route, payload=None):
        nonce = self._gen_nonce()

        if payload:
            j = json.dumps(payload).encode('utf-8')
            body = base64.standard_b64encode(j).decode('utf-8')
            string = proto+' '+route+' '+body+' '+nonce
        else:
            string = proto+' '+route+' '+nonce

        h = hmac.new(self.api_secret.encode('utf-8'), string.encode('utf-8'), hashlib.sha384)
        signature = h.hexdigest()

        return {
            "X-SBTC-APIKEY": self.api_key,
            "X-SBTC-NONCE": nonce,
            "X-SBTC-SIGNATURE": signature,
            "Content-Type": 'application/json'
        }
