from wxPython.wx import *
application = wxPySimpleApp()
# Create a save file dialog
dialog = wxFileDialog ( None, style = wxSAVE )
# Show the dialog and get user input
if dialog.ShowModal() == wxID_OK:
   print 'Selected:', dialog.GetPath()
# The user did not select anything
else:
   print 'Nothing was selected.'
# Destroy the dialog
dialog.Destroy()
