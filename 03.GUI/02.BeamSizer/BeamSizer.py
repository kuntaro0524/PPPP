#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Sat Apr 24 23:02:45 2010

import wx
from SetBeamSize import *

# begin wxGlade: extracode
# end wxGlade

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.label_1 = wx.StaticText(self, -1, "Set beamsize to")
        self.inputSize = wx.TextCtrl(self, -1, "")
        self.label_2 = wx.StaticText(self, -1, "[um]")
        self.goButton = wx.Button(self, -1, "Go")

	# My app
	self.sbs=SetBeamSize()

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.changeSize, self.goButton)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle("frame_2")
        self.label_1.SetFont(wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(self.label_1, 0, 0, 0)
        sizer_3.Add(self.inputSize, 0, 0, 0)
        sizer_3.Add(self.label_2, 0, 0, 0)
        sizer_3.Add((5, 20), 0, 0, 0)
        sizer_3.Add(self.goButton, 0, 0, 0)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        self.Layout()
        # end wxGlade

    def changeSize(self, event): # wxGlade: MainFrame.<event_handler>
        size=float(self.inputSize.GetValue())
	print self.sbs.setSize(size)
        #print size

# end of class MainFrame

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MainFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
