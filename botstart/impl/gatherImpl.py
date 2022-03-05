from gocqhttpbot.botstart.entity import GuildEntity
from gocqhttpbot.botstart.util import SignUtil
import os, sys, re, json, random

GatHerData = [{
    "gather_id": 0,
    "gather_name": "兔子福",
    "gather_type": "SR",
    "gather_chance": 0.3,
    'gather_radish':5
}, {
    "gather_id": 1,
    "gather_name": "瑶瑶福",
    "gather_type": "SS",
    "gather_chance": 0.3,
    'gather_radish':5
}, {
    "gather_id": 2,
    "gather_name": "黑猫福",
    "gather_type": "SS",
    "gather_chance": 0.29,
    'gather_radish':5
}, {
    "gather_id": 3,
    "gather_name": "管理福",
    "gather_type": "SSS",
    "gather_chance": 0.1,
    'gather_radish':15
}, {
    "gather_id": 4,
    "gather_name": "频道主福",
    "gather_type": "SSR",
    "gather_chance": 0.01,
    'gather_radish':20
}
]


# 随机获取一个五福
def getGatHer(guild_id, channel_id, user_id):
    botpath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\频道数据\\集福\\{guild_id}.json'
    # ran = random.random(1, len(GatHerData) - 1)
    get_id = get_number_by_pro()
    flag = False
    cont = 0
    try:
        with open(botpath, "r", encoding="utf-8")as f:
            flist = json.loads(f.read())
            f.close()
            for i in flist:
                if i["user_id"] == user_id:
                    # 查询到用户，默认false
                    flist[cont][f"{get_id}"] += 1
                    break
                else:
                    # 未查询到用户，改为true添加到list
                    flag = True
                cont += 1
            word = {
                "user_id": user_id,
                "0": 1 if get_id == 0 else 0,
                "1": 1 if get_id == 1 else 0,
                "2": 1 if get_id == 2 else 0,
                "3": 1 if get_id == 3 else 0,
                "4": 1 if get_id == 4 else 0
            }

            with open(botpath, "w", encoding="utf-8")as f1:
                if flag:
                    flist.append(word)
                    # flist.append(word)
                json.dump(flist, f1, ensure_ascii=False)
                f1.close()
                GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                                   f"恭喜获得{GatHerData[get_id]['gather_name']}*1\n")
    except:
        word = [{
            "user_id": user_id,
            "0": 1 if get_id == 0 else 0,
            "1": 1 if get_id == 1 else 0,
            "2": 1 if get_id == 2 else 0,
            "3": 1 if get_id == 3 else 0,
            "4": 1 if get_id == 4 else 0
        }]
        with open(botpath, "w", encoding="utf-8")as f1:
            json.dump(word, f1, ensure_ascii=False)
            f1.close()
        GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                           f"恭喜获得{GatHerData[get_id]['gather_name']}*1\n")


# 我的五福
def selectHer(guild_id, channel_id, user_id, at_user):
    botpath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\频道数据\\集福\\{guild_id}.json'
    try:
        with open(botpath, "r", encoding="utf-8")as f:
            flist = json.loads(f.read())
            f.close()
            for i in flist:
                if i["user_id"] == user_id:
                    data = f"{at_user}\n"
                    for j in range(5):
                        data += f"{GatHerData[j]['gather_name']}*{str(i[f'{str(j)}'])}\t稀有度：{GatHerData[j]['gather_type']}\n"
                    return GuildEntity.send_guild_channel_msg(guild_id, channel_id, data)
        return GuildEntity.send_guild_channel_msg(guild_id, channel_id, '暂无数据')
    except:
        return GuildEntity.send_guild_channel_msg(guild_id, channel_id, '暂无数据')


