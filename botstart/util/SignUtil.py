import os, json, sys, random, datetime, re
from time import localtime, strftime, time
from gocqhttpbot.botstart.entity import CQcode, GuildEntity,GroupEntity
from gocqhttpbot.botstart.util import permissions,init
from gocqhttpbot import PATH
# 添加用户
word = {}
texterre = ['🍒打劫失败：你被单杀并且被嘲讽失去了萝卜🥕',
            '🍒打劫失败：遇到了警察被抓走剥玉米失去了萝卜🥕',
            '🍒打劫失败：你在路上被认出通缉犯失去萝卜🥕',
            '🍒打劫失败：你遇到了一条恶犬住院失去了萝卜🥕',
            '🍒打劫失败：你踩到了狗屎摔了一跤住院失去萝卜🥕',
            '🍒打劫失败：你没有追上并被嘲讽小短腿失去萝卜🥕',
            '🍒打劫失败：你被单杀并且被嘲讽失去了萝卜🥕',
            '🍒打劫失败：遇到了警察被抓走剥玉米失去了萝卜🥕',
            '🍒打劫失败：你在路上被认出通缉犯失去萝卜🥕',
            '🍒打劫失败：你遇到了一条恶犬住院失去了萝卜🥕',
            '🍒打劫失败：你踩到了狗屎摔了一跤住院失去萝卜🥕',
            '🍒打劫失败：你没有追上并被嘲讽小短腿失去萝卜🥕', ]
textsuccess = ['🍒打劫成功：你顺利得手并且亲了对方一口获得萝卜🥕',
               '🍒打劫成功：获得萝卜🥕',
               '🍒打劫成功：路上遇到了同伙打劫翻倍获得萝卜🥕 (bus']


# 签到功能
def addUser(guil_id, user_id):
    ran = random.randint(init.CONFIG.min, init.CONFIG.max)
    day = strftime("%d日", localtime())
    word = {
        'user_id': user_id,
        'radish': ran,
        'day': day,
        'rob': init.CONFIG.rob,
        'unrob': init.CONFIG.unrob,
        'pullradish': 0,
        'give': init.CONFIG.give,
        'planting': None  # 种植萝卜
    }
    try:
        obj = write_json(guil_id, word)
    except:
        user_ById(guil_id, user_id)
        obj = write_json(guil_id, word)
        return obj
    return obj


