from gocqhttpbot.botstart.dao import *
import json
class switch:
    def __init__(self,key):
        self.key = key
    def __call__(self,fun):
        def inner(*args,**kwargs):
            res = None
            content = query_one("SELECT * FROM permissions WHERE id = "+str(kwargs['group_id']))
            if content is not None:
                content = json.loads(content['content'])
                # print(content.get(self.key))
                if content.get(self.key) == True:
                    # 这里传入了dict
                    res = fun(kwargs)
                else:
                    param = []
                    content.setdefault(self.key,False)
                    param.append(json.dumps(content))
                    param.append(kwargs['group_id'])
                    exec('UPDATE permissions SET content = ?   WHERE id = ?', param)
            else:
                param =[]
                param.append(kwargs['group_id'])
                param.append('{}')
                exec ("INSERT INTO permissions(id,content)VALUES(?,?)",param)
            return res
        return inner
# 获取所有的信息
def getAll(id):
    data = query_one('SELECT * FROM permissions WHERE id =' + id)['content']
    data = json.loads(data)
    ret = ''
    for i in data:
        ret += f'{i}\t\t{data[i]}\n'
    ret+='\n可控制功能开启或关闭 \n示例：/开启 光遇'
    return ret


# 设置功能开关
def setType(id,module,flag):
    content= query_one('SELECT * FROM permissions WHERE id =' + id)['content']
    content = json.loads(content)
    if module in content:
        param = []
        content[module] = flag
        print(content)
        param.append(json.dumps(content))
        param.append(id)
        exec('UPDATE permissions SET content = ?   WHERE id = ?', param)
        if flag:
            return "成功开启"+module+"功能"
        else:
            return "成功关闭"+module+"功能"
    else:
        return "功能不存在"
