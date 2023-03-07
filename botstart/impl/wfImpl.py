import json, time, re
import requests

from gocqhttpbot.botstart.dao.GroupHanderDao import switch
from gocqhttpbot.botstart.impl import otherImpl, animeImpl
from gocqhttpbot.botstart.entity import GroupEntity

from gocqhttpbot import PATH
import os, sys

from gocqhttpbot.botstart.util import memeImgGenerate, init

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}


def 二次元(loginqq, group):
    urls = ''
    # for i in range(0,3):
    #     url = requests.get('https://www.dmoe.cc/random.php').url
    #     urls =urls + groupentity.uploadgrouppic(loginqq, group, url,type='url')
    for i in range(0, 3):
        url = requests.get('https://www.dmoe.cc/random.php?return=json').text
        urls = urls + GroupEntity.uploadgrouppic(loginqq, group, json.loads(url)['imgurl'], type='url')
    return urls


# 仲裁信息
def arbitration():
    return '\t\n' + requests.get('http://nymph.rbq.life:3000/wf/robot/arbitration').text


# 基于https://github.com/WsureDev/warframe-info-api接口开发的通用接口
def allOutmsg(msg):
    return requests.get('http://nymph.rbq.life:3000/wf/robot/' + msg).text

def invade():
    resp = requests.get('https://api.null00.com/world/ZHCN')
    resp = json.loads(resp.text)['invasions']
    ret = ""
    for i in resp:
        ret += f"{i['node']}（{i['locTag']}）\n{i['attacker']['faction']}vs{i['defender']['faction']}"
        if len(i['attacker']['rewards']) == 0:
            ret += f"\n没有奖励 vs{i['defender']['rewards'][0]['item']}\n\n"
        else:
            ret += f"\n{i['attacker']['rewards'][0]['item']}vs{i['defender']['rewards'][0]['item']}\n\n"
    return  otherImpl.toImage("国服入侵\t\n"+ret,"国服入侵")+otherImpl.toImage("国际服入侵\t\n"+requests.get('http://nymph.rbq.life:3000/wf/robot/invasions').text,"国际服入侵")

# 突击信息
def sortie(type=0):
    resp = requests.get('https://api.null00.com/world/ZHCN')
    resp = json.loads(resp.text)['sortie']
    gf = f'\t\n国服：今日突击:{resp["boss"]}\n派系:{resp["faction"]}' \
         f'\n任务一：{resp["variants"][0]["missionType"]}\n限定:{resp["variants"][0]["modifierType"]}\n地点:{resp["variants"][0]["node"]}\n' \
         f'\n任务二：{resp["variants"][1]["missionType"]}\n限定:{resp["variants"][1]["modifierType"]}\n地点:{resp["variants"][1]["node"]}\n' \
         f'\n任务三：{resp["variants"][2]["missionType"]}\n限定:{resp["variants"][2]["modifierType"]}\n地点:{resp["variants"][2]["node"]}\n'
    if type == 0:
        return gf + '\t\n国际服:\n' + requests.get('http://nymph.rbq.life:3000/wf/robot/sortie').text
    elif type == 1:
        return gf
    else:
        return '\t\n' + requests.get('http://nymph.rbq.life:3000/wf/robot/sortie').text


# 奥迪斯攻略接口
def ordis(msg):
    data = {
        'text': msg
    }
    text = requests.post('https://api.null00.com/ordis/getTextMessage', data=data).text
    text = json.loads(text)['msg']
    # .replace('\/r\/n','\n')
    return text


# warframe维基
def wiki(search):
    resp = requests.get('https://warframe.huijiwiki.com/api.php?action=opensearch&search=' + search, headers=headers)
    resp = json.loads(resp.text)
    msg = '\t\n你要找的是\n'
    for title, url in zip(resp[1], resp[3]):
        msg += f'{title}\n{url}\n'
    return msg


# 平原时间，星际战甲
def dayTime():
    resp = requests.get('https://api.null00.com/world/ZHCN')
    resp = json.loads(resp.text)
    day = resp['cetus']['day']
    times = resp['cetus']['cetusTime']
    if day:
        times = int(times) - int(time.time())
        if times < 0:
            return "现在正从白天轮换到晚上"
        else:
            hours = time.strftime('%H', time.localtime(times))
            hours = int(hours) - 8
            time1 = time.strftime('%M分%S秒', time.localtime(times))
            return f'\t\n现在时间是--白天--\n剩余时间:{hours}时{time1}'
    else:
        times = times - int(time.time())
        if times < 0:
            return "\t\n现在正从晚上轮换到白天"
        else:
            hours = time.strftime('%H', time.localtime(times))
            hours = int(hours) - 8
            time1 = time.strftime('%M分%S秒', time.localtime(times))
            return f'\t\n现在时间是--晚上--\n剩余时间:{hours}时{time1}'


