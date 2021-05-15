import mysql.connector as sql
import pandas as pd
import numpy as np
db=sql.connect(host='localhost',user='root',password='1234',database='algo')
data=pd.read_sql('select * from ticks',con=db,parse_dates=True)
data=pd.DataFrame(data)
data['date'] = data['date'].astype('datetime64[ns]')
data=data.set_index(['date'])
ticks=data[['instrument_token', 'last_price']]
data= ticks.groupby('instrument_token')['last_price'].resample('1min').ohlc().dropna()
print(data['close'])


