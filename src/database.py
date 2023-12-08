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
       self.cur.execute('''DELETE FROM records;''')
       self.connection.commit()
       print('All records have been deleted')

class QueryDatabase(Database):
    def __init__(self, database):
        super().__init__(database)
        self.res = ''

    def queryDate(self, query):
        try:
            self.cur.execute('''SELECT * FROM records WHERE DATE = ?''',(query,))
            self.res = self.cur.fetchall()
            if self.res == []:
                self.__printNotFound()
            else:
                self.__printQuery()
        except sqlite3.Error as e:
            print("SQL QUERY ERROR: ", e)

    def queryTask(self, query):
        try:
            self.cur.execute('''SELECT * FROM records WHERE TASK = ?''',(query,))
            self.res = self.cur.fetchall()
            if self.res == []:
                self.__printNotFound()
            else:
                self.__printQuery()
        except sqlite3.Error as e:
            print("SQL QUERY ERROR: ", e)

    def queryTag(self, query):
        try:
            self.cur.execute('''SELECT * FROM records WHERE TAG = ?''',(query,))
            self.res = self.cur.fetchall()
            if self.res == []:
                self.__printNotFound()
            else:
                self.__printQuery()
        except sqlite3.Error as e:
            print("SQL QUERY ERROR: ", e)

    def queryAll(self):
        try:
            self.cur.execute('''SELECT * FROM records''')
            self.res = self.cur.fetchall()
            if self.res == []:
                self.__printNotFound()
            else:
                return self.res
        except sqlite3.Error as e:
            print("SQL QUERY ERROR: ", e)
        
    def __printQuery(self):
        for record in self.res:
            print(record)

    def __printNotFound(self):
        print('No records found')

    def query(self, query, method):
        sql_query = f'SELECT * FROM records WHERE {method.upper()} = ?'
        try:
            self.cur.execute(sql_query,(query,))
            self.res = self.cur.fetchall()
            if self.res == []:
                self.__printNotFound()
            else:
                self.__printQuery()
        except sqlite3.Error as e:
            print("SQL QUERY ERROR: ", e) 
    
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