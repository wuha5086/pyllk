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

from pyllk_xrc import *
from llkboard import LlkBoard
from llkboard import EVT_UPDATE_INFOBAR
from llkrc import *
import gameconf

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
        self.gconf = gameconf.GameConf();

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
        #self.mnFile = self.MAINMENUBAR.GetMenu(self.MAINMENUBAR.FindMenu("MENU_CONF"))
        self.menuOfCardType= self.GetMenuBar().FindItemById(xrc.XRCID("menu_cardType")).GetSubMenu();

        '''
        self.mnFile= self.GetMenuBar().FindItemById(xrc.XRCID("menu_cardType")).GetSubMenu();
        cfg=[['a', 'this is a'],['b', 'this is b'],['C', 'this is C']]
        for i in cfg:
            #exec 'self.IDmnFile%s =%d' % (i[0],wx.NewId() )  in locals()
            #print eval('self.IDmnFile%s' % i[0])
            menuItem = self.mnFile.Append(-1, i[0], i[1])
            self.Bind(wx.EVT_MENU, self.event, menuItem)
        '''
        ctypes = self.gconf.chessTypeList
        for ct in ctypes:
            menuItem = self.menuOfCardType.Append(-1, ct["name"], ct["name"])
            self.Bind(wx.EVT_MENU, self.onChangeCardType, menuItem);



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


        self.SetIcon(getPyllkIcon())

    def onChangeCardType(self, event):
        print self.menuOfCardType.GetHelpString(event.GetId()).encode(self.gconf.encoding)
        pass

    def OnClose(self, event):
        '''Exit the game.'''
        print 'Exit.'
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

