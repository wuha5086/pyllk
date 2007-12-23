#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Name:        llkgame.py
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
# 文件：$Id$
# 版本：$Revision$

'''
This module contains the llkgame class which offers the algorithms and data structures.
'''
import random
##import wxversion
##wxversion.select('2.8')
from wx import Point as Point




class llkgame:
    ALGORITHM_GAME_STOP = 1
    ALGORITHM_GAME_RUN = 2
    ALGORITHM_GAME_PAUSE = 3

    def __init__(self):
        self.difficulty = 0
        self.level = 0
        self.life = 0
        self.hint = 0
        self.score = 0
        self.row = 0
        self.col = 0
        self.status = llkgame.ALGORITHM_GAME_STOP     #Game status
        self.data = []
        for i in range(10):
            self.data.append([0]*17)      #0:no pic,1: pic1,

    def print_data(self):
        '''Print data, for test purposes'''
        for i in range(10):
            print self.data[i]

    def game_begin(self, data):
        #get a random order of the card image list
        if self.status == llkgame.ALGORITHM_GAME_STOP:
            if data == 1:
                self.row = 6
                self.col = 12
                self.difficulty = 0
                self.level = 0
                self.life = 2
                self.hint = 4
                self.score = 0
            elif data == 2:
                self.row = 7
                self.col = 14
                self.difficulty = 1
                self.level = 0
                self.life = 3
                self.hint = 6
                self.score = 0
            elif data == 3:
                self.row = 8
                self.col = 16
                self.difficulty = 2
                self.level = 0
                self.life = 4
                self.hint = 5
                self.score = 0
            else:
                self.row = 8
                self.col = 16
                self.difficulty = 2
                self.level = 0
                self.life = 4
                self.hint = 5
                self.score = 0
            self.init_data()
            self.status = llkgame.ALGORITHM_GAME_RUN
            return True
        else:
            return False

    def init_data(self):
        picture_type = 36
        i =128
        j = 128
        picture_type_tuple = (21, 25, 32)
        j_tuple = (72, 98, 128)

        picture_type = picture_type_tuple[self.difficulty]
        j = j_tuple[self.difficulty]

        picture_list = list()
        for i in range(j):
            picture_list.append(i/4+1)

        while len(picture_list) !=0:
            i = random.randint(0, j-1)
            self.data[(j-1)/self.col][(j-1)%self.col] = picture_list[i]
            del picture_list[i]
            j-=1

    def can_direct_link(self, p1, p2):
        '''
        Test if p1 and p2 can direct link or not. that is to say,the points between p1 and p2
        at the same row or column are all empty.
        BE CARE:this function do not warrant p1 and p2 have the same type of image.
        '''
        if (p1.x == p2.x) or ( p1.y == p2.y) :
            if(abs(p1.x - p2.x) + abs(p1.y - p2.y) <= 1):
                return True
            else:
                if(p1.x == p2.x and p1.x > -1 and p1.x < self.row):
                    if(p1.y > p2.y):
                        for i in range(p2.y+1, p1.y):
                             if(self.data[p1.x][i] > 0):
                                return False
                    else:
                        for i in range(p1.y+1, p2.y):
                             if(self.data[p1.x][i] > 0):
                                return False
                elif (p1.y == p2.y and p1.y > -1 and p1.y < self.col):
                    if(p1.x > p2.x):
                        for i in range(p2.x+1, p1.x):
                             if(self.data[i][p1.y] > 0):
                                return False
                    else:
                        for i in range(p1.x+1, p2.x):
                             if(self.data[i][p1.y] > 0):
                                return False
                return True
        else:
            return False

    def can_link(self, p1, p2, ptlist):
        '''
        test if p1 and p2 can link.
        first,test if p1 and p2 can direct link,if not,get p1's and p2's adjacent empty points at x and y direction,
        judge if the p1's adjacent empty point can direct link to p2's
        '''
        if self.data[p1.x][p1.y] != self.data[p2.x][p2.y]:
            return False
        if self.can_direct_link(p1, p2) and (ptlist is None): ##!Note! None! or 0-length  #can direct link,no need to return the turn points.
            return True
        else:
            #get adjacent empty points at x and y direction,judge point by point
            p1_list = self.get_points(p1)
            p2_list = self.get_points(p2)

            if(len(p1_list) == 0 or len(p2_list) == 0):
                return False
            else:
                for i in range(0, len(p1_list)):
                    for j in range(0, len(p2_list)):
                        if self.can_direct_link(p1_list[i], p2_list[j]):
                            if ptlist is not None:
                                ptlist.append(p1_list[i])
                                ptlist.append(p2_list[j])
                            del p1_list
                            del p2_list
                            return True
                del p1_list
                del p2_list
                return False

    def get_points(self, p):
        '''
        Find up,down,left and right of point p,get the adjacent empty points,
        form a single list,and return it.
        '''
        p_list = []

        for i in range(p.y+1, self.col+1):
            if i < self.col and self.data[p.x][i] > 0:
                break
            else:
                p_list.append(Point(p.x, i))

        for i in range(p.y-1, -2, -1):
            if i > -1 and self.data[p.x][i] > 0:
                break
            else:
                p_list.append(Point(p.x, i))

        for i in range(p.x+1, self.row+1):
            if i < self.row and self.data[i][p.y] > 0:
                break
            else:
                p_list.append(Point(i, p.y))

        for i in range(p.x-1, -2, -1):
            if i > -1 and self.data[i][p.y] > 0:
                break
            else:
                p_list.append(Point(i, p.y))

        return p_list

    def link(self, p1, p2):
        '''  empty the data of the two points.'''
        self.data[p1.x][p1.y] = 0
        self.data[p2.x][p2.y] = 0
        self.score += 20    #add score

    def game_no_solution(self):
        '''
        test if the current game situation have solution.
        return value:
        0: yes,have solution.
        1: no,need to shuffle the cards.
        2: the cards are all deleted,this level is clear.
        '''
        cards_num = 0
        for i in range(0, self.row):
            for j in range(0, self.col):
                if self.data[i][j] > 0:
                    cards_num +=1
                    for k in range(i, self.row):
                        for l in range(0, self.col):
                            if k == i and l == j:   #exclude the situation of link to itself
                                continue
                            if self.data[k][l] > 0:
                                p1 = Point(i, j)
                                p2 = Point(k, l)
                                if self.can_link(p1, p2, None):
                                    return 0
        if cards_num > 0:
            return 1
        else:
            return 2

    def game_shuffle(self):
        '''
        shuffle cards.
        read the remain cards in data array,form a single list.then traversal the data array,
        at every point that have cards,get a random card from the single list and put it there.
        BE CARE: the life value will be minimised in UI dealing function,because in this function,
        shuffle one time do not certainly get a game situation that have solution,so this function may
        be called more than one time.
        '''
        picture_list = []
        for i in range(0, self.row):
            for j in range(0, self.col):
                if self.data[i][j] > 0:
                    picture_list.append(self.data[i][j])

        for i in range(0, self.row):
            for j in range(0, self.col):
                if self.data[i][j] > 0:
                    m = random.randint(0, len(picture_list)-1)
                    self.data[i][j] = picture_list[m]
                    del picture_list[m]

        if self.game_no_solution() == 1:
            self.game_shuffle()

    def game_change(self, p1, p2):
        foo_list = [self.data_change_0,    #No Change
                    self.data_change_1,    #Move Down
                    self.data_change_2,    #Move Left
                    self.data_change_3,    #Up and Down Separate
                    self.data_change_4,    #Left and Right Separate
                    self.data_change_5,    #Up and Down Converge
                    self.data_change_6,    #Left and Right Converge
                    self.data_change_7,    #Up leftward,Down rightward
                    self.data_change_8,    #Left downward,Right upward
                    self.data_change_9,    #Disperse from Center
                    self.data_change_10    #Centralize
                    ]
        foo_list[self.level](p1, p2)

    def game_next_level(self):
        '''Switch to the next level.'''
        if self.level >= 10:    #11 Levels,from 0 to 10
            return False
        else:
            self.level +=1
            self.life +=1
            self.hint +=1
            if self.level > 5:
                self.score += 400 * self.level
            else:
                self.score += 200 * self.level
            self.score += self.life * 100
            self.score += self.hint * 50
            self.init_data()
            return True

    def data_change_0(self, p1, p2):
        '''No Change, do nothing'''
        pass    #do nothing

    def data_change_1(self, p1, p2):
        '''Move Down'''
        for i in range(p1.x, 0, -1):
            self.data[i][p1.y] = self.data[i-1][p1.y]
        self.data[0][p1.y] = 0
