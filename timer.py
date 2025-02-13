import wx
import time

class ClockWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, None)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)

    def Draw(self, dc):
        t = time.localtime(time.time())
        st = time.strftime("%I:%M:%S", t)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.SetFont(wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL))
        tw, th = dc.GetTextExtent(st)
        dc.DrawText(st, 20, 20)
        
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
