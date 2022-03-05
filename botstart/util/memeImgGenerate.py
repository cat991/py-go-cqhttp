from gocqhttpbot.botstart.entity import GuildEntity, CQcode
from gocqhttpbot.botstart.util import textToImg
import os,sys

#表情包打
def da(guild_id, channel_id,text,at_user):
    try:
        text = textToImg.line_break(text, 16)
        textToImg.toImage('/images/素材/打.png', 70, 85, text, '/images/图片缓存/打.png', int(30/len(text)))
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + CQcode.images('images/图片缓存/打.png'))
    except:
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '生成失败')


#表情包顶
def ding(guild_id, channel_id,text,at_user):
    try:
        text = textToImg.line_break(text, 16)
        textToImg.toImage('/images/素材/支持.png', 200, 110, text, '/images/图片缓存/支持.png', int(200/len(text)))
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + CQcode.images('images/图片缓存/支持.png'))
    except:
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '生成失败')

#入口
def index(guild_id, channel_id,message,at_user):
    if message[:1] == '打':
        da(guild_id,channel_id,message[1:],at_user)
    elif message[:1] == '顶':
        ding(guild_id,channel_id,message[1:],at_user)