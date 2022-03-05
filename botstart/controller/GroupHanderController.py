# 处理加群，邀请等信息
import json
from gocqhttpbot.botstart.entity import GroupEntity

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
    elif request_type == 'group' or (user_id == '2996964572' or user_id == '2460182177'):
        # 自动同意加群
        GroupEntity.set_group_add_request(flag,data['sub_type'])