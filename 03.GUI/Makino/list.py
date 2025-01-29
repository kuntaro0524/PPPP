#coding:utf-8

import wx
caption = (u"No",u"都道府県",u"男女計",u"男",u"女")

data = [
    (1,u"北海道",5570,2638,2933),
    (2,u"青森県",1407,663,744),
    (3,u"岩手県",1364,652,712),
    (4,u"宮城県",2347,1140,1208),
    (5,u"秋田県",1121,527,593),
    (6,u"山形県",1198,575,623),
    (7,u"福島県",2067,1004,1063),
    (8,u"茨城県",2969,1477,1492),
    (9,u"栃木県",2014,1001,1013),
    (10,u"群馬県",2016,993,1024),
    (11,u"埼玉県",7090,3570,3520),
    (12,u"千葉県",6098,3047,3051),
    (13,u"東京都",12758,6354,6405),
    (14,u"神奈川県",8880,4484,4396),
]

class MyFrame1(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame1.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.label_1 = wx.StaticText(self, -1, "label_1")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame1.__set_properties
        self.SetTitle("frame_2")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame1.__do_layout
        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        sizer_8.Add(self.label_1, 0, 0, 0)
        self.SetSizer(sizer_8)
        sizer_8.Fit(self)
        self.Layout()
        # end wxGlade

# end of class MyFrame1


class MyTable(wx.ListCtrl):

    def __init__(self,parent):
        wx.ListCtrl.__init__(self,parent,-1,style = wx.LC_REPORT | wx.LC_VIRTUAL)
        self.InsertColumn(0,caption[0],wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(1,caption[1])
        self.InsertColumn(2,caption[2],wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(3,caption[3],wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(4,caption[4],wx.LIST_FORMAT_RIGHT)

        self.items = data
        self.SetItemCount(len(self.items))
        self.Bind(wx.EVT_LIST_COL_CLICK,self.Sort)

    def OnGetItemText(self,line,col):
        return self.items[line][col]

    def Sort(self,event):
        idx = event.GetColumn()
        self.items.sort(lambda x,y: cmp(x[idx],y[idx]))
        self.DeleteAllItems()
        self.SetItemCount(len(self.items))

class MyDialog(wx.Dialog):

    def __init__(self,parent):
        wx.Dialog.__init__(self,parent,-1,u"MyDialog",size=(450,200))
        self.closeBtn = wx.Button(self,-1,u"閉じる")
        self.Bind(wx.EVT_BUTTON, self.OnClose, self.closeBtn)
        self.table = MyTable(self)

        sz = wx.BoxSizer(wx.VERTICAL)
        sz.Add(self.closeBtn,0)
        sz.Add(self.table,1,wx.EXPAND)
        self.SetSizer(sz)

    def OnClose(self,event):
        self.Close(True)

class MyWindow(wx.Frame):

    def __init__(self,parent,id):
        wx.Frame.__init__(self, parent, id, u"ダイアログの実験",size=(300,200))
        panel=wx.Panel(self)

        dlgBtn = wx.Button(panel,label="dialog",pos=(130,10),size=(60,60))
        exitBtn = wx.Button(panel,label="exit",pos=(130,70),size=(60,60))

        self.Bind(wx.EVT_BUTTON, self.OnDlgBtn, dlgBtn)
        self.Bind(wx.EVT_BUTTON, self.OnExitBtn, exitBtn)

    def OnExitBtn(self,event):
        self.Close(True)

    def OnDlgBtn(self, event):
        box = MyDialog(self)
        anser = box.ShowModal()

if __name__=='__main__':
    app=wx.PySimpleApp()
    frame=MyWindow(parent=None,id=-1)
    frame.Show()
    app.MainLoop()


