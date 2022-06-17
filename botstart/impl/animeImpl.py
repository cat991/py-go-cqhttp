# 自动问答
import json,os
import random,re
from gocqhttpbot import log,PATH
def anime(txt):
    # path = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\data\\anime.json'
    path = PATH + f'\\data\\anime.json'
    with open(path,'r',encoding='utf-8')as f:
        res = json.loads(f.read())
        f.close()
        if txt in res:
            return res[str(txt)][random.randint(0,len(res[str(txt)])-1)]
        else:
            return False
def dinggong():
    # onePath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\data\\dinggong'
    onePath = PATH + f'\\data\\dinggong'
    name = os.listdir(onePath)[random.randint(0, len(os.listdir(onePath))-1)]
    url = 'file:///'+ onePath +'\\' + name
    url = url.replace('\\','/')
    print(f'[CQ:record,file={url}]')
    name = name.replace(".mp3","")
    # numbers = ""
    number = re.findall(f'[0-9]+', name)[0]
    # for i in number:
    #     numbers = numbers + str(i)
    return {
        "name":name.replace(number,""),
        "cq":f'[CQ:record,file={url}]'
    }
    # return result
    # return CQcode.record(f'data\\dinggong\\{os.listdir(onePath)[random.randint(0, len(os.listdir(onePath))-1)]}')
# 疯狂星期四
def crazy():
    file = PATH + "/data/疯狂星期四.json"
    log.info(file)
    with open(file,'r',encoding='utf-8')as f:
        data = json.loads(f.read())
        f.close()
    return data['post'][random.randint(0,len(data['post'])-1)]