import requests
import win32api,win32con
import json,os,sys
configs={
    'url':"http://127.0.0.1:10429",
    'textcont': 0
}

#获取桌面路径
def get_desktop():
    key =win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',0,win32con.KEY_READ)
    return win32api.RegQueryValueEx(key,'Desktop')[0]
#发送私聊消息
def privatemsg(login,toqq,text):
    url =  configs.get('url')+ '/sendprivatemsg'
    print('====>触发私聊消息')
    data = {
    'logonqq':login,
    'toqq':toqq,
    'msg':text
    }
    requests.post(url,data=data)
#获取框架登陆qq信息
def getlogonqq():
    url = configs.get('url')+'/getlogonqq'
    return requests.post(url).text
#上传zk内容图片
def uploadzkpic(loginqq,group,path):
    url = configs.get('url')+'/uploadgrouppic'
    data={
        'logonqq': loginqq,
        'group': group,
        'type':"path",
        'pic':os.path.dirname(os.path.realpath(sys.argv[0]))+'\\'+path+'.png'
    }
    resp = requests.post(url, data=data).text
    resp = json.loads(resp)['ret']
    return resp

#上传群图片
def uploadgrouppic(loginqq,group,path,type='path'):
    url = configs.get('url')+'/uploadgrouppic'
    data={
        'logonqq': loginqq,
        'group': group,
        'type':type,
        'pic':path
    }
    resp = requests.post(url, data=data).text
    resp = json.loads(resp)['ret']
    return resp

#发送群聊消息
def groupmsg(logonqq,group,msg,type=''):
    url = configs.get('url') + '/sendgroupmsg'
    print('====>触发群消息' )
    data = {
        'type':type,
        'logonqq': logonqq,
        'group':group,
        'msg':msg,
        'anonymous':'false'
    }
    requests.post(url, data=data)
#添加群
def addgroup(logonqq,group):
    url = configs.get('url')+'/addgroup'
    data = {
        'logonqq': logonqq,
        'group': group,
        'msg': '你好我是奥迪斯'
    }
    return requests.post(url,data=data)
#取群列表
def getgrouplist(logonqq):
    url = configs.get('url')+'/getgrouplist'
    data = {
        'logonqq':logonqq
    }
    resp = requests.post(url,data=data).text
    resp = json.loads(resp)['list']['List']
    return resp
