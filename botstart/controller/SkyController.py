import os, sys, json, re
from flask import Blueprint
sky = Blueprint("sky",__name__,url_prefix="/skyApi")

@sky.route('/<specified>', methods=['GET', 'POST'])
def skyApi(specified):
    return heimao(specified)

def heimao(specified):
    # 每日任务
    images = []
    botpath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\频道数据\\光遇缓存数据\\{specified}.json'

    resp = ''
    try:
        with open(botpath, 'r', encoding='utf-8')as f:
            # resp = f.read()

            resp = json.loads(f.read())
            f.close()

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
        if '每日任务' in content:
            content = content[content.find('----------------【每日任务】'):]

        cont=0
        # 图片内容
        getImgs = resp['data']['pics']
        for i in getImgs:
            if cont < 3:
                images.append(i['large']['url'])
            cont+=1
        return json.dumps({
            'code': 200,
            'text': content,
            'images': images
        }, ensure_ascii=False)
    except Exception as err:
        print('错误信息：%s' % err)
        return '无内容，请确定你要查询的内容是否存在'
