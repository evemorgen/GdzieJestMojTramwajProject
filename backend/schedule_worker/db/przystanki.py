import os
import logging
import sqlite3
import json


class PrzystankiDb():
    def __init__(self):
        self.db_file = os.environ['TRAM_ROOT'] + '/data/przystanki.db'
        self.db_connection = sqlite3.connect(self.db_file)
        self.cursor = self.db_connection.cursor()
        logging.info('PrzystankiDb object created')

    def get_point_time(self, variantId, lineName, pointId):
        query = """
            select pointName, pointTime, route from przystanki where variantId = '%s' and lineName = '%s' and pointId = '%s';
        """ % (variantId, lineName, pointId)
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        print(data)
        to_return = {
            'pointName': data[0][0],
            'pointTime': json.loads(data[0][1]),
            'route': data[0][2]
        }
        return to_return

    def insert(self, stuff):
        query = """
            insert into przystanki values (%s, %s, '%s', '%s', '%s', '%s');
        """ % (stuff['pointId'], stuff['variantId'], stuff['lineName'], stuff['pointTime'], stuff['pointName'], stuff['route'])
        self.cursor.execute(query)
        self.db_connection.commit()

    def clear_table(self):
        query = "delete from przystanki"
        self.cursor.execute(query)
        self.db_connection.commit()

    def get_terminal_time(self, line, terminal):
        query = "select pointTime from przystanki where lineName = {} and pointName = '{}' and route like '{}%'".format(line, terminal, terminal)
        self.cursor.execute(query)
        time = self.cursor.fetchall()
        ret = []
        if len(time) == 1 or len(time) == 2:
            return time[0][0]
