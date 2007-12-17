#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Name:        llkboard.py
# Purpose:    A python implementation of the popular game Lian Lian Kan
#                   This is a general llk board.
#
# Author:      <pro>
#
# Created:     2007/03/12
# Last updated:2007/07/27
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
This module contains the LlkBoard class which is a window that llk games can be played upon.
'''
##import wxversion
##wxversion.select('2.8')
import wx
import thread
import time
from llkrc import *
import random
from llkgame import *

myEVT_UPDATE_INFOBAR = wx.NewEventType()
EVT_UPDATE_INFOBAR = wx.PyEventBinder(myEVT_UPDATE_INFOBAR, 1)


class GameStatus():
    '''
     此代表当前游戏的状态
    '''
    def __init__(self, diff="",level=0,life=0,hint=0,change="",time=0,score=0):
         self.diff  = diff    #难度
         self.level = level   #等级
         self.life  = life    #生命
         self.hint  = hint    #提示
         self.change= change  #变化
         self.time  = time    #时间
         self.score = score   #成绩

class MyEvent(wx.PyCommandEvent):
    '''Custom event class
    In this case, it is used to deliver info to the father window to update the info bar.'''
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.info = None

    def SetMyVal(self, info):
        self.info = info

    def GetMyVal(self):
        return self.info

class LlkBoard(wx.Window):
    '''This class provides a window that lianliankan game can be played upon.
    It uses wxWidgets and is platform-independent.
    It is reusable and can be used where needs a llk game window.
    '''
    UI_FIXED_START_DRAW_LEFT = 120   #3*(UI_BACK_WIDTH-UI_BACK_BORDER_1)
    UI_FIXED_START_DRAW_TOP = 30
    UI_BACK_WIDTH = 46
    UI_BACK_HEIGHT = 56
    UI_BACK_BORDER_1 = 6
    UI_BACK_BORDER_2 = 6
    UI_IMAGE_SIZE = 32
    MAX_PATH_LENGTH = 300

    def __init__(self, parent, ID, pos = (0, 0), callback = None):
        '''Initialize LlkBoard
        Load resources needed to run the game
        Initialize buffer
        Bind events.'''
        wx.Window.__init__(self, parent, ID, size = (720,480), pos = pos)
##        self.SetBackgroundColour("LIGHTBLUE")
        self.rect = self.GetClientRect()
        self.cdc = wx.ClientDC(self)
##        self.cdc.SetBackground(wx.Brush('CYAN'))
        self.InitBuffer()
##        self.DrawBG(0)
        self.load_resource()
        self.DrawMainBack()
        self.callback = callback    #set callback function
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)    #drawing area clicked
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        # and the refresh event
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)  #for test

        self.game = llkgame()   #create game instance

    def InitBuffer(self):
        """Initialize the bitmap used for buffering the display."""
        size = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(size.width, size.height)
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.SetBackground(wx.Brush('BLACK'))
        dc.Clear()


    def OnLeftDown(self, event):
        """Called when the left mouse button is pressed"""
        pass


    def OnLeftUp(self, event):
        '''
        Called when the left mouse button is released
        in this case, it means the drawing area is clicked
        '''
        if self.game.status == self.game.ALGORITHM_GAME_RUN:
            pos = event.GetPosition()
##            if pos.x < 20 and pos.y < 20:
##                self.game_next_level()      #debug--next level

            if (pos.x > LlkBoard.UI_FIXED_START_DRAW_LEFT - \
            self.game.difficulty*(LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1) and
            pos.x < LlkBoard.UI_FIXED_START_DRAW_LEFT +\
            (self.game.col-self.game.difficulty)*(LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1)):
                if (pos.y > LlkBoard.UI_FIXED_START_DRAW_TOP and
                pos.y < LlkBoard.UI_FIXED_START_DRAW_TOP + self.game.row*(LlkBoard.UI_BACK_HEIGHT-LlkBoard.UI_BACK_BORDER_2)):
                    j = (pos.x - LlkBoard.UI_FIXED_START_DRAW_LEFT + \
                    self.game.difficulty*(LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1))/(LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1)
                    i = (pos.y - LlkBoard.UI_FIXED_START_DRAW_TOP)/(LlkBoard.UI_BACK_HEIGHT-LlkBoard.UI_BACK_BORDER_2)
                    if self.game.data[i][j] == 0:
                        return False
                    if self.ui_point1.x > -1:   #there is a selected card already
                        if self.ui_point1.x != i or self.ui_point1.y != j:
                            self.ui_point2.x = i
                            self.ui_point2.y = j
                            #look if the two selected card could be linked or not, if yes,delete
                            #them,if no,cancel the selected status
                            if self.game.can_link(self.ui_point1,self.ui_point2,None):
##                                print 'This pairs can link.'    #for test
                                self.link(self.ui_point1, self.ui_point2)
                                self.game.link(self.ui_point1, self.ui_point2)
                                #algorithm_link,must be put after ui_link function, because ui_link need
                                #to judge the link path,and before this,the data must not be modified
                                self.progress_timeout(1) #add 1 second after every link action
                                #update info bar
                                self.refresh_top()
                                #sound effect
                                thread.start_new_thread(self.play, ('Link.wav',))
                                #SLEEP 0.2 SECONDS
                                time.sleep(0.1)
                                #judge if current situation of all the cards has a solution
                                #ATTENTION: must judge after the game_change funtion
                                self.game_change(self.ui_point1, self.ui_point2)
                                self.ui_point1 = wx.Point(-1, -1)
                                self.ui_point2 = wx.Point(-1, -1)
                                tmp = self.game.game_no_solution()
                                if tmp == 1:    #No solution,but there are still some cards
                                    self.game_shuffle()
                                elif tmp == 0:
                                    pass    #do nothing
                                elif tmp == 2:  #there are no cards,the stage(or Level) is over
                                    self.game_next_level()
                            else:
##                                print 'This pairs cannot link.'    #for test
                                self.redraw_images()    #ui_redraw_images, this function does not care the selected status
                                self.ui_point1 = wx.Point(-1, -1)    #NOTE
                                #restore the card image at (i,j)
                                #sound effect
                                thread.start_new_thread(self.play, ('CanntLink.wav',))
                        else:   #click the card that has already been selected,so cancel the selected status
                            self.ui_point1 = wx.Point(-1, -1)
                            self.ui_point2 = wx.Point(-1, -1)
                            self.redraw_images()
                            #replace the card image at (i,j)
                            #sound effect
                            thread.start_new_thread(self.play, ('Cancel.wav',))
                    else:   #there is no selected cards
                        self.ui_point1 = wx.Point(i, j)
                        self.ui_point2 = wx.Point(-1, -1)
                        self.replace_image(self.ui_point1, self.ui_point2) #replace card image at (i,j)
                        #sound effect
                        thread.start_new_thread(self.play, ('Click.wav',))
##                    print self.ui_point1, self.ui_point2    #for test
            return True
        else:
            return False

    def OnRightUp(self, event):
        '''Called when the right mouse button is released'''
        if self.game.status == self.game.ALGORITHM_GAME_RUN:
##            pos = event.GetPosition()
##            if pos.x < 20 and pos.y < 20:   #only for test
##                self.game_over(0)      #debug--game over

            if self.ui_point1.x > -1:   #cancel the selected status
                self.redraw_images()
                self.ui_point1 = wx.Point(-1, -1)
                thread.start_new_thread(self.play, ('Cancel.wav',))
            return True
        return False

    def OnMotion(self, event):
        """
        Called when the mouse is in motion.  If the left button is
        dragging then draw a line from the last event position to the
        current one.  Save the coordinants for redraws.
        """
        if event.Dragging() and event.LeftIsDown():
            dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
##            dc.SetPen(self.pen)
            pos = event.GetPosition()
##            coords = (self.pos.x, self.pos.y, pos.x, pos.y)
##            self.curLine.append(coords)
##            dc.DrawLine(*coords)
##            self.pos = pos
##            dc.DrawLine(pos.x, pos.y, pos.x+20, pos.y+20)
            dc.DrawPoint(pos.x, pos.y)

    def OnPaint(self, event):
        """
        Called when the window is exposed.
        """
        # Create a buffered paint DC.  It will create the real
        # wx.PaintDC and then blit the bitmap to it when dc is
        # deleted.  Since we don't need to draw anything else
        # here that's all there is to it.
        dc = wx.BufferedPaintDC(self, self.buffer)

    def OnTimer(self, event):
        '''Timer event handler.'''
        self.progress_timeout(0)    #reduce the time normally

    def game_init(self):
        '''Init, ready to have fun!'''
##        self.game = llkgame()
        self.game.__init__()        #TODO:!NOTICE! problems with re-initialization.improve later
        self.time_remain = 0
        self.ui_point1 = wx.Point(-1, -1)
        self.ui_point2 = wx.Point(-1, -1)
        self.refresh_top()
        self.DrawMainBack()
        return True
        #need polishing

    def get_back(self):
        '''Get a background picture.'''
        rect = self.GetClientRect() #get rect
        (clipx, clipy, clipw, cliph) = rect.Get()
##        self.bgchoice = random.randint(0,15)
        if self.bgchoice is None:
            bg = wx.Bitmap(get_image_path(random.randint(0,20))) #.GetSubBitmap(rect)
        elif self.bgchoice < 20:
            self.bgchoice += 1
        else:
            self.bgchoice = 0
        (bw, bh) = bg.GetSize()
        sizew = min(clipw, bw)
        sizeh = min(cliph, bh)
##        print clipw,bw,cliph,bh #for test
        clip = wx.Rect((bw-sizew)/2, (bh-sizeh)/2, sizew, sizeh)
        self.bg = bg.GetSubBitmap(clip)
        self.bgpos = wx.Point((clipw-sizew)/2,(cliph-sizeh)/2)

    def load_resource(self):
        '''
        Load resources needed for playing the game.
        Return value: True for success, False for failure.
        '''
        #get background image
        self.bgchoice = None
        self.get_back()
##        rect = self.GetClientRect() #get rect
##        (clipx, clipy, clipw, cliph) = rect.Get()
##        bg = wx.Bitmap(get_image_path(random.randint(0,15))) #.GetSubBitmap(rect)
##        (bw, bh) = bg.GetSize()
##        sizew = min(clipw, bw)
##        sizeh = min(cliph, bh)
##        print clipw,bw,cliph,bh #for test
##        clip = wx.Rect((bw-sizew)/2, (bh-sizeh)/2, sizew, sizeh)
##        self.bg = bg.GetSubBitmap(clip)
##        self.bgpos = wx.Point((clipw-sizew)/2,(cliph-sizeh)/2)

        #get a bitmap for each cardimage
        self.cardimages = []
        img = wx.Bitmap(get_image_path('cardimages.png'))
        for i in range(0, LlkBoard.UI_IMAGE_SIZE):
            self.cardimages.append(img.GetSubBitmap(wx.Rect(32*i, 0, 32, 32)))
        del img #of no use from now on, delete it

        #get a bitmap for each cardback
        self.cardbacks = []
        img = wx.Bitmap(get_image_path('cardbacks.png'))
        for i in range(0, 6):   #TODO: convert these to a variable later
            self.cardbacks.append(img.GetSubBitmap(wx.Rect(0, 56*i, 46, 56)))
        del img #of no use from now, delete it

        self.vertical = wx.Bitmap(get_image_path('vertical.png'))
        self.horizon = wx.Bitmap(get_image_path('horizon.png'))
        self.pause = wx.Bitmap(get_image_path('pause.jpg'))
        self.mainback = wx.Bitmap(get_image_path('mainback.jpg'))   #get initial back image
        self.cardback_choice = random.randint(0, 5)

        return True #TODO: Needs polishing

    def game_next_level(self):
        '''
        Next Levels
        if the current level is not the last one(NO.10),then,enter the next level
        otherwise,popup a window,on which give a hint that the player have success
        this difficulty,then over the game,waiting for player to choose another difficulty.
        '''
        #TODO: change background image
        self.timer.Stop()
        if self.game.game_next_level():
            thread.start_new_thread(self.play, ('Win.wav',))
            self.get_back()
            if self.cardback_choice >= 5:
                self.cardback_choice = 0
            else:
                self.cardback_choice += 1
            self.redraw_images()
            self.refresh_top()
            self.ui_point1 = wx.Point(-1, -1)
            self.ui_point2 = wx.Point(-1, -1)
            self.progress_timeout(9999)
            self.refresh_top()
            self.timer.Start()
        else:
            self.game_over(True)

    def game_over(self, success):
        '''Game Over.'''
        self.timer.Stop()
        if success:
            #popup dialog window
            messages = (u'恭喜恭喜,你已经通过"简单"难度,玩玩"一般"吧!',
             u'好利害哦,"一般"都过了,挑战"困难"吧!',
             u'通关了?!什么也不说了，一个字………………牛X')
            msg = messages[self.game.difficulty]
            type  = wx.ICON_INFORMATION
        else:
            #popup dialog window
            msg = u'胜败乃兵家常事,大侠重新来过吧!'
            type = wx.ICON_WARNING

        if success:
            thread.start_new_thread(self.play, ('Win.wav',))
        else:
            thread.start_new_thread(self.play, ('GameOver.wav',))
#            pass

        dlg = wx.MessageDialog(self, msg, u'Message', wx.OK | type)
        dlg.ShowModal()
        dlg.Destroy()

        self.game_init()

    def game_give_up(self):
        '''Function dealing with game giveup, and game over'''
        #stop the timer
        self.timer.Stop()
#	self.bgchoice = None	#delete the background choice, so that we'll see a new one.
	self.get_back()
        if self.game.status != self.game.ALGORITHM_GAME_STOP:
            self.game_init()

    def DrawMainBack(self):
        '''Draw the initial back image.'''
        (width, height) = self.mainback.GetSize().Get()
        (cw, ch) = self.rect.GetSize().Get()
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.SetBackground(wx.Brush('BLACK'))
        dc.Clear()  #clear the dc first
        dc.DrawBitmap(self.mainback, (cw-width)/2, (ch-height)/2)

    def DrawBG(self, choice):
        '''Draw the background picture of the drawingarea'''
        #TODO: choice of user set not to draw background pictures
        #print self.dc.CanDrawBitmap()
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.SetBackground(wx.Brush('BLACK'))
        dc.Clear()  #clear the dc first
##        print 'drawing background'
        dc.DrawBitmap(self.bg, self.bgpos.x, self.bgpos.y) #, useMask=True)


    def replace_image(self, p1, p2):
        '''Replace with new image at (i,j).'''
        #according to the data in the algorithm_game,and selected position, redraw all card images
        #modified from ui_game_begin function
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        #Draw card back image
        if self.cardback_choice >= 5:
            choice = 1
        else:
            choice = self.cardback_choice + 1
        #get card back image
        img = self.cardbacks[choice].GetSubBitmap(wx.Rect(0, 0, LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1,LlkBoard.UI_BACK_HEIGHT-LlkBoard.UI_BACK_BORDER_2))
        dc.DrawBitmap(img, LlkBoard.UI_FIXED_START_DRAW_LEFT + \
        (p1.y - self.game.difficulty)*(LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1),
        LlkBoard.UI_FIXED_START_DRAW_TOP + p1.x*(LlkBoard.UI_BACK_HEIGHT - LlkBoard.UI_BACK_BORDER_2),
        useMask=True)
        del img
        #Draw card's front image
        dc.DrawBitmap(self.cardimages[self.game.data[p1.x][p1.y] - 1],
        LlkBoard.UI_FIXED_START_DRAW_LEFT + (p1.y - self.game.difficulty)*(LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1)+\
        (LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1-LlkBoard.UI_IMAGE_SIZE)/2,
        LlkBoard.UI_FIXED_START_DRAW_TOP + p1.x*(LlkBoard.UI_BACK_HEIGHT - LlkBoard.UI_BACK_BORDER_2)+\
        (LlkBoard.UI_BACK_HEIGHT-LlkBoard.UI_BACK_BORDER_2-LlkBoard.UI_IMAGE_SIZE)/2,
        useMask=True)
##        self.OnPaint(None)
        if p2.x != -1 and p2.y != -1:
            #Draw card back image
            if self.cardback_choice >= 5:
                choice = 1
            else:
                choice = self.cardback_choice + 1
            img = self.cardbacks[choice].GetSubBitmap(wx.Rect(0, 0, LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1,LlkBoard.UI_BACK_HEIGHT-LlkBoard.UI_BACK_BORDER_2))
            dc.DrawBitmap(img, LlkBoard.UI_FIXED_START_DRAW_LEFT + \
            (p2.y - self.game.difficulty)*(LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1),
            LlkBoard.UI_FIXED_START_DRAW_TOP + p2.x*(LlkBoard.UI_BACK_HEIGHT - LlkBoard.UI_BACK_BORDER_2),
            useMask=True)
            del img
            #Draw card's front image
            dc.DrawBitmap(self.cardimages[self.game.data[p2.x][p2.y] - 1],
            LlkBoard.UI_FIXED_START_DRAW_LEFT + (p2.y - self.game.difficulty)*(LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1)+\
            (LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1-LlkBoard.UI_IMAGE_SIZE)/2,
            LlkBoard.UI_FIXED_START_DRAW_TOP + p2.x*(LlkBoard.UI_BACK_HEIGHT - LlkBoard.UI_BACK_BORDER_2)+\
            (LlkBoard.UI_BACK_HEIGHT-LlkBoard.UI_BACK_BORDER_2-LlkBoard.UI_IMAGE_SIZE)/2,
            useMask=True)
##        self.OnPaint(None)

    def redraw_images(self):
        '''Redraw all card images according to data in llkgame'''
##        self.DrawBG(1)  #redraw background picture
        #to avoid flicker, so place draw bg code directly here
        #if there is a better solution?     #TODO:move it to a seperate function
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.SetBackground(wx.Brush('BLACK'))
        dc.Clear()  #clear the dc first
##        print 'drawing background'
        dc.DrawBitmap(self.bg, self.bgpos.x, self.bgpos.y) #, useMask=True)
        #according to the data in the algorithm_game,and selected position, redraw all card images
        #modified from ui_game_begin function
##        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)

        for i in range(0, self.game.row):
            for j in range(0, self.game.col):
                if self.game.data[i][j] > 0:
                    #Draw card back images
                    dc.DrawBitmap(self.cardbacks[self.cardback_choice],
                    LlkBoard.UI_FIXED_START_DRAW_LEFT + (j - self.game.difficulty)*(LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1),
                    LlkBoard.UI_FIXED_START_DRAW_TOP + i*(LlkBoard.UI_BACK_HEIGHT - LlkBoard.UI_BACK_BORDER_2),
                    useMask=True)
                    #Draw card front image
                    dc.DrawBitmap(self.cardimages[self.game.data[i][j] - 1],
                    LlkBoard.UI_FIXED_START_DRAW_LEFT + (j - self.game.difficulty)*(LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1)+\
                    (LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1-LlkBoard.UI_IMAGE_SIZE)/2,
                    LlkBoard.UI_FIXED_START_DRAW_TOP + i*(LlkBoard.UI_BACK_HEIGHT - LlkBoard.UI_BACK_BORDER_2)+\
                    (LlkBoard.UI_BACK_HEIGHT-LlkBoard.UI_BACK_BORDER_2-LlkBoard.UI_IMAGE_SIZE)/2,
                    useMask=True)
##        print 'redraw images done'
        #redraw the client area
##        self.OnPaint(None)  #TODO: correct or not?

    def add_line(self, p1, p2, link_line):
        '''according to the points input, get the link points between the two points
        and add these points to a list
        '''
        if p1.x == p2.x:
            if p1.y < p2.y:
                for i in range(p1.y, p2.y):
                    dict = {
                    'pos':wx.Point(p1.x, i),
                    'direction':4,
                    'frame':0
                    }
                    link_line.append(dict)
            else:
                for i in range(p1.y, p2.y, -1):
                    dict = {
                    'pos':wx.Point(p1.x, i),
                    'direction':3,
                    'frame':0
                    }
                    link_line.append(dict)
        else:   #p1.y == p2.y
            if p1.x < p2.x:
                for i in range(p1.x, p2.x):
                    dict = {
                    'pos':wx.Point(i, p1.y),
                    'direction':2,
                    'frame':0
                    }
                    link_line.append(dict)
            else:
                for i in range(p1.x, p2.x, -1):
                    dict = {
                    'pos':wx.Point(i, p1.y),
                    'direction':1,
                    'frame':0
                    }
                    link_line.append(dict)

    def link(self, p1, p2):
        '''Link two cards'''
        link_line = []
        p3p4 = []
        if self.game.can_direct_link(p1, p2):
            self.add_line(p1, p2, link_line) #direct link
        else:
            self.game.can_link(p1, p2, p3p4)
            self.add_line(p1, p3p4[0], link_line)
            if p3p4[0].x != p3p4[1].x or p3p4[0].y != p3p4[1].y:
                self.add_line(p3p4[0],p3p4[1],link_line)
            self.add_line(p3p4[1],p2,link_line)
        self.draw_line(link_line)
	#self.Refresh(rect = self.rect)	#refresh the window and so the link effect will take place
	self.Update()
##        time.sleep(0.2)     #sleep 0.2 second after the link effect

    def draw_line(self, link_line):
        '''Dealing with the link line effect when delete cards.'''
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        for i in range(0, len(link_line)):
            tmp_dict = link_line[i]
            pos = tmp_dict['pos']
            if tmp_dict['direction'] == 1 or tmp_dict['direction'] == 2:
                tmp_pixbuf = self.vertical
            else:
                tmp_pixbuf = self.horizon
            width = tmp_pixbuf.GetWidth()
            height = tmp_pixbuf.GetHeight()
            if tmp_dict['direction'] == 1:
                dc.DrawBitmap(tmp_pixbuf, LlkBoard.UI_FIXED_START_DRAW_LEFT + (tmp_dict['pos'].y-self.game.difficulty)*(LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1),
                LlkBoard.UI_FIXED_START_DRAW_TOP + tmp_dict['pos'].x*(LlkBoard.UI_BACK_HEIGHT-LlkBoard.UI_BACK_BORDER_2) - 25,
                useMask=True)
            elif tmp_dict['direction'] == 2:
                dc.DrawBitmap(tmp_pixbuf, LlkBoard.UI_FIXED_START_DRAW_LEFT + (tmp_dict['pos'].y-self.game.difficulty)*(LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1),
                LlkBoard.UI_FIXED_START_DRAW_TOP + tmp_dict['pos'].x*(LlkBoard.UI_BACK_HEIGHT-LlkBoard.UI_BACK_BORDER_2) + 25,
                useMask=True)
            elif tmp_dict['direction'] == 3:
                dc.DrawBitmap(tmp_pixbuf, LlkBoard.UI_FIXED_START_DRAW_LEFT + (tmp_dict['pos'].y-self.game.difficulty)*(LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1)-20,
                LlkBoard.UI_FIXED_START_DRAW_TOP + tmp_dict['pos'].x*(LlkBoard.UI_BACK_HEIGHT-LlkBoard.UI_BACK_BORDER_2),
                useMask=True)
            elif tmp_dict['direction'] == 4:
                dc.DrawBitmap(tmp_pixbuf, LlkBoard.UI_FIXED_START_DRAW_LEFT + (tmp_dict['pos'].y-self.game.difficulty)*(LlkBoard.UI_BACK_WIDTH-LlkBoard.UI_BACK_BORDER_1)+20,
                LlkBoard.UI_FIXED_START_DRAW_TOP + tmp_dict['pos'].x*(LlkBoard.UI_BACK_HEIGHT-LlkBoard.UI_BACK_BORDER_2),
                useMask=True)
        #delete the list and free data
        del link_line

    def game_change(self, p1, p2):
        '''
        Change the image cards' position according to the current level value
        the two cards which can link have already been deleted,so only change the position of these cards left.
        '''
##        print 'change', p1, p2
        self.game.game_change(p1, p2)
        self.redraw_images()
        self.ui_point1 = wx.Point(-1, -1)      #NOTE: or to change x,y

    def get_time_limited(self):
        '''Get the time limit of the current level.'''
        if self.game.difficulty == 2:
            return 240
        else:
            return 200


    def progress_timeout(self, value):
        '''Dealing with time stuff.'''
        if value == 9999:   #full fill the time
            self.time_remain = self.get_time_limited()
            return True
        else:
            if value != 0:
                self.time_remain += value
                if self.time_remain > self.get_time_limited():
                    self.time_remain = self.get_time_limited()
                self.refresh_top()
                return True
            else:
                if self.time_remain > 0:
                    self.time_remain -= 1
                    self.refresh_top()
                    return True
                else:
                    self.game_over(False)
                    return False

    def game_hint(self):
        '''Give player a hint.'''
        if self.game.status != self.game.ALGORITHM_GAME_RUN:
            return
        if self.game.hint == 0:
            return
        self.game.hint -= 1
        self.refresh_top()
        for i in range(0, self.game.row):
            for j in range(0, self.game.col):
                if self.game.data[i][j] > 0:
                    for k in range(i, self.game.row):
                        for l in range(0, self.game.col):
                            if k == i and l == j:
                                continue    #exclude the situation of link to itself
                            if self.game.data[k][l] > 0:
                                p1 = wx.Point(i, j)
                                p2 = wx.Point(k, l)
                                if self.game.can_link(p1, p2, None):
                                    self.replace_image(p1, p2)
                                    thread.start_new_thread(self.play, ('Hint.wav',))
                                    return

    def game_shuffle(self):
        '''Shuffle cards.'''
        if self.game.status != self.game.ALGORITHM_GAME_RUN:
            return
        self.timer.Stop()
        if self.game.life == 0:
            self.game_over(False)
            return
        else:
            self.game.life -= 1
            self.refresh_top()
            self.game.game_shuffle()
            self.redraw_images()
            self.ui_point1 = wx.Point(-1, -1)
            thread.start_new_thread(self.play, ('Shuffle.wav',))
            self.timer.Start()

    def game_pause(self):
        '''Pause,hide the card images'''
##        print 'paused'
        if self.game.status == self.game.ALGORITHM_GAME_RUN:
            self.timer.Stop()
            self.game.status = self.game.ALGORITHM_GAME_PAUSE
            (width, height) = self.pause.GetSize().Get()
            (cw, ch) = self.rect.GetSize().Get()
            dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
            dc.SetBackground(wx.Brush('BLACK'))
            dc.Clear()  #clear the dc first
            dc.DrawBitmap(self.pause, (cw-width)/2, (ch-height)/2)
        elif self.game.status == self.game.ALGORITHM_GAME_PAUSE:
            #empty all possible selected status
            self.ui_point1 = wx.Point(-1, -1)
            self.redraw_images()
            self.timer.Start()
            self.game.status = self.game.ALGORITHM_GAME_RUN

    def refresh_top(self):
        '''Refresh the information shown on the top.'''
        if self.game.status != self.game.ALGORITHM_GAME_STOP:
            t_diff = (u'难度:简单', u'难度:一般', u'难度:困难')
            diff = t_diff[self.game.difficulty]
            lev = u'等级:%d'%self.game.level
            t_change = (u'无变化', u'向下', u' 向左', u'上下分离', u'左右分离',
                u'上下集中', u'左右集中', u'上左下右', u'左下右上', u'向外扩散', u'向内集中')
            change =u'变化类型:'+ t_change[self.game.level]
            score = u'%d'%self.game.score
            life = u'生命:%d'%self.game.life
            hint = u'提示:%d'%self.game.hint
            time = int(self.time_remain*100/self.get_time_limited())
##            #TO DO:set progress bar
        else:
            diff = u'难度:'
            lev = u'等级:'
            change = u'变化类型:'
            score = u'0'
            life = u'生命:'
            hint = u'提示:'
            time = 0

        info = GameStatus(diff=diff, level=lev, change=change, score=score, life=life, hint=hint, time=time)


        evt = MyEvent(myEVT_UPDATE_INFOBAR, self.GetId())
        evt. SetMyVal(info)
        self.GetEventHandler().ProcessEvent(evt)    #notice
        #event.Skip()

    def play(self, file):
        '''Play a sound.'''
##        print 'before play...'
        try:
            sound = wx.Sound(get_sound_path(file))
            sound.Play(wx.SOUND_ASYNC)
        except NotImplementedError, v:
            wx.MessageBox(str(v), "Exception Message")
##        print '...after play'


    def game_begin(self, data):
        '''The UI function dealing with the game start process.
        data: stand for game diffictulty, but it is based on 1,and the game difficulty is based on 0,BE CARE!!!
        '''
        if self.game.status != llkgame.ALGORITHM_GAME_STOP:
            return
##        if data != 4:   #data = 4 means resume game process
        #TODO: resume game process
        self.ui_point1 = wx.Point(-1, -1)
        self.ui_point2 = wx.Point(-1, -1)    #cancel all the selected status
        if data == 4:
            pass ##not implemented yet!!!
        else:
            if self.game.game_begin(data) == False: #init the array and other related datas in the algorith_game,ready for starting the game.
                print 'Call algorithm_game_begin function error.'
                return
            #init the drawing area,include background picture and card images.
            self.redraw_images()
            self.progress_timeout(9999)
        self.refresh_top()
        self.timer = wx.Timer(self)
        self.timer.Start(1000)  #start the timer

class PyllkFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Pyllk Frame", style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        board = LlkBoard(self, -1)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = PyllkFrame(None)
    frame.Show(True)
    frame.Fit()
    frame.Raise()
    app.MainLoop()
