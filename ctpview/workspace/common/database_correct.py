import os
import sqlite3
import traceback
from cgi import print_arguments

import pandas as pd


# 遍历数据库，修正数据库
def fix1():
    trader_db_path = '/home/tsaodai/data/trader/control.db'

    conn = sqlite3.connect(trader_db_path)
    command = 'alter table order_lookup rename to order_lookup_temp;'
    conn.execute(command)
    command = 'create table if not exists order_lookup(order_index TEXT, user_id TEXT, order_ref TEXT, price REAL, yesterday_volume INT, today_volume INT)'
    conn.execute(command)
    command = 'insert into order_lookup(order_index , user_id , order_ref , yesterday_volume , today_volume ) select order_index , user_id , order_ref  , yesterday_volume , today_volume from order_lookup_temp'
    conn.execute(command)
    command = 'drop table order_lookup_temp;'
    conn.execute(command)
    conn.commit()
    conn.close()


fix1()