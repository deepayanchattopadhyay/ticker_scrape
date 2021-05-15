import logging
from kiteconnect import KiteConnect
import requests
from urllib.parse import parse_qsl, urljoin, urlparse
import pandas as pd
import datetime
import glob
import os
import time
import numpy as np

api_secret = open('api_secret.txt', 'r').read()
logging.basicConfig(level=logging.DEBUG)
kite = KiteConnect(api_key="22um3v62hlfd1nw8")

# # You can comment line 12 to line 31 after you have done the tokens
# # Login into the URL and PIN and get request token
# # Paste the request token in my_request_token.txt
# # Use this to delete your access token
# url = kite.login_url()
# print(url)
#
# request_token = open('my_request_token.txt','r').read() #2.1
# data = kite.generate_session(request_token, api_secret) #2.2
# # kite.invalidate_access_token(my_access_token)
#
# kite.set_access_token(data["access_token"]) #2.3
# print(data["access_token"]) #2.4
#
# access_token_file = open("access_token.txt","w") #2.5
# access_token_file.write(data["access_token"]) #2.6
# access_token_file.close() #2.7
#
# access_token = open('access_token.txt', 'r').read() #3.1
# kite.set_access_token(access_token) #3.2

# zapp.to_csv(r"C:\Users\deepa\PycharmProjects\Zerodha_Live_Automate_Trading-_using_AI_ML_on_Indian_stock_market-using-basic-python-master\zapp.csv")

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

def job1():
    df = pd.DataFrame(kite.instruments())
    df = df[(df.exchange == "NSE")]
    lookup_table = pd.read_csv("lookup_table.csv")
    lookup_table.rename(columns={'Ticker': 'tradingsymbol'}, inplace=True)
    df = pd.merge(df, lookup_table, on='tradingsymbol')

    filename = str(int(round(time.time() * 1000)))

    df['time_stamp'] = filename

    df.to_csv('C:/Users/deepa/PycharmProjects/Zerodha_Live_Automate_Trading-_using_AI_ML_on_Indian_stock_market-using-basic-python-master/outputs/' + str(filename + '.csv'))

    glued_data = pd.DataFrame()
    for file_name in glob.glob(r'C:/Users/deepa/PycharmProjects/Zerodha_Live_Automate_Trading-_using_AI_ML_on_Indian_stock_market-using-basic-python-master/outputs/' + '*.csv'):
        x = pd.read_csv(file_name, low_memory=False)
        glued_data = pd.concat([glued_data, x], axis=0)
        # print(glued_data)
        glued_data.to_csv(
            'C:/Users/deepa/PycharmProjects/Zerodha_Live_Automate_Trading-_using_AI_ML_on_Indian_stock_market-using-basic-python-master/glued_output/glued_data.csv')

        moving_average = glued_data[['tradingsymbol', 'Close Price', 'time_stamp']]

        moving_average = pd.pivot_table(moving_average, values='Close Price', index=['time_stamp'],
                                    columns='tradingsymbol').reset_index()


        # Take the rolling mean (= moving average) over 6 periods (= 1/2 hour)
        moving_average = moving_average.drop(moving_average.columns[[0]], axis = 1)
        moving_average = moving_average.rolling(2).mean()

        glued_data = pd.read_csv(
            r"C:\Users\deepa\PycharmProjects\Zerodha_Live_Automate_Trading-_using_AI_ML_on_Indian_stock_market-using-basic-python-master\glued_output\glued_data.csv")

        moving_average = glued_data[['tradingsymbol', 'Close Price', 'time_stamp']]

        moving_average = pd.pivot_table(moving_average, values='Close Price', index=['time_stamp'],
                                        columns='tradingsymbol').reset_index()

        # Take the rolling mean (= moving average) over 6 periods (= 1/2 hour)
        moving_average = moving_average.drop(moving_average.columns[[0]], axis=1)
        moving_average = moving_average.rolling(2).mean().T
        moving_average[0] = moving_average[0].fillna(0)


        moving_average.columns = [str(col) + '_record' for col in moving_average.columns]

        positive_negative_momentum_count = (pd.get_dummies(np.sign(moving_average.stack()))
                                            .sum(level=0)
                                            .rename({-1: 'negative_count', 1: 'positive_count'}, axis=1))

        positive_momentum_count = (moving_average.select_dtypes(include='float64').gt(0.001).sum(axis=1)) + 1
        negative_momentum_count = moving_average.select_dtypes(include='float64').lt(0).sum(axis=1)

        last_hour_positive_momentum_count = moving_average[moving_average.columns[-3:]]
        last_hour_positive_momentum_count = (last_hour_positive_momentum_count.select_dtypes(include='float64').gt(
            0.001).sum(axis=1)) + 1

        concat = pd.concat([moving_average, positive_momentum_count, negative_momentum_count,
                            last_hour_positive_momentum_count], axis=1)
        concat.rename(columns={0: 'positive_momentum_count', 1: 'negative_momentum_count',
                               2: 'last_hour_positive_momentum_count'}, inplace=True)

        print(concat)

        concat.to_csv(
            'C:/Users/deepa/PycharmProjects/Zerodha_Live_Automate_Trading-_using_AI_ML_on_Indian_stock_market-using-basic-python-master/glued_output/moving_average.csv')


scheduler = BackgroundScheduler()
scheduler.add_job(job1, IntervalTrigger(), seconds=120, id="job1")
scheduler.start()

# moving_average = moving_average.pct_change()
# moving_average

