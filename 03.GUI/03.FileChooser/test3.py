def OnOpen(self,e):
      """ Open a file"""
      self.dirname = ''
      dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
      if dlg.ShowModal() == wx.ID_OK:
          self.filename = dlg.GetFilename()
          self.dirname = dlg.GetDirectory()
          f = open(os.path.join(self.dirname, self.filename), 'r')
          self.control.SetValue(f.read())
          f.close()
      dlg.Destroy()
