
from gocqhttpbot.botstart.entity import GroupEntity, CQcode
from gocqhttpbot.botstart.impl import wfImpl, skyImpl, guildImpl, animeImpl,RadishImpl,yuleImpl
import json, re,random
from gocqhttpbot import PATH
# 发送群消息
from gocqhttpbot.botstart.util import SignUtil,permissions,init
from gocqhttpbot import log
from gocqhttpbot.botstart.dao import GroupHanderDao

def groupController(data):
    # print('进入群消息处理'+data)
    data = json.loads(data)
    post_type = data['post_type']  # 消息类型
    if post_type == 'notice':
        return
    # 种萝卜
    RadishImpl.run(**data)
    # 光遇
    skyImpl.run(**data)
    # 二次元
    RadishImpl.erciyuan(**data)
    # 星际战甲
    wfImpl.run(**data)
    self_id = str(data['self_id'])  # 框架qq号
    group_id = data['group_id']  # 群号
    raw_message = data['raw_message']  # 原始消息内容
    message = data['message'] # 消息内容
    user_id = str(data['user_id'])  # 触发用户id
    at_id = f'[CQ:at,qq={user_id}]'
    nickname = data['sender']['nickname']
    log.info(f'收到 来自群内用户{nickname}  说  { message if len(message)<20 else message[:20] + "..."}')

    if message == "开启风控" and user_id == str(init.CONFIG.master):
        init.CONFIG.fengkong = True
    elif message == "关闭风控" and user_id == str(init.CONFIG.master):
        init.CONFIG.fengkong = False


    # 指令输出
    for i in pass_list('默认指令'):
        if message == i['instruction']:
            GroupEntity.send_group_msg(group_id, at_id + i['content'])

    if message[:2] == '授权' and len(message) > 10 and not message == "授权功能":
        GroupEntity.send_group_msg(group_id, at_id + permissions.auth(group_id, message[2:]))
    elif "授权功能" == message:
        GroupEntity.send_group_msg(group_id, "因账号被频繁冻结，现改为收费使用。")
    elif message[:5] == '获取授权码' and user_id == str(init.CONFIG.master):
        GroupEntity.send_group_msg(group_id, at_id + permissions.get_auth_code(int(message[5:])))
    elif message == '取消授权' and user_id == str(init.CONFIG.master):
        GroupEntity.send_group_msg(group_id,permissions.delAuth(group_id))
    elif ('菜单' in message or  '功能' in message) and len(message) < 5 and not message == "授权功能":
        if message == '光遇菜单' or message == '光遇功能':
            GroupEntity.send_group_msg(group_id, at_id + CQcode.images('images\\光遇\\菜单.JPG'))
        elif message == '战甲菜单' or message == '战甲功能':
            GroupEntity.send_group_msg(group_id, at_id + wfImpl.warframe(),fengkong=init.CONFIG.fengkong)
        else:
            GroupEntity.send_group_msg(group_id,at_id + wfImpl.caidan())
    elif message == "到期时间" or message == "群授权信息":
        GroupEntity.send_group_msg(group_id,permissions.get_expiration_time(group_id))

    # 未授权拦截
    if permissions.get_auth(group_id) == False:
        return ""


    # 权限控制
    role = data['sender']['role']  # 获取权限 owner 或 admin 或 member

    if message == '/type' or message == "/状态":
        GroupEntity.send_group_msg(group_id,GroupHanderDao.getAll(str(group_id)))
    elif message[:3] == '/开启' and (role == 'owner' or role == 'admin' or user_id == str(init.CONFIG.master)):
        GroupEntity.send_group_msg(group_id,GroupHanderDao.setType(str(group_id),message.replace(" ","")[3:],True))
    elif message[:3] == '/关闭' and (role == 'owner' or role == 'admin' or user_id == str(init.CONFIG.master)):
        GroupEntity.send_group_msg(group_id,GroupHanderDao.setType(str(group_id),message.replace(" ","")[3:],False))



    if message == '食莞' or message == "投喂":
        GroupEntity.send_group_msg(group_id,"好感度 +10 ...")
        # GroupEntity.send_group_msg(group_id, GroupEntity.can_send_record())
        # GroupEntity.send_group_msg(group_id,animeImpl.crazy())
     #-----授权功能-------------------------------------------------------

    elif any(str == message for str in ['射爆', '抽奖','左轮枪游戏','开枪']) and not SignUtil.judge(str(group_id),user_id):
        # other_id = re.findall('[0-9]+',message)[0]
        # GroupEntity.set_group_ban(group_id,other_id,1)
        SignUtil.updataradish(str(group_id), -2, user_id, 0, 0, 0, )
        if not SignUtil.get_user_radish_number(str(group_id), user_id, 2):
            return GroupEntity.send_group_msg(group_id,'你已经没有足够的萝卜来玩游戏了')
        if random.randint(0, 2) == 1:
            if GroupEntity.set_group_ban(group_id,user_id,random.randint(5,10)):
                add = random.randint(10,20)
                GroupEntity.send_group_msg(group_id, f'成功射爆！！获得{str(add)}根萝卜！')
                SignUtil.updataradish(str(group_id),add,user_id,0,0,0,)
            else:
                GroupEntity.send_group_msg(group_id, '射爆了但萝卜丁没有足够的权限')

        else:
            GroupEntity.send_group_msg(group_id,'幸运的活了下来~')
    elif message[:3] == '转语音':
        GroupEntity.send_group_msg(group_id, CQcode.tts(message[3:]))
    elif str(init.CONFIG.botqq) in message and (init.CONFIG.botName in message or '叫一个' in message or '给爷叫一个' in message):
        cq = animeImpl.dinggong()
        GroupEntity.send_group_msg(group_id, cq['cq'])
        GroupEntity.send_group_msg(group_id, cq['name'])

    elif message[:2] == '发单':
        if role == 'owner' or role == 'admin' or user_id == str(init.CONFIG.master):
            if GroupEntity.get_group_at_all_remain(group_id):
                GroupEntity.send_group_msg(group_id, f'[CQ:at,qq=all]\n' + message)
            else:
                GroupEntity.send_group_msg(group_id, at_id + f'该频道的艾特全体次数已用完~')
        else:
            GroupEntity.send_group_msg(group_id, '等你戴上绿帽子我会帮你发的(摆烂)')
    elif message[:4] == '新增口令' and user_id == str(init.CONFIG.master):
        GroupEntity.send_group_msg(group_id, at_id + guildImpl.password(message, '默认指令'))
    elif message[:4] == '删除口令' and user_id == str(init.CONFIG.master):
        GroupEntity.send_group_msg(group_id, at_id + guildImpl.delete_json(message[4:], '默认指令'))
    elif message == '查询口令':
        GroupEntity.send_group_msg(group_id, at_id + guildImpl.queryAll_json('默认指令'))
    elif message[:4] =="羊了个羊":
        try:
            msgList=re.findall(f'[0-9]+', message)
            id = msgList[0]
            n = msgList[1]
            time = msgList[2]
            if int(n) > 10 :
                GroupEntity.send_group_msg(group_id, at_id + "每次次数不能大于10")
                return ""
            GroupEntity.send_group_msg(group_id,at_id+yuleImpl.yang(id,n,time))
        except:
            GroupEntity.send_group_msg(group_id, at_id + "\n输入有误，格式：羊了个羊-ID-次数-时间\n示例：羊了个羊-1234-10-6\n\n也有可能是游戏蹦了")

# 获取指令内容
def pass_list(path):
    botpath = PATH + f'\\频道数据\\指令\\{path}.json'
    try:
        with open(botpath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
    except:
        word = [{
            'instruction': '口令',
            'content': '新增的功能哦~'
        }]
        with open(botpath, 'w', encoding='utf-8') as f2:
            json.dump(word, f2, ensure_ascii=False)
            f2.close()
    return item_list
