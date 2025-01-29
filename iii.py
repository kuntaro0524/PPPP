#!/usr/bin/env python

import wx
import time
import serial
import multiprocessing

# begin wxGlade: extracode
# end wxGlade

class CryoFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: CryoFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.label_1 = wx.StaticText(self, -1, "Current")

        ser = serial.Serial(
                port='/dev/ttyS0',
                baudrate=9600,
                parity=serial.PARITY_EVEN,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.SEVENBITS,
                timeout=1
        )
        # define the control character
        stx = chr(2)
        etx = chr(3)
        cr = chr(13)
        lf = chr(10)
        ser.close()
        ser.open()
        input1 = ' 1, 1,'
        input2 = 'DF'
        ser.write(stx + input1 + etx + input2 + cr + lf)
        #print stx+input1+etx+input2+cr+lf
        out = ''
        out = ser.readline()
        current = out[6:14]
	setvalue = out[17:25]
        ser.close()

        self.text_ctrl_1 = wx.TextCtrl(self, -1, current)
        self.label_2 = wx.StaticText(self, -1, " K")
        self.button_1 = wx.Button(self, -1, "Set Value")
        self.text_ctrl_2 = wx.TextCtrl(self, -1, setvalue)
        self.label_3 = wx.StaticText(self, -1, " K")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnClicked, self.button_1)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: CryoFrame.__set_properties
        self.SetTitle("frame_1")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: CryoFrame.__do_layout

        ser = serial.Serial(
                port='/dev/ttyS0',
                baudrate=9600,
                parity=serial.PARITY_EVEN,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.SEVENBITS,
                timeout=1
        )
        # define the control character
        stx = chr(2)
        etx = chr(3)
        cr = chr(13)
        lf = chr(10)
        ser.close()
        ser.open()
        input1 = ' 1, 1,'
        input2 = 'DF'
        ser.write(stx + input1 + etx + input2 + cr + lf)
        #print stx+input1+etx+input2+cr+lf
        out = ''
        out = ser.readline()
        ret = out[6:14]
        ser.close()
	

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(2, 3, 0, 0)
        grid_sizer_1.Add(self.label_1, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.text_ctrl_1, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.label_2, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.button_1, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.text_ctrl_2, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.label_3, 0, wx.ADJUST_MINSIZE, 0)
        sizer_1.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)

        self.Layout()
        # end wxGlade

    def OnClicked(self, event): # wxGlade: CryoFrame.<event_handler>
	# configure the serial connections (the parameters differs on the device you are connecting to)
	ser = serial.Serial(
	        port='/dev/ttyS0',
		baudrate=9600,
		parity=serial.PARITY_EVEN,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.SEVENBITS,
		timeout=1
	)

	# define the control character
	stx = chr(2)
	etx = chr(3)
	cr = chr(13)
	lf = chr(10)

	ser.close()
	ser.open()

	input = self.text_ctrl_2.GetValue()
	length = len(input)
	#print length
        if length == 8:
                input = input + ','
 	elif length == 7:
		input = ' ' + input + ','
        elif length == 6:
                input = '  ' + input + ','
        elif length == 5:
                input = '   ' + input + ','
        elif length == 4:
                input = '    ' + input + ','
        elif length == 3:
                input = '     ' + input + ','
        elif length == 2:
                input = '      ' + input + ','
        elif length <= 1:
                input = setvalue + ','
        elif length > 8:
                input = input[length-7:length] + ','


	input1 = '11, 0,' + input

	que = input1 + etx
	sum = 0
	w = 0
	for s in que:
	        v = ord(s)
	        w += v
	sum = '%x' % w
	BCC = sum[-1] + sum[-2]
	print BCC

	operation=unicode(stx + input1 + etx + BCC + cr + lf)
	ser.write(operation)

	print stx + input1 + etx + BCC + cr + lf
	out = ''
	out = ser.readline()

	if out[0] == 'A':
		print "Set Value Successfully",
	elif out[0] == 'N':
		print "Communication fault"
	elif out[0] == 'C':
		print "Check Sum Error"
	elif out[0] == 'L':
		print "DB Lock Error"
	elif out[0] == 'F':
		print "Format Error"
	elif out[0] == 'D':
		print "Data Error"
	
	#print out
	ser.close()

	self.__set_properties()

        ser.open()
        input1 = ' 1, 1,'
        input2 = 'DF'
	ustr=unicode(stx+input1+etx+input2+cr+lf)
        ser.write(ustr)
        out = ''
        out = ser.readline()
        current = out[6:14]
        setvalue = out[17:25]
        ser.close()

	self.text_ctrl_1 = wx.TextCtrl(self, -1, current)
        self.__set_properties()
        self.__do_layout()

        event.Skip()
# end of class CryoFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    cryoframe_1 = CryoFrame(None, -1, "")
    app.SetTopWindow(cryoframe_1)
    cryoframe_1.Show()
    app.MainLoop()
