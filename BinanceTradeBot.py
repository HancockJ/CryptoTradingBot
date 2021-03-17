import hmac
import time
import requests
import hashlib

from urllib.parse import urlencode


KEY = '40fa68dbd24d0c35eda02ee744561868b3150ca5bb2a4069a742971970396399'
SECRET = '47e203b17b42142881cbca137cf9c6f297aa937ebf228216486d804772b50a81'
#BASE_URL = 'https://api.binance.us' # production base url
#BASE_URL = 'https://testnet.binance.vision' # testnet base url
BASE_URL = 'https://testnet.binancefuture.com' # testnet base url

''' ======  begin of functions, you don't need to touch ====== '''
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

''' ======  end of functions ====== '''

### public data endpoint, call send_public_request #####
# get klines
#response = send_public_request('/api/v3/klines' , {"symbol": "BTCUSDT", "interval": "1d"})
#print(response)


### USER_DATA endpoints, call send_signed_request #####
# get account informtion
# if you can see the account details, then the API key/secret is correct
# response = send_signed_request('GET', '/api/v3/account')
# print(response)


# # place a limit sell order
# if you see order response, then the parameters setting is correct
# params = {
#    "symbol": "ETHUSDT",
#   "side": "SELL",
#    "type": "LIMIT",
#    "quantity": "5",
#    "price": "1775.05",
#    "timeInforce": "GTC"
# }
# response = send_signed_request('POST', '/fapi/v1/order', params)
# print(response)

# # place an order
# if you see order response, then the parameters setting is correct
# params = {
#     "symbol": "ETHUSDT",
#    "side": "BUY",
#     "type": "MARKET",
#     "quantity": "5",
# }
# response = send_signed_request('POST', '/fapi/v1/order', params)
# print(response)

#cancel an order
params = {
   "symbol": "ETHUSDT",
   "orderid": "734356778"
}
response = send_signed_request('DELETE', '/fapi/v1/order', params)
print(response)


