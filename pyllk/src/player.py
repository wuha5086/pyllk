#-*- encoding: utf-8 -*-
# 文件：$Id$
# 版本：$Revision$

'''
$copyright$
'''

import threading
import time
import codecs
import pygame
import wx
import gamerc
import  pygame.time

class MediaPlayer(object):
    '''

    '''
    STATUS_STOP = 0
    STATUS_PLAYING = 1
    STATS_PAUSE = 2

    playList = None #
    curItem = None # 当前播放条目

    def __init__(self,playList=None):
        self.status = MediaPlayer.STATUS_STOP #当前状态
        self._stopevent = threading.Event()
        self.playList = playList
        self.playerThead = None

    def play(self):
        '''
         play media
        '''
        print "in playing..."
        if self.playerThead == None:
            self.playerThead = PlayerThead(self);
            self.playerThead.setDaemon(True)
            self.playerThead.start();
            self.status = MediaPlayer.STATUS_PLAYING
        else:
            print " is running ignored!"

    def pause(self):
        '''
        暂定播放
        '''
        print "in pause"
        self.__stopPlayThread();
        self.status=MediaPlayer.STATS_PAUSE;

    def playFile(self):
        ''' 实际的播放代码,子类override此方法以实现对应的播放 '''
        pass

    def getNextSong(self,cur=None):
        '''获取下一首 '''
        v = None
        if cur == None:
            v = self.playList[0]
        else:
            i = self.playList.index(cur);
            if( i >= 0 and i < self.playList.__len__()) :
                v = self.playList[i+1]
            else:
                v = self.playList[0]
        return v

    def run(self):
        if(self.playList != None ):
            while not self._stopevent.isSet(): #使音乐能循环重复播放
                #for file in self.playList:
                file = self.getNextSong(self.curItem)
                print 'playing ',file
                self.curItem = file
                try:
                   self.playFile(file)
                except NotImplementedError, v:
                    wx.MessageBox(str(v), "Exception Message")
        pass

    def __stopPlayThread(self):
        ''' 结束当前的播放线程 '''
        self._stopevent.set()
        clock = pygame.time.Clock()
        print "waiting for stop..."

        while( self.playerThead != None  and self.playerThead.isAlive() ):
             print "waiting for stop..."
             clock.tick(35)
        pygame.mixer.music.stop()
        self.playerThead = None
        self._stopevent =  threading.Event();

    def stop(self):
        '''
        stop media
         调用此方法将重新回到原始状态
        '''
        print "in stop"
        self.__stopPlayThread();
        self.curItem =None
        self.status=MediaPlayer.STATUS_STOP

    def isPlaying(self):
        return self.status == MediaPlayer.STATUS_PLAYING


class PlayerThead(threading.Thread):

    def __init__(self, player):
        threading.Thread.__init__(self)
        assert isinstance(player,MediaPlayer)
        self.player = player

    def run(self):
        self.player.run()


class MidiPlayer(MediaPlayer):
    __mixer_inited = False
    def __init__(self,playList=None):
        super(MidiPlayer,self).__init__(playList);
        if(not self.__mixer_inited ):
            freq = 44100    # audio CD quality
            bitsize = -16   # unsigned 16 bit
            channels = 2    # 1 is mono, 2 is stereo
            buffer = 1024    # number of samples
            pygame.mixer.init(freq, bitsize, channels, buffer)
            self.__mixer_inited == True

    def playFile(self,music_file):
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
        try:
            pygame.mixer.music.play()
            while not self._stopevent.isSet() and pygame.mixer.music.get_busy():
                # check if playback has finished
                #print "check if playback has finished"
                clock.tick(30)
        except:
            print "error!"

    def run(self):
        super(MidiPlayer,self).run()











if __name__ == '__main__':
    playList = gamerc.listFiles("data/MID/","[.]mid$")
    player = MidiPlayer(playList);
    player.play();
    time.sleep(5)
    player.stop();

    time.sleep(5)


    player.play();

    print player.status