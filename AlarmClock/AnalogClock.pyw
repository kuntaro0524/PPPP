#!/usr/bin/env python
"""Analog Clock Program"""

#NOTE: Program Properties
__moduleName__ = "AnalogClock.pyw"
__version__ = "11.0611"
__creationDate__ = "2006/12/27"
__revisionDate__ = "2011/06/11"
__author__ = '\"Randy Raymond\" <RandyERaymond@aim.com>'
__history__ = """
11.0611 Work on a persistent alarm file
"""
#TODO: Make a prettier dialog box

#NOTE: Program Imports
import wx, os, platform, pickle
import datetime as dt
import wx.lib.analogclock as ac
import wx.lib.masked as masked
import wx.lib.agw.genericmessagedialog as GMD

#NOTE: Global Variables
wildFile = "WAV File |*.wav|" \
           "All files |*.*"
# file paths
startPath = os.getcwd()
defSndDir = os.path.join(os.path.split(startPath)[0],"Sounds")
alarmFile = os.path.join( startPath, "alarmFile.pkl" )
# location of icon images
iC_ImagePath = startPath
# location of toolbar images
tB_ImagePath = startPath
# the time between alarm checks: 1000 * (Number of Seconds); or,
#  60000 * (Number of Minutes)
refreshDelay = 15000
# Toolbar Flags
TBFLAGS = ( wx.TB_HORIZONTAL
    | wx.NO_BORDER
    | wx.TB_FLAT
    #| wx.TB_TEXT
    #| wx.TB_HORZ_LAYOUT
    )
# Text Control Flags
TCFLAGS = (
    #wx.TE_PROCESS_ENTER
    #| wx.TE_PROCESS_TAB
    wx.TE_MULTILINE
    #| wx.TE_PASSWORD
    #| wx.TE_READONLY
    | wx.TE_RICH
    #| wx.TE_RICH2
    #| wx.TE_AUTO_URL
    #| wx.TE_NOHIDESEL
    #| wx.HSCROLL
    #| wx.TE_LEFT
    #| wx.TE_CENTRE
    #| wx.TE_RIGHT
    #| wx.TE_DONTWRAP
    #| wx.TE_CHARWRAP
    | wx.TE_WORDWRAP
    #| wx.TE_BESTWRAP
    #| wx.TE_CAPITALIZE
    )
#NOTE: Setup the About Box Information
aboutMsg = __moduleName__+" module is an analog display routine.\n\n" + \
    "Author: " + __author__ + "\n\n" + \
    "Please report any bugs, requests or improvements\n" + \
    "to me.\n\n" + \
    "Welcome to wxPython " + wx.VERSION_STRING + "!!"
aboutBoxTitle = "About the Program"
aboutBtnStyle = (
    #wx.OK
    #wx.YES_NO
    #wx.CANCEL
    #wx.YES
    #wx.NO
    wx.NO_DEFAULT
    #wx.HELP
    )
aboutDlgStyle = (
    wx.ICON_INFORMATION
    #wx.ICON_WARNING
    #wx.ICON_EXCLAMATION
    #wx.ICON_ERROR
    #wx.ICON_QUESTION
    )
aboutIconFile = "about.PNG"

class MyAlrmDlg(wx.Dialog):
    """This modal dialog box collects alarm time & sound from user"""
    def __init__( self, *args, **kwds ):
        wx.Dialog.__init__(self, None, -1, 'Alarm Box' )
        self.SetSize((200,100))
        st = wx.StaticText(self, -1, '  Pick an alarm time  ')
        self.tc = masked.TextCtrl( self, -1, "",
            mask         = "##/##/#### ##:## AM",
            excludeChars = "BCDEFGHIJKLMNOQRSTUVWXYZ",
            formatcodes  = "DF!",
            includeChars = "",
            validRegex   = "",
            validRange   = "",
            choices      = "",
            choiceRequired = True,
            defaultValue = wx.DateTime_Now().Format("%m/%d/%Y %I:%M %p"),
            demo         = True,
            name         = "MaskedInput")
        self.tc2 = wx.TextCtrl( self,
            -1,
            value = "text control",
            pos = wx.DefaultPosition,
            size = wx.DefaultSize,
            style = TCFLAGS,
            )
        b1 = wx.Button( self, wx.ID_CANCEL )
        b2 = wx.Button( self, wx.ID_OK )
        dlgSizer = wx.BoxSizer( wx.VERTICAL )
        dlgSizer.Add( st )
        dlgSizer.Add( self.tc )
        dlgSizer.Add( self.tc2 )
        btnSizer = wx.FlexGridSizer( cols=2, hgap=4, vgap=4 )
        btnSizer.Add( b1 )
        btnSizer.Add( b2 )
        dlgSizer.Add( btnSizer )
        self.SetSizer(dlgSizer)
        dlgSizer.Fit(self)
        dlgSizer.Layout()

