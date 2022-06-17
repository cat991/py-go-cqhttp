import re

from gocqhttpbot.botstart.entity import GuildEntity, CQcode,GroupEntity
from gocqhttpbot.botstart.util import textToImg, SignUtil
import json, time, os, sys, random

from gocqhttpbot import PATH
hireTypes = [{
    'name': '打工',
    'nickname': '恭喜兔宝雇佣成功·对方正在为您在工厂打工赚萝卜（16分钟后结算）',
    'pay': 3,
    'obtain': 8,
    'success': '为您不停的打工·为您赚了8个萝卜',
    'lose': '打工太卖力猝死了·您血本无归',
    'time': 60 * 16,
}, {
    'name': '色色',
    'nickname': '您用了两个萝卜吸引了对方·您正在对对方色色',
    'pay': 2,
    'obtain': -2,
    'success': '色色成功·你们成功的谈恋爱了（快交换联系方式吧）',
    'lose': '拒绝色色·并且给了你一巴掌🤭',
    'time': 1,
}, {
    'name': '洗衣服',
    'nickname': '恭喜兔宝雇佣成功·对方正在为您洗衣服赚萝卜（4分钟后结算）',
    'pay': 0,
    'obtain': 2,
    'success': '不停的为您打工洗衣服·您收获了2个萝卜',
    'lose': '洗衣服太卖力被淹死了·您血本无归',
    'time': 60 * 4,
}, {
    'name': '探险',
    'nickname': '恭喜兔宝雇佣成功·对方正在为您探险寻找宝藏（20分钟后结算）',
    'pay': 0,
    'obtain': 10,
    'success': '探险顺利归来·为您带来了10根萝卜',
    'lose': '探险不小心掉下悬崖·您血本无归',
    'time': 60 *20,
}, {
    'name': '送外卖',
    'nickname': '恭喜兔宝雇佣成功·对方正在为您送外卖赚萝卜（12分钟后结算）',
    'pay': 0,
    'obtain': 6,
    'success': '不停的的为您送外卖·您收获了6个萝卜',
    'lose': '送外卖的路上除了车祸升天了·您血本无归',
    'time': 60 * 12,
}]


# 遍历查询所有内容
def monitoring():
    botpath = PATH + f'\\频道数据\\雇佣数据'
    listFile = os.listdir(botpath)
    times = time.time()
    for guil_id in listFile:
        if len(guil_id) > 15:
            file = botpath + f'\\{guil_id}'
            with open(file, 'r', encoding='utf-8') as f:
                fls = json.loads(f.read())
                f.close()
                for flist in fls:
                    if flist['hireTime'] <= times:
                        for typeof in hireTypes:
                            if flist['hireType'] == typeof['name']:
                                at_user = f'[CQ:at,qq={str(flist["user_id"])}] '
                                at_her = f'[CQ:at,qq={flist["hire"]}] '
                                judge = random.randint(0, 2)
                                if judge == 1 or judge == 2:
                                    deletHire(guil_id.replace('.json', ''), flist['hire'])
                                    SignUtil.updataradish(guil_id.replace('.json', ''), int(typeof['obtain']), flist['user_id'], 0, 0, 0)
                                    return GuildEntity.send_guild_channel_msg(guil_id.replace('.json', ''),
                                                                              flist['channel_id'],
                                                                              at_user + at_her + typeof['success'] + CQcode.images(
                                                                                  f'images/雇佣/success{typeof["name"]}.jpg'))
                                elif judge == 0:

                                    deletHire(guil_id.replace('.json', ''), flist['hire'])
                                    SignUtil.updataradish(guil_id.replace('.json', ''), -int(typeof['pay']), flist['user_id'], 0, 0, 0)
                                    return GuildEntity.send_guild_channel_msg(guil_id.replace('.json', ''),
                                                                              flist['channel_id'],
                                                                              at_user + at_her + typeof['lose'] + CQcode.images(
                                                                                  f'images/雇佣/lose{typeof["name"]}.jpg'))
        else:
            file = botpath + f'\\{guil_id}'
            with open(file, 'r', encoding='utf-8') as f:
                fls = json.loads(f.read())
                f.close()
                for flist in fls:
                    if flist['hireTime'] <= times:
                        for typeof in hireTypes:
                            if flist['hireType'] == typeof['name']:
                                at_user = f'[CQ:at,qq={str(flist["user_id"])}] '
                                at_her = f'[CQ:at,qq={flist["hire"]}] '
                                judge = random.randint(0, 2)
                                if judge == 1 or judge == 2:
                                    deletHire(guil_id.replace('.json', ''), flist['hire'])
                                    SignUtil.updataradish(guil_id.replace('.json', ''), int(typeof['obtain']),
                                                          flist['user_id'], 0, 0, 0)
                                    return GroupEntity.send_group_msg(guil_id.replace('.json', ''),
                                                                              at_user + at_her + typeof[
                                                                                  'success'] + CQcode.images(
                                                                                  f'images/雇佣/success{typeof["name"]}.jpg'))
                                elif judge == 0:

                                    deletHire(guil_id.replace('.json', ''), flist['hire'])
                                    SignUtil.updataradish(guil_id.replace('.json', ''), -int(typeof['pay']),
                                                          flist['user_id'], 0, 0, 0)
                                    return GroupEntity.send_group_msg(guil_id.replace('.json', ''),
                                                                              at_user + at_her + typeof[
                                                                                  'lose'] + CQcode.images(
                                                                                  f'images/雇佣/lose{typeof["name"]}.jpg'))

