import win32api,win32con,os,sys
import requests,json
configs={
    'url':"http://127.0.0.1:5700",
    'textcont': 0
}

#获取桌面路径
def get_desktop():
    key =win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',0,win32con.KEY_READ)
    return win32api.RegQueryValueEx(key,'Desktop')[0]




#发送群消息
def send_group_msg(group_id,message):
    url = configs.get('url') + '/send_group_msg'

    data = {
        'group_id':group_id,
        'message':  message,
    }
    requests.post(url, data)


# 获取群艾特次数
def get_group_at_all_remain(group_id):
    url = configs.get('url') + '/get_group_at_all_remain'

    data = {
        'group_id':group_id
    }
    resp = requests.post(url, data).text
    can_at_all = json.loads(resp)['data']['can_at_all']
    return can_at_all

#加好友处理
def set_friend_add_request(flag,remark=''):
    url =configs.get('url') + '/set_friend_add_request'
    data ={
        'flag':flag,#上报消息标识符
        'approve' : True,#默认同意
        'remark':remark #好友备注，默认空
    }
    print(requests.post(url, data))

#处理加群请求或邀请
def set_group_add_request(flag,type,reason=''):
    url = configs.get('url') + '/set_group_add_request'
    data ={
        'flag':flag, #加群标识符
        str(type):type,#
        'approve':True, #默认同意邀请
        'reason':reason#拒绝的理由
    }
    print(requests.post(url, data))

#上传群图片
def uploadgrouppic(path):
    url = configs.get('url')+'/get_image'
    data={
        'file':os.path.dirname(os.path.realpath(sys.argv[0]))+'\\'+path+'.png'
    }
    resp = requests.post(url, data=data).text
    resp = json.loads(resp)
    return resp
#获取群信息
def get_group_info(group_id):
    url = configs.get('url') + '/get_group_info'
    data = {
        'group_id':group_id,
        'no_cache':False
    }
    return requests.post(url,data).text