# 合成
def compound(guild_id, channel_id, user_id):
    botpath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\频道数据\\集福\\{guild_id}.json'
    wufu = 0
    with open(botpath, "r", encoding="utf-8")as f:
        flist = json.loads(f.read())
        f.close()
        cont = 0

        for i in flist:
            if i["user_id"] == user_id:
                for j in range(5):
                    if i[f'{str(j)}'] <= 0:
                        return GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                                                  '请集齐所有福卡后召唤神龙有机会获得1888-5888根萝卜哦')
                    else:
                        wufu+=1
                if wufu == 5:
                    break
            cont += 1

        for jj in range(5):
            flist[cont][f'{str(jj)}'] -= 1
        with open(botpath, "w", encoding="utf-8")as f1:
            json.dump(flist, f1, ensure_ascii=False)
            f1.close()
            ran = random.randint(1888, 5888)
            SignUtil.updataradish(guild_id, ran, user_id, 0, 0, 0)
            addrecord(guild_id,user_id)
        return GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                                  f"恭喜获得{str(ran)}根萝卜，成就绝版身份组!!!！\n萝卜已发放,身份组联系管理修改~~~")


# 修改已有的五福
def updateGatHer(guild_id, channel_id, user_id, gather_name):
    botpath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\频道数据\\集福\\{guild_id}.json'
    with open(botpath, "r", encoding="utf-8")as f:
        flist = json.loads(f.read())
        f.close()
        cont = 0
        for i in flist:
            if i["user_id"] == user_id:
                for j in GatHerData:
                    if j['gather_name'] == gather_name:
                        flist[cont][f'{j["gather_id"]}'] += 1
            cont += 1
        with open(botpath, "w", encoding="utf-8")as f1:
            json.dump(flist, f1, ensure_ascii=False)
            f1.close()
            # guildentity.send_guild_channel_msg(guild_id, channel_id, "增加成功")


# 赠予五福
def giveGatHer(guild_id, channel_id, user_id, at_user, atuser_id, gather_name):
    botpath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\频道数据\\集福\\{guild_id}.json'
    # 判断有没有这个福
    get_gather_id = ""
    for i in GatHerData:
        if i["gather_name"] == gather_name:
            get_gather_id = i["gather_id"]
    if get_gather_id == "":
        return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + "没有该五福，请确认输入是否正确")
    # 获取用户信息和被at用户信息
    try:
        user_info = ""
        info_id = 0
        atuser_info = ""
        atinfo_id = 0
        cont = 0
        with open(botpath, "r", encoding="utf-8")as f:
            flist = json.loads(f.read())
            for i in flist:
                if user_id == i["user_id"]:
                    user_info = i
                    info_id = cont
                if atuser_id == i["user_id"]:
                    atuser_info = i
                    atinfo_id = cont
                cont += 1
            if user_info != "" and atuser_info != "":
                if user_info[f'{str(get_gather_id)}'] > 0:
                    flist[atinfo_id][f'{str(get_gather_id)}'] += 1
                    flist[info_id][f'{str(get_gather_id)}'] -= 1
                    with open(botpath, 'w', encoding="utf-8")as f2:
                        json.dump(flist, f2, ensure_ascii=False)
                        f2.close()
                    return GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                                              at_user + f"[CQ:at,qq={atuser_id}]获得了你赠送的{GatHerData[get_gather_id]['gather_name']}")
                else:
                    return GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                                              at_user + f"可惜你没有那么多{GatHerData[get_gather_id]['gather_name']}了")
            else:
                return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + "其中一名用户还未启用五福系统")

    except:
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + "命令执行失败，或许是因为数据库中没有你的数据？--")


# 按概率随机获取一张福的id
def get_number_by_pro():
    # 用均匀分布中的样本值来模拟概率
    x = random.uniform(0, 1)
    # 累积概率
    cum_pro = 0.0
    # 将可迭代对象打包成元组列表
    for her in GatHerData:
        cum_pro += her["gather_chance"]
        if x < cum_pro:
            # print("概率为：", x)
            return int(her["gather_id"])


