import win32api,win32con,os,sys
import requests,json,random
from gocqhttpbot.botstart.util import permissions,init
from gocqhttpbot.botstart.entity import CQcode
from gocqhttpbot.botstart.impl import otherImpl
configs={
    'url':"http://127.0.0.1:5700",
    'textcont': 0
}

#获取桌面路径
def get_desktop():
    key =win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',0,win32con.KEY_READ)
    return win32api.RegQueryValueEx(key,'Desktop')[0]


#发送群消息
def send_group_msg(group_id,message,flag = True,fengkong= False):
    url = configs.get('url') + '/send_group_msg'
    if fengkong :
        message = otherImpl.toImage(message,"临时风控处理")
    data = {
        'group_id':group_id,
        # 'message':  message + ('\n机器人是免费的,如果你喜欢的话可以点击链接赞助作者哦~\n地址:https://dun.mianbaoduo.com/@heimao' if random.randint(1,10) == 5  else '')
        'message': message
    }
    if init.CONFIG.msgDelet and flag:
        permissions.add_msg_id(requests.post(url, data).text)
    else:
        requests.post(url,data)

# 获取群艾特次数
def get_group_at_all_remain(group_id):
    url = configs.get('url') + '/get_group_at_all_remain'

    data = {
        'group_id':group_id
    }
    resp = requests.post(url, data).text
    can_at_all = json.loads(resp)['data']['can_at_all']
    return can_at_all
#消息撤回
def delete_msg(msg_id):
    url = configs.get('url')+'/delete_msg'
    data = {
        "message_id":msg_id
    }
    try:
        requests.post(url,data)
    except:
        print(f'消息{str(msg_id)}撤回失败')
#禁言功能
def set_group_ban(group_id,user_id,duration):
    url = configs.get('url') + '/set_group_ban'
    data = {
        'group_id': group_id,  #
        'user_id': user_id,  #
        'duration': duration*60  # 分
    }
    status = json.loads(requests.post(url,data).text)
    if status['status'] == 'ok':
        return True
    else:
        return False
#加好友处理
def set_friend_add_request(flag,remark=''):
    url =configs.get('url') + '/set_friend_add_request'
    data ={
        'flag':flag,#上报消息标识符
        'approve' : True,#默认同意
        'remark':remark #好友备注，默认空
    }
    requests.post(url, data)

#处理加群请求或邀请
def set_group_add_request(flag,type,reason=''):
    url = configs.get('url') + '/set_group_add_request'
    data ={
        'flag':flag, #加群标识符
        # str(type):type,#
        'sub_type':type,
        'approve':True, #默认同意邀请
        'reason':reason#拒绝的理由
    }
    requests.post(url, data)

#上传群图片
def uploadgrouppic(path):
    url = configs.get('url')+'/get_image'
    data={
        'file':os.path.dirname(os.path.realpath(sys.argv[0]))+'\\'+path+'.png'
    }
    resp = requests.post(url, data=data).text
    resp = json.loads(resp)
    return resp
#检查是否可以发语音
def can_send_record():
    txt = requests.get(configs.get('url')+"/can_send_record").text

    if json.loads(txt)['data']['yes']:
        return True
    else:
        return False
#获取群信息
def get_group_info(group_id):
    url = configs.get('url') + '/get_group_info'
    data = {
        'group_id':group_id,
        'no_cache':False
    }
    return requests.post(url,data).text
#合并消息处理
def send_group_forward_msg(group_id,content):
    url = configs.get('url') + '/send_group_forward_msg'
    data = {
        'group_id':group_id,
        'messages':content
    }
    return requests.post(url,data).text

#获取陌生人信息
def get_stranger_info(user_id):
    url = configs.get('url') + '/get_stranger_info'
    data = {
        'user_id':int(user_id),
        'no_cache':True
    }
    return requests.post(url,data).text

#获取群列表
def get_group_list():
    url = configs.get('url') + '/get_group_list'
    return requests.post(url).text