# 地球时间
def earthCycle():
    return '\t\n' + requests.get('http://nymph.rbq.life:3000/wf/robot/earthCycle').text


# 奸商信息
def voidTrader():
    resp = requests.get('https://api.null00.com/world/ZHCN')
    resp = json.loads(resp.text)
    arrivals = resp['voidTrader']['arrivals']
    times = resp['voidTrader']['activation']
    place = resp['voidTrader']['node']
    if arrivals:
        guofu = f'\t\n-------国服-------\n奸商已抵达：{place}'
    else:
        times = times - 28800
        times = times - int(time.time())
        if times < 0:
            times = resp['voidTrader']['activation'] + 86400 - (int(time.time()) + 28800)
            # times = (int(time.time())) -resp['voidTrader']['activation']
            # times = int(str(times).replace('-',''))
            day = time.strftime('%d', time.localtime(times))
            time1 = time.strftime('%H时%M分%S秒', time.localtime(times))
            guofu = f'\t\n-------国服-------\n奸商到来时间：{int(day) - 2}天{time1} \n地点：{place}'
        else:
            day = time.strftime('%d', time.localtime(times))
            time1 = time.strftime('%H时%M分%S秒', time.localtime(times))
            guofu = f'\t\n-------国服-------\n奸商到来时间：{int(day) - 1}天{time1} \n地点：{place}'
    guojifu = requests.get('http://nymph.rbq.life:3000/wf/robot/voidTrader').text
    return f'{guofu}\n\n-------国际服-------\n{guojifu}'


# 星际战甲金星温度判断
def states(state):

    if state == 1:
        return '极寒'
    elif state == 2:
        return '寒冷'
    elif state == 3:
        return '温暖'
    elif state == 4:
        return '寒冷'
    elif state == 5:
        return '极寒'


# 星际战甲金星温度
def jxwd():
    resp = requests.get('https://api.null00.com/world/ZHCN')
    resp = json.loads(resp.text)
    times = resp['solaris']['solarisExpiry']
    state = resp['solaris']['state']
    timemms = times - int(time.time())
    if timemms < 0:
        timemms = int(str(timemms).replace("-", ""))
        time1 = time.strftime('%M分%S秒', time.localtime(timemms))
        return f'\t\n山谷温度正从\n{states(int(state))}\n切换到\n{states(int(state + 1))}'
    else:
        time1 = time.strftime('%M分%S秒', time.localtime(timemms))
        return f'\t\n现在温度是--{states(int(state))}--\n{time1}后切换\n--{states(state + 1)}--'


# 火卫二时间
def hw2():
    resp = requests.get('http://nymph.rbq.life:3000/wf/robot/cambionCycle').text
    if 'fass' in resp:
        return resp.replace('fass', '毁灭(fass)')
    else:
        return resp.replace('vome', '秩序(vome)')


# warframe玄骸紫卡交易
def wfrm(str):
    resp = requests.get(f'http://nymph.rbq.life:3000/rm/robot/{str.replace(" ", "")}').text
    # groupentity.groupmsg(loginqq, group, otherImpl.toImage(loginqq, group, resp, 'wfrm'))
    return otherImpl.toImage(resp, 'wfrm')

    # groupentity.uploadzkpic(group_id,resp,'wfrm','false')
#中继站轮换 泰森
def steelPath():
    resp = requests.get('https://api.warframestat.us/pc').text
    data = json.loads(resp)['steelPath']
    return f'\n当前轮换内容是：\n{data["currentReward"]["name"]}\n需要钢精：{data["currentReward"]["cost"]}'

