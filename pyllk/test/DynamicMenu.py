#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

import wx

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        # Menu Bar
        self.frame_1_menubar = wx.MenuBar()
        self.SetMenuBar(self.frame_1_menubar)
        self.mnFile = wx.Menu()


        cfg=[['a', 'this is a'],['b', 'this is b'],['C', 'this is C']]
        for i in cfg:
            exec 'self.IDmnFile%s =%d' % (i[0],wx.NewId() )  in locals()

            self.mnFile.Append(eval('self.IDmnFile%s' % i[0]), i[0], i[1])
            pass
        self.frame_1_menubar.Append(self.mnFile , "File")
        # Menu Bar end

        self.__set_properties()
        self.__do_layout()

        for i in cfg:
            wx.EVT_MENU(self,eval('self.IDmnFile%s' % i[0]),   #***
                        self.event)                             #***


    def __set_properties(self):
        self.SetTitle("frame_1")

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.SetAutoLayout (True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()

    def event(self, event):
        print 'event=', self.mnFile.GetHelpString(event.GetId())        ##***


class MyApp( wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_1 = MyFrame(None, -1, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
