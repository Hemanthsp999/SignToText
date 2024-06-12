import mysql.connector


def connection():
    conn = mysql.connector.connect(host="localhost", user="root",
                                   password="hemanthsp", database="TalkToMe")
    c = conn.cursor()

    return c, conn
