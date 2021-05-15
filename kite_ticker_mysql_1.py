from kiteconnect import KiteTicker
import logging
from py_mysql import *
import pandas as pd
logging.basicConfig(level=logging.DEBUG)
import logging
from kiteconnect import KiteConnect
logging.basicConfig(level=logging.DEBUG)

df = pd.read_csv('lookup_table_2.csv', delimiter=',')
tokens = df.values.flatten().tolist()

api_secret = open('api_secret.txt', 'r').read()
kite = KiteConnect(api_key="22um3v62hlfd1nw8")

## You can comment line 12 to line 31 after you have done the tokens
## Login into the URL and PIN and get request token
## Paste the request token in my_request_token.txt
## Use this to delete your access token
# url = kite.login_url()
# print(url)

# request_token = open('my_request_token.txt','r').read() #2.1
# data = kite.generate_session(request_token, api_secret) #2.2
#
# kite.set_access_token(data["access_token"])
# print(data["access_token"])
#
# access_token_file = open("access_token.txt","w") #2.5
# access_token_file.write(data["access_token"]) #2.6
# access_token_file.close() #2.7

api_key=open('api_key.txt','r').read()
access_token=open('access_token.txt','r').read()

kws = KiteTicker(api_key, access_token, debug=True)

def job1():
    def on_ticks(ws,ticks):
        insert_tick=insert_ticks(ticks)
        print(ticks)

    def on_connect(ws,response):
        ws.subscribe(tokens)
        ws.set_mode(ws.MODE_FULL,tokens)
    def on_close(ws, code, reason):
        pass

    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.on_close = on_close
    kws.connect(threaded=True)

job1()
