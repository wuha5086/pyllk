#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
# 文件：$Id$
# 版本：$Revision$

##import wxversion
##wxversion.select('2.8')
import wx
from wx import EmptyIcon
import re

def get_image_path(name):
    '''Returns the full path of a picture used in the game.'''

    prefix = 'llk_classic/'
    pattern = re.compile('^\d')     #beginning with a digit
    name = str(name)    #convert to string if name is a number

    if re.search(pattern, name):
        num = 1
    else:
        num = 0
    if num == 1:
        fullname = prefix+ 'back' + name + '.jpg'
    else:
        fullname = prefix+ name # + '.png'
##    print fullname
    return fullname


def getPyllkIcon():
    icon = EmptyIcon()
    icon.CopyFromBitmap(wx.Bitmap('llk_classic/logo.png'))
    return icon

def get_sound_path(name):
    '''Returns the full path of a sound file used in the game.'''
    prefix = 'sound/'
    name = str(name)
    fullname = prefix + name
    return fullname







