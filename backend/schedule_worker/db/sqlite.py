import sqlite3


class MpkDb():
    def __init__(self):
       self.db_file = self.db_file = os.environ['TRAM_ROOT'] + '/data/baza.ready.zip'
       self.db_connection = sqlite3.connect(self.db_file)
       self.cursor = db_connection.cursor()
       self.cursor.execute('select name from lines;')
       result = self.cursor.fetchall()
       db_connection.commit()
       logging.info(result)


