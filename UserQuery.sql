import sqlite3

conn = sqlite3.connect('TalkToMe')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE UserDetails
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
              NAME TEXT NOT NULL,
              EMAIL TEXT NOT NULL,
              PHONE_NUMBER TEXT NOT NULL,
              PASSWORD TEXT NOT NULL,
              DEAF TEXT NOT NULL)''')

conn.commit()
conn.close()

