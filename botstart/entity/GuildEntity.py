import requests,random

from gocqhttpbot.botstart.util import permissions

configs = {
    'url': "http://127.0.0.1:5700",
    'textcont': 0
}


# 发送信息到子频道
def send_guild_channel_msg(guild_id, channel_id, message):
    url = configs.get('url') + '/send_guild_channel_msg'
    data = {
        "guild_id": guild_id,
        "channel_id": channel_id,
        "message": message+ ('\n赞 ' if random.randint(1,10) == 5  else ''),
    }
    requests.post(url, data)
    # permissions.add_msg_id(requests.post(url, data).text)

# 获取频道元数据
def get_guild_meta_by_guest(guild_id):
    url = configs.get('url') + '/get_guild_meta_by_guest'
    data = {
        'guild_id': guild_id
    }
    return requests.post(url, data).text
