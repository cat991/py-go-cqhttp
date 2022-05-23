import os, sys, time, json
from gocqhttpbot.botstart.entity import GuildEntity, GroupEntity
from gocqhttpbot.botstart.util import init
import time, re, uuid


# 添加权限用户
def addPermissions(guild_id, channel_id, user_id: str, day: int):
    beneath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\权限\\权限管理列表.json'
    expiration = time.time() + (60 * 60 * 24 * day)
    word = {
        'user_id': user_id,
        'expiration': expiration
    }
    try:
        with open(beneath, 'r', encoding='utf-8') as f:
            per = json.loads(f.read())
            f.close()
            for i in per:
                if i['user_id'] == user_id:
                    i['expiration'] += (60 * 60 * 24 * day)
                    with open(beneath, 'w', encoding='utf-8') as f1:
                        json.dump(per, f1, ensure_ascii=False)
                        f1.close()

                        GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                                           '添加成功，到期时间:' + time.strftime("%Y年%m月%d日",
                                                                                        time.localtime(
                                                                                            i['expiration'])))
                        return True
            else:
                per.append(word)
                with open(beneath, 'w', encoding='utf-8') as f1:
                    json.dump(per, f1, ensure_ascii=False)
                    f1.close()

                    GuildEntity.send_guild_channel_msg(guild_id, channel_id, '添加成功，到期时间:' + time.strftime("%Y年%m月%d日",
                                                                                                          time.localtime(
                                                                                                              expiration)))
                    return True
    except:
        word = [word]
        with open(beneath, 'w', encoding='utf-8') as f1:
            json.dump(word, f1, ensure_ascii=False)
            f1.close()
            GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                               '添加成功，到期时间:' + time.strftime("%Y年%m月%d日", time.localtime(expiration)))

            return True


# 删除用户的权限
def detPermissions(user_id):
    beneath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\权限\\权限管理列表.json'
    cont = 0
    try:
        with open(beneath, 'r', encoding='utf-8') as f:
            per = json.loads(f.read())
            f.close()
            for i in per:
                if i['user_id'] == user_id:
                    del per[cont]
                    with open(beneath, 'w', encoding='utf-8') as f1:
                        json.dump(per, f1, ensure_ascii=False)
                        f1.close()
                        return True
                cont += 1
    except:
        return False


# 获取是否拥有权限
def getPermissions(user_id):
    beneath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\权限\\权限管理列表.json'
    try:
        with open(beneath, 'r', encoding='utf-8') as f:
            per = json.loads(f.read())
            f.close()
            for i in per:
                if i['user_id'] == user_id and i['expiration'] > time.time():
                    return True
            else:
                return False
    except:
        return False


def permissions(data):
    data = json.loads(data)
    message = data['message']  # 消息
    guild_id = data['guild_id']  # 频道id
    channel_id = data['channel_id']  # 子频道id
    user_id = str(data['user_id'])  # 触发用户id
    at_user = f'[CQ:at,qq={user_id}] '
    if message[:4] == '添加管理' and user_id == str(init.CONFIG.masterId):
        at_qq = message[message.index('qq='):message.index(']')].replace('qq=', '')
        numbers = ''
        number = re.findall(f'[0-9]', message[message.index(']'):])
        for i in number:
            numbers = numbers + str(i)
        if numbers == '':
            GuildEntity.send_guild_channel_msg(guild_id, channel_id,
                                               '不支持的操作')
        else:
            print(numbers)
            addPermissions(guild_id, channel_id, at_qq, int(numbers))
    elif message[:4] == '删除管理':
        at_qq = message[message.index('qq='):message.index(']')].replace('qq=', '')
        if detPermissions(at_qq):
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, '已删除该管理')
        else:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, '已删除该管理')


# 保存要撤回消息的id
def add_msg_id(data):
    jdata = json.loads(data)["data"]
    msg_id = jdata["message_id"]
    old_data = ""
    data = {
        "msg_id": msg_id,
        "time": int(time.time())
    }
    path = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\data\\撤回消息id.json'
    if not os.path.exists(path):
        old_data = [data]
    else:
        with open(path, 'r', encoding='utf-8')as f:
            old_data = json.loads(f.read())
            old_data.append(data)
            f.close()
    with open(path, 'w', encoding='utf-8') as f1:
        json.dump(old_data, f1, ensure_ascii=False)
        f1.close()


def msg_monitor():
    while (True):
        time.sleep(10)
        path = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\data\\撤回消息id.json'
        with open(path, 'r', encoding='utf-8') as f:
            per = json.loads(f.read())
            f.close()
            cont = 0
            for i in per:
                if (int(time.time()) - i['time']) > 80:
                    del per[cont]
                    with open(path, 'w', encoding='utf-8') as f1:
                        json.dump(per, f1, ensure_ascii=False)
                        f1.close()
                    GroupEntity.delete_msg(i['msg_id'])
                cont += 1


# -------------------授权功能------------------------------
# 进行授权
def auth(group_id, auth_code):
    auth_path = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\data\\config\\group\\code.json'
    path = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\data\\config\\group\\authdb.json'
    with open(auth_path, 'r', encoding='utf-8')as f:
        if auth_code == f.read():
            f.close()
            auth_db = ''
            if not os.path.exists(path):
                auth_db = [group_id]
            else:
                with open(path, 'r', encoding='utf-8')as f3:
                    auth_db = json.loads(f3.read())
                    auth_db.append(group_id)
                    f3.close()
            with open(path, 'w', encoding='utf-8')as f2:
                json.dump(auth_db, f2, ensure_ascii=False)
                f2.close()
                get_auth_code()
                return '群授权成功，开启萝卜功能'
        else:
            return '授权失败,不存在的授权信息'


# 获取授权码
def get_auth_code():
    path = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\data\\config\\group\\code.json'
    code = uuid.uuid4()
    with open(path, 'w', encoding='utf-8') as f:
        # json.dump(code, f, ensure_ascii=False)
        f.write(str(code))
        f.close()
    return str(code)

#取消群授权
def delAuth(group_id):
    path = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\data\\config\\group\\authdb.json'
    with open(path,'r',encoding='utf-8')as f:
        ls = list(json.loads(f.read()))
        f.close()
        cont = 0
        for i in ls:
            if group_id == i:
                del ls[cont]
                with open(path,'w',encoding='utf-8')as f2:
                    json.dump(ls,f2,ensure_ascii=False)
                    f2.close()
                return '取消授权成功'
            cont += 1
    return '取消授权失败，该群未授权'
# 获取授权信息
def get_auth(group_id) -> bool:
    data = []
    path = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\data\\config\\group\\authdb.json'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8')as f:
            data = json.loads(f.read())
            f.close()
    for i in data:
        if group_id == i:
            return True
    return False
# if __name__ == '__main__':
#     t  = time.time() + 60*60*24*2
#     print(time.strftime("%Y年%m月%d日", time.localtime(t)))
#     print(t)
#     print(time.time())
#     print(time.strftime("%Y年%m月%d日", time.localtime(4924752967.924999)))
