import MySQLdb


def connection():
    conn = MySQLdb.connect(host="localhost", user="root",
                           password="root@hemanthsp", database="TalkToMe")
    c = conn.cursor()

    return c, conn
