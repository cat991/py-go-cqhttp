import requests

from gocqhttpbot.botstart.dao.GroupHanderDao import switch
from gocqhttpbot.botstart.entity import CQcode
from gocqhttpbot.botstart.impl import otherImpl
import urllib.request
import json,os,sys,time
from gocqhttpbot import PATH,log
from io import BytesIO
from PIL import Image
#定义要爬取的微博大V的微博ID
uid='7360748659'

#设置代理IP
proxy_addr="122.241.72.191:808"

#每日任务
def task(specified,test=False):
    imagesCQ = ''
    botpath = PATH + f'\\频道数据\\光遇缓存数据\\{specified}.json'
    # botpath = f'E:\pythonProject\\test1\频道数据\光遇缓存数据\日常.json'
    # resp = requests.get('https://m.weibo.cn/statuses/show?id=' + get_weibo(uid)).text
    resp = ''
    try:
        with open(botpath,'r',encoding='utf-8')as f:
            # resp = f.read()

            resp = json.loads(f.read())
            f.close()
            # print(resp)
        content = resp['data']['text'].replace("<br />", '\n')
        content = re.sub(r'<[^>]+>', "", content, re.S)

        content = content[content.find("=『每日任务』="):content.find("网易云游戏")]
        testIm = otherImpl.toImage(content, 'images\\图片缓存\\光遇日常任务')
        cont = 0
        # 图片内容
        getImgs = resp['data']['pics']
        listImUrl = []
        # print(getImgs)
        for i in getImgs:
            if cont < 4 :
                imagesCQ += CQcode.images(i['large']['url'])
                listImUrl.append(i['large']['url'])
            cont += 1
        if test:
            if os.path.exists(PATH+f"/频道数据/光遇缓存数据/{specified}.jpg"):
                imagesCQ = CQcode.images(f"/频道数据/光遇缓存数据/{specified}.jpg")
            else:
                allImgToOne(specified)
                imagesCQ = CQcode.images(f"/频道数据/光遇缓存数据/{specified}.jpg")
            return imagesCQ
        else:
            return otherImpl.toImage(content, 'images\\图片缓存\\光遇日常任务') + imagesCQ
    except Exception as err:
        log.info('错误信息：%s' % err)
        log.error('------------报错0---------------')
        if get_weibo(uid, specified):
            return '无内容，请确定你要查询的内容是否存在'
        task(specified)

# 死循环监控
def die():
    while (True):
        time.sleep(40)
        if any(time.strftime("%H:%M", time.localtime()) == str for str in ['00:03', '00:10','00:15','12:05']):
            shoudong()
            allImgToOne(gettimeabbreviations()+'日常')
# 合成一张图
def allImgToOne(specified):
    imagesCQ = ''
    botpath = PATH + f'\\频道数据\\光遇缓存数据\\{specified}.json'
    # botpath = f'E:\pythonProject\\test1\频道数据\光遇缓存数据\日常.json'
    # resp = requests.get('https://m.weibo.cn/statuses/show?id=' + get_weibo(uid)).text
    resp = ''
    try:
        with open(botpath,'r',encoding='utf-8')as f:
            # resp = f.read()

            resp = json.loads(f.read())
            f.close()
            # print(resp)
        content = resp['data']['text'].replace("<br />", '\n')
        content = re.sub(r'<[^>]+>', "", content, re.S)

        content = content[content.find("======"):content.find("网易云游戏")]
        testIm = otherImpl.toImage(content, 'images\\图片缓存\\光遇日常任务')
        cont = 0
        # 图片内容
        getImgs = resp['data']['pics']
        listImUrl = []
        # print(getImgs)
        for i in getImgs:
            if cont < 4 :
                imagesCQ += CQcode.images(i['large']['url'])
                listImUrl.append(i['large']['url'])
            cont += 1

        listIm =[]
        testIm = Image.open(PATH+"\\images\\图片缓存\\光遇日常任务.png")
        width,height = testIm.size
        CH = height
        for jj in listImUrl:
            listIm.append(BytesIO(requests.get(jj).content))
        for jj in listIm:
            x, y = Image.open(jj).size
            if width < x:
                width = x
            height += y
        newImg = Image.new(mode="RGB", size=(width, height), color="#FFF")
        newImg.paste(testIm, (0, CH))
        # newImg.show()
        for jj in listIm:
            img = Image.open(jj)
            newImg.paste(img, (0, CH))
            # newImg.show()
            x, y = img.size
            CH += y
        # newImg.show()
        newImg.save(PATH+f"/频道数据/光遇缓存数据/{specified}.jpg")

    except Exception as a:
        log.info('错误信息：%s' % a)


# 手动刷新数据
def shoudong():
    get_weibo(uid,gettimeabbreviations()+'日常')
    get_weibo(uid,'P1预估兑换树')
    return '数据刷新成功'

def gettimeabbreviations()->str :
    MM = time.strftime("%m", time.localtime())
    dd = time.strftime("%d", time.localtime())
    # print(MM[1:] if MM[:1] == "0" else MM)
    # print(dd[1:] if dd[:1] == "0" else dd)
    return f'{MM[1:] if MM[:1] == "0" else MM}.{dd[1:] if dd[:1] == "0" else dd}'
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

                            # return resp
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
#     task("日常")
    # content  = re.sub(r'<[^>]+>',"",get_weibo(uid, "日常")['data']['text'],re.S)
    # print(content[:content.find("网易云游戏")])
    # print(re.compile(r'<[^>]+>', get_weibo(uid, "日常")['data']['text']))
from gocqhttpbot.botstart.entity import GroupEntity
import json, re
# 发送群消息
from gocqhttpbot.botstart.util import init
@switch("光遇")
def run(data):
    print("进入光遇")
    # data = json.loads(data)
    post_type = data['post_type']  # 消息类型
    if post_type == 'notice':
        return
    group_id = data['group_id']  # 群号
    message = data['message']  # 消息内容
    user_id = str(data['user_id'])  # 触发用户id
    at_id = f'[CQ:at,qq={user_id}]'
    if '复刻' == message or '复刻先祖' == message:
        GroupEntity.send_group_msg(group_id, at_id + task('P1预估兑换树'), False)
    elif '每日' == message or '每日任务' == message:
        GroupEntity.send_group_msg(group_id, at_id + task(gettimeabbreviations() + '日常',init.CONFIG.fengkong), False)
    elif message == '更新缓存' and user_id == str(init.CONFIG.master):
        GroupEntity.send_group_msg(group_id, at_id + shoudong())
    elif '兑换图' in message and len(message) < 8:
        GroupEntity.send_group_msg(group_id, at_id + figure(message.replace('兑换图', '')))