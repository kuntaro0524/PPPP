import wx
def on_timer(event):
    pass  # do whatever

TIMER_ID = 100  # pick a number
timer = wx.Timer(panel, TIMER_ID)  # message will be sent to the panel
timer.Start(100)  # x100 milliseconds
wx.EVT_TIMER(panel, TIMER_ID, on_timer)  # call the on_timer function
