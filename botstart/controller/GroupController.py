from gocqhttpbot.botstart.entity import GroupEntity, CQcode, xmlEntity
from gocqhttpbot.botstart.impl import wfImpl, skyImpl, guildImpl, animeImpl, hireImpl
import json, re, os, sys,random

# 发送群消息
from gocqhttpbot.botstart.util import memeImgGenerate, SignUtil,permissions,init

def groupController(data):
    # print('进入群消息处理'+data)
    data = json.loads(data)
    post_type = data['post_type']  # 消息类型
    if post_type == 'notice':
        return
    self_id = str(data['self_id'])  # 框架qq号
    group_id = data['group_id']  # 群号
    raw_message = data['raw_message']  # 原始消息内容
    message = data['message']  # 消息内容
    user_id = str(data['user_id'])  # 触发用户id
    at_id = f'[CQ:at,qq={user_id}]'
    print(f'收到用户{user_id}  的消息：{message}')
    # 二次元老婆对话
    anime = animeImpl.anime(message)
    if anime:
        GroupEntity.send_group_msg(group_id, anime)

    role = data['sender']['role']  # 获取权限 owner 或 admin 或 member

    # 指令输出
    for i in pass_list('默认指令'):
        if message == i['instruction']:
            GroupEntity.send_group_msg(group_id, at_id + i['content'])

    # ————————————————————————————————————种萝卜签到功能，需授权----------------
    if permissions.get_auth(group_id):
        if message == '签到':
            GroupEntity.send_group_msg(group_id, at_id + SignUtil.addUser(str(group_id), user_id))
        elif message == '查询' or message == '我的萝卜':
            GroupEntity.send_group_msg(group_id, at_id + SignUtil.user_ById(str(group_id), user_id))
        elif message == '排行榜' or message == '萝卜榜':
            GroupEntity.send_group_msg(group_id, at_id + SignUtil.queryAll_json(str(group_id)))
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
    elif message[:2] == '授权':
        GroupEntity.send_group_msg(group_id, at_id + permissions.auth(group_id, message[2:]))


    if message == '语音权限':
        GroupEntity.send_group_msg(group_id, GroupEntity.can_send_record())
     #-----授权功能-------------------------------------------------------
    elif message == '获取授权码' and user_id == str(init.CONFIG.master):
        GroupEntity.send_group_msg(group_id, at_id + permissions.get_auth_code())
    elif message == '取消授权' and user_id == str(init.CONFIG.master):
        GroupEntity.send_group_msg(group_id,permissions.delAuth(group_id))
    elif any(str == message for str in ['射爆', '抽奖','左轮枪游戏','开枪']) and not SignUtil.judge(str(group_id),user_id):
        # other_id = re.findall('[0-9]+',message)[0]
        # GroupEntity.set_group_ban(group_id,other_id,1)
        SignUtil.updataradish(str(group_id), -2, user_id, 0, 0, 0, )
        if not SignUtil.get_user_radish_number(str(group_id), user_id, 2):
            return GroupEntity.send_group_msg(group_id,'你已经没有足够的萝卜来玩游戏了')
        if random.randint(0, 2) == 1:
            if GroupEntity.set_group_ban(group_id,user_id,random.randint(3,10)):
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
    elif message[:2].lower() == 'rm' or message[:2].lower() == 'zk':
        message = message[2:]
        GroupEntity.send_group_msg(group_id, at_id + wfImpl.wfrm(message))
    elif message[:2] == '攻略':
        GroupEntity.send_group_msg(group_id, at_id + wfImpl.ordis(message[2:]))
    elif message == '地球时间':
        GroupEntity.send_group_msg(group_id, at_id + wfImpl.earthCycle())
    elif message == '平原时间':
        try:
            GroupEntity.send_group_msg(group_id, at_id + wfImpl.dayTime())
        except:
            GroupEntity.send_group_msg(group_id, at_id + '正在进行昼夜更替，稍后查询哦')
    elif message == '平原':
        try:
            GroupEntity.send_group_msg(group_id,
                                       at_id + f'夜灵平原{wfImpl.dayTime()}  \n\n金星山谷{wfImpl.jxwd()}\n\n火卫二\n{wfImpl.hw2()}')
        except:
            GroupEntity.send_group_msg(group_id, at_id + '正在进行昼夜更替，稍后查询哦')
    elif message == '仲裁' or message == '仲裁任务':
        GroupEntity.send_group_msg(group_id, at_id + wfImpl.arbitration())
    elif message[:4].lower() == 'wiki':
        GroupEntity.send_group_msg(group_id, at_id + wfImpl.wiki(message[4:]))

    # elif msg == '二次元':
    #     botutils.groupmsg(loginqq, group, botImpl.二次元(loginqq, group))
    elif message[:2] == '遗物':
        # GroupEntity.send_group_msg(group_id, at_id + wfImpl.search_relics(message[2:],True))
        GroupEntity.send_group_forward_msg(group_id, wfImpl.search_relics(message[2:], True))
    elif '突击' in message and len(message) <= 5:
        if message == '突击':
            GroupEntity.send_group_msg(group_id, at_id + wfImpl.sortie(0))
        elif message == '国服突击':
            GroupEntity.send_group_msg(group_id, at_id + wfImpl.sortie(1))
        elif message == '国际服突击':
            GroupEntity.send_group_msg(group_id, at_id + wfImpl.sortie(2))

    elif message == '金星温度' or message == '山谷' or message == '金星':
        try:
            GroupEntity.send_group_msg(group_id, at_id + wfImpl.jxwd())
        except:
            GroupEntity.send_group_msg(group_id, at_id + '金星的温度现在不稳定，请稍后查询哦')
    elif message == '火卫二' or message == 'hw2':
        try:
            GroupEntity.send_group_msg(group_id, at_id + wfImpl.hw2())
        except:
            GroupEntity.send_group_msg(group_id, at_id + '当前查询出现了一点小状况，请联系作者修复')
    # elif message == '菜单' or message == '功能':
    #     if guildImpl.get_group_info(group_id, '光遇') or guildImpl.get_group_info(group_id, 'sky'):
    #         GroupEntity.send_group_msg(group_id, at_id + CQcode.images('images\\光遇\\菜单.JPG'))
    #     else:
    #         GroupEntity.send_group_msg(group_id, at_id + wfImpl.warframe())
    elif ('菜单' in message or  '功能' in message) and len(message) < 6:
        if message == '光遇菜单' or message == '光遇功能':
            GroupEntity.send_group_msg(group_id, at_id + CQcode.images('images\\光遇\\菜单.JPG'))
        elif message == '战甲菜单' or message == '战甲功能':
            GroupEntity.send_group_msg(group_id, at_id + wfImpl.warframe())
        else:
            GroupEntity.send_group_msg(group_id,at_id + wfImpl.caidan())
    elif "授权功能" == message :
        GroupEntity.send_group_msg(group_id,"授权以激活使用萝卜丁娱乐功能，如签到，雇佣，种萝卜")
    elif message == '奸商' or message == '虚空商人':
        try:
            GroupEntity.send_group_msg(group_id, at_id + wfImpl.voidTrader())
        except:
            GroupEntity.send_group_msg(group_id, at_id + '当前查询出现了一点小状况，请联系作者修复')
    # elif msg[:2] == '翻译':
    #     botutils.groupmsg(loginqq, group, botImpl.botci(msg[2:]))

    # elif msg == '查询口令':
    #     botutils.groupmsg(loginqq, group, botImpl.queryAll_json())

    elif message == '火卫二赏金':
        GroupEntity.send_group_msg(group_id, at_id + wfImpl.allOutmsg('EntratiSyndicate'))
    elif message == '地球赏金':
        GroupEntity.send_group_msg(group_id, at_id + wfImpl.allOutmsg('Ostrons'))
    elif message == '金星赏金':
        GroupEntity.send_group_msg(group_id, at_id + wfImpl.allOutmsg('Solaris'))
    elif message == '达尔沃' or message == '折扣':
        GroupEntity.send_group_msg(group_id, at_id + wfImpl.dailyDeals())
    elif message == '地球赏金':
        GroupEntity.send_group_msg(group_id, at_id + wfImpl.allOutmsg('Ostrons'))
    elif message == '入侵':
        GroupEntity.send_group_msg(group_id, at_id + wfImpl.allOutmsg('invasions'))
    elif message == '活动':
        GroupEntity.send_group_msg(group_id, at_id + wfImpl.allOutmsg('events'))
    elif message == '中继站轮换' or message == '泰森':
        GroupEntity.send_group_msg(group_id, at_id + wfImpl.steelPath())
    elif any(str in message[:1] for str in ['打', '顶']) and len(message) < 5:
        GroupEntity.send_group_msg(group_id, at_id + memeImgGenerate.index(message))
    elif message[:2].lower() == 'wm':
        mod_rank = re.findall(f'[0-9]+',message)
        if len(mod_rank) == 0:
            mod_rank ='0'
        else:
            mod_rank = mod_rank[0]
        message = message[2:].replace(mod_rank,"").replace(" ","")
        # mod_rank = ''
        # if re.findall(f'[0-9]', message[2:]):
        #     mod_ranks = re.findall(f'[0-9]', message[2:].replace(" ", ""))
        #     for m in mod_ranks:
        #         mod_rank = mod_rank + m
        #     message = message[2:].replace(" ", "").replace(mod_rank, "")
        # else:
        #     mod_rank = '0'
        #     message = message[2:].replace(" ", "")
        GroupEntity.send_group_msg(group_id, at_id + wfImpl.wfwm(message, mod_rank))
    elif '复刻' == message or '复刻先祖' == message:
        GroupEntity.send_group_msg(group_id, at_id + skyImpl.task('P1预估兑换树'))
    elif '每日' == message or '每日任务' == message:
        GroupEntity.send_group_msg(group_id, at_id + skyImpl.task('每日任务'))
    elif message == '更新缓存' and user_id == str(init.CONFIG.master):
        GroupEntity.send_group_msg(group_id, at_id + skyImpl.shoudong())
    elif '兑换图' in message:
        GroupEntity.send_group_msg(group_id, at_id + skyImpl.figure(message.replace('兑换图', '')))
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


# 获取指令内容
def pass_list(path):
    botpath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\频道数据\\指令\\{path}.json'
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
