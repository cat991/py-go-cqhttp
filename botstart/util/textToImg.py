from PIL import ImageFont, Image, ImageDraw
import os,sys
def toImage(imageFile,x,y,text,pathName,size):
    oo = os.path.dirname(os.path.realpath(sys.argv[0]))
    imageFile = oo + imageFile
    pathName = oo + pathName
    # 导入本地字体路径及设置字体大小
    font = ImageFont.truetype(oo+"/images/字体/kuaile.ttf", size)
    # 打开本地所需图片
    im1 = Image.open(imageFile)

    # 在图片上添加文字
    draw = ImageDraw.Draw(im1)
    draw.text(xy=(x, y), text=text, font=font,fill=(1, 0, 0))

    im1.save(pathName)

'''
line=text
size=多少字换行
'''
def line_break(line,size):
    LINE_CHAR_COUNT = size * 2  # 每行字符数：30个中文字符(=60英文字符)
    TABLE_WIDTH = 4
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
