
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
import stat
import codecs
import pygame

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

def listFiles(path,reStr=None):
    '''
        path: 路径 ; reStr : 匹配的正则表达式过滤条件,默认为None即不进行过滤

        返回path下文件路径列表
    '''
    names = os.listdir(path)
    files =[];
    for name in names:
        if(reStr != None and re.search(reStr,name) == None):
            continue
        try:
            fp = os.path.join(path, name);
            st = os.lstat(fp)
        except os.error:
            continue
        if not stat.S_ISDIR(st.st_mode) :
           fp = os.path.abspath(fp)
           files.append(fp)
    return files;

__mixer_inited = False


def play_music(music_file,callbackFn = None):
    if(not __mixer_inited ):
        freq = 44100    # audio CD quality
        bitsize = -16   # unsigned 16 bit
        channels = 2    # 1 is mono, 2 is stereo
        buffer = 1024    # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)
        __mixer_inited == True

    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(0.8)

    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print "Music file %s loaded!" % music_file
    except pygame.error:
        print "File %s not found! (%s)" % (music_file, pygame.get_error())
        return
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        # check if playback has finished
        print "check if playback has finished"
        if( callbackFn != None):
            cabllbackFn()
        clock.tick(30)


class GameConf():
    CHESS_CONFIG_FILE = "data/Chess/Chess.ini" # 扩展图案配置文件

    def __init__(self):
        self.chessTypeDict = getDictsByIni(GameConf.CHESS_CONFIG_FILE)
        self.encoding = os.sys.getfilesystemencoding()
        self.bgMusicList = listFiles("data/MID","[.]mid$")

if __name__ == '__main__':
    gconf = GameConf();
    types = gconf.chessTypeDict;
    for t in types:
        print t,types[t]

    files = listFiles("data/MID/","[.]mid$")
    print files
