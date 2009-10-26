# -------------------------------------------------------------------------
#     Copyright (C) 2008-2010 Martin Strohalm <mmass@biographics.cz>

#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#     GNU General Public License for more details.

#     Complete text of GNU GPL can be found in the file LICENSE in the
#     main directory of the program
# -------------------------------------------------------------------------

# load libs
import time
import copy
import wx
import config


# CONSTANTS
# ---------

# set mac
if wx.Platform == '__WXMAC__':
    SMALL_FONT_SIZE = 11
    SASH_SIZE = 1
    SASH_COLOUR = (111,111,111)
    PANEL_SPACE_MAIN = 20
    GRIDBAG_VSPACE = 10
    GRIDBAG_HSPACE = 5
    
    GAUGE_HEIGHT = -1
    GAUGE_SPACE = 15
    
    MAIN_TOOLBAR_TOOLSIZE = (30,22)
    MAIN_TOOLBAR_STYLE = wx.TB_FLAT|wx.TB_NODIVIDER|wx.TB_HORIZONTAL|wx.TB_TEXT
    
    TOOLBAR_HEIGHT = 38
    TOOLBAR_LSPACE = 15
    TOOLBAR_RSPACE = 15
    TOOLBAR_TOOLSIZE = (-1,-1)
    CONTROLBAR_HEIGHT = 32
    CONTROLBAR_LSPACE = 15
    CONTROLBAR_RSPACE = 15
    BOTTOMBAR_HEIGHT = 32
    BOTTOMBAR_LSPACE = 10
    BOTTOMBAR_RSPACE = 10
    BOTTOMBAR_TOOLSIZE = (-1,-1)
    SMALL_BUTTON_HEIGHT = -1
    SMALL_TEXTCTRL_HEIGHT = 18
    BUTTON_SIZE_CORRECTION = -3
    
    LISTCTRL_STYLE_SINGLE = wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VRULES|wx.NO_BORDER
    LISTCTRL_STYLE_MULTI = wx.LC_REPORT|wx.LC_VRULES|wx.NO_BORDER
    LISTCTRL_SPACE = 20
    LISTCTRL_ALTCOLOUR = wx.Colour(230,240,250)
    LISTCTRL_SORT = -1
    LISTCTRL_NO_SPACE = -3
    if config.main['macListCtrlGeneric']:
        LISTCTRL_NO_SPACE = -2
        LISTCTRL_STYLE_SINGLE = wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VRULES|wx.LC_HRULES|wx.SIMPLE_BORDER
        LISTCTRL_STYLE_MULTI = wx.LC_REPORT|wx.LC_VRULES|wx.LC_HRULES|wx.SIMPLE_BORDER
        LISTCTRL_ALTCOLOUR = None
        LISTCTRL_SORT = 1
    
    DOCTREE_COLOUR = (214,221,229)
    DOCTREE_BULLETSIZE = 4
    DOCTREE_STYLE = wx.TR_DEFAULT_STYLE|wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT
    
    PLOTCANVAS_STYLE = wx.NO_BORDER
    GRID_STYLE = wx.NO_BORDER
    SLIDER_STYLE = wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS
    SEQUENCE_FONT_SIZE = 12


