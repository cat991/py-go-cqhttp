import requests,json
import re
def chouqian(msg,user_id):
    res = requests.get(f'https://api.iyk0.com/gdlq/?msg={msg}&n={user_id}')
    try:
        res = json.loads(res.text)
        if res['code'] == 200:
            data = res['title']
            data += '\n'+res['desc']
            # for i in res['data']:
            #     data += '\n'+i['sign'] + '\n'+i['sign_desc'] + '\n'
            if len(res["data"][3]) < 3:
                data += f'\n解签：\n{res["data"][0]["sign_desc"]}'
            else:
                data += f'\n解签：\n{res["data"][3]["sign_desc"]}'
        else:
            data = res['msg']
        return data
    except:
        return res.text



def yiyan():
    res = requests.get('http://api.guaqb.cn/v1/onesaid/').text

    return f'兔宝·你抽出的纸条是：🍒{res}'
def icp(url):
    res = requests.get('https://www.hlapi.cn/api/icp?url='+url).text
    return res
def duanzi():
    res = requests.get('https://www.hlapi.cn/api/gxdz').text
    return res
def wuduanzi():
    res = requests.get('https://res.abeim.cn/api-text_wu?export=json').text
    res = json.loads(res)
    return  res['content']
def ping(url):
    res = requests.get('https://res.abeim.cn/api-ping?domain='+url).text
    res = json.loads(res)
    return res

# 刷羊了个羊
def yang(id ,n,time):
    t = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQzMjcyNDYsIm5iZiI6MTY2MzIyNTA0NiwiaWF0IjoxNjYzMjIzMjQ2LCJqdGkiOiJDTTpjYXRfbWF0Y2g6bHQxMjM0NTYiLCJvcGVuX2lkIjoiIiwidWlkIjo4MzU0MzAxNCwiZGVidWciOiIiLCJsYW5nIjoiIn0.5qpiRRjxwUmN1U8Qst8dFBMWMQyWi26DcfTgHIITZds"
    url = f'https://cat-match.easygame2021.com/sheep/v1/game/user_info?uid={str(id)}&t={t}'
    # print(url)
    info = requests.get(url)
    # print(info.text)
    data = json.loads(info.text)['data']
    openID = data['wx_open_id']
    # print(openID)
    openInfo = requests.post("https://cat-match.easygame2021.com/sheep/v1/user/login_oppo",
                             data={"uid": openID, "nick_name": "黑猫", "avatar": 1, "sex": 1}).text
    # print(openInfo)
    t = json.loads(openInfo)['data']['token']
    # print(t)
    for i in range(0,int(n)):
        res =requests.get(f"https://cat-match.easygame2021.com/sheep/v1/game/game_over?rank_score=1&rank_state=1&rank_time={str(time)}&rank_role=1&skin=1&t={t}").text
        requests.get(
            f"https://cat-match.easygame2021.com/sheep/v1/game/topic_game_over?rank_score=1&rank_state=1&rank_time={time}&rank_role=1&skin=1&t={t}")
        # print(res)
    # print("昵称"+data['nick_name'])
    return f"{data['nick_name']}刷取成功，到游戏看看吧"