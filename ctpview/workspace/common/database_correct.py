import sqlite3
import traceback


class DatabaseCorrect():

    def __init__(self):
        pass

    def update(self):
        return self.fix1()

    def fix1(self):
        trader_db_path = '/home/tsaodai/data/trader/control.db'

        try:
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
            return 0
        except:
            error_msg = traceback.format_exc()
            print('%s %s' % (trader_db_path, error_msg))
            return -1


databasecorrect = DatabaseCorrect()

if __name__ == "__main__":
    databasecorrect.update()
