#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Name:        pyllk.py
# Purpose:    A python implementation of the popular game Lian Lian Kan
#
# Author:      <pro>
#
# Created:     2007/03/12
# Copyright:   (c) 2007
# Licence:     <GPL>
#-----------------------------------------------------------------------------
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Library General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#-----------------------------------------------------------------------------
# 文件：$Id$
# 版本：$Revision$


'''
Python implementation of the popular game LianLianKan.
主程序
'''
##import wxversion
##wxversion.select('2.8')
import wx
import wx.xrc as xrc
import thread
from pyllk_xrc import *
from llkboard import LlkBoard
from llkboard import EVT_UPDATE_INFOBAR
import gamerc

class PyllkAbout(xrcABOUT):
    def __init__(self, parent):
        xrcABOUT.__init__(self, parent)
        self.ABOUT_CLOSE.Bind(wx.EVT_BUTTON, self.OnClose)
        self.ABOUT_THANKS.Bind(wx.EVT_BUTTON, self.OnThanks)

    def OnClose(self, event):
##        print 'Event Triggered'
        self.Close()

    def OnThanks(self, event):
        thanks = xrcTHANKS(self)
        thanks.ShowModal()
        thanks.Fit()

class PyllkHowToPlay(xrcHOWTOPLAY):
    def __init__(self, parent):
        xrcHOWTOPLAY.__init__(self, parent)

class PyllkMainFrame(xrcMAINFRAME):
    def __init__(self, parent):
        xrcMAINFRAME.__init__(self, parent)
        self.gconf = gamerc.GameConf();

        # Define variables for the controls
        self.MAINMENUBAR = self.GetMenuBar()
        self.MENU_GAME = xrc.XRCCTRL(self, "MENU_GAME")
        self.SINGLEGAME = xrc.XRCCTRL(self, "SINGLEGAME")
        self.MENUEASY = self.MAINMENUBAR.FindItemById(xrc.XRCID("MENUEASY"))
        self.MENUNORMAL = self.MAINMENUBAR.FindItemById(xrc.XRCID("MENUNORMAL"))
        self.MENUHARD = self.MAINMENUBAR.FindItemById(xrc.XRCID("MENUHARD"))
        self.MENURESUME = self.MAINMENUBAR.FindItemById(xrc.XRCID("MENURESUME"))
        self.TWOPLAYERGAME = xrc.XRCCTRL(self, "TWOPLAYERGAME")
        self.NETPLAYGAME = xrc.XRCCTRL(self, "NETPLAYGAME")
        self.MENUGIVEUP = self.MAINMENUBAR.FindItemById(xrc.XRCID("MENUGIVEUP"))
        self.MENUQUIT = self.MAINMENUBAR.FindItemById(xrc.XRCID("MENUQUIT"))
        self.MENU_FUNC = xrc.XRCCTRL(self, "MENU_FUNC")
        self.MENUHINT = self.MAINMENUBAR.FindItemById(xrc.XRCID("MENUHINT"))
        self.MENUSHUFFLE = self.MAINMENUBAR.FindItemById(xrc.XRCID("MENUSHUFFLE"))
        self.MENUPAUSEPROCEED = self.MAINMENUBAR.FindItemById(xrc.XRCID("MENUPAUSEPROCEED"))
        self.MENUHIDE = self.MAINMENUBAR.FindItemById(xrc.XRCID("MENUHIDE"))
        self.MENU_CONF = xrc.XRCCTRL(self, "MENU_CONF")
        self.MENU_MARK = xrc.XRCCTRL(self, "MENU_MARK")
        self.MENU_ABOUT = xrc.XRCCTRL(self, "MENU_ABOUT")
        self.MENUITEM_HOWTOPLAY = self.MAINMENUBAR.FindItemById(xrc.XRCID("MENUITEM_HOWTOPLAY"))
        self.MENUITEM_ABOUT = self.MAINMENUBAR.FindItemById(xrc.XRCID("MENUITEM_ABOUT"))
        self.LABEL_DIFF = xrc.XRCCTRL(self, "LABEL_DIFF")
        self.LABEL_LEVEL = xrc.XRCCTRL(self, "LABEL_LEVEL")
        self.LABEL_LIFE = xrc.XRCCTRL(self, "LABEL_LIFE")
        self.LABEL_HINT = xrc.XRCCTRL(self, "LABEL_HINT")
        self.LABEL_CHANGE = xrc.XRCCTRL(self, "LABEL_CHANGE")
        self.GAUGE_TIME = xrc.XRCCTRL(self, "GAUGE_TIME")
        self.LABEL_SCORE = xrc.XRCCTRL(self, "LABEL_SCORE")
        self.menuOfCardType = self.GetMenuBar().FindItemById(xrc.XRCID("menu_cardType")).GetSubMenu();
        self.menuOfBgMusic = self.GetMenuBar().FindItemById(xrc.XRCID("menu_bgMusic"));
        self.menuOfGameMusic = self.GetMenuBar().FindItemById(xrc.XRCID("menu_gameMusic"));


        '''
           初始化 设置-->牌面图案 子菜单
        '''
        ctypes = self.gconf.chessTypeDict
        for ct in ctypes:
            menuItem = self.menuOfCardType.Append(-1, ctypes[ct]["name"], ct)
            self.Bind(wx.EVT_MENU, self.onChangeCardType, menuItem);
        del ctypes


        ##        PyllkMenuBar = xrcMAINMENUBAR(None)
        ##        self.SetMenuBar(PyllkMenuBar)
        self.SetBackgroundColour(wx.NullColour)
        self.board = LlkBoard(self, -1, pos = (0,20))
        self.Bind(wx.EVT_MENU, self.OnClose, id=xrc.XRCID('MENUQUIT'))
        self.Bind(wx.EVT_MENU, self.OnGiveup, id=xrc.XRCID('MENUGIVEUP'))
        self.Bind(wx.EVT_MENU, self.OnAbout, id=xrc.XRCID('MENUITEM_ABOUT'))
        self.Bind(wx.EVT_MENU, self.OnHowToPlay, id=xrc.XRCID('MENUITEM_HOWTOPLAY'))
        self.Bind(wx.EVT_MENU, self.game_start, id=xrc.XRCID('MENUEASY'), id2=xrc.XRCID('MENUHARD'))
        self.Bind(wx.EVT_MENU, self.OnHint, id=xrc.XRCID('MENUHINT'))
        self.Bind(wx.EVT_MENU, self.OnShuffle, id=xrc.XRCID('MENUSHUFFLE'))
        self.Bind(wx.EVT_MENU, self.OnPause, id=xrc.XRCID('MENUPAUSEPROCEED'))
        self.Bind(EVT_UPDATE_INFOBAR, self.update_info, id = self.board.GetId())


        self.menuOfBgMusic.Check(self.board.bgSound)
        self.menuOfGameMusic.Check(self.board.gameSound)

        self.Bind(wx.EVT_MENU, self.OnGameSound, id=self.menuOfGameMusic.GetId())
        self.Bind(wx.EVT_MENU, self.OnBgSound, id=self.menuOfBgMusic.GetId())

        self.SetIcon(gamerc.getPyllkIcon())

        thread.start_new_thread(self.PlayBgSound,())



    def PlayBgSound(self):
        '''Play a bg sound.'''
        checked = self.menuOfBgMusic.IsChecked()

        def isChecked():
            return self.menuOfBgMusic.IsChecked();

