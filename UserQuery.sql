import database

conn = connection()
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE UserDetails
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
              NAME VARCHAR(100) NOT NULL,
              EMAIL VARCHAR UNIQUE NOT NULL,
              PHONE_NUMBER INT(100) NOT NULL,
              PASSWORD VARCHAR(100) NOT NULL,
              DEAF INT(2) NOT NULL)''')

conn.commit()
conn.close()

