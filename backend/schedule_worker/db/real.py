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
