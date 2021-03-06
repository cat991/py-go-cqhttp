import os, json, sys, random, datetime, re
from time import localtime, strftime, time
from gocqhttpbot.botstart.entity import CQcode, GuildEntity,GroupEntity
from gocqhttpbot.botstart.util import permissions,init
from gocqhttpbot import PATH
# æ·»å ç¨æ·
word = {}
texterre = ['ðæå«å¤±è´¥ï¼ä½ è¢«åæå¹¶ä¸è¢«å²è®½å¤±å»äºèåð¥',
            'ðæå«å¤±è´¥ï¼éå°äºè­¦å¯è¢«æèµ°å¥çç±³å¤±å»äºèåð¥',
            'ðæå«å¤±è´¥ï¼ä½ å¨è·¯ä¸è¢«è®¤åºéç¼ç¯å¤±å»èåð¥',
            'ðæå«å¤±è´¥ï¼ä½ éå°äºä¸æ¡æ¶ç¬ä½é¢å¤±å»äºèåð¥',
            'ðæå«å¤±è´¥ï¼ä½ è¸©å°äºçå±æäºä¸è·¤ä½é¢å¤±å»èåð¥',
            'ðæå«å¤±è´¥ï¼ä½ æ²¡æè¿½ä¸å¹¶è¢«å²è®½å°ç­è¿å¤±å»èåð¥',
            'ðæå«å¤±è´¥ï¼ä½ è¢«åæå¹¶ä¸è¢«å²è®½å¤±å»äºèåð¥',
            'ðæå«å¤±è´¥ï¼éå°äºè­¦å¯è¢«æèµ°å¥çç±³å¤±å»äºèåð¥',
            'ðæå«å¤±è´¥ï¼ä½ å¨è·¯ä¸è¢«è®¤åºéç¼ç¯å¤±å»èåð¥',
            'ðæå«å¤±è´¥ï¼ä½ éå°äºä¸æ¡æ¶ç¬ä½é¢å¤±å»äºèåð¥',
            'ðæå«å¤±è´¥ï¼ä½ è¸©å°äºçå±æäºä¸è·¤ä½é¢å¤±å»èåð¥',
            'ðæå«å¤±è´¥ï¼ä½ æ²¡æè¿½ä¸å¹¶è¢«å²è®½å°ç­è¿å¤±å»èåð¥', ]
textsuccess = ['ðæå«æåï¼ä½ é¡ºå©å¾æå¹¶ä¸äº²äºå¯¹æ¹ä¸å£è·å¾èåð¥',
               'ðæå«æåï¼è·å¾èåð¥',
               'ðæå«æåï¼è·¯ä¸éå°äºåä¼æå«ç¿»åè·å¾èåð¥ (bus']


# ç­¾å°åè½
def addUser(guil_id, user_id):
    ran = random.randint(init.CONFIG.min, init.CONFIG.max)
    day = strftime("%dæ¥", localtime())
    word = {
        'user_id': user_id,
        'radish': ran,
        'day': day,
        'rob': init.CONFIG.rob,
        'unrob': init.CONFIG.unrob,
        'pullradish': 0,
        'give': init.CONFIG.give,
        'planting': None  # ç§æ¤èå
    }
    try:
        obj = write_json(guil_id, word)
    except:
        user_ById(guil_id, user_id)
        obj = write_json(guil_id, word)
        return obj
    return obj


# ç¨æ·æ ¡éªæ¥å£
def judge(guild_id, user_id):
    ym = strftime("%Yå¹´%mæ", localtime())
    botpath = PATH + f'\\é¢éæ°æ®\\{ym + guild_id}.json'
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


# å¤æ­ç¨æ·èåæ°éæ¯å¦è¿ä¹å¤
def get_user_radish_number(guild_id, user_id, number):
    ym = strftime("%Yå¹´%mæ", localtime())
    botpath = PATH + f'\\é¢éæ°æ®\\{ym + guild_id}.json'
    with open(botpath, 'r', encoding='utf-8')as f:
        flist = json.loads(f.read())
        for i in flist:
            if i['user_id'] == user_id:
                if i['radish'] >= number:
                    return True
        return False