# 结算删除信息
def deletHire(guild_id, hire):

    bypath = PATH + f'\\频道数据\\雇佣数据\\{guild_id}.json'
    cont = 0
    with open(bypath, 'r', encoding='utf-8') as f:
        item_list = json.loads(f.read())
        f.close()
        for i in item_list:
            if i['hire'] == str(hire):
                del item_list[cont]
                with open(bypath, 'w', encoding='utf-8') as f2:
                    json.dump(item_list, f2, ensure_ascii=False)
                    f2.close()
            cont += 1


# 添加雇佣信息
def addHire(guild_id, channel_id, user_id, at_qq, hireType):
    if SignUtil.judge(guild_id, user_id) :
        return GuildEntity.send_guild_channel_msg(guild_id, channel_id, f'[CQ:at,qq={at_qq}] ' + '数据库中没有你的数据，请先签到，发送：签到')
    at_user = f'[CQ:at,qq={str(user_id)}] '
    cont = 0
    conts = 0
    flag = True
    if user_id == at_qq:
        return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '无法雇佣自己')

    for typeof in hireTypes:
        conts += 1
        if typeof['name'] == hireType:
            flag = False
            bypath = PATH + f'\\频道数据\\雇佣数据\\{str(guild_id)}.json'
            try:
                with open(bypath, 'r', encoding='utf-8') as f:
                    data = json.loads(f.read())
                    f.close()
                    for datalist in data:
                        if datalist['hire'] == at_qq:
                            return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '对方已被雇佣')
                        if datalist['user_id'] == user_id:
                            cont += 1
                    if cont >= 2:
                        return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '最多只能雇佣两个人哦~')
                    else:
                        word = {
                            'channel_id': str(channel_id),  # 子频道id
                            'user_id': str(user_id),  # 主人id
                            'hire': str(at_qq),  # 被雇佣人id
                            'hireTime': time.time() + int(typeof['time']),  # 被雇佣的时间
                            'hireType': typeof['name']  # 雇佣类型
                        }
                        # #将新传入的dict对象追加至list中
                        data.append(word)
                        # #将追加的内容与原有内容写回（覆盖）原文件
                        with open(bypath, 'w', encoding='utf-8') as f2:
                            json.dump(data, f2, ensure_ascii=False)
                            f2.close()
                        return GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                                                  at_user + typeof['nickname'] + CQcode.images(
                                                                      f'images/雇佣/{typeof["name"]}.jpg'))
            except:
                data = [{
                    'channel_id': str(channel_id),  # 子频道id
                    'user_id': str(user_id),  # 主人id
                    'hire': str(at_qq),  # 被雇佣人id
                    'hireTime': time.time() + int(typeof['time']),  # 被雇佣的时间
                    'hireType': typeof['name']  # 雇佣类型
                }]
                with open(bypath, 'w', encoding='utf-8') as f2:
                    json.dump(data, f2, ensure_ascii=False)
                    f2.close()
                return GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                                          at_user + typeof['nickname'] + CQcode.images(
                                                              f'images/雇佣/{typeof["name"]}.jpg'))

    if flag:
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '没有该类型的任务~')



