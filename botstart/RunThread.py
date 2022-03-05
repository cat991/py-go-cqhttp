from subprocess import Popen, PIPE, STDOUT
from flask import Flask, request
from gocqhttpbot.botstart.controller import GroupController, GuildController, SkyController,GroupHanderController
from gocqhttpbot.botstart.impl import hireImpl, skyImpl
import json, os, time
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(2)

import threading

app = Flask(__name__)

configs = {
    'textcont': 0
}


# 清空命令行
def clear():
    if configs['textcont'] == 20:
        os.system('cls')
        configs['textcont'] = 0
    else:
        configs['textcont'] += 1
    return configs['textcont']


@app.route('/', methods=['GET', 'POST'])
def index():
    data = request.get_data()
    clear()

    try:
        data = json.loads(data)
        #群消息内容
        if 'message_type' in data:
            # 处理群消息
            if data['message_type'] == 'group':
                executor.submit(GroupController.groupController, json.dumps(data))
            elif data['message_type'] == 'guild':
            #处理频道消息
                executor.submit(GuildController.guildController, json.dumps(data))
            else:
                pass
        elif 'request_type' in data:
            executor.submit(GroupHanderController.groupHanderController,json.dumps(data))
    except Exception as result:
        print(data)
        print('未知错误%s' % result)

    return request.get_data()


@app.route('/skyApi/<specified>', methods=['GET', 'POST'])
def skyApi(specified):
    return SkyController.heimao(specified)


class runapp(threading.Thread):
    def __init__(self, ):
        threading.Thread.__init__(self)

    def run(self):
        try:
            run()
        except:
            print('通信启动失败')


class runexe(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, ):
        threading.Thread.__init__(self)

    def run(self):
        try:
            exe_command('go-cqhttp_windows_386.exe')
        except:
            print('核心文件运行失败')


class runhire(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, ):
        threading.Thread.__init__(self)

    def run(self):
        try:
            time.sleep(30)
            hireImpl.die()
        except Exception as result:
            print('定时器出错%s' % result)
            time.sleep(5)
            hireImpl.die()


class runsky(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, ):
        threading.Thread.__init__(self)

    def run(self):
        try:
            time.sleep(60)
            skyImpl.die()
        except Exception as result:
            print('光遇定时器出错%s' % result)
            time.sleep(5)
            skyImpl.die()


def exe_command(command):
    """
    执行 shell 命令并实时打印输出
    :param command: shell 命令
    :return: process, exitcode
    """
    process = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)

    with process.stdout:
        print('作者Qq：2996964572')
        print('git开源地址：暂无')
        for line in iter(process.stdout.readline, b''):

            if '用户交流' in line.decode().strip() or '48;5' in line.decode().strip():
                pass
            elif '扫描二维码' in line.decode().strip():
                print(line.decode().strip())
                print('扫描当前路径下生成的qrcode.png')
            else:
                pass
                # print(line.decode().strip())

    exitcode = process.wait()
    return process, exitcode


def run():
    # app.run(host='127.0.0.1', port=5701, debug=True)
    app.run(host='0.0.0.0', port=5701, debug=False)
    app.run()
