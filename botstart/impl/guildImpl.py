from gocqhttpbot.botstart.entity import GuildEntity,GroupEntity
import json
from gocqhttpbot import PATH
#获取频道名称
def get_guil_name(guild_id,text):
  data = GuildEntity.get_guild_meta_by_guest(guild_id)
  data = json.loads(data)['data']
  guild_name = data['guild_name'] #频道昵称
  if text in guild_name.lower():
    return True
  else:
    return False

#获取群名称
def get_group_info(group_id,text):
  data = GroupEntity.get_group_info(group_id)
  group_name = json.loads(data)['data']['group_name']
  if text in group_name.lower():
    return True
  else:
    return False



#输出和写入json数据到文件
def write_json(obj,path):
    #首先读取已有的json文件中的内容
    botpath = PATH + f'\\频道数据\\指令\\{path}.json'
    cont = 0
    with open(botpath, 'r',encoding='utf-8') as f:
        item_list = json.loads(f.read())
        f.close()
        for i in item_list:
            if i['instruction'] == obj['instruction']:
                item_list[cont]['content'] = obj['content']
                with open(botpath, 'w', encoding='utf-8') as f2:
                    json.dump(item_list, f2, ensure_ascii=False)
                    f2.close()
                return '口令修改成功'
            cont += 1
        else:
            # #将新传入的dict对象追加至list中
            item_list.append(obj)
            # #将追加的内容与原有内容写回（覆盖）原文件

            with open(botpath, 'w', encoding='utf-8') as f2:
                json.dump(item_list, f2, ensure_ascii=False)
                f2.close()
            return '口令新增成功'

#添加指令
word = {}
def password(msg,path):
    instruction = msg[msg.index('新增口令'):msg.index('内容')].replace('新增口令','')
    content = msg[msg.index('内容'):].replace('内容','')
    word = {
        'instruction': instruction,
        'content' : content
    }

    return  write_json(word,path)

#查询所有口令
def queryAll_json(path):
    botpath = PATH + f'\\频道数据\\指令\\{path}.json'
    cont = ''
    with open(botpath, 'r', encoding='utf-8') as f:
        item_list = json.loads(f.read())
        f.close()
        for i in item_list:
           cont = cont + ','+i['instruction']
    return cont
#删除json节点
def delete_json(msg,path):
    botpath = PATH + f'\\频道数据\\指令\\{path}.json'
    cont = 0
    with open(botpath, 'r', encoding='utf-8') as f:
        item_list = json.loads(f.read())
        f.close()
        for i in item_list:
            if i['instruction'] == msg:
                del item_list[cont]
                with open(botpath, 'w', encoding='utf-8') as f2:
                    json.dump(item_list, f2, ensure_ascii=False)
                    f2.close()
                return '删除成功'
            cont += 1
    return '删除失败'