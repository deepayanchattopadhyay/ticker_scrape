import logging
from kiteconnect import KiteTicker
import os
import pandas as pd
import openpyxl
import logging
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import operator
import inspect
import datetime,kite_ticker_excel,os,random;
import collections
import operator
import xlwings as xw
now = datetime.datetime.now()

from py_mysql import *

logging.basicConfig(level=logging.DEBUG)

# Initialise
kws = KiteTicker("22um3v62hlfd1nw8", "qYuFAavUYNVKAQY6kyd4Dwtk7R8JM4DM")

wb = xw.Book(r'C:\Users\deepa\PycharmProjects\Zerodha_Live_Automate_Trading-_using_AI_ML_on_Indian_stock_market-using-basic-python-master\store.xlsx')
sht = wb.sheets['Sheet1']

row=2


def on_ticks(ws, ticks):
    global row
    print(row)
    try:
        for company_data in ticks:
            sht.range('A'+str(row)).value=company_data['last_price']
            sht.range('B'+str(row)).value=company_data['volume']
            sht.range('C'+str(row)).value=company_data['buy_quantity']
            sht.range('D'+str(row)).value=company_data['sell_quantity']
            sht.range('E' + str(row)).value = company_data['timestamp']
            sht.range('F' + str(row)).value = company_data['instrument_token']
            row=row+1
    except Exception as e:
        raise e



# Read the CSV into a pandas data frame (df)
#   With a df you can do many things
#   most important: visualize data with Seaborn
df = pd.read_csv('lookup_table_2.csv', delimiter=',')
subscribe = df.values.flatten().tolist()

# subscribe = [3014145, 121345, 1147137, 1793, 4923649]

def on_connect(ws, response):
    ws.subscribe(subscribe)
    ws.set_mode(ws.MODE_FULL,subscribe)

# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.connect()