# set windows
elif wx.Platform == '__WXMSW__':
    SMALL_FONT_SIZE = 8
    SASH_SIZE = 3
    SASH_COLOUR = None
    PANEL_SPACE_MAIN = 10
    GRIDBAG_VSPACE = 7
    GRIDBAG_HSPACE = 5
    
    GAUGE_HEIGHT = 15
    GAUGE_SPACE = 10
    
    MAIN_TOOLBAR_TOOLSIZE = (22,22)
    MAIN_TOOLBAR_STYLE = wx.TB_FLAT|wx.TB_NODIVIDER|wx.TB_HORIZONTAL
    
    TOOLBAR_HEIGHT = 36
    TOOLBAR_LSPACE = 0
    TOOLBAR_RSPACE = 10
    TOOLBAR_TOOLSIZE = (-1,-1)
    CONTROLBAR_HEIGHT = 32
    CONTROLBAR_LSPACE = 10
    CONTROLBAR_RSPACE = 10
    BOTTOMBAR_HEIGHT = 22
    BOTTOMBAR_LSPACE = 0
    BOTTOMBAR_RSPACE = 0
    BOTTOMBAR_TOOLSIZE = (-1,-1)
    SMALL_BUTTON_HEIGHT = 22
    SMALL_TEXTCTRL_HEIGHT = -1
    BUTTON_SIZE_CORRECTION = 0
    
    LISTCTRL_STYLE_SINGLE = wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VRULES|wx.LC_HRULES|wx.SUNKEN_BORDER
    LISTCTRL_STYLE_MULTI = wx.LC_REPORT|wx.LC_VRULES|wx.LC_HRULES|wx.SUNKEN_BORDER
    LISTCTRL_NO_SPACE = 0
    LISTCTRL_SPACE = 0
    LISTCTRL_ALTCOLOUR = None
    LISTCTRL_SORT = 1
    
    DOCTREE_COLOUR = (255,255,255)
    DOCTREE_BULLETSIZE = 5
    DOCTREE_STYLE = wx.TR_DEFAULT_STYLE|wx.TR_HAS_BUTTONS
    
    PLOTCANVAS_STYLE = wx.SUNKEN_BORDER
    GRID_STYLE = wx.SUNKEN_BORDER
    SLIDER_STYLE = wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS
    SEQUENCE_FONT_SIZE = 10

# set gtk
elif wx.Platform == '__WXGTK__':
    SMALL_FONT_SIZE = 10
    SASH_SIZE = 3
    SASH_COLOUR = None
    PANEL_SPACE_MAIN = 10
    GRIDBAG_VSPACE = 7
    GRIDBAG_HSPACE = 5
    
    GAUGE_HEIGHT = 15
    GAUGE_SPACE = 10
    
    MAIN_TOOLBAR_TOOLSIZE = (22,22)
    MAIN_TOOLBAR_STYLE = wx.TB_FLAT|wx.TB_NODIVIDER|wx.TB_HORIZONTAL
    
    TOOLBAR_HEIGHT = 36
    TOOLBAR_LSPACE = 0
    TOOLBAR_RSPACE = 10
    TOOLBAR_TOOLSIZE = (32,26)
    CONTROLBAR_HEIGHT = 32
    CONTROLBAR_LSPACE = 10
    CONTROLBAR_RSPACE = 10
    BOTTOMBAR_HEIGHT = 28
    BOTTOMBAR_LSPACE = 0
    BOTTOMBAR_RSPACE = 0
    BOTTOMBAR_TOOLSIZE = (32,26)
    SMALL_BUTTON_HEIGHT = 25
    SMALL_TEXTCTRL_HEIGHT = 23
    BUTTON_SIZE_CORRECTION = 0
    
    LISTCTRL_STYLE_SINGLE = wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VRULES|wx.LC_HRULES|wx.SUNKEN_BORDER
    LISTCTRL_STYLE_MULTI = wx.LC_REPORT|wx.LC_VRULES|wx.LC_HRULES|wx.SUNKEN_BORDER
    LISTCTRL_NO_SPACE = 0
    LISTCTRL_SPACE = 0
    LISTCTRL_ALTCOLOUR = None
    LISTCTRL_SORT = 1
    
    DOCTREE_COLOUR = (255,255,255)
    DOCTREE_BULLETSIZE = 4
    DOCTREE_STYLE = wx.TR_DEFAULT_STYLE|wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT|wx.SUNKEN_BORDER
    
    PLOTCANVAS_STYLE = wx.SUNKEN_BORDER
    GRID_STYLE = wx.SUNKEN_BORDER
    SLIDER_STYLE = wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS
    SEQUENCE_FONT_SIZE = 10


