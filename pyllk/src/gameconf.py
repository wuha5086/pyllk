#-*- encoding: utf-8 -*-
# 文件：$id$
# 版本： $Revision$


import ConfigParser
#import IniFile
import string, os, sys
import codecs


def getDictListByIni(file):
    cf = ConfigParser.ConfigParser()
    #cf =IniFile.IniFile("pyllk.conf",encoding="utf-8")
    cf.read(file)
    #cf.read("pyllk.conf")
    #cf.readfp(codecs.open( "pyllk.conf", "r", "utf-8" ))
    #sEncoding = os.sys.getfilesystemencoding()

    types =[]

    # 返回所有的section
    s = cf.sections()
    #print 'section:', s
    for i in s:
       # print cf.items(i)
        m ={}
        for j in cf.options(i):
            m[j] = cf.get(i,j);
        #print m['type']
        types.append(m)
    #print types;
    return types

class GameConf():
    CHESS_CONFIG_FILE = "data/Chess/Chess.ini" # 扩展图案配置文件

    def __init__(self):
        self.chessTypeList = getDictListByIni(GameConf.CHESS_CONFIG_FILE)
        self.encoding = os.sys.getfilesystemencoding()

    if __name__ == '__main__':
        gconf = GameConf();
        types = gconf.chessTypeList;
        print types

