import wx
import os

def File_Dialog():    
# setup the GUI main loop
    app = wx.PySimpleApp()
    filename = wx.FileSelector(message='Select IMS File', default_path=os.getcwd(), parent=None)
    return filename


