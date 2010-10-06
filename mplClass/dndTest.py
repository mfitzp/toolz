#!/usr/bin/python

# dragdrop.py

import sys
from PyQt4 import QtGui

def embed_ipython(w):
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed(user_ns = dict(w = w))
    ipshell()

class Button(QtGui.QPushButton):
    def __init__(self, title, parent):
        QtGui.QPushButton.__init__(self, title, parent)
        self.setAcceptDrops(True)
        self.curMimeData = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
        else:
            event.ignore() 

    def dropEvent(self, event):
        print event.mimeData().text()
        self.setText(event.mimeData().text())
        self.curMimeData = event.mimeData()


class DragDrop(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.resize(280, 150)
        self.setWindowTitle('Simple Drag & Drop')

        edit = QtGui.QLineEdit('', self)
        edit.setDragEnabled(True)
        edit.move(30, 65)

        self.button = Button("Button", self)
        self.button.move(170, 65)

        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)

app = QtGui.QApplication(sys.argv)
icon = DragDrop()
icon.show()
embed_ipython(icon)
app.exec_()