# 添加雇佣信息 q群适配
def addHire_group(group_id, user_id, at_qq, hireType):
    if SignUtil.judge(group_id, user_id) :
        return GroupEntity.send_group_msg(group_id, f'[CQ:at,qq={at_qq}] ' + '数据库中没有你的数据，请先签到，发送：签到')
    at_user = f'[CQ:at,qq={str(user_id)}] '
    cont = 0
    conts = 0
    flag = True
    if user_id == at_qq:
        return GroupEntity.send_group_msg(group_id, at_user + '无法雇佣自己')

    for typeof in hireTypes:
        conts += 1
        if typeof['name'] == hireType:
            flag = False
            bypath = PATH + f'\\频道数据\\雇佣数据\\{str(group_id)}.json'
            try:
                with open(bypath, 'r', encoding='utf-8') as f:
                    data = json.loads(f.read())
                    f.close()
                    for datalist in data:
                        if datalist['hire'] == at_qq:
                            return GroupEntity.send_group_msg(group_id, at_user + '对方已被雇佣')
                        if datalist['user_id'] == user_id:
                            cont += 1
                    if cont >= 2:
                        return GroupEntity.send_group_msg(group_id, at_user + '最多只能雇佣两个人哦~')
                    else:
                        word = {
                            'user_id': str(user_id),  # 主人id
                            'hire': str(at_qq),  # 被雇佣人id
                            'hireTime': time.time() + int(typeof['time']),  # 被雇佣的时间
                            'hireType': typeof['name']  # 雇佣类型
                        }
                        # #将新传入的dict对象追加至list中
                        data.append(word)
                        # #将追加的内容与原有内容写回（覆盖）原文件
                        with open(bypath, 'w', encoding='utf-8') as f2:
                            json.dump(data, f2, ensure_ascii=False)
                            f2.close()
                        return GroupEntity.send_group_msg(group_id,
                                                                  at_user + typeof['nickname'] + CQcode.images(
                                                                      f'images/雇佣/{typeof["name"]}.jpg'))
            except:
                data = [{
                    'user_id': str(user_id),  # 主人id
                    'hire': str(at_qq),  # 被雇佣人id
                    'hireTime': time.time() + int(typeof['time']),  # 被雇佣的时间
                    'hireType': typeof['name']  # 雇佣类型
                }]
                with open(bypath, 'w', encoding='utf-8') as f2:
                    json.dump(data, f2, ensure_ascii=False)
                    f2.close()
                return GroupEntity.send_group_msg(group_id,
                                                          at_user + typeof['nickname'] + CQcode.images(
                                                              f'images/雇佣/{typeof["name"]}.jpg'))

    if flag:
        GroupEntity.send_group_msg(group_id, at_user + '没有该类型的任务~')




# 死循环监控
def die():
    while (True):
        time.sleep(2)
        monitoring()