##        print 'before play...'
        if(checked):
            musicList = self.gconf.bgMusicList
            for file in musicList:
                print 'playing ',file
                try:
                   gamerc.play_music(file,callbackFn=isChecked)
                except NotImplementedError, v:
                    wx.MessageBox(str(v), "Exception Message")
        else:
            print 'playing ignored'
##        print '...after play'

    def onChangeCardType(self, event):
        name = self.menuOfCardType.GetHelpString(event.GetId()) # type name
        type = self.gconf.chessTypeDict[name]
        #print name.encode(self.gconf.encoding),type
        self.board.changeCardType(type);


    def OnGameSound(self,event=None):
        self.board.gameSound =  not self.board.gameSound
        self.menuOfBgMusic.Check(self.board.gameSound)
    def OnBgSound(self,event=None):
        self.board.gameSound = not self.board.gameSound
        self.menuOfBgMusic.Check(self.board.gameSound)
        thread.start_new_thread(self.PlayBgSound,())

    def OnClose(self, event):
        '''Exit the game.'''
        print 'Exit.'
        gamerc.stopBgMusic();
        self.Close()

    def OnGiveup(self, event):
        '''Give up the game.'''
        self.board.game_give_up()
        self.MENUGIVEUP.Enable(False)

    def OnHint(self, event):
        '''Give player a hint.'''
        self.board.game_hint()

    def OnShuffle(self, event):
        '''Shuffle cards.'''
        self.board.game_shuffle()

    def OnPause(self, event):
        '''Pause the game.'''
        self.board.game_pause()

    def OnAbout(self, event):
        about = PyllkAbout(self)
        about.ShowModal()
        about.Fit()

    def OnHowToPlay(self, event):
        PyllkHowToPlay(self).ShowModal()

    def game_start(self, event):
        '''start the game'''
        #print 'event game start'
        id = event.GetId()
        if id == xrc.XRCID('MENUEASY'):
            self.board.game_init()
            self.board.game_begin(1)
        elif id == xrc.XRCID('MENUNORMAL'):
            self.board.game_init()
            self.board.game_begin(2)
        elif id == xrc.XRCID('MENUHARD'):
            self.board.game_init()
            self.board.game_begin(3)
        self.MENUGIVEUP.Enable(True)

    def update_info(self, event):
        '''update the status label and progress bar'''
        info = event.info
        self.LABEL_DIFF.SetLabel(info.diff)
        self.LABEL_LEVEL.SetLabel(info.level)
        self.LABEL_CHANGE.SetLabel(info.change)
        self.LABEL_SCORE.SetLabel(info.score)
        self.LABEL_LIFE.SetLabel(info.life)
        self.LABEL_HINT.SetLabel(info.hint)
        self.GAUGE_TIME.SetValue(info.time)


def main():
        app = wx.App(0)
        PyllkMainFrame(None).Show()
        app.MainLoop()

if __name__ == '__main__':
    main()