# set others
else:
    SMALL_FONT_SIZE = 8
    SASH_SIZE = 3
    SASH_COLOUR = None
    PANEL_SPACE_MAIN = 10
    GRIDBAG_VSPACE = 7
    GRIDBAG_HSPACE = 5
    
    GAUGE_HEIGHT = 15
    GAUGE_SPACE = 10
    
    MAIN_TOOLBAR_TOOLSIZE = (22,22)
    MAIN_TOOLBAR_STYLE = wx.TB_FLAT|wx.TB_NODIVIDER|wx.TB_HORIZONTAL
    
    TOOLBAR_HEIGHT = 36
    TOOLBAR_LSPACE = 0
    TOOLBAR_RSPACE = 10
    TOOLBAR_TOOLSIZE = (-1,-1)
    CONTROLBAR_HEIGHT = 32
    CONTROLBAR_LSPACE = 10
    CONTROLBAR_RSPACE = 10
    BOTTOMBAR_HEIGHT = 22
    BOTTOMBAR_LSPACE = 0
    BOTTOMBAR_RSPACE = 0
    BOTTOMBAR_TOOLSIZE = (-1,-1)
    SMALL_BUTTON_HEIGHT = 22
    SMALL_TEXTCTRL_HEIGHT = -1
    BUTTON_SIZE_CORRECTION = 0
    
    LISTCTRL_STYLE_SINGLE = wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VRULES|wx.LC_HRULES|wx.SUNKEN_BORDER
    LISTCTRL_STYLE_MULTI = wx.LC_REPORT|wx.LC_VRULES|wx.LC_HRULES|wx.SUNKEN_BORDER
    LISTCTRL_NO_SPACE = 0
    LISTCTRL_SPACE = 0
    LISTCTRL_ALTCOLOUR = None
    LISTCTRL_SORT = 1
    
    DOCTREE_COLOUR = (255,255,255)
    DOCTREE_BULLETSIZE = 5
    DOCTREE_STYLE = wx.TR_DEFAULT_STYLE|wx.TR_HAS_BUTTONS
    
    PLOTCANVAS_STYLE = wx.SUNKEN_BORDER
    GRID_STYLE = wx.SUNKEN_BORDER
    SLIDER_STYLE = wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS
    SEQUENCE_FONT_SIZE = 10
    


# RUN AFTER APP INIT
# ------------------

def appInit():
    """Run after application initialize."""
    
    # set MAC
    if wx.Platform == '__WXMAC__':
        wx.SystemOptions.SetOptionInt("mac.listctrl.always_use_generic", config.main['macListCtrlGeneric'])
        wx.ToolTip.SetDelay(1500)
    
    # set WIN
    elif wx.Platform == '__WXMSW__':
        wx.SMALL_FONT.SetPointSize(SMALL_FONT_SIZE)
    
    # set GTK
    elif wx.Platform == '__WXGTK__':
        wx.SMALL_FONT.SetPointSize(SMALL_FONT_SIZE)
# ----



# MODIFIED WX OBJECTS
# -------------------

class bgrPanel(wx.Panel):
    """Simple panel with image background."""
    
    def __init__(self, parent, id, image, size=(-1,-1)):
        wx.Panel.__init__(self, parent, id, size=size)
        self.SetMinSize(size)
        
        self.image = image
        
        # set paint event to title image
        wx.EVT_PAINT(self, self._onPaint)
    # ----
    
    
    def _onPaint(self, event=None):
        
        # create paint surface
        dc = wx.PaintDC(self)
        dc.Clear()
        
        # tile/wallpaper the image across the canvas
        for x in range(0, self.GetSize()[0], self.image.GetWidth()):
            dc.DrawBitmap(self.image, x, 0, True)
    # ----
    
    


