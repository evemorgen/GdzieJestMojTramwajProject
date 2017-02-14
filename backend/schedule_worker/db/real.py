import os
import sqlite3
import logging


class RealDb():
    def __init__(self):
        self.db_file = os.environ['TRAM_ROOT'] + '/data/real.db'
        self.db_connection = sqlite3.connect(self.db_file)
        self.cursor = self.db_connection.cursor()
        logging.info('RealDb object created')

    def get_all(self):
        query = "select * from real_data"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        logging.info(data)

    def insert_point(self, mes_id, lat, lon, line, ts):
        query = "insert into real_data values (%s, %s, %s, %s, %s)" % (mes_id, line, lat, lon, ts)
        self.cursor.execute(query)
        self.db_connection.commit()
