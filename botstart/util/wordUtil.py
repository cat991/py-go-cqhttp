import json
from gocqhttpbot import PATH


# 查询所有口令
def queryAllPermiss(guild_id, channel_id):
    botpath = PATH + f'\\权限\\{guild_id}.json'
    flag = False
    try:
        with open(botpath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
            for i in item_list:
                if i == channel_id:
                    flag = True
    except:
        addPermiss(guild_id,channel_id)
        with open(botpath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
            for i in item_list:
                if i == channel_id:
                    return True
    return flag


# 删除json节点
def delete_Permiss(guild_id, channel_id):
    botpath = PATH + f'\\权限\\{guild_id}.json'
    cont = 0
    with open(botpath, 'r', encoding='utf-8') as f:
        item_list = json.loads(f.read())
        f.close()
        for i in item_list:
            if i == channel_id:
                del item_list[cont]
                with open(botpath, 'w', encoding='utf-8') as f2:
                    json.dump(item_list, f2, ensure_ascii=False)
                    f2.close()
                return '解除屏蔽成功'
            cont += 1
    return '解除屏蔽失败'


# 添加权限频道
def addPermiss(guild_id, channel_id):
    # 首先读取已有的json文件中的内容
    botpath = PATH + f'\\权限\\{guild_id}.json'
    cont = 0
    try:
        with open(botpath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
            for i in item_list:
                if i == channel_id:
                    return '已屏蔽该频道'
                cont += 1
            else:
                # #将新传入的dict对象追加至list中
                item_list.append(channel_id)
                # #将追加的内容与原有内容写回（覆盖）原文件
                with open(botpath, 'w', encoding='utf-8') as f2:
                    json.dump(item_list, f2, ensure_ascii=False)
                    f2.close()
                return '频道已屏蔽'
    except:
        word = [
            channel_id
        ]
        with open(botpath, 'w', encoding='utf-8') as f2:
            json.dump(word, f2, ensure_ascii=False)
            f2.close()
    return '频道已屏蔽'


def ad(guild_id, channel_id):
    botpath = PATH + f'\\权限\\{guild_id}.json'
    try:
        with open(botpath, 'r', encoding='utf-8') as f:
            item_list = json.loads(f.read())
            f.close()
    except:
        word = [
            channel_id
        ]
        with open(botpath, 'w', encoding='utf-8') as f2:
            json.dump(word, f2, ensure_ascii=False)
            f2.close()

    return '数据库中没有您的数据，请先签到'
