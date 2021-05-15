from kiteconnect import KiteConnect
api_key="Your API KEY"
api_secret="Your API Secret"
kite=KiteConnect(api_key,api_secret)
kite.request_access_token('Your Access Token',api_secret)
kite.place_order(tradingsymbol='SBIN',quantity=1,exchange='NSE',order_type='MARKET',transaction_type='BUY',product='CNC')