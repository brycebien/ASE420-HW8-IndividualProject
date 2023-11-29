import sqlite3
from src.utility import Console

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
    console = Console()
    user_input = input("Enter a command (record DATE FROM TO TASK :TAG)(query :TAG or DATE or TASK)")
    console.processCommand(user_input)
    console.runCommands()