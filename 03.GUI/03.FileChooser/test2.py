import wx
import os

# setup the GUI main loop
app = wx.App()

filename = wx.FileSelector(default_path=os.getcwd())
