# coding: utf-8
import wx 

class MwFrame ( wx.Frame ):
	def __init__( self ):
		wx.Frame.__init__( self, None, -1, "Title", size=(200, 100) )
		wx.StaticText( self, -1, "name:", pos=(0, 3) )
		self.textCtrl = wx.TextCtrl( self, -1, "", pos=(40, 0) )

		button = wx.Button( self, label="submit", pos=(25, 25) )
		self.Bind( wx.EVT_BUTTON, self.OnSubmit, button )
	
	def OnSubmit( self, event ):
		wx.MessageBox( self.textCtrl.GetValue(), "your name", wx.OK )