# warframe物品交易
def wfwm(msg, mod_rank):
    if msg == "":
        return "出现了一点小错误呢"
    str = {}
    msg = botci(msg)
    # print(msg)
    # print(type(msg))
    str['itme'] = msg["code"]
    str['mod_rank'] = int(mod_rank)
    if str['itme'] == '无':
        return '暂时无该物品黑话信息或该物品本就无法交易'
    resp = requests.get(
        f'https://api.warframe.market/v1/items/{str["itme"].replace(" ", "_").lower()}/orders?include=item')
    resp = json.loads(resp.text)

    try:
        orderslist = resp['payload']['orders']
        orderslist = sorted(orderslist, key=lambda x: x["platinum"], reverse=False)

        orderre = f'\t\n默认展示价格最低前10个\n你要搜索的是：{msg["main"]} \n翻译：{msg["zh"]}'

    except:

        return '\t\n搜索出现了一点小状况,检查是否错别字或重新查询'
    cont = 0  # 统计10个
    number = 0  # 统计全部价格
    conts = 0  # 统计全部
    for i in orderslist:
        if i['order_type'] == "sell":
            number += i['platinum']
            conts += 1
        if str['mod_rank'] == 0:
            if i['order_type'] == "sell" and cont < 10 and i['user']['status'] != "offline":  # 判断是否是出售商品
                cont += 1
                baijin = i['platinum']  # 获取到的白鸡
                name = i['user']['ingame_name']  # 获取到的游戏名
                state = i['user']['status']
                orderre += f' \n白金:{baijin}--游戏id: {name}'
        else:
            if i['order_type'] == "sell" and cont < 10 and i['user']['status'] != "offline" and i['mod_rank'] == str[
                'mod_rank']:  # 判断是否是出售商品
                cont += 1
                baijin = i['platinum']  # 获取到的白鸡
                name = i['user']['ingame_name']  # 获取到的游戏名
                state = i['user']['status']
                orderre += f' \n白金:{baijin}--游戏id: {name}--物品等级:{str["mod_rank"]}级'
                # orderre += f'\n在线状态：{"在线" if state != "offline" else "离线"}\n白金:{baijin}---游戏昵称: {name}'
    # print(orderre)
    if cont == 0:
        return '\t\n没有该商品或并没有查到该等级的商品'
    else:
        return orderre + f'\n总出售人数{conts}人，平均:{int(number / conts)}白鸡'


# 翻译&warframe查字典
def botci(keys, flag=True):
    path = PATH + "\\WF_Sale.json"
    # if any(str in keys for str in ['蓝', '头', '机', '体','系统','场景','枪','前纪','古纪','后纪','中纪','装饰']) and flag:
    try:
        with open(path, "r", encoding="utf-8") as f:
            file_list = json.loads(f.read())
        #     print(type(file_list))
        # keys = input("战甲")
        if flag:
            keys += "一套"
        # print(keys)
        result = fuzzy_finder(keys, file_list)
        if len(result) == 0 and flag:
            return botci(keys.replace('一套', ''), False)
        elif len(result) == 0 and flag == False:
            return {
                "main": "无",
                "zh": "无",
                "code": "无"
            }
        else:
            return result[0]
            # return result[len(result) - 1]
    except Exception as e:
        print("出现错误" % e)
        if flag:
            return botci(keys.replace('一套', ''), False)
        else:
            return {
                "main": "无",
                "zh": "无",
                "code": "无"
            }

    # resp = requests.get(f'http://nymph.rbq.life:3000/dict/tran/robot/{str.replace(" ", "")}').text
    # num = 0
    # # ret ={}
    # txt = ''
    # for lis in resp.split('\n'):
    #     num += 1
    #     if num == 2:
    #         itme = re.findall(f'\\[(.*?)]', lis)
    #         txt = itme[0]
    #         # txt = itme[0].replace(' ', '_').lower()
    #         # ret={
    #         #     'itme':itme[0].replace(' ', '_').lower(),
    #         #      'str':itme[0],
    #         #     'mod_rank':mod_rank
    #         # }
    # try:
    #     # return wfwm(ret)
    #     return txt
    # except:
    #     return resp


def fuzzy_finder(key, data):
    # 结果列表
    suggestions = []
    # 非贪婪匹配，转换 'djm' 为 'd.*?j.*?m'
    pattern = '.*?'.join(key)
    # pattern = '.*%s.*'%(key)
    # print("pattern",pattern)
    # 编译正则表达式
    regex = re.compile(pattern)
    for item in data:
        # print("zh",item['zh'])
        # 检查当前项是否与regex匹配。
        match = regex.search(item['zh'].lower())
        if match:
            # 如果匹配，就添加到列表中
            suggestions.append(item)
    return suggestions


