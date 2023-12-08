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

    def queryDate(self, query):
        try:
            self.cur.execute('''SELECT * FROM records WHERE DATE = ?''',(query,))
            self.__printQuery(self.cur.fetchall())
        except sqlite3.Error as e:
            print("SQL QUERY ERROR: ", e)

    def queryTask(self, query):
        try:
            self.cur.execute('''SELECT * FROM records WHERE TASK = ?''',(query,))
            self.__printQuery(self.cur.fetchall())

        except sqlite3.Error as e:
            print("SQL QUERY ERROR: ", e)

    def queryTag(self, query):
        try:
            self.cur.execute('''SELECT * FROM records WHERE TAG = ?''',(query,))
            self.__printQuery(self.cur.fetchall())
        except sqlite3.Error as e:
            print("SQL QUERY ERROR: ", e)

    def queryAll(self):
        try:
            self.cur.execute('''SELECT * FROM records''')
            return(self.cur.fetchall())
        except sqlite3.Error as e:
            print("SQL QUERY ERROR: ", e)
        
    def __printQuery(self, res):
        for record in res:
            print(record)

    
class RecordDatabase(Database):
    def __init__(self, database):
        super().__init__(database)
    
    def record(self, inputs):
        date, start_time, end_time, task, tag = inputs
        try:
            self.cur.execute('''INSERT INTO records (DATE, FROM_TIME, TO_TIME, TASK, TAG)
                            VALUES (?, ?, ?, ?, ?);
                            ''', (date, start_time, end_time, task, tag))
            self.connection.commit()
        except sqlite3.Error as e:
            print("SQL RECORD ERROR: ", e)