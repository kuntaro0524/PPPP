import wx

List = ["tukasa","konata","kagami","miwiki","yutaka","minami"]

class MyExcalibur(wx.PySimpleApp):
    
    def OnInit(self):
        Frm = wx.Frame(None, -1, "wxPython", size=(400,48),pos=(400,400))
        self.TxtCtr = wx.TextCtrl(Frm, -1)
        self.TxtCtr.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.lbFrame = wx.Frame(None, 0, "wxPython", size=(420,200),pos=(400,448),style=wx.DOUBLE_BORDER)
        self.LBox = wx.ListBox(self.lbFrame, -1, choices = List, size=(415,200))
        Frm.Show()
        self.lbFrame.Show()
        self.TxtCtr.SetFocus()
        return 1

    def OnKeyDown(self,event):
        key = event.GetKeyCode()
        if key ==  wx.WXK_ESCAPE:
            wx.Exit()
        elif key == wx.WXK_UP:
            count = self.LBox.GetCount()
            next = self.LBox.GetSelection() - 1
            if next >=  0:
                self.LBox.SetSelection(next)
            else: self.LBox.SetSelection(count - 1)
        elif key == wx.WXK_DOWN:
            count = self.LBox.GetCount()
            next = self.LBox.GetSelection() + 1
            if next < count:
                self.LBox.SetSelection(next)
            else: self.LBox.SetSelection(0)
        else: event.Skip()

app = MyExcalibur()
app.MainLoop()

