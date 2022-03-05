from gocqhttpbot.botstart.entity import GuildEntity, CQcode
from gocqhttpbot.botstart.util import textToImg
import os,sys

def sign(guild_id, channel_id,user_id,at_user,message):
    botpath = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\频道数据\\功能菜单.json'
    if message[:4] == '修改功能' and user_id == '144115218676755577':
        with open(botpath , 'w' ,encoding='utf-8')as f:
            f.write(message[4:])
            f.close()
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '修改成功')
    elif message == '功能':
        try:
            with open(botpath, 'r', encoding='utf-8') as f:
                text = f.read()
                f.close()
                text = textToImg.line_break(text,16)
                textToImg.toImage('/images/素材/rabbitText.jpg',100,280,text,'/images/图片缓存/菜单.png',80)
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + CQcode.images('images/图片缓存/菜单.png'))
        except:
            GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '联系作者编写功能')
    else:
        GuildEntity.send_guild_channel_msg(guild_id, channel_id, at_user + '你没有权限进行修改')


def warframe(cha):
    pass