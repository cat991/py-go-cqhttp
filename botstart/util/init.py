import os, sys, yaml
from gocqhttpbot import PATH

class CONFIG():
    botqq: int
    botName: str
    master: int
    max: int
    min: int
    rob: int
    unrob: int
    give: int
    msgDelet: bool
    masterId:int

def get_config():
    # print("sys.path[0] = ", sys.path[0])
    # print("os.getcwd() = ", os.getcwd())
    # config_path = os.path.join(os.getcwd(), "..") + f'\\data\\config\\config.yml'
    # config_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + f'\\data\\config\\config.yml'
    # config_path = os.path.dirname(os.path.realpath(sys.argv[0])) + f'\\data\\config\\config.yml'
    config_path = PATH + f'\\data\\config\\config.yml'
    print("读取到路径" + config_path)
    with open(config_path, "r", encoding="utf8")as f:
        config = yaml.load(f.read(), yaml.CLoader)
        CONFIG.botqq = config['botqq']
        CONFIG.master = config['master']
        CONFIG.min = config['radish']['min']
        CONFIG.max = config['radish']['max']
        CONFIG.rob = config['radish']['rob']
        CONFIG.unrob = config['radish']['unrob']
        CONFIG.give = config['radish']['give']
        CONFIG.msgDelet = config['msgDelet']
        CONFIG.botName = config['botName']
        CONFIG.masterId = config['masterId']
        # print(config)
