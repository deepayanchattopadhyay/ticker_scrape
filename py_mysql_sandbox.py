#use algo; database will get change and will get assigned
# then create table ticks(instrument_token int, last_price float(32), volume int, depth varchar(255), instrument_token int, date varchar(255));
#create table ticks(instrument_token int, last_price float(32), volume int, depth_sell_quantity_0 int,  depth_sell_quantity_1 int, varchar(255), date varchar(255))
#create table ticks(instrument_token int, last_price float(32), volume int, depth_sell_quantity_0 int,  depth_sell_quantity_1 int, date varchar(255))
#drop table ticks
# truncate table ticks
#drop database algo
#create database algo

import pymysql
db=pymysql.connect(host='localhost',user='root',password='12345',database='algo')
insert_into_table='insert into ticks(instrument_token,last_price,volume,sell_qty,buy_qty,sell_0_quantity,sell_1_quantity,sell_2_quantity,sell_3_quantity,sell_4_quantity,buy_0_quantity,buy_1_quantity,buy_2_quantity,buy_3_quantity,buy_4_quantity,date) values(%(instrument_token)s,%(last_price)s,%(volume)s,%(sell_qty)s,%(buy_qty)s,%(sell_0_quantity)s,%(sell_1_quantity)s,%(sell_2_quantity)s,%(sell_3_quantity)s,%(sell_4_quantity)s,%(buy_0_quantity)s,%(buy_1_quantity)s,%(buy_2_quantity)s,%(buy_3_quantity)s,%(buy_4_quantity)s,%(date)s)'

def insert_ticks(ticks):
    c=db.cursor()
    for tick in ticks:
        c.execute(insert_into_table,{'instrument_token':tick['instrument_token'],'last_price':tick['last_price'],
                                     'volume':tick['volume'],
                                     'sell_qty': tick['sell_quantity'],
                                     'buy_qty': tick['buy_quantity'],
                                     'sell_0_quantity': tick['depth']['sell'][0]['quantity'],
                                     'sell_1_quantity': tick['depth']['sell'][1]['quantity'],
                                     'sell_2_quantity': tick['depth']['sell'][2]['quantity'],
                                     'sell_3_quantity': tick['depth']['sell'][3]['quantity'],
                                     'sell_4_quantity': tick['depth']['sell'][4]['quantity'],
                                     'buy_0_quantity': tick['depth']['buy'][0]['quantity'],
                                     'buy_1_quantity': tick['depth']['buy'][1]['quantity'],
                                     'buy_2_quantity': tick['depth']['buy'][2]['quantity'],
                                     'buy_3_quantity': tick['depth']['buy'][3]['quantity'],
                                     'buy_4_quantity': tick['depth']['buy'][4]['quantity'],
                                     'date': tick['timestamp']})
    try:
        db.commit()
    except Exception:
        db.rollback()