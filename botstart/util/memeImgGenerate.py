from gocqhttpbot.botstart.entity import GuildEntity, CQcode
from gocqhttpbot.botstart.util import textToImg
import os,sys

#表情包打
def da(text):
    try:
        text = textToImg.line_break(text, 16)
        textToImg.toImage('/images/素材/打.png', 70, 85, text, '/images/图片缓存/打.png', int(30/len(text)))
        return CQcode.images('images/图片缓存/打.png')
    except:
        return '生成失败'


#表情包顶
def ding(text):
    try:
        text = textToImg.line_break(text, 16)
        textToImg.toImage('/images/素材/支持.png', 200, 110, text, '/images/图片缓存/支持.png', int(200/len(text)))
        return CQcode.images('images/图片缓存/支持.png')
    except:
        return '生成失败'
#入口
def index(message):
    if message[:1] == '打':
        return da(message[1:])
    elif message[:1] == '顶':
        return ding(message[1:])