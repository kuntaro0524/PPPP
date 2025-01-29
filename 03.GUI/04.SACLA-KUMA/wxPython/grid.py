#!/usr/bin/python
#
# Grid Scan User Interface
#  Written by Takanori Nakane @ Kyoto University, 2013
#
# Tested on Python 2.6.5, Ubuntu 10.04 LTS

import wx
import math

# FIXME: How to define constant?
RECT = 0
OVAL = 1

class MainPanel(wx.Frame):
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent, title="Grid UI Test")
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # Beam Size
        st1 = wx.StaticText(panel, -1, 'Beam Size:')
        beamsizes = [(1, 1), (3, 5), (3, 10), (7, 15), (10, 10)]
        self.beamSize = wx.Choice(panel, -1, choices = [])
        for beam_size in beamsizes:
            self.beamSize.Append("%d x %d" % beam_size, beam_size)
        self.beamSize.SetSelection(2) # Necessary
        self.beamSize.Bind(wx.EVT_CHOICE, self.OnBeamSizeChoice)
        hbox.Add(st1)
        hbox.Add(self.beamSize)

        # Beam Shape
        st2 = wx.StaticText(panel, -1, 'Beam Shape:')
        self.beamShape = wx.Choice(panel, -1, choices = ['Rectangle', 'Circle'])
        self.beamShape.Bind(wx.EVT_CHOICE, self.OnBeamShapeChoice)
        hbox.Add(st2)
        hbox.Add(self.beamShape)

        # Panels
        self.grid = GridPanel(panel)
        vbox.Add(hbox)
        vbox.Add(self.grid)
        panel.SetSizer(vbox)
        vbox.Fit(self)

        self.updateGridSettings()
        self.grid.Refresh()

    def updateGridSettings(self):
        beam_size = self.beamSize.GetClientData(self.beamSize.GetSelection())
        self.grid.beam_width = self.grid.beam_interval_width = beam_size[0] * 5 # FIXME: use correct transformation
        self.grid.beam_height = self.grid.beam_interval_height = beam_size[1] * 5

        shape = self.beamShape.GetStringSelection()
        if shape == "Rectangle":
            self.grid.beam_shape = RECT
        else:
            self.grid.beam_shape = OVAL
        

    def OnBeamSizeChoice(self, event=None):
        self.updateGridSettings()
        self.grid.resetGrid()

    def OnBeamShapeChoice(self, event=None):
        self.updateGridSettings()
        self.grid.Refresh()


class Spot: # Spot to shoot
    def __init__(self, pos, id, enabled=True):
        self.pos = pos
        self.id = id
        self.enabled = enabled


