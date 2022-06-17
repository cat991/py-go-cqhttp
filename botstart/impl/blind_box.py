from gocqhttpbot.botstart.entity import GuildEntity, CQcode
from gocqhttpbot.botstart.util import  SignUtil,permissions,init
import json, os, sys, random
from time import localtime, strftime
from gocqhttpbot import PATH

# 抽盲盒需要的消费
smoke_blind_box_number = 38
# 放入盲盒需要的消费
put_box_number = 18


# 抽出盲盒
def smoke_blind_box(guild_id, channel_id, user_id, at_user, message):

    if '男生' in message:
        bypath = PATH + f'\\频道数据\\盲盒数据\\男生盲盒.json'
    else:
        bypath = PATH + f'\\频道数据\\盲盒数据\\女生盲盒.json'

    if SignUtil.judge(guild_id, user_id):
        return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '数据库中没有你的数据，请先签到，发送：签到')

    if radish(guild_id, user_id, smoke_blind_box_number):

        return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '你没有足够的萝卜抽取盲盒了')
        # return guildentity.send_guild_channel_msg(guild_id, channel_id,
        #                                           at_user + f'抽取盲盒需要{str(smoke_blind_box_number)}个萝卜，你需要赚到足够多的萝卜才能继续使用哦')

    try:
        with open(bypath, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            f.close()
            conts = len(data)
            cont = random.randint(1, conts) - 1
            data[cont]['cont'] = data[cont]['cont'] + 1
            with open(bypath, 'w', encoding='utf-8') as f2:
                json.dump(data, f2, ensure_ascii=False)
                f2.close()
            guild_data_id = data[cont]['guild_id']
            guildata = GuildEntity.get_guild_meta_by_guest(guild_data_id)
            guildata = json.loads(guildata)['data']
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + f'共有{str(conts)}个盲盒\n'
                                                                               f'你抽出的是来自:{guildata["guild_name"]}\n'
                                                                               f'[CQ:at,qq={data[cont]["user_id"]}]的盲盒\n'
                                                                               f'编号:{str(cont)}\n'
                                                                               f'内容是：{data[cont]["content"]}')
            SignUtil.updataradish(guild_id, -int(smoke_blind_box_number), user_id, 0, 0, 0)
    except:
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + f'系统出错了？或是没有盲盒内容，请投入一个盲盒试试')


# 放入盲盒
def put_blind_box(guild_id, channel_id, user_id, at_user, message):
    if '男生' in message:
        bypath = PATH + f'\\频道数据\\盲盒数据\\男生盲盒.json'
    else:
        bypath = PATH + f'\\频道数据\\盲盒数据\\女生盲盒.json'
    if SignUtil.judge(guild_id, user_id):
        return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '数据库中没有你的数据，请先签到，发送：签到')

    if radish(guild_id, user_id, put_box_number):
        return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '你没有足够的萝卜进行盲盒投放了')
        # return guildentity.send_guild_channel_msg(guild_id, channel_id,
        #                                           at_user + f'放入盲盒需要{str(put_box_number)}根萝卜，你需要赚到足够多的萝卜才能继续使用哦')
    if len(message[5:]) < 6:
        return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '请多输入点内容哦~')

    SignUtil.updataradish(guild_id, -int(put_box_number), user_id, 0, 0, 0)
    try:
        with open(bypath, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            f.close()
            word = {
                'guild_id': str(guild_id),  # 频道id
                'channel_id': str(channel_id),  # 子频道id
                'user_id': str(user_id),  # 主人id
                'content': message[5:],  # 盲盒的内容
                'cont': 0  # 统计被抽取的次数
            }
            # #将新传入的dict对象追加至list中
            data.append(word)
            # #将追加的内容与原有内容写回（覆盖）原文件
            with open(bypath, 'w', encoding='utf-8') as f2:
                json.dump(data, f2, ensure_ascii=False)
                f2.close()
            return GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                                      at_user + f'消费{str(put_box_number)}根萝卜投放盲盒成功')
    except:
        word = [{
            'guild_id': str(guild_id),  # 频道id
            'channel_id': str(channel_id),  # 子频道id
            'user_id': str(user_id),  # 主人id
            'content': message[5:],  # 盲盒的内容
            'cont': 0  # 统计被抽取的次数
        }]
        with open(bypath, 'w', encoding='utf-8') as f2:
            json.dump(word, f2, ensure_ascii=False)
            f2.close()
        return GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                                  at_user + f'消费{str(put_box_number)}根萝卜投放盲盒成功')


