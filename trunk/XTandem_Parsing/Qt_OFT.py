#!/usr/bin/env python

"""PyQt4 port of the dialogs/standarddialogs example from Qt v4.x"""

import sys
from PyQt4 import QtCore, QtGui


class Open_File_Dialog(QtGui.QDialog):
    MESSAGE = QtCore.QT_TR_NOOP("<p>Message boxes have a caption, a text, and up to "
                                "three buttons, each with standard or custom texts.</p>"
                                "<p>Click a button or press Esc.</p>")

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.openFilesPath = QtCore.QString()

        self.errorMessageDialog = QtGui.QErrorMessage(self)

        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel

        self.openFileNameLabel = QtGui.QLabel()
        self.openFileNameLabel.setFrameStyle(frameStyle)
        self.openFileNameButton = QtGui.QPushButton(self.tr("Open File"))

        self.connect(self.openFileNameButton, QtCore.SIGNAL("clicked()"), self.setOpenFileName)

        layout = QtGui.QGridLayout()
        layout.setColumnStretch(1, 1)
        layout.setColumnMinimumWidth(1, 250)

        layout.addWidget(self.openFileNameButton, 0, 0)
        layout.addWidget(self.openFileNameLabel, 0, 1)

        self.setLayout(layout)

        self.setWindowTitle(self.tr("Open File:"))

    def setOpenFileName(self):
        '''
        This is the line of code you are looking for!!!!!!!!!!!!!!!!!!!!!!!!
        '''
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                                         self.tr("QFileDialog.getOpenFileName()"),
                                         self.openFileNameLabel.text(),
                                         self.tr("All Files (*);;Text Files (*.txt)"))
        if not fileName.isEmpty():
            self.openFileNameLabel.setText(fileName)




if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog = Open_File_Dialog()
    sys.exit(dialog.exec_())