# 判断用户是否拥有这个福
def judge(guild_id, user_id, gather_name):
    botpath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\频道数据\\集福\\{guild_id}.json'
    get_gather_id = ""
    for i in GatHerData:
        if i["gather_name"] == gather_name:
            get_gather_id = i["gather_id"]
    try:
        # 判断有没有这个福
        with open(botpath, 'r', encoding='utf-8')as f:
            flist = json.loads(f.read())
            f.close()
            for i in flist:
                if i['user_id'] == user_id:
                    if i["user_id"] == user_id:
                        if i[f'{str(get_gather_id)}'] > 0:
                            return True  # 有福卡
        if get_gather_id == "":
            return False  # 没有福卡
    except:
        return False  # 没有福卡


# 抽奖功能,消费抽取五福
def gamble(guild_id, channel_id, user_id, at_user):
    if SignUtil.judge(guild_id, user_id):
        return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '数据库中没有你的数据，请先签到，发送：签到')
    else:
        if SignUtil.get_user_radish_number(guild_id, user_id, 88):
            SignUtil.updataradish(guild_id, -88, user_id, 0, 0, 0)
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '已扣除88根萝卜')
            getGatHer(guild_id, channel_id, user_id)
        else:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + "等你拥有这么多萝卜再来购买吧~")

# 出售五福
def sell(guild_id, channel_id, user_id, at_user, gather_name, number):
    botpath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\频道数据\\集福\\交易大厅\\{guild_id}.json'
    botpath1 = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\频道数据\\集福\\{guild_id}.json'
    sellcode = False
    get_gather_id = ""
    id = random.randrange(1000, 9999)
    for i in GatHerData:
        if i["gather_name"] == gather_name:
            get_gather_id = i["gather_id"]
    if get_gather_id == "":
        return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '好像并没有这种类型的五福哦~~')
    try:
        if judge(guild_id, user_id, gather_name):
            sellcode = True
            with open(botpath, 'r', encoding='utf-8')as f:  # 交易
                flist = json.loads(f.read())
                f.close()
            with open(botpath1, "r", encoding="utf-8")as f1:  # 福
                flist1 = json.loads(f1.read())
                f1.close()
                cont = 0
                for i in flist1:
                    if i["user_id"] == user_id:
                        for j in GatHerData:
                            if j['gather_name'] == gather_name:
                                flist1[cont][f'{j["gather_id"]}'] -= 1
                    cont += 1
                word = {
                    "id": id,  # 随机生成订单id
                    "user_id": user_id,  # 用户id
                    "radish": number,  # 出售价格
                    "gather_name": gather_name  # 五福名
                }
                flist.append(word)
                with open(botpath, 'w', encoding='utf-8')as f2:
                    json.dump(flist, f2, ensure_ascii=False)
                    f2.close()
                with open(botpath1, 'w', encoding='utf-8')as f3:
                    json.dump(flist1, f3, ensure_ascii=False)
                    f3.close()
                GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                                   at_user + f'成功出售{gather_name}\n售价:{number},单号:{id}\n如需购买的用户请发送:购买五福+单号')

        else:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '要先拥有这个福才能出售哦~~')


    except:
        if sellcode:
            with open(botpath1, "r", encoding="utf-8")as f1:  # 福
                flist1 = json.loads(f1.read())
                f1.close()
                cont = 0
                for i in flist1:
                    if i["user_id"] == user_id:
                        for j in GatHerData:
                            if j['gather_name'] == gather_name:
                                flist1[cont][f'{j["gather_id"]}'] -= 1
                    cont += 1
                word = [{
                    "id": id,  # 随机生成订单id
                    "user_id": user_id,  # 用户id
                    "radish": number,  # 出售价格
                    "gather_name": gather_name  # 五福名
                }]
                with open(botpath, 'w', encoding='utf-8')as f2:
                    json.dump(word, f2, ensure_ascii=False)
                    f2.close()
                with open(botpath1, 'w', encoding='utf-8')as f3:
                    json.dump(flist1, f3, ensure_ascii=False)
                    f3.close()
                GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                                   at_user + f'成功出售{gather_name}\n售价:{number},单号:{id}\n如需购买的用户请发送:购买五福+单号')

        else:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '要先拥有这个福才能出售哦~~')
