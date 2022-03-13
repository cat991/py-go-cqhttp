def groupToImgOneLin(txt,imgUrl):
    return f'[CQ:xml,data=<?xml version="1.0" encoding="UTF-8" standalone="yes"?><msg serviceID="1"><item layout="4"><title>{txt}</title><picture cover="{imgUrl}"/></item></msg>]'
def groupSmallImgToBigImg(url):
    return f'[CQ:cardimage,file={url}]'
