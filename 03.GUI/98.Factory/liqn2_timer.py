import wx
import time
import datetime

class ClockWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, None)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)
	self.starttime=datetime.datetime.now()

    def Draw(self, dc):
        currtime=datetime.datetime.now()
        diff=(currtime-self.starttime).seconds
        #print currtime,diff
        st="Last fill: %s\nCurrent  :%s\nRemained :%8.3f [sec]"%(self.starttime,currtime,7200.0-diff)

        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL))
        tw, th = dc.GetTextExtent(st)
        dc.DrawText(st, 50, 50)
        
    def OnTimer(self, evt):
        dc = wx.BufferedDC(wx.ClientDC(self))
        self.Draw(dc)

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)

app = wx.PySimpleApp()
frm = ClockWindow(app)
frm.Show()
app.MainLoop()
