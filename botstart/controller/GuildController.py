from gocqhttpbot.botstart.entity import GuildEntity, CQcode,xmlEntity
from gocqhttpbot.botstart.impl import yuleImpl, wfImpl,hireImpl,guildImpl,blind_box,skyImpl
from gocqhttpbot.botstart.util import SignUtil, wordUtil,memeImgGenerate,permissions
import json, re,time,os,sys


def guildController(data):
    data = json.loads(data)
    message = data['message']  # 消息
    guild_id = data['guild_id']  # 频道id
    channel_id = data['channel_id']  # 子频道id
    user_id = str(data['user_id'])  # 触发用户id
    at_user = f'[CQ:at,qq={user_id}] '
    nickname = data['sender']['nickname']

    pass_path = '默认指令'
    # 获取指令路径并输出
    for i in pass_list('配置内容'):
        if guild_id == i['instruction']:
            pass_path = i['content']
            break

    if (message == '屏蔽' or message == '关闭') and (user_id == '144115218676755577' or user_id == str(
            json.loads(GuildEntity.get_guild_meta_by_guest(guild_id))['data']['owner_id'])):

        GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                           at_user + wordUtil.addPermiss(guild_id, channel_id))
    elif (message == '解除屏蔽' or message == '开启') and (user_id == '144115218676755577' or user_id == str(
            json.loads(GuildEntity.get_guild_meta_by_guest(guild_id))['data']['owner_id'])):
        GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                           at_user + wordUtil.delete_Permiss(guild_id, channel_id))
    elif message[:4] == '新增口令' and (user_id == '144115218676755577' or permissions.getPermissions(user_id)):

        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user +guildImpl.password(message,pass_path))
    elif message[:4] == '删除口令' and (user_id == '144115218676755577' or permissions.getPermissions(user_id)):
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user +guildImpl.delete_json(message[4:],pass_path))
    elif message == '查询口令':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + guildImpl.queryAll_json(pass_path))
    elif message[:4] == '指令隔离'and (user_id == '144115218676755577'):
        if message[4:] == '':
            GuildEntity.send_guild_channel_msg(guild_id,channel_id,at_user+'隔离内容为空')
        else:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user +guildImpl.password(f'新增口令{guild_id}内容{message[4:]}','配置内容'))

    # 这是屏蔽功能
    if wordUtil.queryAllPermiss(guild_id, channel_id):
        return ''


    for j in pass_list(pass_path):
        if message == j['instruction']:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + j['content'])

    if message == '测试':

        # GuildEntity.send_guild_channel_msg(guild_id,channel_id,f'[CQ:json,data={xmlEntity.getEmbed()}]')
        pass

    elif message[:3] == '转语音':
        # guildentity.send_guild_channel_msg(guild_id,channel_id,CQcode.tts(message[3:]))
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, '仅支持qq群')
    elif message == '抽签' or message=='抛杯' or message == '解签':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + yuleImpl.chouqian(message, user_id))
    elif message == '一言' or message == '抽纸条':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + yuleImpl.yiyan())
    # elif message == '段子' or message == '来个段子':
    #     guildentity.send_guild_channel_msg(guild_id, channel_id, at_user +yuleimpl.duanzi())
    elif message[:3] == '查备案':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                           at_user + yuleImpl.icp(message[3:]))
    elif message[:4] == 'ping':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                           at_user + yuleImpl.ping(message[4:]))
    # elif message == '污段子':
    #     guildentity.send_guild_channel_msg(guild_id, channel_id,at_user + yuleimpl.wuduanzi())
    elif message[:2].lower() == 'rm' or message[:2].lower() == 'zk':
        message = message[2:]
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.wfrm(message))
    elif message[:2] == '攻略':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.ordis(message[2:]))
    elif message == '地球时间':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.earthCycle())
    elif message == '平原时间':
        try:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.dayTime())
        except:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '正在进行昼夜更替，稍后查询哦')
    elif message == '仲裁' or message == '仲裁任务':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.arbitration())
    elif message[:4].lower() == 'wiki':
        message = message[4:].replace(" ", "")
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.wiki(message))

        # elif msg == '二次元':
        #     botutils.groupmsg(loginqq, group, botImpl.二次元(loginqq, group))
    elif message[:2] == '遗物':
        message = message[2:].replace(" ","")
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.search_relics(message))
    elif '突击' in message and len(message) <= 5:
        if message == '突击':
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.sortie(0))
        elif message == '国服突击':
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.sortie(1))
        elif message == '国际服突击':
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.sortie(2))

    elif message[:4] == '金星温度':
        try:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.jxwd())
        except:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '金星的温度现在不稳定，请稍后查询哦')
    elif message == '火卫二' or message == 'hw2':
        try:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.hw2())
        except:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '当前查询出现了一点小状况，请联系作者修复')
    elif message == '菜单':
        if guildImpl.get_guil_name(guild_id,'战甲') or guildImpl.get_guil_name(guild_id,'warframe'):
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.caidan())
        else:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + CQcode.images('images/菜单.jpg'))
    elif message == '奸商' or message == '虚空商人':
        try:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.voidTrader())
        except:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '当前查询出现了一点小状况，请联系作者修复')
    elif message == '火卫二赏金':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.allOutmsg('EntratiSyndicate'))
    elif message == '地球赏金':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.allOutmsg('Ostrons'))
    elif message == '金星赏金':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.allOutmsg('Solaris'))
    elif message == '达尔沃' or message == '折扣':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.dailyDeals())
    elif message == '地球赏金':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.allOutmsg('Ostrons'))
    elif message == '入侵':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.allOutmsg('invasions'))
    elif message == '活动':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.allOutmsg('events'))
    elif message[:2].lower() == 'wm':
        mod_rank = ''
        if re.findall(f'[0-9]', message[2:]):
            mod_ranks = re.findall(f'[0-9]', message[2:].replace(" ", ""))
            for m in mod_ranks:
                mod_rank = mod_rank + m
            message = message[2:].replace(" ", "").replace(mod_rank, "")
        else:
            mod_rank = '0'
            message = message[2:].replace(" ", "")
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + wfImpl.wfwm(message, mod_rank))
    # elif message=='功能' or message[:4] == '修改功能':
    #     menuImpl.sign(guild_id,channel_id,user_id,at_user,message)

    elif message == '获取' or message == '获取机器人':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + f'如有需要请联系Qq2996964572')
    elif '盲盒' in message:
        blind_box.box(json.dumps(data))
    elif message[:4] == '全服狂欢' and user_id == '144115218676755577':
        blind_box.hilarity(guild_id, channel_id, message)
    elif '管理' in message:
        permissions.permissions(json.dumps(data))
    elif '五福功能' == message:
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + f'五福功能已关闭。如有需要请联系Qq2996964572')
    # elif '五福' in message:
    #     gatherImpl.gather(json.dumps(data))


    # 光遇功能
    elif '复刻' == message or '复刻先祖' == message:
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + skyImpl.task('本周复刻'))
    elif '每日' == message or '每日任务' == message:
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + skyImpl.task('每日任务'))
    elif message == '更新缓存' and (user_id == '144115218676755577' or permissions.getPermissions(user_id)):
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + skyImpl.shoudong())
    elif '兑换图' in message:
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + skyImpl.figure(message.replace('兑换图', '')))

    # 萝卜丁功能
    if guildImpl.get_guil_name(guild_id, '战甲') or guildImpl.get_guil_name(guild_id, 'warframe'):
        return ''
    elif message == '签到':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                           at_user + SignUtil.addUser(guild_id, channel_id, user_id, nickname))
    elif message == '查询' or message == '我的萝卜':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                           at_user + SignUtil.user_ById(guild_id, user_id))
    elif message[:2] == '查看':
        try:
            at_qq = message[message.index('qq='):message.index(']')].replace('qq=', '')

            GuildEntity.send_guild_channel_msg(guild_id, channel_id, SignUtil.user_ById(guild_id, at_qq))
        except Exception as e:

            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '你先艾特个人')
    elif message == '排行榜' or message == '萝卜榜':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                           at_user + SignUtil.queryAll_json(guild_id))
    elif message == '上个月排行榜' or message == '上个月萝卜榜':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                           at_user + SignUtil.queryAll_json(guild_id, 1))
    elif '萝卜' in message:
        SignUtil.sig_index(json.dumps(data))

    elif message[:2] == '打劫' or message[:2] == '抢劫':

        try:
            # at_qq = re.findall(f'\\[CQ:at,qq=(.*?)] ', message[2:])
            at_qq = message[message.index('qq='):message.index(']')].replace('qq=', '')
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, SignUtil.rob(guild_id, user_id, at_qq))
        except:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '你先艾特个人')
    elif message[:2] == '赠送':
        try:
            numbers = ''
            number = re.findall(f'[0-9]', message[message.index(']'):])
            for i in number:
                numbers = numbers + str(i)
            at_qq = message[message.index('qq='):message.index(']')].replace('qq=', '')
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, SignUtil.give(guild_id, user_id, at_qq, int(numbers)))
        except:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '没写数量？')
    elif '雇佣' in message:
        hireImpl.hire(json.dumps(data))
    elif message == '赞助' or message == '支持' or message == '赞助作者' or message == '支持作者':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '赞助：https://afdian.net/@cat991')
    elif any(str in message[:1] for str in ['打', '顶']):
        memeImgGenerate.index(guild_id, channel_id, message, at_user)
    elif message == '功能':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + CQcode.images('images/菜单.jpg'))

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
            'content': '可自定的指令集'
        }]
        with open(botpath, 'w', encoding='utf-8') as f2:
            json.dump(word, f2, ensure_ascii=False)
            f2.close()
    return item_list