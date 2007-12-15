#!/usr/bin/env python
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

'''
Python implementation of the popular game LianLianKan.
'''
##import wxversion
##wxversion.select('2.8')
import wx
import wx.xrc as xrc

from pyllk_xrc import *
from llkboard import LlkBoard
from llkboard import EVT_UPDATE_INFOBAR
from llkrc import *

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
        self.LABEL_DIFF.SetLabel(event.info[0])
        self.LABEL_LEVEL.SetLabel(event.info[1])
        self.LABEL_CHANGE.SetLabel(event.info[2])
        self.LABEL_SCORE.SetLabel(event.info[3])
        self.LABEL_LIFE.SetLabel(event.info[4])
        self.LABEL_HINT.SetLabel(event.info[5])
        self.GAUGE_TIME.SetValue(event.info[6])
        

def main():
    app = wx.App()
    PyllkMainFrame(None).Show()
    app.MainLoop()
    
if __name__ == '__main__':
    main()