class GridPanel(wx.Panel):
    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.img = wx.Image("test.jpg", wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        self.SetSize(self.img.GetSize())

        # Beam parameters
        self.beam_interval_width = 10
        self.beam_interval_height = 50
        self.beam_width = 10
        self.beam_height = 50
        self.beam_shape = RECT # OVAL
        self.beam_center_x = 100
        self.beam_center_y = 150

        # Spots
        self.spots = []

        # For mouse events
        self.dragging = False
        self.drag_start_x = self.drag_start_y = 0
        self.grid_top = self.grid_left = self.grid_right = self.grid_bottom = 0 # can I get rid of this?

        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnMiddleUp)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

    def OnPaint(self, event=None):
        dc = wx.BufferedDC(wx.PaintDC(self))
        dc.DrawBitmap(self.img, 0, 0, True)
        self.drawGrid(dc)
    
    def drawSpot(self, dc, spot):
        if spot.enabled == False:
            dc.DrawLine(spot.pos[0], spot.pos[1], spot.pos[0] + self.beam_width, spot.pos[1] + self.beam_height)
        dc.DrawText(str(spot.id), spot.pos[0], spot.pos[1] + self.beam_height / 2)
            
        if (self.beam_shape == RECT):
            dc.DrawRectangle(spot.pos[0], spot.pos[1], self.beam_width + 1, self.beam_height + 1)
        elif (self.beam_shape == OVAL):
            dc.DrawEllipse(spot.pos[0], spot.pos[1], self.beam_width + 1, self.beam_height + 1)


    def drawGrid(self, dc):
        dc.SetPen(wx.Pen(wx.RED, 1))#, wx.DOT))
        dc.SetBrush(wx.Brush(wx.WHITE, wx.TRANSPARENT))
        dc.SetFont(wx.Font(5, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        dc.SetTextForeground(wx.RED)

        for spot in self.spots:
            self.drawSpot(dc, spot)

    def resetGrid(self):
        self.grid_top = self.grid_left = self.grid_right = self.grid_bottom = 0 # can I get rid of this?
        self.spots = []
        self.Refresh()

    def generateSpots(self, sx, sy, ex, ey):
        self.ix = (ex - sx) / self.beam_interval_width
        self.iy = (ey - sy) / self.beam_interval_height
        # TODO: allow dragging leftwards and upwards
        if (self.ix <= 0 or self.iy <= 0):
            return

        dx = dy = 1
        self.grid_left = min(sx, ex); self.grid_right = max(sx, ex);
        self.grid_top = min(sy, ey); self.grid_bottom = max(sy, ey);
        if (self.ix < 0):
            dx = -1; self.ix *= -1
        if (self.iy < 0):
            dy = -1; self.iy *= -1
        
        self.spots = []
        cnt = 0
        for y in range(0, self.iy):
            for x in range(0, self.ix):
                self.spots.append(Spot([sx + x * dx * self.beam_interval_width, 
                                        sy + y * dy * self.beam_interval_height], cnt))
                cnt += 1 # FIXME: This results in strange spot order

    def moveSpots(self, dx, dy):
        self.grid_left += dx
        self.grid_top += dy
        self.grid_right += dx
        self.grid_bottom += dy

        for spot in self.spots:
            spot.pos[0] += dx
            spot.pos[1] += dy

    def pickSpot(self, x, y):
        for spot in self.spots:
            if (x > spot.pos[0] and x < spot.pos[0] + self.beam_interval_width and
                y > spot.pos[1] and y < spot.pos[1] + self.beam_interval_height):
                return spot
        return None

    def updateDragOrigin(self, event):
        self.dragging = True
        self.drag_start_x = event.X
        self.drag_start_y = event.Y

    def OnLeftDown(self, event=None):
        self.updateDragOrigin(event)

    def OnLeftUp(self, event=None):
        self.dragging = False

    def OnRightUp(self, event=None):
        spot = self.pickSpot(event.X, event.Y)
        if spot:
            spot.enabled = not spot.enabled
        self.Refresh()

    def OnLeftDClick(self, event=None):
        spot = self.pickSpot(event.X, event.Y)
        if spot:
            print("Double clicked on spot #%d" % spot.id)


    def OnMiddleDown(self, event=None):
        self.updateDragOrigin(event)

    def OnMiddleUp(self, event=None):
        self.dragging = False

    def OnMotion(self, event=None):
        if (self.dragging == False):
            return
        dx = event.X - self.drag_start_x
        dy = event.Y - self.drag_start_y

        if (event.LeftIsDown()):
            # Dragging inside grid FIXME: related to generateSpots() upwards and leftwards
            if (self.grid_left + 3 < self.drag_start_x and self.drag_start_x - 3 < self.grid_right and
                self.grid_top + 3 < self.drag_start_y and self.drag_start_y - 3 < self.grid_bottom):
                self.moveSpots(dx, dy)
                self.updateDragOrigin(event)
            
            else: # Outside grid
                self.generateSpots(self.drag_start_x, self.drag_start_y, event.X, event.Y)

        elif (event.MiddleIsDown()):
            self.moveSpots(dx, dy)
            self.updateDragOrigin(event)

        self.Refresh()

app = wx.App(False)
frame = MainPanel()
frame.Show()
app.MainLoop()
