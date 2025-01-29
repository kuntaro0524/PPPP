"""
This program implements a bare-bones text editor
that can load, modify and save documents.
"""

__author__     = "Aaron Straup Cope"
__url__        = "http://aaronland.info/python/wxpython/examples/005-wx-textedit.py"
__version__    = "0.1"
__cvsversion__ = "$Revision: 1.1 $"
__date__       = "$Date: 2004/04/02 14:42:59 $"
__copyright__  = "Copyright (c) 2004 Aaron Straup Cope"
__license__    = "Python"

from wxPython.wx import *
from sys import argv
import os

#

TITLE       = "wxExampleCode: simple text editor"
ABOUT_TITLE = "About Me"
ABOUT_BODY  = "wxExampleCode: simple text editor\n" \
	      "http://aaronland.info/python/wxpython/examples/"

ID_ABOUT  = wxNewId()
ID_OPEN	  = wxNewId()
ID_SAVE	  = wxNewId()
ID_SAVEAS = wxNewId()
ID_EXIT   = wxNewId()

#

class MyFrame(wxFrame):
    def __init__(self, parent, ID, title):

	self.__filename__ = NULL
	
	#

        wxFrame.__init__(self, parent, ID, title,
                         wxDefaultPosition,
			 wxSize(400, 600),
			 style=wxDEFAULT_FRAME_STYLE|wxNO_FULL_REPAINT_ON_RESIZE)


        self.CreateStatusBar()
        self.SetStatusText("This is the statusbar")

	#

        FileMenu = wxMenu()

        FileMenu.Append(ID_OPEN,
			"&Open",
			"Open a document")

        FileMenu.AppendSeparator()

        FileMenu.Append(ID_SAVE,
			"&Save",
			"Save current document")

        FileMenu.Append(ID_SAVEAS,
			"Save as",
			"Save current document to another file")

        FileMenu.AppendSeparator()

        FileMenu.Append(ID_EXIT,
			"E&xit",
			"Terminate the program")

	#

        HelpMenu = wxMenu()

        HelpMenu.Append(ID_ABOUT,
			"&About",
			"More information about this program")

        #
		    
        menuBar = wxMenuBar()

        menuBar.Append(FileMenu, "&File")
	menuBar.Append(HelpMenu,"&Help")

        self.SetMenuBar(menuBar)

	#

        EVT_MENU(self, ID_ABOUT,  self.About)
        EVT_MENU(self, ID_SAVE,   self.Save)
        EVT_MENU(self, ID_SAVEAS, self.SaveAs)
        EVT_MENU(self, ID_OPEN,   self.Open)
        EVT_MENU(self, ID_EXIT,   self.Quit)

	#

        self.control = wxTextCtrl(self,
				  1,
				  style=wxTE_MULTILINE)

        #
				  
        if len(argv) > 1:

	   if os.path.exists(argv[1]):
	      self.Load(argv[1])
	   else:
	      self.Alert("Error",
			 argv[1] + "is not a valid file")


    #

    def About(self, event):
	self.Alert(ABOUT_TITLE,ABOUT_BODY)

    #

    def Open(self,event):

	filename = wxFileSelector("Choose a file to open")

	if filename:
	    self.Load(filename)

    #
	    
    def Load(self,filename):

        self.__filename__ = filename

	self.control.LoadFile(filename)
	self.SetStatusText(filename)

    #

    def Save(self,event):

	if self.__filename__:
	   self.control.SaveFile(self.__filename__)
	else:
	   self.SaveAs(event)

    #

    def SaveAs(self,event) :

	   filename = wxFileSelector("Save current document as")

	   if filename:
	   	self.control.SaveFile(filename)
		self.__filename__ = filename
	   else:
		self.Alert("Alert","save as cancelled")

    #

    def Quit(self, event):

	if self.control.IsModified:

	   answer = wxMessageBox("Document has been modified\n"
			         "Do you want to save it?",
			         "Confirm",
			         wxYES_NO | wxCANCEL);

	   if (answer == wxYES):
	      self.Save(event)

	   if (answer == wxCANCEL):
	      return false

        self.Close(true)

    #

    def Alert(self,title,msg):
        dlg = wxMessageDialog(self, msg,
                              title,
			      wxOK | wxICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

#

class MyApp(wxApp):
      def OnInit(self):
        frame = MyFrame(NULL, -1, TITLE)
        frame.Show(true)
        self.SetTopWindow(frame)

        return true

#

app = MyApp()
app.MainLoop()

