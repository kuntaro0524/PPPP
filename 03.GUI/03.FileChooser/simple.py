from wxPython.wx import *

application = wxPySimpleApp()

# Create a list of filters
# This should be fairly simple to follow, so no explanation is necessary

filters = 'All files (*.*)|*.*|Text files (*.txt)|*.txt'

dialog = wxFileDialog ( None, message = 'Open something....', wildcard = filters, style = wxOPEN | wxMULTIPLE )

if dialog.ShowModal() == wxID_OK:
   # We'll have to make room for multiple files here
   selected = dialog.GetPaths()
   for selection in selected:
      print 'Selected:', selection

else:

   print 'Nothing was selected.'

dialog.Destroy()
