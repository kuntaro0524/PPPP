import wx
import wx_utils
from wx_utils import XRC

class MainFrame(wx.Frame):
    def __init__(self,parent=None):
        pre=wx.PreFrame()
        XRC().LoadOnFrame(pre,parent,'MainFrame')
        self.PostCreate(pre)

def main():
    app = wx.App()                               
    wx_utils.XrcInit("resource/resource.xrc")    
    frame = MainFrame()                          
    app.SetTopWindow(frame)                      
    frame.Show(True)                             
    app.MainLoop()                               

if __name__=="__main__":
    main()
