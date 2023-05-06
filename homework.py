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
    print (df)

    print ("\n")

    time.sleep(1)

    df = pd.concat([bids, asks])
    
    timestamp = datetime.datetime.now()
    req_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    df['quantity'] = df['quantity'].round(decimals=4)
    df['timestamp'] = req_timestamp
    
    current_time = datetime.datetime.now()
    last_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    if current_time >= last_time:
        df.to_csv("./bithumb-orderbook2.csv", index=False, header=False, mode = 'a')
    else:
        df.to_csv("./bithumb-orderbook.csv", index=False, header=False, mode = 'a')



 





   
