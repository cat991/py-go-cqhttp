from gocqhttpbot.botstart.dao.GroupHanderDao import switch
from gocqhttpbot.botstart.entity import GroupEntity
from gocqhttpbot.botstart.impl import hireImpl, animeImpl
import json, re,random
# 发送群消息
from gocqhttpbot.botstart.util import  SignUtil,init
@switch("种萝卜")
def run(data):
    print("进入萝卜")
    # data = json.loads(data)
    post_type = data['post_type']  # 消息类型
    if post_type == 'notice':
        return
    self_id = str(data['self_id'])  # 框架qq号
    group_id = data['group_id']  # 群号
    raw_message = data['raw_message']  # 原始消息内容
    message = data['message']  # 消息内容
    user_id = str(data['user_id'])  # 触发用户id
    at_id = f'[CQ:at,qq={user_id}]'
    nickname = data['sender']['nickname']
    if message == '签到':
        GroupEntity.send_group_msg(group_id, at_id + SignUtil.addUser(str(group_id), user_id))
    elif message == '查询' or message == '我的萝卜':
        GroupEntity.send_group_msg(group_id, at_id + SignUtil.user_ById(str(group_id), user_id))
    elif message == '排行榜' or message == '萝卜榜':
        GroupEntity.send_group_msg(group_id, at_id + SignUtil.queryAll_json(str(group_id)),fengkong=init.CONFIG.fengkong)
    elif '萝卜丁抽奖' == message[:5] :
        try:
            mod_rank = re.findall(f'[0-9]+', message)[0]
            GroupEntity.send_group_msg(group_id,f'中奖数字：{str(random.randint(1,int(mod_rank)))}')
        except Exception:
            pass
            # GroupEntity.send_group_msg(group_id,"可能出现了一点小bug'？")
    elif '萝卜' in message:
        SignUtil.sig_index_group(json.dumps(data))
    elif message[:2] == '打劫' or message[:2] == '抢劫':

        try:
            at_qq = re.findall('[0-9]+', message)[0]
            GroupEntity.send_group_msg(group_id, SignUtil.rob(str(group_id), user_id, at_qq))
            return
        except:
            GroupEntity.send_group_msg(group_id, at_id  + '你先艾特个人')
    elif message[:2] == '赠送':
        try:
            numbers = re.findall('[0-9]+', message)[1]
            at_qq = re.findall('[0-9]+', message)[0]
            GroupEntity.send_group_msg(group_id,
                                               SignUtil.give(str(group_id), user_id, at_qq, int(numbers)))
        except:
            GroupEntity.send_group_msg(group_id, at_id + '没写数量？')
    elif '雇佣' in message:
        hireImpl.hire_group(json.dumps(data))
    return None
@switch("二次元")
def erciyuan(data):
    # 二次元老婆对话
    group_id = data['group_id']  # 群号
    message = data['message']  # 消息内容
    anime = animeImpl.anime(message)
    if anime:
        GroupEntity.send_group_msg(group_id, anime,False)