# import sqlite3 as sql
import psycopg2 as sql
import os


def clear_all():
    conn = sql.connect(host='ec2-54-243-150-10.compute-1.amazonaws.com',
                       database='dvmjo6pvokn3v',
                       user='icknsevpzbardh',
                       port='5432',
                       password='5c195733c2d92181a25b5e73f8870c9b3788157e90380bcbdef013daa743644d')

    # conn = sql.connect('data.db', check_same_thread=False)

    tables = ['data', 'entries', 'sid']

    for t in tables:
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS %s" % t)
        conn.commit()

    c = conn.cursor()
    c.execute("create table data (name varchar(512), passwd char(32), email varchar(512))")
    conn.commit()
    c.close()

    c = conn.cursor()
    c.execute("create table entries (id int, name varchar(512), time varchar(32), "
              "icon varchar(512), message varchar(4096), room varchar(512));")
    c.execute('create table sid (nid int, s int);')
    c.execute('insert into sid values (0, 0);')
    c.execute('update sid set nid = 1 where s = 0;')
    conn.commit()
    c.close()
    conn.close()


if __name__ == '__main__':
    clear_all()