def functionss(guild_id, channel_id, user_id, at_user, message):
    botpath = PATH + f'\\频道数据\\雇佣菜单.json'
    if message[:6] == '修改雇佣功能' and user_id == '144115218676755577':
        with open(botpath, 'w', encoding='utf-8')as f:
            f.write(message[6:])
            f.close()
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '修改成功')
    elif message == '雇佣功能':
        try:
            with open(botpath, 'r', encoding='utf-8') as f:
                text = f.read()
                f.close()
                text = textToImg.line_break(text, 16)
                textToImg.toImage('/images/素材/rabbitText.jpg', 100, 280, text, '/images/图片缓存/雇佣菜单.png', 80)
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + CQcode.images('images/图片缓存/雇佣菜单.png'))
        except:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '联系作者编写功能')
    else:
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '你没有权限进行修改')


def userHire(guild_id, channel_id, user_id):
    bypath = PATH + f'\\频道数据\\雇佣数据\\{guild_id}.json'
    at_user = f'[CQ:at,qq={user_id}]'
    hire_content = '你的雇佣信息如下:\n'
    with open(bypath, 'r', encoding='utf-8') as f:
        item_list = json.loads(f.read())
        f.close()
        for i in item_list:
            if i['user_id'] == user_id:
                shijian = time.strftime("%M:%S", time.localtime(int(i["hireTime"]) - int(time.time())))
                hire_content = hire_content + f'[CQ:at,qq={str(i["hire"])}] 被雇佣去:{i["hireType"]}\n还差{shijian}分钟自动结算\n \n'

    return GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + hire_content)

def userHire_group(group_id, user_id):
    bypath = PATH + f'\\频道数据\\雇佣数据\\{group_id}.json'
    at_user = f'[CQ:at,qq={user_id}]'
    hire_content = '你的雇佣信息如下:\n'
    with open(bypath, 'r', encoding='utf-8') as f:
        item_list = json.loads(f.read())
        f.close()
        for i in item_list:
            if i['user_id'] == user_id:
                shijian = time.strftime("%M:%S", time.localtime(int(i["hireTime"]) - int(time.time())))
                hire_content = hire_content + f'[CQ:at,qq={str(i["hire"])}] 被雇佣去:{i["hireType"]}\n还差{shijian}分钟自动结算\n \n'

    return GroupEntity.send_group_msg(group_id, at_user + hire_content)

# 雇佣功能
def hire_guild(data):
    data = json.loads(data)
    message = data['message']  # 消息
    guild_id = data['guild_id']  # 频道id
    channel_id = data['channel_id']  # 子频道id
    user_id = str(data['user_id'])  # 触发用户id
    at_user = f'[CQ:at,qq={user_id}] '
    if message == '雇佣功能' or message[:6] == '修改雇佣功能':
        functionss(guild_id, channel_id, user_id, at_user, message)
    elif message[:2] == '雇佣':
        hireType = message[message.index(']'):].replace(']', '').replace(' ', '')
        # at_qq = message[message.index('qq='):message.index(']')].replace('qq=', '')
        at_qq = re.findall('[0-9]+', message)[0]
        addHire(guild_id, channel_id, user_id, at_qq, hireType)
    elif message == '我的雇佣':
        userHire(guild_id, channel_id, user_id)


def hire_group(data):
    data = json.loads(data)
    self_id = str(data['self_id'])  # 框架qq号
    group_id = str(data['group_id'])  # 群号
    message = data['message']  # 消息内容
    user_id = str(data['user_id'])  # 触发用户id
    at_id = f'[CQ:at,qq={user_id}]'
    if message[:2] == '雇佣':
        hireType = message[message.index(']'):].replace(']', '').replace(' ', '')
        # at_qq = message[message.index('qq='):message.index(']')].replace('qq=', '')
        at_qq = re.findall('[0-9]+',message)[0]
        addHire_group(group_id, user_id, at_qq, hireType)
    elif message == '我的雇佣':
        userHire_group(group_id, user_id)