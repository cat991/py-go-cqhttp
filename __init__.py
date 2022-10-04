
import logging
from pathlib import Path

# print("\033[31m这是红色字体\033[0m")
# print("\033[32m这是绿色字体\033[0m")
# print("\033[33m这是黄色字体\033[0m")
# print("\033[34m这是蓝色字体\033[0m")
# print("\033[38m这是默认字体\033[0m")
# '\033[1;33m[%(levelname)s] %(funcName)s (%(filename)s:%(lineno)s):\033[0m%(message)s'
logging.basicConfig(level = logging.INFO,format = '\033[33m[%(levelname)s]\033[0m \033[31m%(funcName)s (%(filename)s:%(lineno)s):\033[0m \033[34m%(message)s\033[0m')
log = logging.getLogger(__name__)
# PATH = str(Path('../').absolute()) #测试
PATH = str(Path('').absolute()) #生产