# 处理加群，邀请等信息
import json
from gocqhttpbot.botstart.entity import GroupEntity
from gocqhttpbot.botstart.util import init

def groupHanderController(data):
    data = json.loads(data)

    self_id = data['self_id'] #收到消息的机器人
    request_type = data['request_type']#消息类型，好友添加：friend，群邀请：group
    user_id = str(data['user_id'])#发送请求的q号
    comment = data['comment']#验证信息
    flag  = data['flag'] #消息标识符
    # if user_id == '2996964572' or user_id == '2460182177':
    #     pass
    # else:
    #     return

    if request_type == 'friend':
        # 自动同意添加好友
        GroupEntity.set_friend_add_request(flag)
    # elif request_type == 'group' and (user_id == str(init.CONFIG.master) or user_id == '2460182177') and data['sub_type'] == 'invite':
    elif request_type == 'group' and user_id == str(init.CONFIG.master) and data['sub_type'] == 'invite':
        # 自动同意加群
        GroupEntity.set_group_add_request(flag,data['sub_type'])
    elif data['sub_type'] == 'add':
        #自动同意申请加群
        user_info = json.loads(GroupEntity.get_stranger_info(user_id))['data']
        if 15 < int(user_info['level']):
            GroupEntity.set_group_add_request(flag,data['sub_type'])