from gocqhttpbot.botstart.impl import wfImpl
import re

def webbot(message):
    if message == '你好':
        return '好个屁'
    elif message[:2].lower() == 'rm' or message[:2].lower() == 'zk':
        message = message[2:]
        return  wfImpl.wfrm(message)
    elif message[:2] == '攻略':
        return  wfImpl.ordis(message[2:])
    elif message == '地球时间':
        return  wfImpl.earthCycle()
    elif message == '平原时间':
        try:
            return  wfImpl.dayTime()
        except:
            return  '正在进行昼夜更替，稍后查询哦'
    elif message == '平原':
        try:
            return f'夜灵平原{wfImpl.dayTime()}  \n\n金星山谷{wfImpl.jxwd()}\n\n火卫二\n{wfImpl.hw2()}'
        except:
            return '游戏内正在进行昼夜更替，稍后查询哦'
    elif message == '仲裁' or message == '仲裁任务':
        return  wfImpl.arbitration()
    elif message[:4].lower() == 'wiki':
        return  wfImpl.wiki(message[4:])

        # elif msg == '二次元':
        #     botutils.groupmsg(loginqq, group, botImpl.二次元(loginqq, group))
    elif message[:2] == '遗物':
        # return  wfImpl.search_relics(message[2:],True))
         return wfImpl.search_relics(message[2:], True)
    elif '突击' in message and len(message) <= 5:
        if message == '突击':
            return  wfImpl.sortie(0)
        elif message == '国服突击':
            return  wfImpl.sortie(1)
        elif message == '国际服突击':
            return  wfImpl.sortie(2)

    elif message[:4] == '金星温度':
        try:
            return  wfImpl.jxwd()
        except:
            return  '金星的温度现在不稳定，请稍后查询哦'
    elif message == '火卫二' or message == 'hw2':
        try:
            return  wfImpl.hw2()
        except:
            return  '当前查询出现了一点小状况，请联系作者修复'
    elif message == '菜单':
        return '暂无'

    elif message == '奸商' or message == '虚空商人':
        try:
            return  wfImpl.voidTrader()
        except:
            return  '当前查询出现了一点小状况，请联系作者修复'
    elif message == '火卫二赏金':
        return  wfImpl.allOutmsg('EntratiSyndicate')
    elif message == '地球赏金':
        return  wfImpl.allOutmsg('Ostrons')
    elif message == '金星赏金':
        return  wfImpl.allOutmsg('Solaris')
    elif message == '达尔沃' or message == '折扣':
        return  wfImpl.dailyDeals()
    elif message == '地球赏金':
        return  wfImpl.allOutmsg('Ostrons')
    elif message == '入侵':
        return  wfImpl.allOutmsg('invasions')
    elif message == '活动':
        return  wfImpl.allOutmsg('events')
    elif message[:2].lower() == 'wm':
        mod_rank = re.findall(f'[0-9]+',message)
        if len(mod_rank) == 0:
            mod_rank ='0'
        else:
            mod_rank = mod_rank[0]
        message = message[2:].replace(mod_rank,"").replace(" ","")
        # mod_rank = ''
        # if re.findall(f'[0-9]', message[2:]):
        #     mod_ranks = re.findall(f'[0-9]', message[2:].replace(" ", ""))
        #     for m in mod_ranks:
        #         mod_rank = mod_rank + m
        #     message = message[2:].replace(" ", "").replace(mod_rank, "")
        # else:
        #     mod_rank = '0'
        #     message = message[2:].replace(" ", "")
        return  wfImpl.wfwm(message, mod_rank)
    else:
        return '最少说点什么吧？'