# è·åç¨æ·ä¿¡æ¯ï¼æ¥è¯¢
def user_ById(guil_id, user_id):
    global planting
    ym = strftime("%Yå¹´%mæ", localtime())
    day = strftime("%dæ¥", localtime())
    botpath = PATH + f'\\é¢éæ°æ®\\{ym + guil_id}.json'
    try:
        with open(botpath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
    except:
        word = [{
            'user_id': str(user_id),  # ç¨æ·id
            'radish': random.randint(init.CONFIG.min, init.CONFIG.max),  # èåæ°é
            'day': day,  # æ¥æ
            'rob': init.CONFIG.rob,  # æå«æ¬¡æ°
            'unrob': init.CONFIG.unrob,  # è¢«æå«æ¬¡æ°
            'pullradish': 0,  # æèå 0å1
            'give': init.CONFIG.give,  # å¯èµ éèåæ°é
            'planting': None  # ç§æ¤èå
        }]
        with open(botpath, 'w', encoding='utf-8') as f2:
            json.dump(word, f2, ensure_ascii=False)
            f2.close()
        return 'æ°æ®åºä¸­æ²¡ææ¨çæ°æ®ï¼è¯·åç­¾å°'
    planting = f'ðç§æ¤:æ ç§æ¤ç©'

    for i in item_list:
        if user_id == i['user_id']:
            if i['planting'] is not None:
                if float(i['planting']) <= time():
                    planting = f'ðç§æ¤:æ¨çèåå·²æç {i["planting"] <= time()}'
                else:
                    shijian = strftime("%M:%S", localtime(int(i["planting"]) - int(time())))
                    # print(localtime(int(i["planting"]) - int(time())))
                    planting = f'ðç§æ¤:{shijian}åå¯æ¶è·'
            return f'\nåå®æ¨çèç¯®å­ð¥ï¼\nðèåæ°éï¼èåð¥Â·{i["radish"]}\n' \
                   f'ðæå«æ¬¡æ°ï¼{i["rob"]}\nðè¢«æå«æ¬¡æ°ï¼{i["unrob"]}\n' \
                   f'ðèµ éæ°éï¼ä»æ¥å¯èµ é{i["give"]}æ ¹èåð¥\n' \
                   f'{planting}\n'


    return 'æ°æ®åºä¸­æ²¡ææ¨çæ°æ®ï¼è¯·åç­¾å°'


# æè¡æ¦æ¥è¯¢
def queryAll_json(guil_id, m=0):
    ym = ''
    if m == 0:
        ym = strftime("%Yå¹´%mæ", localtime())
    else:
        ym = (datetime.datetime.now() + datetime.timedelta(days=-30)).strftime("%Yå¹´%mæ")
    day = strftime("%dæ¥", localtime())
    try:
        botpath = PATH + f'\\é¢éæ°æ®\\{ym + guil_id}.json'
        content = '\næè¡æ¦å¦ä¸ï¼\n'
        cont = 1
        with open(botpath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
        item_list = sorted(item_list, key=lambda x: int(x["radish"]), reverse=True)
        for i in item_list:
            if cont <= 5:
                content = content + f'ðç¬¬{str(cont)}å ï¼[CQ:at,qq={i["user_id"]}]\nð¥èç¯®å­ï¼èåð¥Â·{str(i["radish"])}ð¥\n\n'
                cont = cont + 1
    except:
        return 'æ²¡æä¸ä¸ªæçæ°æ®'
    return content


# å é¤jsonèç¹
def delete_json(guil_id, at_id):
    ym = strftime("%Yå¹´%mæ", localtime())
    day = strftime("%dæ¥", localtime())
    botpath = PATH + f'\\é¢éæ°æ®\\{ym + guil_id}.json'
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
                return 'å é¤æå'
            cont += 1
    return 'å é¤å¤±è´¥'


# è¾åºååå¥jsonæ°æ®å°æä»¶
def write_json(guild_id, obj):
    # é¦åè¯»åå·²æçjsonæä»¶ä¸­çåå®¹
    ym = strftime("%Yå¹´%mæ", localtime())
    day = strftime("%dæ¥", localtime())
    botpath = PATH + f'\\é¢éæ°æ®\\{ym + guild_id}.json'
    cont = 0
    with open(botpath, 'r', encoding='utf-8') as f:
        item_list = json.loads(f.read())
        f.close()
        for i in item_list:
            if i['user_id'] == obj['user_id']:
                if i['day'] == obj['day']:
                    return 'ðåå®Â·ä»æ¥ç­¾è¿å°äºå¦ï¼åæ ¹ç³è«è¦æå¤©åæ¥å§ð¡'
                item_list[cont]['day'] = obj['day']
                item_list[cont]['radish'] += int(obj['radish'])
                item_list[cont]['rob'] = init.CONFIG.rob
                item_list[cont]['unrob'] = init.CONFIG.unrob
                item_list[cont]['give'] = init.CONFIG.give
                with open(botpath, 'w', encoding='utf-8') as f2:
                    json.dump(item_list, f2, ensure_ascii=False)
                    f2.close()
                    # äºç¦åè½
                # gatherImpl.getGatHer(guild_id, channel_id, i['user_id'])
                return f'ç­¾å°æå,è·å¾{obj["radish"]}èåð¥{CQcode.images("images/ç­¾å°æå.png")}'
            cont += 1
        else:
            # #å°æ°ä¼ å¥çdictå¯¹è±¡è¿½å è³listä¸­
            item_list.append(obj)
            # #å°è¿½å çåå®¹ä¸åæåå®¹ååï¼è¦çï¼åæä»¶
            with open(botpath, 'w', encoding='utf-8') as f2:
                json.dump(item_list, f2, ensure_ascii=False)
                f2.close()
            # äºç¦åè½
            # gatherImpl.getGatHer(guild_id, channel_id, i['user_id'])
            return f'ðåå®Â·æ­åé¦æ¬¡ç­¾å°ï¼æ¨è·å¾äº{obj["radish"]}æ ¹èåð¥ ãåå®æå¤©è®°å¾æ¥ç­¾å°å¦[CQ:face,id=319]ã{CQcode.images("images/é¦æ¬¡ç­¾å°.png")}'


# æå«
def rob(guil_id, user_id, at_id):
    radish = random.randint(5, 8)
    ran = random.randint(0, 2)
    ym = strftime("%Yå¹´%mæ", localtime())
    beneath = PATH + f'\\é¢éæ°æ®\\{ym + guil_id}.json'
    cont = 0
    user_id_text = ''
    at_id_text = ''
    try:
        with open(beneath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
    except:
        return f' æ°æ®åºä¸­å¯è½æ²¡æä½ çä¿¡æ¯ï¼è¯·ç­¾å°ååè¯è¯'
    for i in item_list:
        if i['user_id'] == str(user_id):
            user_id_text = item_list[cont]
        if i['user_id'] == str(at_id):
            at_id_text = item_list[cont]
        cont += 1
    if at_id_text == '' or user_id_text == '':
        return f'[CQ:at,qq={user_id}] å¶ä¸­æä¸ä¸ªäººæ²¡ç­¾å°æ æ³æå«å¦~'
    if at_id_text['unrob'] == 0:
        return f'[CQ:at,qq={user_id}] ðåå®Â·æ¨æå«çåå®é­åå¤ªå¤§å·²ç»æå«ä¸éäºå¦ï¼å¿«å»æ¢å¦ä¸ä¸ªç®æ å­ð³'
    elif user_id_text['rob'] == 0:
        return f'[CQ:at,qq={user_id}]ðåå®Â·ä»å¤©ä½ èªå·±æå«äºå¾å¤æ¬¡äºå¦ï¼åå£è¶ä¼æ¯ä¸ä¸å­ðµ'
    elif ran == 0 or ran == 1:
        updataradish(guil_id, radish, user_id, -1, -1, 0, at_id)
        # updataradish(guil_id, -int(radish), at_id, 0, -1, 0)
        # return f'[CQ:at,qq={user_id}] è¿ä¸ªbè¦æ¢å«ä½  \n[CQ:at,qq={at_id}] ä½ è¢«æåæ¢å« {radish}æ ¹èå' \
        return f'[CQ:at,qq={user_id}] ' + textsuccess[random.randint(1, len(textsuccess) - 1)] + str(
            radish) + CQcode.images('images/æå«æå.png')
    else:
        er = random.randint(1, 2)
        updataradish(guil_id, -int(er), user_id, -1, 0, 0)
        return f'[CQ:at,qq={user_id}] ' + texterre[random.randint(1, len(texterre) - 1)] + str(er) + CQcode.images(
            'images/æå«å¤±è´¥.png')


# æèå
def pull(guil_id, user_id):
    shu = random.randint(2, 5)
    ym = strftime("%Yå¹´%mæ", localtime())
    botpath = PATH + f'\\é¢éæ°æ®\\{ym + guil_id}.json'

    try:
        with open(botpath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
    except:
        return f'æ°æ®åºä¸­å¯è½æ²¡æä½ çä¿¡æ¯ï¼è¯·ç­¾å°ååè¯è¯'
    cont = 0
    for i in item_list:
        if user_id == i['user_id']:
            if i['planting'] is None:
                return 'è¯·åç§æ¤èå,åé:ç§èå'
            else:
                if float(i['planting']) >= time():
                    return f'æ¨çèåè¿æªæç,è¯·ç­å¾æçååæ¥æ¶è·å§~'
                else:
                    item_list[cont]['planting'] = None
                    with open(botpath, 'w', encoding='utf-8') as f2:
                        json.dump(item_list, f2, ensure_ascii=False)
                        f2.close()
                    updataradish(guil_id, shu, user_id, 0, 0, 0)
                    return f'å¤å³çå°åæåæ¶è·{shu}æ ¹èå{CQcode.images("images/æ¶è·æ»¡æ»¡.png")}'
        cont += 1
    return f'æ°æ®åºä¸­å¯è½æ²¡æä½ çä¿¡æ¯ï¼è¯·ç­¾å°ååè¯è¯'


# ç§èå
def seed(guil_id, user_id):
    if judge(guil_id, user_id):
        return 'æ°æ®åºä¸­æ²¡æä½ çæ°æ®ï¼è¯·åç­¾å°ï¼åéï¼ç­¾å°'
    ym = strftime("%Yå¹´%mæ", localtime())
    botpath = PATH + f'\\é¢éæ°æ®\\{ym + guil_id}.json'
    try:
        with open(botpath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
    except:
        return f' æ°æ®åºä¸­å¯è½æ²¡æä½ çä¿¡æ¯ï¼è¯·ç­¾å°ååè¯è¯'
    cont = 0
    shijian = int(time()) + 60 * 15
    for i in item_list:
        if i['user_id'] == user_id:
            if i['planting'] is not None:
                return 'è¯·ç­å¾ä½ çèåæçæ¶è·ååè¿è¡ç§æ¤å¦~'
            item_list[cont]['planting'] = int(shijian)
            with open(botpath, 'w', encoding='utf-8') as f2:
                json.dump(item_list, f2, ensure_ascii=False)
                f2.close()
        cont += 1
    return f'ç§æ¤æåï¼15åéååæ¥æ¶å{CQcode.images("images/ç§æ¤æå.png")}'


# ä¿®æ¹æå«åçæ¬¡æ°åèåæ°é
def updataradish(guil_id, radish, user_id, rob, unrob, give, atuser_id=""):
    ym = strftime("%Yå¹´%mæ", localtime())
    botpath = PATH + f'\\é¢éæ°æ®\\{ym + guil_id}.json'

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


# èµ éèå
def give(guil_id, user_id, at_id, number):
    ym = strftime("%Yå¹´%mæ", localtime())
    beneath = PATH + f'\\é¢éæ°æ®\\{ym + guil_id}.json'
    cont = 0
    user_id_text = ''
    at_id_text = ''
    try:
        with open(beneath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
    except:
        return f' æ°æ®åºä¸­å¯è½æ²¡æä½ çä¿¡æ¯ï¼è¯·ç­¾å°ååè¯è¯'
    for i in item_list:
        if i['user_id'] == str(user_id):
            user_id_text = item_list[cont]
        if i['user_id'] == str(at_id):
            at_id_text = item_list[cont]
        cont += 1
    if at_id_text == '' or user_id_text == '':
        return f'[CQ:at,qq={user_id}] å¶ä¸­æä¸ä¸ªäººæ²¡ç­¾å°æ æ³èµ éèåå¦~'

    if user_id_text['give'] >= int(number) > 0:
        updataradish(guil_id, -int(number), user_id, 0, 0, number, at_id)
        # updataradish(guil_id, number, at_id, 0, 0, 0)
        return f'[CQ:at,qq={at_id}]ðåå®Â·æ¨çå¥½åé©¬ä¸åè¹Â·è·è·ææçç»æ¨éäºèåð¥*{str(number)}'
    elif user_id_text['radish'] < int(number):
        return f'[CQ:at,qq={user_id}]ä½ èªå·±é½èº«æ åæäº'
    else:
        return f'[CQ:at,qq={user_id}]ä½ å·²ç»ä¸è½éåå¤äº'


def sig_index_guild(datas):
    datas = json.loads(datas)
    message = datas['message']  # æ¶æ¯
    guild_id = datas['guild_id']  # é¢éid
    channel_id = datas['channel_id']  # å­é¢éid
    user_id = str(datas['user_id'])  # è§¦åç¨æ·id
    at_user = f'[CQ:at,qq={user_id}] '
    if message == 'ç§èå':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user +
                                           seed(guild_id, user_id))
    elif message == 'æèå':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user +
                                           pull(guild_id, user_id))
    elif message[:4] == 'æ£é¤èå' and (user_id == str(init.CONFIG.masterId) or permissions.getPermissions(user_id)):
        # at_qq = message[message.index('qq='):message.index(']')].replace('qq=', '')
        # numbers = ''
        # number = re.findall(f'[0-9]', message[message.index(']'):])
        # for i in number:
        #     numbers = numbers + str(i)

        at_qq = re.findall(f'[0-9]+', message)[0]
        numbers = re.findall(f'[0-9]+', message)[1]
        updataradish(guild_id, -int(numbers), at_qq, 0, 0, 0)
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user +
                                           f'æåæ£é¤{numbers}æ ¹èå')
    elif message[:4] == 'å¢å èå' and (user_id == str(init.CONFIG.masterId) or permissions.getPermissions(user_id)):
        # at_qq = message[message.index('qq='):message.index(']')].replace('qq=', '')
        at_qq = re.findall(f'[0-9]+', message)[0]
        # numbers = ''
        # number = re.findall(f'[0-9]', message[message.index(']'):])
        # for i in number:
        #     numbers = numbers + str(i)
        numbers = re.findall(f'[0-9]+', message)[1]
        updataradish(guild_id, int(numbers), at_qq, 0, 0, 0)
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user +
                                           f'æåæ·»å {numbers}æ ¹èå')
def sig_index_group(datas):
    data = json.loads(datas)
    group_id = str(data['group_id'])  # ç¾¤å·
    message = data['message']  # æ¶æ¯åå®¹
    user_id = str(data['user_id'])  # è§¦åç¨æ·id
    at_id = f'[CQ:at,qq={user_id}]'
    if message == 'ç§èå':
        GroupEntity.send_group_msg(group_id,at_id+seed(group_id, user_id))
    elif message == 'æèå':
        GroupEntity.send_group_msg(group_id, at_id +
                                           pull(group_id, user_id))
    elif message[:4] == 'æ£é¤èå' and (user_id == str(init.CONFIG.masterId) or permissions.getPermissions(user_id)):
        # at_qq = message[message.index('qq='):message.index(']')].replace('qq=', '')
        # numbers = ''
        # number = re.findall(f'[0-9]', message[message.index(']'):])
        at_qq = re.findall(f'[0-9]+', message)[0]
        number = re.findall(f'[0-9]+', message)[1]
        # for i in number:
        #     numbers = numbers + str(i)
        updataradish(group_id, -int(number), at_qq, 0, 0, 0)
        GroupEntity.send_group_msg(group_id, at_id +
                                           f'æåæ£é¤{number}æ ¹èå')
    elif message[:4] == 'å¢å èå' and (user_id == str(init.CONFIG.master) or permissions.getPermissions(user_id)):
        # at_qq = message[message.index('qq='):message.index(']')].replace('qq=', '')
        # numbers = ''
        # number = re.findall(f'[0-9]', message[message.index(']'):])
        # for i in number:
        #     numbers = numbers + str(i)
        at_qq = re.findall(f'[0-9]+', message)[0]
        numbers = re.findall(f'[0-9]+',message)[1]
        updataradish(group_id, int(numbers), at_qq, 0, 0, 0)
        GroupEntity.send_group_msg(group_id, at_id +
                                           f'æåæ·»å {numbers}æ ¹èå')