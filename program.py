import sqlite3
connection = sqlite3.connect("HW-8.db")
cur = connection.cursor()

#use CRUD opperations to query the database -- store this in utility?

#cur.execute("drop table records")
cur.execute('''
            CREATE TABLE IF NOT EXISTS records(
                ID INTEGER PRIMARY KEY,
                DATE TEXT,
                FROM_TIME TEXT,
                TO_TIME TEXT,
                TASK TEXT,
                TAG TEXT
            )
''')
connection.commit()

while(True):        
    user_input = input('enter a command\n')
    # res = cur.execute("SELECT * FROM records WHERE Tag = '" + user_input + "'")
    # print(res.fetchall())