#出售五福给系统
def sellSys(guild_id, channel_id, user_id, gather_name):
    botpath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\频道数据\\集福\\{guild_id}.json'
    if judge(guild_id,user_id,gather_name):
        get_gather_id = ""
        number = 0
        for i in GatHerData:
            if i['gather_name'] ==gather_name:
                get_gather_id = i['gather_id']
                number = i['gather_radish']
                break

        cont = 0
        with open(botpath,'r',encoding='utf-8')as f:
            flist = json.loads(f.read())
            f.close()
            for i in flist:
                if i["user_id"] == user_id:
                    flist[cont][f"{get_gather_id}"] -= 1
                    SignUtil.updataradish(guild_id, number, user_id, 0, 0, 0)
                    break
                cont+=1
        with open(botpath,'w',encoding='utf-8')as f1:
            json.dump(flist,f1,ensure_ascii=False)
            f1.close()
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, f"成功出售{gather_name}~\n获得{number}根萝卜")

    else:
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, f"你没有{gather_name}可以出售了")
    # 'gather_radish':5

# 购买五福
def buy(guild_id, channel_id, user_id, at_user, message):
    botpath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\频道数据\\集福\\交易大厅\\{guild_id}.json'
    code = True
    try:
        with open(botpath,'r',encoding='utf-8')as f:
            flist = json.loads(f.read())
            f.close()
            cont = 0
            for i in flist:
                if i['id'] == int(message):
                    code = False
                    if SignUtil.get_user_radish_number(guild_id, user_id, i['radish']):
                        del flist[cont]
                        with open(botpath,'w',encoding='utf-8')as f1:
                            json.dump(flist,f1,ensure_ascii=False)
                            f1.close()
                        updateGatHer(guild_id,channel_id,user_id,i['gather_name'])
                        SignUtil.updataradish(guild_id, -int(i['radish']), user_id, 0, 0, 0, i['user_id'])
                        return GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                                                  at_user + f"购买成功，已扣除{i['radish']}根萝卜！\n恭喜获得：{i['gather_name']}!!!")
                    else:
                       return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + "等你拥有这么多萝卜再来购买吧~")
                cont+=1
            if code:
                GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + f"无订单{message}的物品信息，购买失败!!")
    except:
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + f"无订单{message}的物品信息，购买失败")

# 交易大厅信息
def trading(guild_id, channel_id, at_user, message=""):
    botpath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\频道数据\\集福\\交易大厅\\{guild_id}.json'
    t = 0
    data = f'你搜索的是:{message}'
    try:
        with open(botpath, 'r', encoding='utf-8')as f:
            flist = json.loads(f.read())
            f.close()
            # item_list = sorted(item_list, key=lambda x: int(x["radish"]), reverse=True)
            for i in flist:
                if t >= 5:
                    break
                if message == "":
                    data += f"\n单号:{i['id']}\t物品:{i['gather_name']}\n售价:{i['radish']}萝卜\t用户:[CQ:at,qq={i['user_id']}]\n"
                    t+=1
                else:
                    if i['gather_name']==message:
                        t+=1
                        data += f"\n单号:{i['id']}\t物品:{i['gather_name']}\n售价:{i['radish']}萝卜\t用户:[CQ:at,qq={i['user_id']}]\n"
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + data)

    except:
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + "未知物品或输入错误")

