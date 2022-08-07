from botTest.botstart.dao import query_one,query

data = query_one("SELECT * FROM list_test where id = 3 order by id desc ")
print(data)

