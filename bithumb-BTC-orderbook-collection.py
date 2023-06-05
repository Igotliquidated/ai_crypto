import time
import requests
import pandas as pd
import datetime
import os

header = True 

while True:
    book = {}
    response = requests.get('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
    book = response.json()

    data = book['data']

    bids = pd.DataFrame(data['bids']).apply(pd.to_numeric, errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids['type'] = 0

    asks = pd.DataFrame(data['asks']).apply(pd.to_numeric, errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1

    df = pd.concat([bids, asks])
    timestamp = int(time.time())
    print(df)

    print("\n")

    time.sleep(1)

    df = pd.concat([bids, asks])

    timestamp = datetime.datetime.now()
    req_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    df['quantity'] = df['quantity'].round(decimals=4)
    df['timestamp'] = req_timestamp

    current_time = datetime.datetime.now()
    filename = f"./{current_time.strftime('%Y-%m-%d')}-bithumb-btc-orderbook.csv"


    df.to_csv(filename, index=False, header=header, mode='a')
    header = False 