##        print 'data0 - ',self.data[0][p1.y]    #debug
        i = p2.x
        if p1.y == p2.y and p1.x > p2.x:
            i += 1
        for i in range(i, 0, -1):
            self.data[i][p2.y] = self.data[i-1][p2.y]
        self.data[0][p2.y] = 0

    def data_change_2(self, p1, p2):
        '''Move Left'''
        #BE CARE: the last column is not in the for loop.
        for j in range(p1.y, self.col-1):
            self.data[p1.x][j] = self.data[p1.x][j+1]
        self.data[p1.x][self.col-1] = 0
        j = p2.y
        if p1.x == p2.x and p1.y < p2.y:
            j -= 1
        for j in range(j, self.col-1):
            self.data[p2.x][j] = self.data[p2.x][j+1]
        self.data[p2.x][self.col-1] = 0

    def data_change_3(self, p1, p2):
        '''Up and Down Separate'''
        tmp_start = p1.x
        tmp_end = self.row/2
        if tmp_start < tmp_end:
            tmp_end -= 1
        i = tmp_start
        if tmp_start != tmp_end:
            while i != tmp_end:
                sign = (tmp_end - tmp_start)/abs(tmp_end - tmp_start)
                self.data[i][p1.y] = self.data[i+sign][p1.y]
                self.data[i+sign][p1.y] =0
                i += sign

        tmp_start = p2.x
        tmp_end = self.row/2
        if tmp_start < tmp_end:
            tmp_end -= 1
        if p1.y == p2.y:    #p1 and p2 are in the same column
            if p1.x < self.row/2 and p2.x < self.row/2: #p1 and p2 are all in the up half rows
                if p1.x < p2.x: #p1's move will change p2's positon
                    tmp_start -= 1  #start position move up
            elif p1.x >= self.row/2 and p2.x >= self.row/2: #p1 and p2 are all in  the down half rows
                if p1.x > p2.x:
                    tmp_start += 1
        i = tmp_start
        if tmp_start != tmp_end:
            while (i != tmp_end):
                sign = (tmp_end - tmp_start)/abs(tmp_end - tmp_start)
                self.data[i][p2.y] = self.data[i+sign][p2.y]
                self.data[i+sign][p2.y] = 0
                i += sign

    def data_change_4(self, p1, p2):
        '''Left and Right Separate'''
        tmp_start = p1.y
        tmp_end = self.col/2
        if tmp_start < tmp_end:
            tmp_end -= 1
        j = tmp_start
        if tmp_start != tmp_end:
            while j != tmp_end:
                sign = (tmp_end - tmp_start)/abs(tmp_end - tmp_start)
                self.data[p1.x][j] = self.data[p1.x][j+sign]
                self.data[p1.x][j+sign] =0
                j += sign

        tmp_start = p2.y
        tmp_end = self.col/2
        if tmp_start < tmp_end:
            tmp_end -= 1
        if p1.x == p2.x:    #p1 and p2 are in the same row
            if p1.y < self.col/2 and p2.y < self.col/2: #p1 and p2 are all in the left half columns
                if p1.y < p2.y: #p1's move will change p2's positon
                    tmp_start -= 1  #start position move left
            elif p1.y >= self.col/2 and p2.y >= self.col/2: #p1 and p2 are all in  the right half columns
                if p1.y > p2.y:
                    tmp_start += 1
        j = tmp_start
        if tmp_start != tmp_end:
            while (j != tmp_end):
                sign = (tmp_end - tmp_start)/abs(tmp_end - tmp_start)
                self.data[p2.x][j] = self.data[p2.x][j+sign]
                self.data[p2.x][j+sign] = 0
                j += sign

    def data_change_5(self, p1, p2):
        '''Up and Down Converge'''
        tmp_start = p1.x
        if (p1.x < self.row/2):
            tmp_end = 0
        else:
            tmp_end = self.row - 1
        i = tmp_start
        if tmp_start != tmp_end:
            while i != tmp_end:
                sign = (tmp_end - tmp_start)/abs(tmp_end - tmp_start)
                self.data[i][p1.y] = self.data[i+sign][p1.y]
                self.data[i+sign][p1.y] = 0
                i += sign
        tmp_start = p2.x
        if p2.x < self.row/2:
            tmp_end = 0
        else:
            tmp_end = self.row - 1
        if p1.y == p2.y:    #p1 and p2 are in the same column
            if p1.x < self.row/2 and p2.x < self.row/2: #p1 and p2 are all in the up half rows
                if p1.x > p2.x: #p1's move will change p2's positon
                    tmp_start += 1  #start positon move down
            elif p1.x >= self.row/2 and p2.x >= self.row/2:   #p1 and p2 are all in the down half rows
                if p1.x < p2.x:
                    tmp_start -= 1
        i = tmp_start
        if tmp_start != tmp_end:
            while i != tmp_end:
                sign = (tmp_end - tmp_start)/abs(tmp_end - tmp_start)
                self.data[i][p2.y] = self.data[i+sign][p2.y]
                self.data[i+sign][p2.y] = 0
                i += sign

    def data_change_6(self, p1, p2):
        '''Left and Right Converge'''
        tmp_start = p1.y
        if (p1.y < self.col/2):
            tmp_end = 0
        else:
            tmp_end = self.col - 1
        j = tmp_start
        if tmp_start != tmp_end:
            while j != tmp_end:
                sign = (tmp_end - tmp_start)/abs(tmp_end - tmp_start)
                self.data[p1.x][j] = self.data[p1.x][j+sign]
                self.data[p1.x][j+sign] = 0
                j += sign
        tmp_start = p2.y
        if p2.y < self.col/2:
            tmp_end = 0
        else:
            tmp_end = self.col - 1
        if p1.x == p2.x:    #p1 and p2 are in the same row
            if p1.y < self.col/2 and p2.y < self.col/2: #p1 and p2 are all in the left half columns
                if p1.y > p2.y: #p1's move will change p2's positon
                    tmp_start += 1  #start positon move right
            elif p1.y >= self.col/2 and p2.y >= self.col/2:   #p1 and p2 are all in the right half columns
                if p1.y < p2.y:
                    tmp_start -= 1
        j = tmp_start
        if tmp_start != tmp_end:
            while j != tmp_end:
                sign = (tmp_end - tmp_start)/abs(tmp_end - tmp_start)
                self.data[p2.x][j] = self.data[p2.x][j+sign]
                self.data[p2.x][j+sign] = 0 #this sentence can be write outside of while loop in some way
                j += sign

    def data_change_7(self, p1, p2):
        '''Up leftward,Down rightward'''
        if p1.x < self.row/2:   #leftward
            for j in range(p1.y, self.col-1):
                self.data[p1.x][j] = self.data[p1.x][j+1]
            self.data[p1.x][self.col-1] = 0
        else:   #rightward
            for j  in range(p1.y, 0, -1):
                self.data[p1.x][j] = self.data[p1.x][j-1]
            self.data[p1.x][0] = 0
        j = p2.y
        if p2.x < self.row/2:   #leftward
            if p1.x == p2.x and p1.y < p2.y:
                j -= 1
            for j in range(j, self.col-1):
                self.data[p2.x][j] = self.data[p2.x][j+1]
            self.data[p2.x][self.col-1] = 0
        else:   #rightward
            if p1.x == p2.x and p1.y > p2.y:
                j += 1
            for j in range(j, 0, -1):
                self.data[p2.x][j] = self.data[p2.x][j-1]
            self.data[p2.x][0] = 0

    def data_change_8(self, p1, p2):
        '''Left downward,Right upward'''
        if p1.y < self.col/2:   #downward
            for i in range(p1.x, 0, -1):
                self.data[i][p1.y] = self.data[i-1][p1.y]
            self.data[0][p1.y] = 0
        else:   #upward
            for i  in range(p1.x, self.row-1):
                self.data[i][p1.y] = self.data[i+1][p1.y]
            self.data[self.row-1][p1.y] = 0
        i = p2.x
        if p2.y < self.col/2:   #downward
            if p1.y == p2.y and p1.x > p2.x:
                i += 1
            for i in range(i, 0, -1):
                self.data[i][p2.y] = self.data[i-1][p2.y]
            self.data[0][p2.y] = 0
        else:   #upward
            if p1.y == p2.y and p1.x < p2.x:
                i -= 1
            for i in range(i, self.row-1):
                self.data[i][p2.y] = self.data[i+1][p2.y]
            self.data[self.row-1][p2.y] = 0

    def data_change_9(self, p1, p2):
        '''
        Disperse from Center
        first,left and right seperate,and then up and down seperate
        '''
        p3 = Point()
        p4 = Point()
        self.data_change_4(p1, p2)   #1.left and right seperate
        #find p1,p2 's position after 'left and right seperate',then do 'up and down seperate' on p1,p2 's new position
        p3.x = p1.x
        if p1.y < self.col/2:
            p3.y = 0
            sign = 1
        else:
            p3.y = self.col - 1
            sign = -1
        while self.data[p3.x][p3.y] != 0:
            p3.y += sign

        p4.x = p2.x
        if p2.y < self.col/2:
            p4.y = 0
            sign = 1
        else:
            p4.y = self.col - 1
            sign = -1
        while self.data[p4.x][p4.y] != 0:
            p4.y += sign

        #modify in case of special situation
        if p1.x == p2.x:
            if p1.y < self.col/2 and p2.y < self.col/2:
                p4.y = p3.y + 1
            elif p1.y >= self.col/2 and p2.y >= self.col/2:
                p4.y = p3.y - 1

        #p3,p4 are the new position of p1,p2 after 'left and right seperate',
        #do 'up and down seperate' on them
        self.data_change_3(p3, p4)

    def data_change_10(self, p1, p2):
        '''
        Centralize
        first do 'Left Right Converge' and then 'Up Down Converge'
        '''
        p3 = Point()
        p4 = Point()
        self.data_change_6(p1, p2)   #first do 'Left Right Converge'
        #find the new position of p1,p2 after 'Left Right Converge',then do 'Up Down Converge' on new position
        p3.x = p1.x
        if p1.y < self.col/2:
            p3.y = self.col/2 - 1
            sign = -1
        else:
            p3.y = self.col/2
            sign = 1
        while self.data[p3.x][p3.y] != 0:
            p3.y += sign

        p4.x = p2.x
        if p2.y < self.col/2:
            p4.y = self.col/2 -1
            sign = -1
        else:
            p4.y = self.col/2
            sign = 1
        while self.data[p4.x][p4.y] != 0:
            p4.y += sign

        #modify in case of special situation
        if p1.x == p2.x:
            if p1.y < self.col/2 and p2.y < self.col/2:
                p4.y = p3.y - 1
            elif p1.y >= self.col/2 and p2.y >= self.col/2:
                p4.y = p3.y + 1

        #p3,p4 are the new position of p1,p2 after 'Left Right Converge',
        #do 'Up Down Converge' on them
        self.data_change_5(p3, p4)


