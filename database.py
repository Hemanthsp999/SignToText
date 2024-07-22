import MySQLdb

"""
import sqlite3
def connection():
    conn = sqlite3.connect('TalkToMe.db')
    c = conn.cursor()
    return c,conn
"""


def connection():
    conn = MySQLdb.connect(host="localhost", user="****",
                           password="*****", database="TalkToMe")
    c = conn.cursor()

    return c, conn