#添加五福获奖记录
def addrecord(guild_id, user_id):
    botpath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\频道数据\\集福\\获奖记录\\{guild_id}.json'
    try:
        with open(botpath, 'r', encoding='utf-8')as f:
            flist = json.loads(f.read())
            f.close()
            word = {
                "user_id": user_id,
                "number": 0
            }
            flist.append(word)
            with open(botpath, 'w', encoding='utf-8')as f2:
                json.dump(flist, f2, ensure_ascii=False)
                f2.close()
    except:
        word = [{
            "user_id":user_id,
            "number":0
        }]
        with open(botpath,'w',encoding='utf-8')as f3:
            json.dump(word,f3,ensure_ascii=False)
            f3.close()
#查看获奖记录
def getrecord(guild_id, channel_id,at_user):
    botpath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\频道数据\\集福\\获奖记录\\{guild_id}.json'
    data = '以下是已合成五福的获奖者：\n'
    try:
        with open(botpath,'r',encoding='utf-8')as f:
            flist = json.loads(f.read())
            f.close()
            for i in flist:
                data += f' [CQ:at,qq={i["user_id"]}]  \n'
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + data)
    except:
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '暂无数据')
# 主页
def gather(data):
    data = json.loads(data)
    message = data['message']  # 消息
    guild_id = data['guild_id']  # 频道id
    channel_id = data['channel_id']  # 子频道id
    user_id = str(data['user_id'])  # 触发用户id
    at_user = f'[CQ:at,qq={user_id}] '

    if message == '我的五福':
        selectHer(guild_id, channel_id, user_id, at_user)
    # elif message[:4] == '增加五福':
    #     updateGatHer(guild_id,channel_id,user_id,message[4:])
    # elif message == '测试五福':
    #     getGatHer(guild_id, channel_id, user_id)
    elif message == '合成五福':
        compound(guild_id, channel_id, user_id)
    elif message == '五福功能':
        GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                           "五福获奖记录\n我的五福\n合成五福\n交易五福  (将五福挂载到交易大厅\n--示例：交易五福兔子福666）\n五福交易大厅 + 兔子福\n购买五福 + 单号\n出售五福 + 兔子福  (按系统默认价格出售 \n抽取五福\n赠予五福 @ +兔子福\n")
    elif message[:4] == '交易五福':
        numbers = re.findall('\d', message)
        number = ''
        for i in numbers:
            number += str(i)
        gather_name = message[4:].replace(number, "")
        sell(guild_id, channel_id, user_id, at_user, gather_name, int(number))
    elif message[:6] == '五福交易大厅':
        trading(guild_id, channel_id, at_user,message[6:])
    elif message[:4] == '购买五福':
        buy(guild_id, channel_id, user_id, at_user, message[4:])
    elif message[:4] == '赠予五福':
        atuser_id = message[message.index('qq='):message.index(']')].replace('qq=', '')
        gather_name = message[message.index(']'):].replace("]", "").replace(" ", "")
        giveGatHer(guild_id, channel_id, user_id, at_user, atuser_id, gather_name)
    elif message == '抽取五福' or message == '抽五福':
        gamble(guild_id, channel_id, user_id, at_user)
    elif message[:4] == '出售五福':
        sellSys(guild_id,channel_id,user_id,message[4:])
    elif message == '五福获奖记录':
        getrecord(guild_id,channel_id,at_user)
# if __name__ == '__main__':
#     for j in range(5):
#         print(j)
#
#     id = random.randrange(100000,9999999)
#     print(id)
#     # botpath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\频道数据\\集福\\312671636379380.json'
#     botpath = 'E:\\pythonProject\\test1\\频道数据\\集福\\312671636379380.json'
#     with open(botpath, "r", encoding="UTF-8")as f:
#         flist = json.loads(f.read())
#         f.close()
#         cont = 0
#         for i in flist:
#             if i["user_id"] == '144115218676755577':
#                 for j in range(5):
#                     if i[f'{str(j)}'] <= 0:
#                         print(i[f'{str(j)}'])
#     for j in range(5):
#         print(j)
#      修改概率
#     for i in range(100):
#         n = get_number_by_pro()
#         print("返回的值为：", GatHerData[n]['gather_name'],n)