#class UIFrame(wx.MiniFrame):   # this one hides stuff
class UIFrame(wx.Frame):
    """Create a Frame instance and make instance of panel"""
    def __init__(self, *args, **kwds):

        # the height of the frame client area determines the number height
        self.frameSize = ( 200, 230 )
        self.frameStyle = \
            wx.DEFAULT_FRAME_STYLE
        #    wx.BORDER_SUNKEN\
        #    | wx.BORDER_THEME
        #    | wx.CLIP_CHILDREN
        #    | wx.NO_FULL_REPAINT_ON_RESIZE
        #    | wx.FRAME_NO_TASKBAR\
        self.frameIconFile = "ELT.ICO"
        self.frameTitle = __moduleName__
        self.screenRes = wx.GetClientDisplayRect()[2:]
        self.frameLocation = ( self.screenRes[0]-self.frameSize[0], 0 )

        wx.Frame.__init__(self, None, -1, "", 
            self.frameLocation, 
            size=self.frameSize,
            style=self.frameStyle
            )

        #NOTE: now allow for a list of alarms, Time & Message
        try:
            self.alarm_file = open(alarmFile, 'rb')
            self.AlarmDB = pickle.load(self.alarm_file)
            self.alarm_file.close()
        except:
            print "File alarmFile.pkl was not read in. A new one will be created."
            self.AlarmDB = list()
        # default alarm sound
        self.AlarmSound = "BANJO.WAV"

        # Date for the status bar
        self.CurrentDate=dt.datetime.today()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.CreateMenuBar()
        self.CreateStatusBar()
        self.__set_properties()
        self.__do_layout()

        # idle event repaints the status bar date
        self.Bind(wx.EVT_IDLE, self.OnIdleStatus)

        # setup a timer for the alarms
        self.alarmTimer = wx.Timer()
        self.alarmTimer.Start(refreshDelay)
        self.alarmTimer.Bind(wx.EVT_TIMER, self.OnAlarmTimer)

    def __set_properties(self):
        self.SetTitle(self.frameTitle)
        self.SetIcon(wx.Icon(os.path.join(iC_ImagePath, self.frameIconFile),
            wx.BITMAP_TYPE_ICO))
        self.SetStatusText(self.CurrentDate.ctime()[:10] +" "+\
            self.CurrentDate.ctime()[-4:])

    def __do_layout(self):
        """Setup the clock features"""
        c2 = ac.AnalogClock(self,
            hoursStyle=ac.TICKS_DECIMAL,
            minutesStyle=ac.TICKS_CIRCLE,
            clockStyle=ac.SHOW_HOURS_TICKS |
                       ac.SHOW_MINUTES_TICKS |
                       ac.SHOW_HOURS_HAND |
                       ac.SHOW_MINUTES_HAND #|
                       #ac.SHOW_SECONDS_HAND
            )
        c2.SetTickSize(25, target=ac.HOUR)
        c2.SetTickFont(wx.Font(12, wx.FONTFAMILY_ROMAN, wx.NORMAL, wx.BOLD))
        c2.SetHandFillColour(wx.Colour(0, 255, 0), target=ac.HOUR)
        c2.SetHandBorderColour(wx.Colour(0, 0, 0))
        c2.SetHandFillColour(wx.Colour(255, 0, 128), target=ac.MINUTE)
        c2.SetHandBorderColour(wx.Colour(0, 0, 0))
        c2.SetTickFillColour(wx.BLACK)
        c2.SetTickBorderColour(wx.BLACK)
        c2.SetFaceBorderWidth(1)
        #c2.SetForegroundColour(wx.Colour(0, 0, 0))
        c2.SetBackgroundColour(wx.Colour(155, 180, 208))
        c2.SetFaceFillColour(wx.Colour(155, 180, 208))
        #c2.SetShadowColour(wx.Colour(255, 213, 213))

    #NOTE: Menubar creation methods
    def CreateMenuBar( self ):
        def menuData():
            return ((
                "&File",
                    ("&Sound", "Pick a Sound File To Play", self.OnSelectSound),
                    ("&Alarm", "Pick an alarm time.", self.OnAlarmSelect),
                    ("", "", ""),
                    ("&Quit", "Shutdown the Calendar Program.", self.OnClose)),
                ("Help",
                    ("&About", "Information about this program", self.OnAbout)
                ))
        def CreateMenu( menuData ):
            menu = wx.Menu()
            for eachLabel, eachStatus, eachHandler in menuData:
                if not eachLabel:
                    menu.AppendSeparator()
                    continue
                menuItem = menu.Append(-1, eachLabel, eachStatus)
                self.Bind(wx.EVT_MENU, eachHandler, menuItem)
            return menu
        menuBar = wx.MenuBar()
        for eachMenuData in menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1:]
            menuBar.Append(CreateMenu(menuItems), menuLabel)
        self.SetMenuBar(menuBar)

    def OnSelectSound( self, evt ):
        global defSndDir
        dlg = wx.FileDialog(wx.GetTopLevelParent(self),
                            message = "Choose an alarm sound",
                            defaultDir = defSndDir,
                            wildcard = wildFile,
                            style = wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.AlarmSound = dlg.GetPath()
            defSndDir = os.path.split(self.AlarmSound)[0]
        dlg.Destroy()

    def OnAlarmSelect( self, evt ):
        dlg = MyAlrmDlg()
        if dlg.ShowModal() == wx.ID_OK:
            strTime = dlg.tc.GetValue()
            if (strTime[17:18] == 'P') and (strTime[11:13] != '12'):
                iHour = int(strTime[11:13])+12
            else:
                iHour = int(strTime[11:13])
            self.AlarmCheck = True
            aTime = dt.datetime(
                int(strTime[6:10]),
                int(strTime[:2]),
                int(strTime[3:5]),
                iHour,
                int(strTime[14:16]),
                )
            self.AlarmDB.append([
                aTime,              # alarm time
                dlg.tc2.GetValue()  # alarm message
                ])
        dlg.Destroy()

    def OnAlarmTimer( self, evt ):
        """when the timer event fires, come here"""
        # stop timer so that we don't get multiple messages
        self.alarmTimer.Stop()
        for i in self.AlarmDB:
            # i will be list of pairs, time & message
            if dt.datetime.now() >= i[0]:
                # alarm time is up, try to sound the alarm
                try:
                    alarmMsg = i[1]+" -> "+str(i[0])
                    wx.Sound.PlaySound(self.AlarmSound, wx.SOUND_SYNC)
                    dlgAlarm = wx.MessageDialog( self,
                        alarmMsg,
                        'Alarm Message Box',
                        wx.OK | wx.ICON_INFORMATION
                        #| wx.YES_NO
                        #| wx.NO_DEFAULT
                        #| wx.CANCEL
                        #| wx.ICON_INFORMATION
                        )
                    dlgAlarm.ShowModal()
                    dlgAlarm.Destroy()
                except NotImplementedError, v:
                    wx.MessageBox(str(v), "Exception Message")
                self.AlarmDB.remove(i)

        #NOTE: store a list of alarms before leaving
        try:
            self.alarm_file = open( alarmFile, 'wb' )
            pickle.dump( self.AlarmDB, self.alarm_file )
            self.alarm_file.close()
        except:
            print "Something went wrong with the alarmFile.pkl file save."
        # restart the timer now, before we leave
        self.alarmTimer.Start()

    def Reserved(self, event):
        pass

    def OnIdleStatus(self, event):
        """refresh the status bar time"""
        self.SetStatusText(self.CurrentDate.ctime()[:10]+" "+\
            self.CurrentDate.ctime()[-4:])

    def OnAbout(self, event):
        dlg = GMD.GenericMessageDialog( self, aboutMsg, aboutBoxTitle,
            aboutBtnStyle | aboutDlgStyle )
        dlg.SetIcon(wx.Icon(os.path.join(iC_ImagePath,aboutIconFile),
            eval("wx.BITMAP_TYPE_"+aboutIconFile[-3:])))
        dlg.ShowModal()
        dlg.Destroy()

    def OnClose(self, event):
        self.Close()
        self.Destroy()
        event.Skip()

class App(wx.App):
    """Application class"""

    def OnInit(self):
        self.frame = UIFrame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

def main():
    app = App()
    app.MainLoop()

if __name__ == '__main__':
    main()
