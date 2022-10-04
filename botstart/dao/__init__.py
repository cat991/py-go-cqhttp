import sqlite3
import pymysql
from gocqhttpbot import PATH
def query(sql:str,number:int = None)->list:
    init()
    cursor.execute(sql)
    if number :
        data = cursor.fetchmany(number)
    else:
        data = cursor.fetchall()
    close()
    return data

def exec(sql:str, param:list=None)->bool:
    init()
    if param is None:
        param = []
    cursor.execute(sql,param)
    conn.commit()
    close()
    return True


def query_one(sql:str)->dict:
    init()
    cursor.execute(sql)
    data = cursor.fetchone()
    # print(data)
    close()
    return data

# 关闭sql游标
def close():
    cursor.close()
    conn.close()

def init ():
    sql = "0"
    global cursor
    global conn
    if sql == "1":
        # mysql
        # print("初始化mysql")
        conn = pymysql.connect(host='url', port=3306, user='root', passwd='123456', db='qq_bot')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    else:
        # sqlite
        # print("初始化sqlite")
        def dict_factory(cursor, row):
            d = {}
            for index, col in enumerate(cursor.description):
                d[col[0]] = row[index]
            return d
        conn = sqlite3.connect(PATH+'/data/bot.db')
        conn.row_factory = dict_factory
        cursor = conn.cursor()

