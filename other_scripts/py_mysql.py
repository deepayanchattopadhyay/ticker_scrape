#use algo; database will get change and will get assigned
# then create table ticks(instrument_token int, last_price float(32),instrument_token int, date varchar(255));
#drop table ticks
# truncate table ticks
#drop database algo
#create database algo

import pymysql
db=pymysql.connect(host='localhost',user='root',password='1234',database='algo')
insert_into_table='insert into ticks(instrument_token,last_price,volume,date) values(%(instrument_token)s,%(last_price)s,%(volume)s,%(date)s)'
def insert_ticks(ticks):
    c=db.cursor()
    for tick in ticks:
        c.execute(insert_into_table,{'instrument_token':tick['instrument_token'],'last_price':tick['last_price'],
                                    'volume':tick['volume'],'date':tick['timestamp']})
    try:
        db.commit()
    except Exception:
        db.rollback()