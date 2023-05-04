import time
import requests
import pandas as pd
import datetime


while True:
    
   

    book = {}
    response = requests.get ('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
    book = response.json()


    data = book['data']

    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids = bids.reset_index(); del bids['index']
    bids['type'] = 0
    
    asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1 

    df = pd.concat([bids, asks])
    timestamp=int(time.time())
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    print(dt_object)
    print (df)

    print ("\n")

    time.sleep(4.9)
    continue;

    df = bids.append(asks)
    
    timestamp = datetime.datetime.now()
    req_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    df['quantity'] = df['quantity'].round(decimals=4)
    df['timestamp'] = req_timestamp
    
    
    df.to_csv("./2022-05-18-bithumb-orderbook.csv", index=False, header=False, mode = 'a')

 





   