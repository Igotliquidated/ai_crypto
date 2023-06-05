import pandas as pd

df = pd.read_csv('2023-05-08-bithumb-btc-orderbook.csv', header=0)

df['timestamp'] = pd.to_datetime(df['timestamp'])


start_time = pd.to_datetime('00:00:01').time()
end_time = pd.to_datetime('03:00:10').time()
filtered_df = df[(df['timestamp'].dt.time >= start_time) & (df['timestamp'].dt.time <= end_time)]


gr_o = filtered_df[['price', 'quantity', 'type', 'timestamp']]

gr_bid_level = filtered_df[filtered_df['type'] == 0][['price', 'quantity', 'timestamp']]
gr_ask_level = filtered_df[filtered_df['type'] == 1][['price', 'quantity', 'timestamp']]

def cal_mid_price(gr_bid_level, gr_ask_level):
    bid_top = max(gr_bid_level.price) if len(gr_bid_level) > 0 else 0  
    ask_top = max(gr_ask_level.price) if len(gr_ask_level) > 0 else 0  
    mid_price = (bid_top + ask_top) / 2
    return mid_price

def live_cal_book_i_v1(param, gr_bid_level, gr_ask_level, mid):
    mid_price = mid

    ratio = param[0]
    level = param[1]
    interval = param[2]

    quant_v_bid = gr_bid_level.quantity**ratio
    price_v_bid = gr_bid_level.price * quant_v_bid

    quant_v_ask = gr_ask_level.quantity**ratio
    price_v_ask = gr_ask_level.price * quant_v_ask
    
    askQty = quant_v_ask.values.sum()
    bidPx = price_v_bid.values.sum()
    bidQty = quant_v_bid.values.sum()
    askPx = price_v_ask.values.sum()
    bid_ask_spread = interval
        
    book_price = 0  
    if bidQty > 0 and askQty > 0:
        book_price = (((askQty*bidPx)/bidQty) + ((bidQty*askPx)/askQty)) / (bidQty+askQty)

    indicator_value = (book_price - mid_price) / bid_ask_spread # indicator_value = book_imbalance
    
    return indicator_value

timestamps = []
mid_prices = []
indicator_values = []

for group_key, group in gr_o.groupby(['timestamp']):
    timestamp = group_key
    
    gr_bid_level_group = gr_bid_level[gr_bid_level['timestamp'].isin(group['timestamp'])]
    gr_ask_level_group = gr_ask_level[gr_ask_level['timestamp'].isin(group['timestamp'])]
    
    mid_price = cal_mid_price(gr_bid_level_group, gr_ask_level_group)
    
    param = [1.5, 2, 0.5]  
    indicator_value = live_cal_book_i_v1(param, gr_bid_level_group, gr_ask_level_group, mid_price)
    
    timestamps.append(timestamp)
    mid_prices.append(mid_price)
    indicator_values.append(indicator_value)

result_df = pd.DataFrame({'timestamp': timestamps, 'mid_price': mid_prices, 'indicator_value': indicator_values})
result_df.to_csv('2023-05-08-bithumb-BTC-feature.csv', index=False)

