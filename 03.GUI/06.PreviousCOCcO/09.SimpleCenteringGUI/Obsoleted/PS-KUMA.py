#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade HG on Sat Feb  2 21:14:53 2013

import wx
import sys
sys.path.append("/data/03.Sacla/SSSS/BLctrl")
from  ScheduleSACLA import *
from Gonio import *
from File import *
from MyException import *
import numpy
from Crystal import *

class MyFrame2(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame2.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.label_1 = wx.StaticText(self, -1, "Image dir")
        self.rootDire = wx.TextCtrl(self, -1, "/data/psii/")
        self.label_1_copy_2 = wx.StaticText(self, -1, "Schedule (start /data3)")
        self.scheDire = wx.TextCtrl(self, -1, "/data3/")
        self.label_2_copy = wx.StaticText(self, -1, "Data prefix")
        self.text_ctrl_3_copy = wx.TextCtrl(self, -1, "prefix")
        self.label_4 = wx.StaticText(self, -1, "Start phi")
        self.text_ctrl_4 = wx.TextCtrl(self, -1, "30.0")
        self.label_6 = wx.StaticText(self, -1, "[deg.]")
        self.label_7 = wx.StaticText(self, -1, "Step length")
        self.text_ctrl_5 = wx.TextCtrl(self, -1, "0.05")
        self.label_8 = wx.StaticText(self, -1, "[mm]")
        self.label_1_copy_1 = wx.StaticText(self, -1, "Start point")
        self.label_3 = wx.StaticText(self, -1, "X")
        self.sxBox = wx.TextCtrl(self, -1, "0.0000")
        self.label_3_copy = wx.StaticText(self, -1, "Y")
        self.syBox = wx.TextCtrl(self, -1, "0.0000")
        self.label_3_copy_1 = wx.StaticText(self, -1, "Z")
        self.szBox = wx.TextCtrl(self, -1, "0.0000")
        self.setStartXYZ = wx.Button(self, -1, "Set")
        self.label_1_copy_1_copy = wx.StaticText(self, -1, "End point")
        self.label_3_copy_2 = wx.StaticText(self, -1, "X")
        self.exBox = wx.TextCtrl(self, -1, "0.0000")
        self.label_3_copy_copy = wx.StaticText(self, -1, "Y")
        self.eyBox = wx.TextCtrl(self, -1, "0.0000")
        self.label_3_copy_1_copy = wx.StaticText(self, -1, "Z")
        self.ezBox = wx.TextCtrl(self, -1, "0.0000")
        self.setEndXYZ = wx.Button(self, -1, "Set")
        self.label_1_copy_1_copy_copy = wx.StaticText(self, -1, "End point")
        self.previewButton = wx.Button(self, -1, "Preview")
        self.genScheButton = wx.Button(self, -1, "Generate Schedule")
        self.label_10 = wx.StaticText(self, -1, "Vector length", style=wx.ALIGN_RIGHT)
        self.simVecLen = wx.TextCtrl(self, -1, "0.0000")
        self.label_11 = wx.StaticText(self, -1, "[mm]")
        self.label_10_copy = wx.StaticText(self, -1, "Gap dist", style=wx.ALIGN_RIGHT)
        self.simGapDist = wx.TextCtrl(self, -1, "0.0000")
        self.label_11_copy = wx.StaticText(self, -1, "[mm]")
        self.label_10_copy_1 = wx.StaticText(self, -1, "Points", style=wx.ALIGN_RIGHT)
        self.simNumPoints = wx.TextCtrl(self, -1, "0.0000")
        self.label_11_copy_1 = wx.StaticText(self, -1, "[pts]")
        self.sizer_9_staticbox = wx.StaticBox(self, -1, "")
        self.button_9 = wx.Button(self, -1, "pushQuit")
        self.appendButton = wx.Button(self, -1, "Append")
        self.deleteButton = wx.Button(self, -1, "Delete")
        self.clearAllButton = wx.Button(self, -1, "Clear All")
        self.button_6_copy = wx.Button(self, -1, "Save the list to file")
        self.sizer_3_staticbox = wx.StaticBox(self, -1, "Action")
        self.label_1_copy = wx.StaticText(self, -1, "Explanation of the point")
        self.inputComment = wx.TextCtrl(self, -1, "")
        self.sizer_8_staticbox = wx.StaticBox(self, -1, "Comment")
        self.list_ctrl_1 = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.button_6 = wx.Button(self, -1, "Move to the selected")
        self.sizer_7_staticbox = wx.StaticBox(self, -1, "LIST")
        self.sizer_6_copy_staticbox = wx.StaticBox(self, -1, "List")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.pushSetStart, self.setStartXYZ)
        self.Bind(wx.EVT_BUTTON, self.pushSetEnd, self.setEndXYZ)
        self.Bind(wx.EVT_BUTTON, self.pushPreview, self.previewButton)
        self.Bind(wx.EVT_BUTTON, self.pushGenSche, self.genScheButton)
        self.Bind(wx.EVT_BUTTON, self.pushQuit, self.button_9)
        self.Bind(wx.EVT_BUTTON, self.OnAppend, self.appendButton)
        self.Bind(wx.EVT_BUTTON, self.Ondelete, self.deleteButton)
        self.Bind(wx.EVT_BUTTON, self.OnClearAll, self.clearAllButton)
        self.Bind(wx.EVT_BUTTON, self.saveGlistToFile, self.button_6_copy)
        self.Bind(wx.EVT_LIST_INSERT_ITEM, self.OnListInsertItem, self.list_ctrl_1)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListSelected, self.list_ctrl_1)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDobleClick, self.list_ctrl_1)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnListColClick, self.list_ctrl_1)
        self.Bind(wx.EVT_BUTTON, self.moveToSelected, self.button_6)
        # end wxGlade

		# kuntaro definition
        host = '172.28.112.5'
        port = 10101
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host,port))
        self.s.settimeout(10.0)

        # Gonio definition
        self.list_ctrl_1.InsertColumn(0,"GonioX",width=100)
        self.list_ctrl_1.InsertColumn(1,"GonioY",width=100)
        self.list_ctrl_1.InsertColumn(2,"GonioZ",width=100)
        self.list_ctrl_1.InsertColumn(3,"Comment",width=200)
        self.gonio=Gonio(self.s)
        self.selected=-1
        self.gonio_list=[]
        ttt=[0,0,0]
        self.sv=array(ttt)
        self.ev=array(ttt)
        self.stepphi=0.1

    def __set_properties(self):
        # begin wxGlade: MyFrame2.__set_properties
        self.SetTitle("KUMA system")
        self.label_1.SetMinSize((120, 21))
        self.rootDire.SetMinSize((500, 31))
        self.label_1_copy_2.SetMinSize((152, 21))
        self.scheDire.SetMinSize((500, 31))
        self.text_ctrl_3_copy.SetMinSize((200, 31))
        self.label_4.SetMinSize((120, 21))
        self.text_ctrl_4.SetMinSize((100, 31))
        self.text_ctrl_5.SetMinSize((110, 31))
        self.label_8.SetMinSize((32, 21))
        self.label_1_copy_1.SetMinSize((120, 21))
        self.label_3.SetMinSize((20, 21))
        self.sxBox.SetMinSize((100, 31))
        self.label_3_copy.SetMinSize((20, 21))
        self.syBox.SetMinSize((100, 31))
        self.label_3_copy_1.SetMinSize((20, 21))
        self.szBox.SetMinSize((100, 31))
        self.label_1_copy_1_copy.SetMinSize((120, 21))
        self.label_3_copy_2.SetMinSize((20, 21))
        self.exBox.SetMinSize((100, 31))
        self.label_3_copy_copy.SetMinSize((20, 21))
        self.eyBox.SetMinSize((100, 31))
        self.label_3_copy_1_copy.SetMinSize((20, 21))
        self.ezBox.SetMinSize((100, 31))
        self.label_1_copy_1_copy_copy.SetMinSize((120, 21))
        self.genScheButton.SetMinSize((150, 50))
        self.label_10.SetMinSize((100, 21))
        self.simVecLen.SetMinSize((100, 31))
        self.simVecLen.SetBackgroundColour(wx.Colour(212, 209, 219))
        self.label_10_copy.SetMinSize((100, 21))
        self.simGapDist.SetMinSize((100, 31))
        self.simGapDist.SetBackgroundColour(wx.Colour(212, 209, 219))
        self.label_10_copy_1.SetMinSize((100, 21))
        self.simNumPoints.SetMinSize((100, 31))
        self.simNumPoints.SetBackgroundColour(wx.Colour(212, 209, 219))
        self.button_9.SetBackgroundColour(wx.Colour(255, 69, 10))
        self.button_9.SetForegroundColour(wx.Colour(0, 0, 0))
        self.appendButton.SetMinSize((117, 32))
        self.deleteButton.SetMinSize((117, 32))
        self.clearAllButton.SetMinSize((117, 32))
        self.button_6_copy.SetMinSize((117, 32))
        self.label_1_copy.SetMinSize((156, 25))
        self.inputComment.SetMinSize((200, 25))
        self.list_ctrl_1.SetMinSize((300,200))
        self.button_6.SetMinSize((150, 32))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame2.__do_layout
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_6_copy_staticbox.Lower()
        sizer_6_copy = wx.StaticBoxSizer(self.sizer_6_copy_staticbox, wx.HORIZONTAL)
        self.sizer_7_staticbox.Lower()
        sizer_7 = wx.StaticBoxSizer(self.sizer_7_staticbox, wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_8_staticbox.Lower()
        sizer_8 = wx.StaticBoxSizer(self.sizer_8_staticbox, wx.HORIZONTAL)
        self.sizer_3_staticbox.Lower()
        sizer_3 = wx.StaticBoxSizer(self.sizer_3_staticbox, wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_17 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_9_staticbox.Lower()
        sizer_9 = wx.StaticBoxSizer(self.sizer_9_staticbox, wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_12_copy_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2_copy_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2_copy_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2_copy_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.label_1, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(self.rootDire, 0, wx.ADJUST_MINSIZE, 0)
        sizer_10.Add(sizer_2, 1, wx.EXPAND, 0)
        sizer_2_copy_2.Add(self.label_1_copy_2, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2_copy_2.Add(self.scheDire, 0, wx.ADJUST_MINSIZE, 0)
        sizer_10.Add(sizer_2_copy_2, 1, wx.EXPAND, 0)
        sizer_2_copy_1.Add(self.label_2_copy, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2_copy_1.Add(self.text_ctrl_3_copy, 0, wx.ADJUST_MINSIZE, 0)
        sizer_10.Add(sizer_2_copy_1, 1, wx.EXPAND, 0)
        sizer_4.Add(self.label_4, 0, wx.ADJUST_MINSIZE, 0)
        sizer_4.Add(self.text_ctrl_4, 0, wx.ADJUST_MINSIZE, 0)
        sizer_4.Add(self.label_6, 0, wx.ADJUST_MINSIZE, 0)
        sizer_4.Add((50, 20), 0, wx.ADJUST_MINSIZE, 0)
        sizer_4.Add(self.label_7, 0, wx.ADJUST_MINSIZE, 0)
        sizer_4.Add(self.text_ctrl_5, 0, wx.ADJUST_MINSIZE, 0)
        sizer_4.Add(self.label_8, 0, wx.ADJUST_MINSIZE, 0)
        sizer_10.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_2_copy.Add(self.label_1_copy_1, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2_copy.Add(self.label_3, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2_copy.Add(self.sxBox, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2_copy.Add(self.label_3_copy, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2_copy.Add(self.syBox, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2_copy.Add(self.label_3_copy_1, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2_copy.Add(self.szBox, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2_copy.Add(self.setStartXYZ, 0, wx.ADJUST_MINSIZE, 0)
        sizer_10.Add(sizer_2_copy, 1, wx.EXPAND, 0)
        sizer_2_copy_copy.Add(self.label_1_copy_1_copy, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2_copy_copy.Add(self.label_3_copy_2, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2_copy_copy.Add(self.exBox, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2_copy_copy.Add(self.label_3_copy_copy, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2_copy_copy.Add(self.eyBox, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2_copy_copy.Add(self.label_3_copy_1_copy, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2_copy_copy.Add(self.ezBox, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2_copy_copy.Add(self.setEndXYZ, 0, wx.ADJUST_MINSIZE, 0)
        sizer_10.Add(sizer_2_copy_copy, 1, wx.EXPAND, 0)
        sizer_6.Add(self.label_1_copy_1_copy_copy, 0, wx.ADJUST_MINSIZE, 0)
        sizer_6.Add(self.previewButton, 0, wx.ADJUST_MINSIZE, 0)
        sizer_6.Add(self.genScheButton, 0, wx.ADJUST_MINSIZE, 0)
        sizer_10.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_9.Add(sizer_10, 0, wx.EXPAND, 0)
        sizer_11.Add((20, 31), 0, wx.ADJUST_MINSIZE, 0)
        sizer_12.Add((20, 20), 0, wx.ADJUST_MINSIZE, 0)
        sizer_12.Add(self.label_10, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_12.Add(self.simVecLen, 0, wx.ADJUST_MINSIZE, 0)
        sizer_12.Add(self.label_11, 0, wx.ADJUST_MINSIZE, 0)
        sizer_11.Add(sizer_12, 1, wx.EXPAND, 0)
        sizer_12_copy.Add((20, 20), 0, wx.ADJUST_MINSIZE, 0)
        sizer_12_copy.Add(self.label_10_copy, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_12_copy.Add(self.simGapDist, 0, wx.ADJUST_MINSIZE, 0)
        sizer_12_copy.Add(self.label_11_copy, 0, wx.ADJUST_MINSIZE, 0)
        sizer_11.Add(sizer_12_copy, 1, wx.EXPAND, 0)
        sizer_12_copy_1.Add((20, 20), 0, wx.ADJUST_MINSIZE, 0)
        sizer_12_copy_1.Add(self.label_10_copy_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_12_copy_1.Add(self.simNumPoints, 0, wx.ADJUST_MINSIZE, 0)
        sizer_12_copy_1.Add(self.label_11_copy_1, 0, wx.ADJUST_MINSIZE, 0)
        sizer_11.Add(sizer_12_copy_1, 1, wx.EXPAND, 0)
        sizer_9.Add(sizer_11, 1, wx.EXPAND, 0)
        sizer_17.Add(sizer_9, 1, wx.EXPAND, 0)
        sizer_17.Add(self.button_9, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        sizer_5.Add(sizer_17, 0, wx.EXPAND, 0)
        sizer_5.Add(sizer_1, 1, wx.EXPAND, 0)
        sizer_3.Add(self.appendButton, 0, wx.ALL, 10)
        sizer_3.Add(self.deleteButton, 0, wx.ALL, 10)
        sizer_3.Add(self.clearAllButton, 0, wx.ALL, 10)
        sizer_3.Add(self.button_6_copy, 0, wx.ALL, 10)
        sizer_6_copy.Add(sizer_3, 0, wx.ALL|wx.EXPAND, 10)
        sizer_8.Add(self.label_1_copy, 0, 0, 0)
        sizer_8.Add(self.inputComment, 0, 0, 0)
        sizer_7.Add(sizer_8, 0, wx.EXPAND, 0)
        sizer_7.Add(self.list_ctrl_1, 3, wx.ALL|wx.EXPAND, 10)
        sizer_13.Add((200, 20), 0, 0, 0)
        sizer_13.Add(self.button_6, 0, 0, 0)
        sizer_7.Add(sizer_13, 0, wx.EXPAND, 0)
        sizer_6_copy.Add(sizer_7, 1, wx.EXPAND, 0)
        sizer_5.Add(sizer_6_copy, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_5)
        sizer_5.Fit(self)
        self.Layout()
        # end wxGlade

    def pushSetStart(self, event): # wxGlade: MyFrame2.<event_handler>
        if self.selected!=-1:
                xstr=self.list_ctrl_1.GetItem(self.selected,0).GetText()
                ystr=self.list_ctrl_1.GetItem(self.selected,1).GetText()
                zstr=self.list_ctrl_1.GetItem(self.selected,2).GetText()

                xmm=float(xstr)
                ymm=float(ystr)
                zmm=float(zstr)

		tmp=[xmm,ymm,zmm]
		self.sv=array(tmp)

        self.sxBox.SetValue(xstr)
        self.syBox.SetValue(ystr)
        self.szBox.SetValue(zstr)

    def pushSetEnd(self, event): # wxGlade: MyFrame2.<event_handler>
        if self.selected!=-1:
                xstr=self.list_ctrl_1.GetItem(self.selected,0).GetText()
                ystr=self.list_ctrl_1.GetItem(self.selected,1).GetText()
                zstr=self.list_ctrl_1.GetItem(self.selected,2).GetText()

                xmm=float(xstr)
                ymm=float(ystr)
                zmm=float(zstr)


		#TEMP
		#zmm=zmm+0.1
		tmp=[xmm,ymm,zmm]
		self.ev=array(tmp)

        #str="%8.4f %8.4f %8.4f"%(xmm,ymm,zmm)
        self.exBox.SetValue(xstr)
        self.eyBox.SetValue(ystr)
        self.ezBox.SetValue(zstr)

        #self.gv.setOrigVec(xmm,ymm,zmm)

    def prep(self):
        vec=self.ev-self.sv
        self.veclen=linalg.norm(vec)
        # PHI string
        self.phi=float(self.text_ctrl_4.GetValue())
        #print "PHI",self.phi
        phirad=radians(self.phi)
        cosphi=cos(phirad)
        # step length
        step=float(self.text_ctrl_5.GetValue())
        self.step_mod=step*1.0/cosphi
		# N points
        self.npoints=int(self.veclen/self.step_mod)+1
		# Recalculating step length based on N points
        if self.npoints!=1:
            self.step_mod=self.veclen/float(self.npoints-1)
        else:
            print "Too short!!!"
        print self.npoints
        # Offset
        self.offset=int(self.phi/self.stepphi)

    def setPreview(self):
		self.simVecLen.SetValue("%8.4f"%self.veclen)
		self.simGapDist.SetValue("%8.4f"%self.step_mod)
		self.simNumPoints.SetValue("%d"%self.npoints)

    def pushPreview(self, event): # wxGlade: MyFrame2.<event_handler>
		self.prep()
		self.setPreview()

    def pushGenSche(self, event): # wxGlade: MyFrame2.<event_handler>
        self.prep()
        self.setPreview()

        step_mod_um=self.step_mod*1000.0 # mm to um

        # Schedule file
        sch=ScheduleSACLA()

        start=[self.sv[0],self.sv[1],self.sv[2]]
        end=[self.ev[0],self.ev[1],self.ev[2]]

        sch.stepAdvanced(start,end,step_mod_um,1,self.phi,self.stepphi,1)
        sch.setOffset(self.offset)
        sch.setDataName(self.text_ctrl_3_copy.GetValue())
        sch.setDir(self.rootDire.GetValue())

        # Activate honmono
        sch_dire=self.scheDire.GetValue()
        schfile="%s/psii.sch"%sch_dire
        sch.make(schfile)

    def pushQuit(self, event): # wxGlade: MyFrame2.<event_handler>
		self.s.close()
		print "Close connection"

    def OnAppend(self, event): # wxGlade: MyFrame2.<event_handler>
        phi="%8.2f"%self.gonio.getPhi()
        gx="%8.4f"%self.gonio.getXmm()
        gy="%8.4f"%self.gonio.getYmm()
        gz="%8.4f"%self.gonio.getZmm()

        code=(phi,gx,gy,gz)
        self.gonio_list.insert(0,code)

        # get comment
        comment=self.inputComment.GetValue()

        self.list_ctrl_1.InsertStringItem(0,gx)
        self.list_ctrl_1.SetStringItem(0,1,gy)
        self.list_ctrl_1.SetStringItem(0,2,gz)
        self.list_ctrl_1.SetStringItem(0,3,comment)

    def Ondelete(self, event): # wxGlade: MyFrame2.<event_handler>
        if self.selected!=-1:
                self.list_ctrl_1.DeleteItem(self.selected)
                del self.gonio_list[self.selected]
                print self.gonio_list
                self.selected=-1

        if len(self.gonio_list)==0:
                self.selected=-1

    def OnClearAll(self, event): # wxGlade: MyFrame2.<event_handler>
        self.list_ctrl_1.DeleteAllItems()
        self.gonio_list=[]
        self.selected=-1

    def saveGlistToFile(self, event): # wxGlade: MyFrame2.<event_handler>
        print "Event handler `saveGlistToFile' not implemented!"
        event.Skip()

    def OnListInsertItem(self, event): # wxGlade: MyFrame2.<event_handler>
        print "Event handler `OnListInsertItem' not implemented!"
        event.Skip()

    def OnListSelected(self, event): # wxGlade: MyFrame2.<event_handler>
        print "Event handler `OnListSelected' not implemented!"
        event.Skip()

    def OnDobleClick(self, event): # wxGlade: MyFrame2.<event_handler>
        print "Event handler `OnDobleClick' not implemented!"
        event.Skip()

    def OnListColClick(self, event): # wxGlade: MyFrame2.<event_handler>
        print "Event handler `OnListColClick' not implemented!"
        event.Skip()

    def moveToSelected(self, event): # wxGlade: MyFrame2.<event_handler>
        if self.selected!=-1:
                xstr=self.list_ctrl_1.GetItem(self.selected,0).GetText()
                ystr=self.list_ctrl_1.GetItem(self.selected,1).GetText()
                zstr=self.list_ctrl_1.GetItem(self.selected,2).GetText()

                xmm=float(xstr)
                ymm=float(ystr)
                zmm=float(zstr)
                self.gonio.moveXYZmm(xmm,ymm,zmm)

    def OnListSelected(self, event): # wxGlade: MyFrame2.<event_handler>
        self.selected=event.m_itemIndex


# end of class MyFrame2


class ExpCondDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ExpCondDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.label_5 = wx.StaticText(self, -1, "Directory", style=wx.ALIGN_CENTRE)
        self.text_ctrl_1 = wx.TextCtrl(self, -1, "")
        self.label_5_copy = wx.StaticText(self, -1, "Data name", style=wx.ALIGN_CENTRE)
        self.text_ctrl_1_copy = wx.TextCtrl(self, -1, "")
        self.label_5_copy_copy = wx.StaticText(self, -1, "Start serial", style=wx.ALIGN_CENTRE)
        self.text_ctrl_1_copy_copy = wx.TextCtrl(self, -1, "")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ExpCondDialog.__set_properties
        self.SetTitle("dialog_1")
        self.label_5.SetMinSize((100, 18))
        self.text_ctrl_1.SetMinSize((200, 25))
        self.label_5_copy.SetMinSize((100, 25))
        self.text_ctrl_1_copy.SetMinSize((100, 25))
        self.label_5_copy_copy.SetMinSize((74, 18))
        self.text_ctrl_1_copy_copy.SetMinSize((100, 25))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ExpCondDialog.__do_layout
        sizer_14 = wx.BoxSizer(wx.VERTICAL)
        sizer_16_copy_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_16 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_16.Add(self.label_5, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_16.Add(self.text_ctrl_1, 0, 0, 0)
        sizer_14.Add(sizer_16, 0, wx.EXPAND, 0)
        sizer_16_copy_4.Add(self.label_5_copy, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_16_copy_4.Add(self.text_ctrl_1_copy, 0, 0, 0)
        sizer_16_copy_4.Add(self.label_5_copy_copy, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_16_copy_4.Add(self.text_ctrl_1_copy_copy, 0, 0, 0)
        sizer_14.Add(sizer_16_copy_4, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_14)
        sizer_14.Fit(self)
        self.Layout()
        # end wxGlade

# end of class ExpCondDialog


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("frame_1")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_26 = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer_26)
        sizer_26.Fit(self)
        self.Layout()
        # end wxGlade

# end of class MyFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_3 = MyFrame2(None, -1, "")
    app.SetTopWindow(frame_3)
    frame_3.Show()
    app.MainLoop()
