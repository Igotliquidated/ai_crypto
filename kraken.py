import time
import os
import requests
import urllib.parse
import hashlib
import hmac
import base64
import json 

api_url = "https://api.kraken.com"
api_key='JEk4qX8oqnoEYobv6MCauXqdfo6vKEfnDm1ytVZSwW/ONHPIY099H7aS'
api_sec='sZWRUL/RsHtETyqQYGv0PApJCiEfY2MbTSll+FXoLnUwOqzYfNnAcjNOWgWUBrcM7vK4i/E5l37cOyXUsQLkzw=='

def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

#A. get_balnce 
def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)             
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req
resp = kraken_request('/0/private/Balance', {
    "nonce": str(int(1000*time.time()))
}, api_key, api_sec)

print(resp.json())   

#B. get_open_order
def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)             
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req
resp = kraken_request('/0/private/OpenOrders', {
    "nonce": str(int(1000*time.time())),
    "trades": True
}, api_key, api_sec)

print(resp.json())

#C. place_order
def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)             
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req

resp = kraken_request('/0/private/AddOrder', {
    "nonce": str(int(1000*time.time())),
    "ordertype": "limit",
    "type": "buy",
    "volume": 1,
    "pair": "BTCUSDT",
    "price": 28000
}, api_key, api_sec)

print(resp.json())