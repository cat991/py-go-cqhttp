from botTest import *

def query(sql:str,number:int = None)->list:
    cursor.execute(sql)
    if number :
        data = cursor.fetchmany(number)
    else:
        data = cursor.fetchall()
    close()
    return data

def query_one(sql:str)->dict:
    cursor.execute(sql)
    data = cursor.fetchone()
    close()
    return data

# 关闭sql游标
def close():
    cursor.close()
    conn.close()