# 获取商品折扣
def dailyDeals():
    resp = requests.get('https://api.null00.com/world/ZHCN')
    resp = json.loads(resp.text)['dailyDeals']
    dail1 = '国服折扣：'
    for i in resp:
        item = i['item']  # 商品名称
        times = i['expiry'] - time.time()  # 剩余时间
        discount = str(i['discount']) + '%'  # 折扣百分比
        originalPrice = i['originalPrice']  # 原价
        salePrice = i['salePrice']  # 折扣后的价格
        residue = i['total'] - i['sold']  # 剩余库存
        time1 = time.strftime('%H时%M分%S秒', time.localtime(times))
        dail1 += f'\n商品:{item} (-{discount})\n价格:{salePrice}({originalPrice})\n库存:{residue} \n时间:还剩余{time1}\n'
    dail2 = '\n国际服折扣：' + allOutmsg('dailyDeals')
    return dail1 + dail2


# 发送群公告
def group_announcement(logonqq, msg):
    list = GroupEntity.getgrouplist(logonqq)
    for i in list:
        GroupEntity.groupmsg(logonqq, i['groupnum'], msg)


# 遗物查询功能
def search_relics(search, flg=False):
    url = f'https://www.ourwarframe.com/app/api/index/list?page=1&pageSize=30&search={search}&type&stock'
    ret = ''
    resp = requests.get(url).text
    resp = json.loads(resp)
    data = resp['data']
    cont = 0
    for text in data:
        size = f'遗物:{text["name"]}\n' \
               f'铜档:\n{text["copper_1"]["name"]}\t价值奸商币{text["copper_1"]["price"]}\n{text["copper_2"]["name"]}\t价值奸商币{text["copper_2"]["price"]}\n{text["copper_3"]["name"]}\t价值奸商币{text["copper_3"]["price"]}\n' \
               f'银档:\n{text["silver_1"]["name"]}\t价值奸商币{text["silver_1"]["price"]}\n{text["silver_2"]["name"]}\t价值奸商币{text["silver_2"]["price"]}\n' \
               f'金档:\n{text["gold"]["name"]}\t价值奸商币{text["gold"]["price"]}\n ' \
               f'数据由{text["contribute"]}提供\n核桃'
        if text["stock"] != True:
            size = size + '暂未入库'
        else:
            size = size + '已入库'
        ret = ret + otherImpl.toImage(size, 'images\\遗物图片缓存\\relics' + str(cont))
        cont = cont + 1
    content = []
    if flg:
        itemlist = re.findall('\[(.*?)]',ret)
        for item in itemlist:
            item = item.replace("\\", "/")
            items = {
                "type": "node",
                "data": {
                    "name": search,
                    "uin": "180802337",
                    "content": f'[{item}]'
                }
            }
            content.append(items)
        # print(str(content).replace("'",'"'))
        return str(content).replace("'",'"')
    return ret


# 星际战甲菜单
def caidan():
    return """
----当前菜单----
光遇菜单 | 战甲菜单
授权功能 | 赞助作者
/状态   |  /type

    """

def warframe():
    return """
你要的菜单来了
-----菜单-----
攻略  关键词
wiki  关键词 
物品交易: wm  
紫卡交易：rm & zk 
平原时间 & 地球时间 
金星温度 
火卫二 & hw2 
虚空商人 & 奸商  
双服突击 
仲裁 & 仲裁任务 
查询口令
遗物 关键词(仅支持国服) 
中继站轮换 & 泰辛
---频道主命令---
屏蔽 & 关闭
接触屏蔽 & 开启
    """

def strategy(txt):
    onePath = PATH + f'\\频道数据\\星际战甲攻略数据'
    pathName = ''
    for filename in os.listdir(onePath):
        if txt in filename:
            pathName = filename
            break
    if pathName == '':
        return False
    pathNew = onePath + f'\\{pathName}\\'
    with open(pathNew + '内容.txt', 'r', encoding='utf-8')as f:
        content = f.read()
        # print('内容--------------', content)
        f.close()
    finlist = re.findall(f'\[(.*?)]', content)
    for finImg in finlist:
        content = content.replace(f'[{finImg}]', f'[CQ:image,file=file:///{pathNew}/{finImg}]')
    return content

    # path = PATH + "\\WF_Sale.json"
