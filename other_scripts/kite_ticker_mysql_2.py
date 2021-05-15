from kiteconnect import KiteTicker
import logging
from py_mysql import *
logging.basicConfig(level=logging.DEBUG)

api_key=open('api_key.txt','r').read()
access_token=open('access_token.txt','r').read()
tokens=[53703431,112129]
kws=KiteTicker(api_key,access_token)


def on_ticks(ws,ticks):
    insert_tick=insert_ticks(ticks)
    print(ticks)


def on_connect(ws,response):
    ws.subscribe(tokens)
    ws.set_mode(ws.MODE_FULL,tokens)

def on_close(ws, code, reason):
    ws.stop()


kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close
kws.connect(threaded=True)










import logging
from kiteconnect import KiteTicker

logging.basicConfig(level=logging.DEBUG)


kws = KiteTicker("22um3v62hlfd1nw8", "OLWjBBUpA1s9Ybc1CQbqWBk7mvF6lcEm", debug=True)



def on_ticks(ws, ticks):
    print("Ticks: {}".format(ticks))


def on_connect(ws, response):
    ws.subscribe([738561, 5633])

    ws.set_mode(ws.MODE_FULL, [738561])


def on_close(ws, code, reason):
    pass

kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close
kws.connect(threaded=True)
