class sortListCtrl(wx.ListCtrl):
    """ListCtrl with automatic sorter."""
    
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.LC_REPORT):
        wx.ListCtrl.__init__(self, parent, id, pos, size, style)
        
        self.Bind(wx.EVT_LIST_COL_CLICK, self._onColClick)
        
        self._data = None
        self._currentCol = 0
        self._currentDirection = LISTCTRL_SORT
        self._secondaryCol = None
        
        self._defaultColour = self.GetBackgroundColour()
        self._altColour = None
    # ----
    
    
    def _onColClick(self, evt):
        """Sort data by this column."""
        
        # check data
        if not self._data:
            return
        
        # get selected column
        oldCol = self._currentCol
        self._currentCol = evt.GetColumn()
        
        # update direction flag
        if oldCol == self._currentCol:
            self._currentDirection *= -1
        else:
            self._currentDirection = LISTCTRL_SORT
        
        # sort data
        self.SortItems(self._columnSorter)
        evt.Skip()
        
        # set row colour
        self._updateItemBackground()
    # ----
    
    
    def _columnSorter(self, key1, key2):
        """Sort data."""
        
        # check data
        if not self._data:
            return self._currentDirection
        
        # get values
        item1 = self._data[key1][self._currentCol]
        item2 = self._data[key2][self._currentCol]
        
        # compare values
        comp = cmp(item1, item2)
        if comp == 0 and self._secondaryCol != None:
            item1 = self._data[key1][self._secondaryCol]
            item2 = self._data[key2][self._secondaryCol]
            comp = cmp(item1, item2)
        
        # set direction
        comp *= self._currentDirection
        
        return comp
    # ----
    
    
    def _updateItemBackground(self):
        """Update item background colours."""
        
        # check colours
        if not self._altColour or self._defaultColour == self._altColour:
            return
        
        # update each row
        for row in xrange(self.GetItemCount()):
            item = self.GetItem(row)
            bgrColour = self.GetItemBackgroundColour(row)
            if row % 2 and (bgrColour == self._defaultColour or bgrColour == (-1,-1,-1,255)):
                self.SetItemBackgroundColour(row, self._altColour)
            else:
                self.SetItemBackgroundColour(row, self._defaultColour)
    # ----
    
    
    def setSecondarySortColumn(self, col):
        """Set secondary column to sort by."""
        self._secondaryCol = col
    # ----
    
    
    def setDataMap(self, data):
        """Set data."""
        self._data = data
    # ----
    
    
    def setAltColour(self, colour):
        """Set alternate background colour."""
        self._altColour = colour
    # ----
    
    
    def getSelected(self):
        """Return indexes of selected items."""
        
        selected = []
        
        i = -1
        while True:
            i = self.GetNextItem(i, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
            if i == -1:
                break
            else:
                selected.append(i)
        
        selected.sort()
        return selected
    # ----
    
    
    def sort(self, col=None):
        """Sort by last or selected column."""
        
        # get column
        if col != None:
            if self._currentCol != col:
                self._currentDirection = LISTCTRL_SORT
        
        # sort data
        self.SortItems(self._columnSorter)
        
        # set row colour
        self._updateItemBackground()
    # ----
    
    


class scrollTextCtrl(wx.TextCtrl):
    """TextCtrl with scoll."""
    
    def __init__(self, parent, id=-1, value="", step=None, multiplier=None, digits=0, limits=(None,None), pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, validator=wx.DefaultValidator):
        wx.TextCtrl.__init__(self, parent, id, value, pos, size, style, validator)
        
        self.Bind(wx.EVT_KEY_DOWN, self._onKey)
        if wx.Platform == '__WXMAC__':
            self.Bind(wx.EVT_MOUSEWHEEL, self._onScroll)
        
        self._digits = digits
        self._scrollStep = step
        self._scrollMultiplier = multiplier
        self._min = limits[0]
        self._max = limits[1]
    # ----
    
    
    def _onScroll(self, evt):
        """Increase or decrease value while scrolling."""
        
        # set new value
        self._setNewValue(evt.GetWheelRotation(), evt.m_altDown)
    # ----
    
    
    def _onKey(self, evt):
        """Use up and down keys."""
        
        # get key
        key = evt.GetKeyCode()
        
        # get direction
        if key == wx.WXK_UP:
            direction = 1
        elif key == wx.WXK_DOWN:
            direction = -1
        else:
            evt.Skip()
            return
        
        # set new value
        self._setNewValue(direction, evt.m_altDown)
    # ----
    
    
    def _setNewValue(self, direction, precise):
        """Calculate and set new value."""
        
        # get and check current value
        old = self.GetValue()
        try:
            old = float(old)
        except:
            wx.Bell()
            return
        
        # make new value
        if self._scrollStep:
            new = old + (self._scrollStep * direction)
        elif self._scrollMultiplier and precise:
            new = old + (old * self._scrollMultiplier * direction * 0.1)
        elif self._scrollMultiplier:
            new = old + (old * self._scrollMultiplier * direction)
        else:
            return
        
        # check limits
        if self._min != None and new < self._min:
            new = self._min
        elif self._max != None and new > self._max:
            new = self._max
        
        # format value
        if new > 10000 or new < -10000:
            format = '%0.1e'
        else:
            format = '%0.' + `self._digits` + 'f'
        new = format % new
        
        # set new value
        self.SetValue(new)
    # ----
    
    
    def setScrollStep(self, value):
        """Set scroll step."""
        self._scrollStep = value
    # ----
    
    
    def setScrollMultiplier(self, value):
        """Set scroll multiplier."""
        self._scrollMultiplier = value
    # ----
    
    
    def setMin(self, value):
        """Set minimum."""
        self._min = value
    # ----
    
    
    def setMax(self, value):
        """Set maximum."""
        self._max = value
    # ----
    
    
    def setDigits(self, value):
        """Set number of digits."""
        self._digits = value
    # ----
    
    


class gauge(wx.Gauge):
    """Gauge."""
    
    def __init__(self, parent, id=-1, size=(-1, GAUGE_HEIGHT), style=wx.GA_HORIZONTAL):
        wx.Gauge.__init__(self, parent, id, size=size, style=style)
    # ----
    
    
    def pulse(self):
        """Pulse gauge."""
        
        self.Pulse()
        try: wx.Yield()
        except: pass
        time.sleep(0.05)
    # ----
    
    


class gaugePanel(wx.Dialog):
    """Processing panel."""
    
    def __init__(self, parent, title, label):
        wx.Dialog.__init__(self, parent, -1, title, style=(wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP) & ~ (wx.SYSTEM_MENU | wx.RESIZE_BORDER | wx.RESIZE_BOX | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.CLOSE_BOX))
        
        self.parent = parent
        self.label = label
        
        # make GUI
        panel = wx.Panel(self, -1)
        self.label = wx.StaticText(panel, -1, label)
        self.label.SetFont(wx.SMALL_FONT)
        self.gauge = wx.Gauge(panel, -1, size=(250, GAUGE_HEIGHT))
        
        # pack elements
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label, 0, wx.BOTTOM, 5)
        sizer.Add(self.gauge, 0, wx.EXPAND, 0)
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer, 0, wx.ALL, PANEL_SPACE_MAIN)
        
        self.Layout()
        mainSizer.Fit(self)
        self.SetSizer(mainSizer)
    # ----
    
    
    def setLabel(self, label):
        """Set new label."""
        self.label.SetLabel(label)
    # ----
    
    
    def pulse(self):
        """Pulse gauge."""
        
        self.gauge.Pulse()
        try: wx.Yield()
        except: pass
        time.sleep(0.05)
    # ----
    
    
    def show(self):
        """Show panel."""
        
        self.Center()
        self.Show()
        self.MakeModal(True)
        try: wx.SafeYield()
        except: pass
    # ----
    
    
    def close(self):
        """Hide panel"""
        
        self.MakeModal(False)
        self.Destroy()
    # ----
    