@switch('星际战甲')
def run(data):
    group_id = data['group_id']  # 群号
    message = data['message']  # 消息内容
    user_id = str(data['user_id'])  # 触发用户id
    at_id = f'[CQ:at,qq={user_id}]'
    if message[:2].lower() == 'rm' or message[:2].lower() == 'zk':
        message = message[2:]
        GroupEntity.send_group_msg(group_id, at_id + wfrm(message))
    elif message[:2] == '攻略':
        GroupEntity.send_group_msg(group_id, at_id + ordis(message[2:]))
    elif message == '地球时间':
        GroupEntity.send_group_msg(group_id, at_id + earthCycle())
    elif message == '平原时间':
        try:
            GroupEntity.send_group_msg(group_id, at_id + dayTime())
        except:
            GroupEntity.send_group_msg(group_id, at_id + '正在进行昼夜更替，稍后查询哦')
    elif message == '平原':
        try:
            GroupEntity.send_group_msg(group_id,
                                       at_id + f'夜灵平原{dayTime()}  \n\n金星山谷{jxwd()}\n\n火卫二\n{hw2()}',
                                       fengkong=init.CONFIG.fengkong)
        except:
            GroupEntity.send_group_msg(group_id, at_id + '正在进行昼夜更替，稍后查询哦')
    elif message == '仲裁' or message == '仲裁任务':
        GroupEntity.send_group_msg(group_id, at_id + arbitration())
    elif message[:4].lower() == 'wiki':
        GroupEntity.send_group_msg(group_id, at_id + wiki(message[4:]))
    elif message[:2] == '遗物':
        GroupEntity.send_group_forward_msg(group_id, search_relics(message[2:], True))
    elif '突击' in message and len(message) <= 5:
        if message == '突击':
            GroupEntity.send_group_msg(group_id, at_id + sortie(0))
        elif message == '国服突击':
            GroupEntity.send_group_msg(group_id, at_id + sortie(1))
        elif message == '国际服突击':
            GroupEntity.send_group_msg(group_id, at_id + sortie(2))
    elif message == '金星温度' or message == '山谷' or message == '金星':
        try:
            GroupEntity.send_group_msg(group_id, at_id + jxwd())
        except:
            GroupEntity.send_group_msg(group_id, at_id + '金星的温度现在不稳定，请稍后查询哦')
    elif message == '火卫二' or message == 'hw2':
        try:
            GroupEntity.send_group_msg(group_id, at_id + hw2())
        except:
            GroupEntity.send_group_msg(group_id, at_id + '当前查询出现了一点小状况，请联系作者修复')
    elif message == '疯狂星期四':
        GroupEntity.send_group_msg(group_id, animeImpl.crazy())
    
    elif message == '奸商' or message == '虚空商人':
        try:
            GroupEntity.send_group_msg(group_id, at_id + voidTrader())
        except:
            GroupEntity.send_group_msg(group_id, at_id + '当前查询出现了一点小状况，请联系作者修复')
    elif message == '火卫二赏金':
        GroupEntity.send_group_msg(group_id, at_id + allOutmsg('EntratiSyndicate'))
    elif message == '地球赏金':
        GroupEntity.send_group_msg(group_id, at_id + allOutmsg('Ostrons'))
    elif message == '金星赏金':
        GroupEntity.send_group_msg(group_id, at_id + allOutmsg('Solaris'))
    elif message == '达尔沃' or message == '折扣':
        GroupEntity.send_group_msg(group_id, at_id + dailyDeals())
    elif message == '地球赏金':
        GroupEntity.send_group_msg(group_id, at_id + allOutmsg('Ostrons'))
    elif message == '入侵':
        GroupEntity.send_group_msg(group_id, at_id + invade())
    elif message == '活动':
        GroupEntity.send_group_msg(group_id, at_id + allOutmsg('events'))
    elif message == '中继站轮换' or message == '泰辛':
        GroupEntity.send_group_msg(group_id, at_id + steelPath())
    elif any(str in message[:1] for str in ['打', '顶']) and len(message) < 5:
        GroupEntity.send_group_msg(group_id, at_id + memeImgGenerate.index(message))
    elif message[:2].lower() == 'wm':
        mod_rank = re.findall(f'[0-9]+', message)
        if len(mod_rank) == 0:
            mod_rank = '0'
        else:
            mod_rank = mod_rank[0]
        message = message[2:].replace(mod_rank, "").replace(" ", "")
        GroupEntity.send_group_msg(group_id, at_id + wfwm(message, mod_rank), fengkong=init.CONFIG.fengkong)