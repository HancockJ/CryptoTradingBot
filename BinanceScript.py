import hmac
import time
import requests
import hashlib
import Config

from urllib.parse import urlencode

KEY = Config.binance_key_info["public"]
SECRET = Config.binance_key_info["private"]
BASE_URL = Config.BINANCE_URL


def hashing(query_string):
    return hmac.new(SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()


def get_timestamp():
    return int(time.time() * 1000)


def dispatch_request(http_method):
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json;charset=utf-8',
        'X-MBX-APIKEY': KEY
    })
    return {
        'GET': session.get,
        'DELETE': session.delete,
        'PUT': session.put,
        'POST': session.post,
    }.get(http_method, 'GET')


# used for sending request requires the signature
def send_signed_request(http_method, url_path, payload={}):
    query_string = urlencode(payload, True)
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = 'timestamp={}'.format(get_timestamp())

    url = BASE_URL + url_path + '?' + query_string + '&signature=' + hashing(query_string)
    print("{} {}".format(http_method, url))
    params = {'url': url, 'params': {}}
    response = dispatch_request(http_method)(**params)
    return response.json()


# used for sending public data request
def send_public_request(url_path, payload={}):
    query_string = urlencode(payload, True)
    url = BASE_URL + url_path
    if query_string:
        url = url + '?' + query_string
    print("{}".format(url))
    response = dispatch_request('GET')(url=url)
    return response.json()


# View the account information for given public and private key
def view_account():
    response = send_signed_request('GET', '/api/v3/account')
    print(response)


# Create a buy order for a given symbol and quantity
def buy_order(symbol_name, quantity):
    # # place an order
    # if you see order response, then the parameters setting is correct
    params = {
        "symbol": symbol_name,
        "side": "BUY",
        "type": "MARKET",
        "quantity": quantity
    }
    response = send_signed_request('POST', '/fapi/v1/order', params)
    print(response)


# Create a sell limit oder for a given symbol and price
def sell_limit_order(symbol_name, order_type, quantity, price):
    # place an order
    # if you see order response, then the parameters setting is correct
    params = {
        "symbol": symbol_name,
        "side": "SELL",
        "type": order_type,
        "quantity": quantity,
        "price": price,
        "timeInforce": "GTC"
    }
    response = send_signed_request('POST', '/fapi/v1/order', params)
    print(response)


# Create a sell order at market price, for a given symbol and quantity
def sell_order(symbol_name, quantity):
    params = {
        "symbol": symbol_name,
        "side": "SELL",
        "type": "MARKET",
        "quantity": quantity
    }
    response = send_signed_request('POST', '/fapi/v1/order', params)
    print(response)


# Cancel a given buy or sell order
def cancel_oder(symbol_name, order_id):
    params = {
        "symbol": symbol_name,
        "orderid": order_id
    }
    response = send_signed_request('DELETE', '/fapi/v1/order', params)
    print(response)

def getPrice(symbol_name):
    params = {
        "symbol": symbol_name,
    }
    response = send_signed_request('GET', '/fapi/v1/ticker/price', params)
    print(response)

getPrice("DOGEUSDT")