# 用户校验接口
def judge(guild_id, user_id):
    ym = strftime("%Y年%m月", localtime())
    botpath = PATH + f'\\频道数据\\{ym + guild_id}.json'
    try:
        with open(botpath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
            for i in item_list:
                if user_id == i['user_id']:
                    return False
    except:
        return True
    return True


# 判断用户萝卜数量是否这么多
def get_user_radish_number(guild_id, user_id, number):
    ym = strftime("%Y年%m月", localtime())
    botpath = PATH + f'\\频道数据\\{ym + guild_id}.json'
    with open(botpath, 'r', encoding='utf-8')as f:
        flist = json.loads(f.read())
        for i in flist:
            if i['user_id'] == user_id:
                if i['radish'] >= number:
                    return True
        return False


# 获取用户信息，查询
def user_ById(guil_id, user_id):
    global planting
    ym = strftime("%Y年%m月", localtime())
    day = strftime("%d日", localtime())
    botpath = PATH + f'\\频道数据\\{ym + guil_id}.json'
    try:
        with open(botpath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
    except:
        word = [{
            'user_id': str(user_id),  # 用户id
            'radish': random.randint(init.CONFIG.min, init.CONFIG.max),  # 萝卜数量
            'day': day,  # 日期
            'rob': init.CONFIG.rob,  # 打劫次数
            'unrob': init.CONFIG.unrob,  # 被打劫次数
            'pullradish': 0,  # 拔萝卜 0和1
            'give': init.CONFIG.give,  # 可赠送萝卜数量
            'planting': None  # 种植萝卜
        }]
        with open(botpath, 'w', encoding='utf-8') as f2:
            json.dump(word, f2, ensure_ascii=False)
            f2.close()
        return '数据库中没有您的数据，请先签到'
    planting = f'🍒种植:无种植物'

    for i in item_list:
        if user_id == i['user_id']:
            if i['planting'] is not None:
                if float(i['planting']) <= time():
                    planting = f'🍒种植:您的萝卜已成熟 {i["planting"] <= time()}'
                else:
                    shijian = strftime("%M:%S", localtime(int(i["planting"]) - int(time())))
                    # print(localtime(int(i["planting"]) - int(time())))
                    planting = f'🍒种植:{shijian}后可收获'
            return f'\n兔宝您的菜篮子🥘：\n🍒萝卜数量：萝卜🥕·{i["radish"]}\n' \
                   f'🍒打劫次数：{i["rob"]}\n🍒被打劫次数：{i["unrob"]}\n' \
                   f'🍒赠送数量：今日可赠送{i["give"]}根萝卜🥕\n' \
                   f'{planting}\n'


    return '数据库中没有您的数据，请先签到'


# 排行榜查询
def queryAll_json(guil_id, m=0):
    ym = ''
    if m == 0:
        ym = strftime("%Y年%m月", localtime())
    else:
        ym = (datetime.datetime.now() + datetime.timedelta(days=-30)).strftime("%Y年%m月")
    day = strftime("%d日", localtime())
    try:
        botpath = PATH + f'\\频道数据\\{ym + guil_id}.json'
        content = '\n排行榜如下：\n'
        cont = 1
        with open(botpath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
        item_list = sorted(item_list, key=lambda x: int(x["radish"]), reverse=True)
        for i in item_list:
            if cont <= 5:
                content = content + f'🍒第{str(cont)}名 ：[CQ:at,qq={i["user_id"]}]\n🥘菜篮子：萝卜🥕·{str(i["radish"])}🥕\n\n'
                cont = cont + 1
    except:
        return '没有上个月的数据'
    return content


# 删除json节点
def delete_json(guil_id, at_id):
    ym = strftime("%Y年%m月", localtime())
    day = strftime("%d日", localtime())
    botpath = PATH + f'\\频道数据\\{ym + guil_id}.json'
    cont = 0
    with open(botpath, 'r', encoding='utf-8') as f:
        item_list = json.loads(f.read())
        f.close()
        for i in item_list:
            if i['user_id'] == at_id:
                del item_list[cont]
                with open(botpath, 'w', encoding='utf-8') as f2:
                    json.dump(item_list, f2, ensure_ascii=False)
                    f2.close()
                return '删除成功'
            cont += 1
    return '删除失败'


# 输出和写入json数据到文件
def write_json(guild_id, obj):
    # 首先读取已有的json文件中的内容
    ym = strftime("%Y年%m月", localtime())
    day = strftime("%d日", localtime())
    botpath = PATH + f'\\频道数据\\{ym + guild_id}.json'
    cont = 0
    with open(botpath, 'r', encoding='utf-8') as f:
        item_list = json.loads(f.read())
        f.close()
        for i in item_list:
            if i['user_id'] == obj['user_id']:
                if i['day'] == obj['day']:
                    return '🍒兔宝·今日签过到了哦！吃根糖葫芦明天再来吧🍡'
                item_list[cont]['day'] = obj['day']
                item_list[cont]['radish'] += int(obj['radish'])
                item_list[cont]['rob'] = init.CONFIG.rob
                item_list[cont]['unrob'] = init.CONFIG.unrob
                item_list[cont]['give'] = init.CONFIG.give
                with open(botpath, 'w', encoding='utf-8') as f2:
                    json.dump(item_list, f2, ensure_ascii=False)
                    f2.close()
                    # 五福功能
                # gatherImpl.getGatHer(guild_id, channel_id, i['user_id'])
                return f'签到成功,获得{obj["radish"]}萝卜🥕{CQcode.images("images/签到成功.png")}'
            cont += 1
        else:
            # #将新传入的dict对象追加至list中
            item_list.append(obj)
            # #将追加的内容与原有内容写回（覆盖）原文件
            with open(botpath, 'w', encoding='utf-8') as f2:
                json.dump(item_list, f2, ensure_ascii=False)
                f2.close()
            # 五福功能
            # gatherImpl.getGatHer(guild_id, channel_id, i['user_id'])
            return f'🍒兔宝·恭喜首次签到！您获得了{obj["radish"]}根萝卜🥕 【兔宝明天记得来签到哦[CQ:face,id=319]】{CQcode.images("images/首次签到.png")}'


# 打劫
def rob(guil_id, user_id, at_id):
    radish = random.randint(5, 8)
    ran = random.randint(0, 2)
    ym = strftime("%Y年%m月", localtime())
    beneath = PATH + f'\\频道数据\\{ym + guil_id}.json'
    cont = 0
    user_id_text = ''
    at_id_text = ''
    try:
        with open(beneath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
    except:
        return f' 数据库中可能没有你的信息？请签到后再试试'
    for i in item_list:
        if i['user_id'] == str(user_id):
            user_id_text = item_list[cont]
        if i['user_id'] == str(at_id):
            at_id_text = item_list[cont]
        cont += 1
    if at_id_text == '' or user_id_text == '':
        return f'[CQ:at,qq={user_id}] 其中有一个人没签到无法打劫哦~'
    if at_id_text['unrob'] == 0:
        return f'[CQ:at,qq={user_id}] 🍒兔宝·您打劫的兔宝魅力太大已经打劫上限了哦！快去换另一个目标叭🍳'
    elif user_id_text['rob'] == 0:
        return f'[CQ:at,qq={user_id}]🍒兔宝·今天你自己打劫了很多次了哦！喝口茶休息一下叭🍵'
    elif ran == 0 or ran == 1:
        updataradish(guil_id, radish, user_id, -1, -1, 0, at_id)
        # updataradish(guil_id, -int(radish), at_id, 0, -1, 0)
        # return f'[CQ:at,qq={user_id}] 这个b要抢劫你 \n[CQ:at,qq={at_id}] 你被成功抢劫 {radish}根萝卜' \
        return f'[CQ:at,qq={user_id}] ' + textsuccess[random.randint(1, len(textsuccess) - 1)] + str(
            radish) + CQcode.images('images/打劫成功.png')
    else:
        er = random.randint(1, 2)
        updataradish(guil_id, -int(er), user_id, -1, 0, 0)
        return f'[CQ:at,qq={user_id}] ' + texterre[random.randint(1, len(texterre) - 1)] + str(er) + CQcode.images(
            'images/打劫失败.png')


# 拔萝卜
def pull(guil_id, user_id):
    shu = random.randint(2, 5)
    ym = strftime("%Y年%m月", localtime())
    botpath = PATH + f'\\频道数据\\{ym + guil_id}.json'

    try:
        with open(botpath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
    except:
        return f'数据库中可能没有你的信息？请签到后再试试'
    cont = 0
    for i in item_list:
        if user_id == i['user_id']:
            if i['planting'] is None:
                return '请先种植萝卜,发送:种萝卜'
            else:
                if float(i['planting']) >= time():
                    return f'您的萝卜还未成熟,请等待成熟后再来收获吧~'
                else:
                    item_list[cont]['planting'] = None
                    with open(botpath, 'w', encoding='utf-8') as f2:
                        json.dump(item_list, f2, ensure_ascii=False)
                        f2.close()
                    updataradish(guil_id, shu, user_id, 0, 0, 0)
                    return f'勤劳的小兔成功收获{shu}根萝卜{CQcode.images("images/收获满满.png")}'
        cont += 1
    return f'数据库中可能没有你的信息？请签到后再试试'


# 种萝卜
def seed(guil_id, user_id):
    if judge(guil_id, user_id):
        return '数据库中没有你的数据，请先签到，发送：签到'
    ym = strftime("%Y年%m月", localtime())
    botpath = PATH + f'\\频道数据\\{ym + guil_id}.json'
    try:
        with open(botpath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
    except:
        return f' 数据库中可能没有你的信息？请签到后再试试'
    cont = 0
    shijian = int(time()) + 60 * 15
    for i in item_list:
        if i['user_id'] == user_id:
            if i['planting'] is not None:
                return '请等待你的萝卜成熟收获后再进行种植哦~'
            item_list[cont]['planting'] = int(shijian)
            with open(botpath, 'w', encoding='utf-8') as f2:
                json.dump(item_list, f2, ensure_ascii=False)
                f2.close()
        cont += 1
    return f'种植成功，15分钟后回来收取{CQcode.images("images/种植成功.png")}'


# 修改打劫后的次数和萝卜数量
def updataradish(guil_id, radish, user_id, rob, unrob, give, atuser_id=""):
    ym = strftime("%Y年%m月", localtime())
    botpath = PATH + f'\\频道数据\\{ym + guil_id}.json'

    cont = 0
    with open(botpath, 'r', encoding='utf-8') as f:
        item_list = json.loads(f.read())
        f.close()
        for i in item_list:
            if i['user_id'] == user_id:
                item_list[cont]['rob'] += int(rob)
                item_list[cont]['radish'] += int(radish)
                item_list[cont]['give'] -= int(give)
                # item_list[cont]['rob'] = int(item_list[cont]['rob']) + int(rob)
                # item_list[cont]['unrob'] = int(item_list[cont]['unrob']) + int(unrob)
                # item_list[cont]['radish'] = int(item_list[cont]['radish']) + int(radish)
                # item_list[cont]['give'] = int(item_list[cont]['give']) - int(give)
            if atuser_id != "":
                if i['user_id'] == atuser_id:
                    item_list[cont]['unrob'] += int(unrob)
                    item_list[cont]['radish'] -= int(radish)
            cont += 1
        with open(botpath, 'w', encoding='utf-8') as f2:
            json.dump(item_list, f2, ensure_ascii=False)
            f2.close()


# 赠送萝卜
def give(guil_id, user_id, at_id, number):
    ym = strftime("%Y年%m月", localtime())
    beneath = PATH + f'\\频道数据\\{ym + guil_id}.json'
    cont = 0
    user_id_text = ''
    at_id_text = ''
    try:
        with open(beneath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
    except:
        return f' 数据库中可能没有你的信息？请签到后再试试'
    for i in item_list:
        if i['user_id'] == str(user_id):
            user_id_text = item_list[cont]
        if i['user_id'] == str(at_id):
            at_id_text = item_list[cont]
        cont += 1
    if at_id_text == '' or user_id_text == '':
        return f'[CQ:at,qq={user_id}] 其中有一个人没签到无法赠送萝卜哦~'

    if user_id_text['give'] >= int(number) > 0:
        updataradish(guil_id, -int(number), user_id, 0, 0, number, at_id)
        # updataradish(guil_id, number, at_id, 0, 0, 0)
        return f'[CQ:at,qq={at_id}]🍒兔宝·您的好友马不停蹄·跌跌撞撞的给您送了萝卜🥕*{str(number)}'
    elif user_id_text['radish'] < int(number):
        return f'[CQ:at,qq={user_id}]你自己都身无分文了'
    else:
        return f'[CQ:at,qq={user_id}]你已经不能送再多了'


def sig_index_guild(datas):
    datas = json.loads(datas)
    message = datas['message']  # 消息
    guild_id = datas['guild_id']  # 频道id
    channel_id = datas['channel_id']  # 子频道id
    user_id = str(datas['user_id'])  # 触发用户id
    at_user = f'[CQ:at,qq={user_id}] '
    if message == '种萝卜':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user +
                                           seed(guild_id, user_id))
    elif message == '拔萝卜':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user +
                                           pull(guild_id, user_id))
    elif message[:4] == '扣除萝卜' and (user_id == str(init.CONFIG.masterId) or permissions.getPermissions(user_id)):
        # at_qq = message[message.index('qq='):message.index(']')].replace('qq=', '')
        # numbers = ''
        # number = re.findall(f'[0-9]', message[message.index(']'):])
        # for i in number:
        #     numbers = numbers + str(i)

        at_qq = re.findall(f'[0-9]+', message)[0]
        numbers = re.findall(f'[0-9]+', message)[1]
        updataradish(guild_id, -int(numbers), at_qq, 0, 0, 0)
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user +
                                           f'成功扣除{numbers}根萝卜')
    elif message[:4] == '增加萝卜' and (user_id == str(init.CONFIG.masterId) or permissions.getPermissions(user_id)):
        # at_qq = message[message.index('qq='):message.index(']')].replace('qq=', '')
        at_qq = re.findall(f'[0-9]+', message)[0]
        # numbers = ''
        # number = re.findall(f'[0-9]', message[message.index(']'):])
        # for i in number:
        #     numbers = numbers + str(i)
        numbers = re.findall(f'[0-9]+', message)[1]
        updataradish(guild_id, int(numbers), at_qq, 0, 0, 0)
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user +
                                           f'成功添加{numbers}根萝卜')
def sig_index_group(datas):
    data = json.loads(datas)
    group_id = str(data['group_id'])  # 群号
    message = data['message']  # 消息内容
    user_id = str(data['user_id'])  # 触发用户id
    at_id = f'[CQ:at,qq={user_id}]'
    if message == '种萝卜':
        GroupEntity.send_group_msg(group_id,at_id+seed(group_id, user_id))
    elif message == '拔萝卜':
        GroupEntity.send_group_msg(group_id, at_id +
                                           pull(group_id, user_id))
    elif message[:4] == '扣除萝卜' and (user_id == str(init.CONFIG.masterId) or permissions.getPermissions(user_id)):
        # at_qq = message[message.index('qq='):message.index(']')].replace('qq=', '')
        # numbers = ''
        # number = re.findall(f'[0-9]', message[message.index(']'):])
        at_qq = re.findall(f'[0-9]+', message)[0]
        number = re.findall(f'[0-9]+', message)[1]
        # for i in number:
        #     numbers = numbers + str(i)
        updataradish(group_id, -int(number), at_qq, 0, 0, 0)
        GroupEntity.send_group_msg(group_id, at_id +
                                           f'成功扣除{number}根萝卜')
    elif message[:4] == '增加萝卜' and (user_id == str(init.CONFIG.master) or permissions.getPermissions(user_id)):
        # at_qq = message[message.index('qq='):message.index(']')].replace('qq=', '')
        # numbers = ''
        # number = re.findall(f'[0-9]', message[message.index(']'):])
        # for i in number:
        #     numbers = numbers + str(i)
        at_qq = re.findall(f'[0-9]+', message)[0]
        numbers = re.findall(f'[0-9]+',message)[1]
        updataradish(group_id, int(numbers), at_qq, 0, 0, 0)
        GroupEntity.send_group_msg(group_id, at_id +
                                           f'成功添加{numbers}根萝卜')