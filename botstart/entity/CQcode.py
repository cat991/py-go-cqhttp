import os, sys


def images(path):
    oo = os.path.dirname(os.path.realpath(sys.argv[0])).replace('\\', '/')
    if 'http' in path:
        return f'[CQ:image,file={path}]'
    return f'[CQ:image,file=file:///{oo}/{path}]'


def tts(txt):
    return f'[CQ:tts,text={txt}]'


def record(path):
    oo = os.path.dirname(os.path.realpath(sys.argv[0])).replace('\\', '/')
    if 'http' in path:
        return f'[CQ:record,file={path}]'

    return f'[CQ:image,file=file:///{oo}/{path}.mp3]'