class validator(wx.PyValidator):
    """Text validator."""
    
    def __init__(self, flag):
        wx.PyValidator.__init__(self)
        self.flag = flag
        self.Bind(wx.EVT_CHAR, self.OnChar)
    # ----
    
    
    def Clone(self):
        return validator(self.flag)
    # ----
    
    
    def TransferToWindow(self):
        return True
    # ----
    
    
    def TransferFromWindow(self):
        return True
    # ----
    
    
    def OnChar(self, evt):
        ctrl = self.GetWindow()
        value = ctrl.GetValue()
        key = evt.GetKeyCode()
        
        # define navigation keys
        navKeys = (wx.WXK_HOME, wx.WXK_LEFT, wx.WXK_UP,
                    wx.WXK_END, wx.WXK_RIGHT, wx.WXK_DOWN,
                    wx.WXK_NUMPAD_HOME, wx.WXK_NUMPAD_LEFT, wx.WXK_NUMPAD_UP,
                    wx.WXK_NUMPAD_END, wx.WXK_NUMPAD_RIGHT, wx.WXK_NUMPAD_DOWN)
                    
        # navigation keys
        if key in navKeys or key < wx.WXK_SPACE or key == wx.WXK_DELETE:
            evt.Skip()
            return
        
        # illegal characters
        elif key > 255:
            return
        
        # int only
        elif self.flag == 'int' and chr(key) in '-0123456789':
            evt.Skip()
            return
        
        # positive int only
        elif self.flag == 'intPos' and chr(key) in '0123456789':
            evt.Skip()
            return
        
        # floats only
        elif self.flag == 'float' and (chr(key) in '-0123456789.'):
            evt.Skip()
            return
        
        # positive floats only
        elif self.flag == 'floatPos' and (chr(key) in '0123456789.'):
            evt.Skip()
            return
        
        # error
        else:
            wx.Bell()
            return
    # ----
    



