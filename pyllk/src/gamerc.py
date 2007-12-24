#-*- encoding: utf-8 -*-
# 文件：$Id$
# 版本：$Revision$
'''
    rc = Resource Config
    This is a resource config module of game.

'''
import re
import wx
import ConfigParser
#import IniFile
import string, os, sys
import codecs

def getImagePath(name):
    '''Returns the full path of a picture used in the game.
       name 应该相应的扩展名
    '''

    prefix = 'llk_classic/'
    fullname = prefix+ name # + '.png'
    #print fullname
    return fullname

def getBackImagePath(no):
    ''' Return the full path of background picture
        no - the number of the pricture
    '''

    prefix = 'llk_classic/'
    name = str(no)
    fullname = prefix+ 'back' + name + '.jpg'
    return fullname

def getPyllkIcon():
    ''' get game icon      '''
    icon = wx.EmptyIcon()
    icon.CopyFromBitmap(wx.Bitmap('llk_classic/logo.png'))
    return icon

def get_sound_path(name):
    '''Returns the full path of a sound file used in the game.'''
    prefix = 'sound/'
    name = str(name)
    fullname = prefix + name
    return fullname

def getDictsByIni(file):
    '''
        转换ini文件成对应的dicto数组

    '''
    cf = ConfigParser.ConfigParser()
    #cf =IniFile.IniFile("pyllk.conf",encoding="utf-8")
    cf.read(file)
    #cf.read("pyllk.conf")
    #cf.readfp(codecs.open( "pyllk.conf", "r", "utf-8" ))
    #sEncoding = os.sys.getfilesystemencoding()

    types ={}

    # 返回所有的section
    s = cf.sections()
    #print 'section:', s
    for i in s:
       # print cf.items(i)
        m ={}
        for j in cf.options(i):
            m[j] = cf.get(i,j);
        #print m['type']
        types[i]=m
    #print types;
    return types

class GameConf():
    CHESS_CONFIG_FILE = "data/Chess/Chess.ini" # 扩展图案配置文件

    def __init__(self):
        self.chessTypeDict = getDictsByIni(GameConf.CHESS_CONFIG_FILE)
        self.encoding = os.sys.getfilesystemencoding()

if __name__ == '__main__':
    gconf = GameConf();
    types = gconf.chessTypeDict;
    for t in types:
        print t,types[t]
