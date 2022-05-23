# 自动问答
import json,os,sys
import random,re
from gocqhttpbot.botstart.entity import CQcode
def anime(txt):
    path = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\data\\anime.json'
    # path = '../../data/anime.json'
    with open(path,'r',encoding='utf-8')as f:
        res = json.loads(f.read())
        f.close()
        if txt in res:
            return res[str(txt)][random.randint(0,len(res[str(txt)])-1)]
        else:
            return False
def dinggong():
    onePath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\data\\dinggong'
    # onePath = f'..\\..\\..\\data\\dinggong'
    # pathName = ''
    # print(os.listdir(onePath))
    # print(len(os.listdir(onePath)))
    # result = res.replace('urls','file:///'+onePath +'\\' +os.listdir(onePath)[random.randint(0, len(os.listdir(onePath))-1)])
    name = os.listdir(onePath)[random.randint(0, len(os.listdir(onePath))-1)]
    url = 'file:///'+ onePath +'\\' + name
    # url = f'https://gonggongkedu.oss-cn-beijing.aliyuncs.com/bot语音/{name}'
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

