from datetime import datetime
import re
import sqlite3

class Database:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cur = self.connection.cursor()
        self._createDatabase()

    def _createDatabase(self):
        try:
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS records(
                    ID INTEGER PRIMARY KEY,
                    DATE TEXT,
                    FROM_TIME TEXT,
                    TO_TIME TEXT,
                    TASK TEXT,
                    TAG TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            print("CREATE DATABASE ERROR: ", e)

class DeleteDatabase(Database):
    def __init__(self, database):
        super().__init__(database)

    def delete(self):
       self.cur.execute('''DROP TABLE records;''')
       self.connection.commit()

class QueryDatabase(Database):
    def __init__(self, database):
        super().__init__(database)

    def query(self, query):
        try:
           # query = query[0]
            if query.lower() == 'today': #records from today's date
                date = datetime.now().strftime("%Y/%m/%d")
                self.cur.execute('''SELECT * FROM records WHERE DATE = ?''',(date,))
            elif re.match(r'\d{4}/\d{2}/\d{2}', query): #records from certain date
                self.cur.execute('''SELECT * FROM records WHERE DATE = ?''',(query,))
            elif query.startswith(':'): #records with a certain tag
                self.cur.execute('''SELECT * FROM records WHERE TAG = ?''',(query,))
            else: #records with a certain task
                self.cur.execute('''SELECT * FROM records WHERE TASK = ?''',(query,))
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print("SQL QUERY ERROR: ", e)
    
class RecordDatabase(Database):
    def __init__(self, database):
        super().__init__(database)
    
    def record(self, date, start_time, end_time, task, tag):
        try:
            self.cur.execute('''INSERT INTO records (DATE, FROM_TIME, TO_TIME, TASK, TAG)
                            VALUES (?, ?, ?, ?, ?);
                            ''', (date, start_time, end_time, task, tag))
            self.connection.commit()
        except sqlite3.Error as e:
            print("SQL RECORD ERROR: ", e)