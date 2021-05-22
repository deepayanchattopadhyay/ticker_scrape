from kiteconnect import KiteTicker
import logging
from py_mysql_sandbox import *
import pandas as pd
logging.basicConfig(level=logging.DEBUG)
import os
from pprint import pprint
from kiteconnect import KiteConnect
from selenium import webdriver
import time

os.chdir(r"C:\Users\zerodha\PycharmProjects\zerodha\Fetch_Ticker_Data_Scripts")



df = pd.read_csv('lookup_table_2.csv', delimiter=',')
tokens = df.values.flatten().tolist()

def autologin():
    token_path = r'C:\Users\zerodha\PycharmProjects\zerodha\Fetch_Ticker_Data_Scripts\all_keys.txt'
    key_secret = open(token_path,'r').read().split()
    kite = KiteConnect(api_key=key_secret[0])
    service = webdriver.chrome.service.Service(r"C:\Users\zerodha\Downloads\chromedriver_win32\chromedriver")
    service.start()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options = options.to_capabilities()
    driver = webdriver.Remote(service.service_url, options)
    driver.get(kite.login_url())
    driver.implicitly_wait(10)
    username = driver.find_element_by_xpath('// *[ @ id = "userid"]')
    password = driver.find_element_by_xpath('//*[@id="password"]')
    username.send_keys(key_secret[2])
    password.send_keys(key_secret[3])
    driver.find_element_by_xpath('//*[@id="container"]/div/div/div/form/div[4]/button').click()
    pin = driver.find_element_by_xpath('//*[@id="pin"]')
    pin.send_keys(key_secret[4])
    driver.find_element_by_xpath('//*[@id="container"]/div/div/div/form/div[3]/button').click()
    time.sleep(10)
    request_token = driver.current_url.split('=')[1].split('&action')[0]
    with open(r'C:\Users\zerodha\PycharmProjects\zerodha\Fetch_Ticker_Data_Scripts\my_request_token.txt', 'w') as the_file:
        the_file.write(request_token)
    driver.quit()

autologin()
request_token = open(r"C:\Users\zerodha\PycharmProjects\zerodha\Fetch_Ticker_Data_Scripts\my_request_token.txt",
                         'r').read()

while len(request_token) < 30:
    print('trying_again')
    autologin()
    request_token = open(r"C:\Users\zerodha\PycharmProjects\zerodha\Fetch_Ticker_Data_Scripts\my_request_token.txt",
                         'r').read()
    print(request_token)

token_path = r'C:\Users\zerodha\PycharmProjects\zerodha\Fetch_Ticker_Data_Scripts\all_keys.txt'
key_secret = open(token_path, 'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
data = kite.generate_session(request_token, key_secret[5]) #2.2
kite.set_access_token(data["access_token"])
access_token = data["access_token"]
print(access_token)
with open(r'C:\Users\zerodha\PycharmProjects\zerodha\Fetch_Ticker_Data_Scripts\access_token.txt', 'w') as the_file:
    the_file.write(access_token)
print(access_token)

kws = KiteTicker(key_secret[0], access_token, debug=True)
timeout = time.time() + 60 * 60 * 8  # 55.5 minutes from now, 8 hours from now add 60 *4.5 if you want 4.5 mins

while True:
    timer = 0
    def on_ticks(ws, ticks):
        insert_tick = insert_ticks(ticks)
        pprint(ticks)

    def on_connect(ws, response):
        ws.subscribe(tokens)
        ws.set_mode(ws.MODE_FULL, tokens)

    def on_close(ws, code, reason):
        pass

    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.on_close = on_close
    kws.connect(threaded=True)
    time.sleep(10)

    if timer == 480 or time.time() > timeout:
        break
    timer = timer - 1
    time.sleep(5)


