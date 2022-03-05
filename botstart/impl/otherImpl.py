from PIL import Image, ImageDraw, ImageFont
from gocqhttpbot.botstart.entity import CQcode
import win32api,win32con,os
from bot.langconv import *
LINE_CHAR_COUNT = 30*2  # 每行字符数：30个中文字符(=60英文字符)
CHAR_SIZE = 30
TABLE_WIDTH = 4

def TraditionalToSimplified(line):          #繁体转简体
    line=Converter("zh-hans").convert(line)
    return line


def SimplifiedToTraditional(line):          #简体转繁体
    line=Converter("zh-hant").convert(line)
    return line


def line_break(line):
    ret = ''
    width = 0
    for c in line:
        if len(c.encode('utf8')) == 3:  # 中文
            if LINE_CHAR_COUNT == width + 1:  # 剩余位置不够一个汉字
                width = 2
                ret += '\n' + c
            else: # 中文宽度加2，注意换行边界
                width += 2
                ret += c
        else:
            if c == '\t':
                space_c = TABLE_WIDTH - width % TABLE_WIDTH  # 已有长度对TABLE_WIDTH取余
                ret += ' ' * space_c
                width += space_c
            elif c == '\n':
                width = 0
                ret += c
            else:
                width += 1
                ret += c
        if width >= LINE_CHAR_COUNT:
            ret += '\n'
            width = 0
    if ret.endswith('\n'):
        return ret
    return ret + '\n'

#获取桌面路径
def get_desktop():
    key =win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',0,win32con.KEY_READ)
    return win32api.RegQueryValueEx(key,'Desktop')[0]

#开始制作图片
def toImage(txt,path):
    output_str = line_break(txt)
    d_font = ImageFont.truetype('C:/Windows/Fonts/simsun.ttc', CHAR_SIZE)
    lines = output_str.count('\n')  # 计算行数

    image = Image.new("L", (LINE_CHAR_COUNT*CHAR_SIZE // 2, CHAR_SIZE*lines), "white")
    draw_table = ImageDraw.Draw(im=image)
    draw_table.text(xy=(0, 0), text=output_str, fill='#000000', font= d_font, spacing=4)  # spacing调节机制不清楚如何计算

    # image.show()  # 直接显示图片
    image.save(os.path.dirname(os.path.realpath(sys.argv[0]))+'\\'+path+'.png', 'PNG')  # 保存在当前路径下，格式为PNG
    image.close()
    return CQcode.images(path+'.png')