# 查看自己投入的盲盒
def user_box(guild_id, channel_id, user_id, at_user):
    box_content_nan = '男生盲盒：\n'
    box_content_nv = '女生盲盒：\n'

    bypath1 = PATH + f'\\频道数据\\盲盒数据\\男生盲盒.json'
    cont = 0
    with open(bypath1, 'r', encoding='utf-8') as f1:
        data1 = json.loads(f1.read())
        f1.close()
        for i in data1:
            if i['user_id'] == user_id:
                box_content_nan = box_content_nan + f'盲盒编号：{str(cont)},({i["cont"]})内容{i["content"][:4]}\n'
            cont += 1
    bypath2 = PATH + f'\\频道数据\\盲盒数据\\女生盲盒.json'
    cont = 0
    with open(bypath2, 'r', encoding='utf-8') as f2:
        data2 = json.loads(f2.read())
        f2.close()
        for f in data2:
            if f['user_id'] == user_id:
                box_content_nv = box_content_nv + f'盲盒编号：{str(cont)},({f["cont"]})内容{f["content"][:4]}\n'
            cont += 1
    box_content = box_content_nan + box_content_nv
    box_content = box_content.replace('[CQ','[图片]').replace('[C','[图片]').replace('[','[图片]')
    return GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                              at_user + box_content)


# 判断用户是否有足够多的萝卜
def radish(guil_id, user_id, number):
    ym = strftime("%Y年%m月", localtime())
    beneath = PATH + f'\\频道数据\\{ym + guil_id}.json'
    cont = 0
    user_id_text = ''
    item_list = ''
    try:
        with open(beneath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
    except:
        return True
    for i in item_list:
        if i['user_id'] == str(user_id):
            user_id_text = i
        cont += 1
    if int(user_id_text['radish']) >= int(number):
        return False
    else:
        return True


# 销毁盲盒
def delete_box(guild_id, channel_id, user_id, at_user, message,admin=False):
    if '男生' in message:
        bypath = PATH + f'\\频道数据\\盲盒数据\\男生盲盒.json'
    else:
        bypath = PATH + f'\\频道数据\\盲盒数据\\女生盲盒.json'
    cont = message[6:]
    try:
        with open(bypath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
            if admin is False:
                if item_list[int(cont)]['user_id'] == user_id:
                    if radish(guild_id, user_id, 100):
                        return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '你没有足够的萝卜进行盲盒销毁哦~')
                    SignUtil.updataradish(guild_id, -100, user_id, 0, 0, 0)
                else:
                    return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '这并非你的盲盒，你无权销毁他人盲盒哦~')
            del item_list[int(cont)]
            with open(bypath, 'w', encoding='utf-8') as f2:
                json.dump(item_list, f2, ensure_ascii=False)
                f2.close()
                if admin is False:
                    return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + f'编号{str(cont)}盲盒已被销毁,消费100萝卜')
                else:
                    return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + f'编号{str(cont)}盲盒已被销毁')
    except:
        return GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                                  at_user + f'编号{str(cont)}盲盒销毁失败，原因可能是数据库没有该编号数据')
#增加所有频道的所有萝卜
def hilarity(guild_id, channel_id,message):
    botpath = PATH + f'\\频道数据'
    listFile = os.listdir(botpath)
    ym = strftime("%Y年%m月", localtime())
    number = message[4:]
    for fileName in listFile:
        if ym in fileName :
            file = botpath + f'\\{fileName}'
            with open(file, 'r', encoding='utf-8') as f:
                fls = json.loads(f.read())
                f.close()
                for i in fls:
                    i['radish'] = i['radish'] + int(number)
            with open(file, 'w', encoding='utf-8') as f2:
                json.dump(fls, f2, ensure_ascii=False)
                f2.close()
    GuildEntity.send_guild_channel_msg(guild_id, channel_id, f'全服狂欢成功,所有人增加{str(number)}根萝卜')

def functionss(guild_id, channel_id, at_user):
    GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + CQcode.images('images/盲盒功能.png'))


def box(datas):
    datas = json.loads(datas)
    message = datas['message']  # 消息
    guild_id = datas['guild_id']  # 频道id
    channel_id = datas['channel_id']  # 子频道id
    user_id = str(datas['user_id'])  # 触发用户id
    at_user = f'[CQ:at,qq={user_id}] '
    if message == '抽男生盲盒' or message == '抽女生盲盒':
        smoke_blind_box(guild_id, channel_id, user_id, at_user, message)
    elif message[:5] == '投男生盲盒' or message[:5] == '投女生盲盒':
        # at_qq = message[message.index('qq='):message.index(']')].replace('qq=', '')#获取被艾特的人的qq
        put_blind_box(guild_id, channel_id, user_id, at_user, message)
    elif message == '盲盒功能':
        functionss(guild_id, channel_id, at_user)
    elif message[:6] == '销毁男生盲盒' or message[:6] == '销毁女生盲盒' :
        if user_id == str(init.CONFIG.masterId) or permissions.getPermissions(user_id):
            delete_box(guild_id, channel_id,user_id, at_user, message,True)
        else:
            delete_box(guild_id, channel_id,user_id, at_user, message)
    elif message == '我的盲盒':
        user_box(guild_id, channel_id, user_id, at_user)
