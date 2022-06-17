import requests,re
from gocqhttpbot.botstart.entity import CQcode
from gocqhttpbot.botstart.impl import otherImpl
import urllib.request
import json,os,sys,time
from gocqhttpbot import PATH
#定义要爬取的微博大V的微博ID
uid='7360748659'

#设置代理IP
proxy_addr="122.241.72.191:808"

#每日任务
def task(specified):
    imagesCQ = ''
    botpath = PATH + f'\\频道数据\\光遇缓存数据\\{specified}.json'
    # resp = requests.get('https://m.weibo.cn/statuses/show?id=' + get_weibo(uid)).text
    resp = ''
    try:
        with open(botpath,'r',encoding='utf-8')as f:
            # resp = f.read()

            resp = json.loads(f.read())
            f.close()
            # print(resp)
        content = re.findall('</span></a>(.*?)<a href=', resp['data']['text'])[0]
        content = content.replace('<br />', '\n')
        if '<a' in content:
            ls1 = re.findall('<a(.*?)>', content)
            for i in ls1:
                content = content.replace(i, '').replace('<a>', '').replace('</a>', '')

        if '<img' in content:
            ls2 = re.findall('<img(.*?)>', content)
            for i in ls2:
                content = content.replace(i, '').replace('<img>', '')

        if '<span' in content:
            ls3 = re.findall('<span(.*?)>', content)
            for i in ls3:
                content = content.replace(i, '').replace('<span>', '').replace('</span>', '')

        cont = 0
        # 图片内容
        getImgs = resp['data']['pics']
        # print(getImgs)
        for i in getImgs:
            if cont < 3 :
                imagesCQ += CQcode.images(i['large']['url'])
            cont += 1

        return otherImpl.toImage(content,'images\\图片缓存\\光遇日常任务')+imagesCQ
    except Exception as err:
        print('错误信息：%s' % err)
        print('------------报错0---------------')
        if get_weibo(uid, specified):
            return '无内容，请确定你要查询的内容是否存在'
        task(specified)

# 死循环监控
def die():
    while (True):
        time.sleep(60)
        if time.strftime("%H:%M", time.localtime()) == '00:03':
            get_weibo(uid,'日常')
            get_weibo(uid,'P1预估兑换树')
# 手动刷新数据
def shoudong():
    get_weibo(uid,'日常')
    get_weibo(uid,'P1预估兑换树')
    return '数据刷新成功'

#定义页面打开函数
def use_proxy(url,proxy_addr):
    req=urllib.request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    proxy=urllib.request.ProxyHandler({'http':proxy_addr})
    opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data=urllib.request.urlopen(req).read().decode('utf-8','ignore')
    return data

def get_containerid(url):
    global containerid
    data=use_proxy(url,proxy_addr)
    content=json.loads(data).get('data')
    for data in content.get('tabsInfo').get('tabs'):
        if(data.get('tab_type')=='weibo'):
            containerid=data.get('containerid')
    return containerid
# 获取json内容并保存
def get_weibo(uid,specified):
    botpaht = PATH + f'\\频道数据\\光遇缓存数据\\{specified}.json'
    i=1
    while True:
        url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+uid
        weibo_url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+uid+'&containerid='+get_containerid(url)+'&page='+str(i)
        try:
            data=use_proxy(weibo_url,proxy_addr)
            content=json.loads(data).get('data')
            cards=content.get('cards')
            if(len(cards)>0):
                for j in range(len(cards)):
                    # print("-----正在爬取第"+str(i)+"页，第"+str(j)+"条微博------")
                    card_type=cards[j].get('card_type')
                    if(card_type==9):
                        mblog=cards[j].get('mblog')
                        attitudes_count=mblog.get('attitudes_count')
                        comments_count=mblog.get('comments_count')
                        created_at=mblog.get('created_at')
                        reposts_count=mblog.get('reposts_count')
                        scheme=cards[j].get('scheme')
                        text=mblog.get('text')
                        resp = ''
                        if specified in text:
                            # print("微博地址："+str(scheme)+"\n"+"发布时间："+str(created_at)+"\n"+"微博内容："+text+"\n"+"点赞数："+str(attitudes_count)+"\n"+"评论数："+str(comments_count)+"\n"+"转发数："+str(reposts_count)+"\n")

                            # return re.findall('.<a href="/status/(.*?)">',text)[0]
                            us = re.findall('status/(.*?)\?mblogid', scheme)[0]
                            resp = requests.get('https://m.weibo.cn/statuses/show?id=' + us).text
                            resp = json.loads(resp)
                            # return re.findall('status/(.*?)\?mblogid', scheme)[0]


                            with open(botpaht,'w',encoding='utf-8') as fh:
                                json.dump(resp,fh,ensure_ascii=False)
                                fh.close()
                                return False


                        #     fh.write("----第"+str(i)+"页，第"+str(j)+"条微博----"+"\n")
                        #     print("微博地址：" + str(scheme) + "\n" + "发布时间：" + str(
                        #         created_at) + "\n" + "微博内容：" + text + "\n" + "点赞数：" + str(
                        #         attitudes_count) + "\n" + "评论数：" + str(comments_count) + "\n" + "转发数：" + str(
                        #         reposts_count) + "\n")

                            # fh.write("微博地址："+str(scheme)+"\n"+"发布时间："+str(created_at)+"\n"+"微博内容："+text+"\n"+"点赞数："+str(attitudes_count)+"\n"+"评论数："+str(comments_count)+"\n"+"转发数："+str(reposts_count)+"\n")
                i+=1
                return True
            else:
                break
        except Exception as e:
            print(e)
            return '今日任务抓取出错'
#获取官方url
def getUrl():
    resp = requests.get('https://ds.163.com/square/5cb546a0d5456870b97d9424/?type=%E4%BC%98%E8%B4%A8%E7%83%AD%E9%97%A8&page=1').text
    list = re.findall('</time></div></div>(.*?)class="user-avatar__link"', resp)
    for i in list:
        if '下一位' in i:
            content = re.findall('<a href="(.*?)"', i)
            try:
                return getContent(content[0],content)
            except :
                return '暂无新的复刻信息，请稍后再尝试查询！'
    # print(resp)
#获取url页面内的复刻内容
def getContent(suffix,conten):
    url = 'https://ds.163.com'
    resp = requests.get(url+suffix).text
    original = '原文and其他相关链接地址'
    # print(resp)
    text = re.findall('<meta data-n-head="ssr" property="og:description" content="(.*?)">',resp)[0]
    imgUrl = re.findall('<meta data-n-head="ssr" property="og:image" content="(.*?)">',resp)[0]
    img = CQcode.images(imgUrl)
    for i in conten:
        original =original + url + i+'\n'

    return text +img + original

def figure(name):
    botpaht = PATH + f'\\images\\光遇\\光遇兑换图'
    jpglist = ''
    for filename in os.listdir(botpaht):
        jpglist += filename.replace('.jpg','兑换图') + '\n'
    if os.path.exists(botpaht+f'\\{name}.jpg'):
        return CQcode.images(f'\\images\\光遇\\光遇兑换图\\{name}.jpg')
    else:
        return '\n当前兑换图未被收录，已收录兑换图有:\n' + jpglist

# if __name__ == '__main__':
#     get_weibo(uid,"日常")