#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
if __name__ == '__main__':
    gs = GameStatus(1,2,3,change=5);
    print gs.change