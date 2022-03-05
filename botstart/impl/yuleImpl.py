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