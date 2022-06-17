import sys
from PIL import Image
import numpy as np
import os
from gocqhttpbot import PATH



def pushImg():
    pic = ''
    try:
        pic = PATH + '\gocqhttpbot\qrcode.png'  # 获取图片路径参数
    except:
        pass
    img = Image.open(pic)  # 获取图片对象
    width = img.width  # 获取图片宽度
    height = img.height  # 获取图片高度

    gray_img = img.convert('L')  # 图片转换为'L'模式  模式“L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度

    scale = width // 200  # 图片缩放100长度
    char_lst = ' .:-=+*#%@'  # 要替换的字符
    char_len = len(char_lst)  # 替换字符的长度

    for y in range(0, height, scale):  # 根据缩放长度 遍历高度
        for x in range(0, width, scale):  # 根据缩放长度 遍历宽度
            choice = gray_img.getpixel((x, y)) * char_len // 255  # 获取每个点的灰度  根据不同的灰度填写相应的 替换字符
            if choice == char_len:
                choice = char_len - 1
            sys.stdout.write(char_lst[choice])  # 写入控制台
        sys.stdout.write('\n')
        sys.stdout.flush()


def main():
    file = PATH + '\gocqhttpbot\qrcode.png'
    img = np.array(Image.open(file).convert('L'), 'f')
    #img1=np.zeros(shape=[51,51])
    img1=img[0:img.shape[0]:5,0:img.shape[1]:5]
    img1=img1//37

    for i in range(51):
        str = "echo "
        for j in range(51):
            if img1[i,j]==0:
                str=str+'\x1b[41;31m  '
            elif img1[i,j]==1:
                str=str+'\x1b[42;31m  '
            elif img1[i,j]==2:
                str=str+'\x1b[43;31m  '
            elif img1[i,j]==3:
                str=str+'\x1b[44;31m  '
            elif img1[i,j]==4:
                str=str+'\x1b[45;31m  '
            elif img1[i,j]==5:
                str=str+'\x1b[46;31m  '
            elif img1[i, j] == 6:
                str = str + '\x1b[47;31m  '
        str = str + '\x1b[0m'
        os.system(str)