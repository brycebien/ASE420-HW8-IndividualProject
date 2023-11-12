import sqlite3
connection = sqlite3.connect("HW-8.db")
cur = connection.cursor()

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

user_input = input('enter a query tag\n')
res = cur.execute("SELECT * FROM records WHERE Tag = '" + user_input + "'")

print(res.fetchall())