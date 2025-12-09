import sqlite3
import traceback
import os


class DatabaseCorrect():

    def __init__(self):
        pass

    def update(self):
        return self.fix1()

    def fix1(self):
        ret = 0
        trader_db_path = '/home/tsaodai/data/trader/control.db'

        conn = sqlite3.connect(trader_db_path)
        try:
            command = 'alter table order_lookup rename to order_lookup_temp;'
            conn.execute(command)
            command = 'create table if not exists order_lookup(order_index TEXT, user_id TEXT, yesterday_order_ref TEXT, today_order_ref TEXT, yesterday_volume INT, today_volume INT);'
            conn.execute(command)
            command = 'insert into order_lookup(order_index, user_id, yesterday_order_ref, yesterday_volume, today_volume) select order_index, user_id, order_ref, yesterday_volume, today_volume from order_lookup_temp'
            conn.execute(command)
            command = 'update order_lookup set today_order_ref="";'
            conn.execute(command)
            command = 'drop table order_lookup_temp;'
            conn.execute(command)
            conn.commit()
            print('correct %s order_lookup: add yesterday_order_ref ..' % (trader_db_path))
        except:
            error_msg = traceback.format_exc()
            print('%s %s' % (trader_db_path, error_msg))
            ret = -1
        conn.close()

        return ret


databasecorrect = DatabaseCorrect()

if __name__ == "__main__":
    databasecorrect.update()
