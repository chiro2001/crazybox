import sqlite3 as sql
import os

conn = sql.connect('database.db')
c = conn.cursor()
c.execute("select * from data")
data = c.fetchall()
print(data)
c.close()
conn.close()

conn = sql.connect('entries.db')
c = conn.cursor()
c.execute("select * from entries")
data = c.fetchall()
print(data)
c.close()
conn.close()

