import json, time, re
import requests
from gocqhttpbot.botstart.impl import otherImpl
from gocqhttpbot.botstart.entity import GroupEntity

import os, sys

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
    return '\t\n' + requests.get('http://nymph.rbq.life:3000/wf/robot/' + msg).text


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
        hours = time.strftime('%H', time.localtime(times))
        hours = int(hours) - 8
        time1 = time.strftime('%M分%S秒', time.localtime(times))
        return f'\t\n现在时间是--白天--\n剩余时间:{hours}时{time1}'
    else:
        times = times - int(time.time())
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
    times = times - int(time.time())
    time1 = time.strftime('%M分%S秒', time.localtime(times))
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


# warframe物品交易
def wfwm(msg, mod_rank):
    str = {}
    str['itme'] = botci(msg)
    str['mod_rank'] = int(mod_rank)
    str['str'] = msg
    resp = requests.get(
        f'https://api.warframe.market/v1/items/{str["itme"].replace(" ", "_").lower()}/orders?include=item')
    resp = json.loads(resp.text)
    try:
        orderslist = resp['payload']['orders']
        orderslist = sorted(orderslist, key=lambda x: x["platinum"], reverse=False)

        orderre = f'\t\n默认展示价格最低前10个\n你要搜索的是：{str["str"]} \n翻译：{str["itme"]}'
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

    if cont == 0:
        return '\t\n没有该商品或并没有查到该等级的商品'
    else:
        return orderre + f'\n总出售人数{conts}人，平均:{int(number / conts)}白鸡'


# 翻译&warframe查字典
def botci(str):
    resp = requests.get(f'http://nymph.rbq.life:3000/dict/tran/robot/{str.replace(" ", "")}').text
    num = 0
    # ret ={}
    txt = ''
    for lis in resp.split('\n'):
        num += 1
        if num == 2:
            itme = re.findall(f'\\[(.*?)]', lis)
            txt = itme[0]
            # txt = itme[0].replace(' ', '_').lower()
            # ret={
            #     'itme':itme[0].replace(' ', '_').lower(),
            #      'str':itme[0],
            #     'mod_rank':mod_rank
            # }
    try:
        # return wfwm(ret)
        return txt
    except:
        return resp
#获取商品折扣
def dailyDeals():
    resp = requests.get('https://api.null00.com/world/ZHCN')
    resp = json.loads(resp.text)['dailyDeals']
    dail1 = '国服折扣：'
    for i in resp:
        item = i['item']   #商品名称
        times = i['expiry'] - time.time() #剩余时间
        discount = str(i['discount']) + '%'#折扣百分比
        originalPrice = i['originalPrice']#原价
        salePrice = i['salePrice'] #折扣后的价格
        residue = i['total'] - i['sold'] #剩余库存
        time1 = time.strftime('%H时%M分%S秒', time.localtime(times))
        dail1 += f'\n商品:{item} (-{discount})\n价格:{salePrice}({originalPrice})\n库存:{residue} \n时间:还剩余{time1}\n'
    dail2 = '\n国际服折扣：'+allOutmsg('dailyDeals')
    return  dail1 + dail2

# 发送群公告
def group_announcement(logonqq, msg):
    list = GroupEntity.getgrouplist(logonqq)
    for i in list:
        GroupEntity.groupmsg(logonqq, i['groupnum'], msg)


# 遗物查询功能
def search_relics(search):
    url = f'https://www.ourwarframe.com/app/api/index/list?page=1&pageSize=10&search={search}&type&stock'
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

    return ret


# 菜单
def caidan():
    return f'\t\n你要的菜单来了' \
           f'\n---菜单---' \
           f'\n攻略  关键词' \
           f'\nwiki  关键词' \
           f'\n物品交易: wm ' \
           f'\n紫卡交易：rm & zk' \
           f'\n平原时间 & 地球时间' \
           f'\n金星温度 ' \
           f'\n火卫二 & hw2' \
           f'\n虚空商人 & 奸商 ' \
           f'\n双服突击 ' \
           f'\n仲裁 & 仲裁任务' \
           f'\n查询口令' \
           f'\n遗物 关键词(仅支持国服)' \
           f'\n ↓↓↓频道主命令↓↓↓' \
           f'\n屏蔽 & 关闭' \
           f'\n接触屏蔽 & 开启'
