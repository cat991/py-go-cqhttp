import os, sys
from gocqhttpbot.botstart.entity import GroupEntity
import requests
import ffmpeg
def images(path):
    oo = os.path.dirname(os.path.realpath(sys.argv[0])).replace('\\', '/')
    if 'http' in path:
        return f'[CQ:image,file={path}]'

    return f'[CQ:image,file=file:///{oo}/{path}]'


def tts(txt):
    return f'[CQ:tts,text={txt}]'


def record(path):

    oo = os.path.dirname(os.path.realpath(sys.argv[0])).replace('\\', '/')
    if 'http' in path:
        return f'[CQ:record,file={path}]'
    elif os.path.exists(f'{oo}/{path}'):

        return f'[CQ:record, file=file:///{oo}/{path}]'
    else:
        return '语音文件不存在'

def download_file(path):
    url = GroupEntity.configs.get('url') + '/download_file'
    oo = os.path.dirname(os.path.realpath(sys.argv[0])).replace('\\', '/')
    data = {
        'url':f'file:///{oo}/{path}'
        # 'thread_count': 3,
        # 'headers':'User-Agent=YOUR_UA[\r\n]Referer=https://www.baidu.com'
    }
    resp = requests.post(url,data)
    print(resp.status_code)
    return resp.text
def json_formt(text):
    print(text.replace('&','&amp;').replace(',','&#44;').replace('[','&#91;').replace(']','&#93;'))
    return text.replace('&','&amp;').replace(',','&#44;').replace('[','&#91;').replace(']','&#93;')