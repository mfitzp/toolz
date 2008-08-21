#!/usr/bin/env python
import sys
import os

from PyQt4 import QtCore
from PyQt4 import QtGui
import numpy as N
import scipy as S


from Bio import SeqIO

'''Need to add option to read gzipped dat files and maybe parse a whole directory'''


class Fasta_Converter:
    def __init__(self, file2convert,  newfilename,  parent = None):
        self.converted = False
        self.recordCount = None
        self.parent = None
        if parent:
            self.parent = parent

        
        inputhandle = open(str(file2convert),  "rU")# rU = read universal
        outputhandle = open(str(newfilename),  "w")# w = write
        
        try:
            datRecords = SeqIO.parse(inputhandle,  "swiss")# swiss is for the SwissProt *dat format
            SeqIO.write(datRecords, outputhandle,  "fasta")
            self.converted = True
        except:
            inputhandle.close()
            outputhandle.close()
            raise
            

class OpenFile(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('Convert UniProt *.dat to *.fasta')
        self.centralwidget = QtGui.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        
    
        self.hlayout = QtGui.QHBoxLayout()
        self.filelabel = QtGui.QLabel("Converted File Name:")
        self.lineEdit = QtGui.QLineEdit()
        self.hlayout.addWidget(self.filelabel)
        self.hlayout.addWidget(self.lineEdit)
        
        self.hlayout2 = QtGui.QHBoxLayout()
        self.folderlabel = QtGui.QLabel("Converted File Name:")
        self.lineEdit2 = QtGui.QLineEdit()
        self.folderCheck = QtGui.QCheckBox("Parse Folder")
        self.hlayout2.addWidget(self.folderlabel)
        self.hlayout2.addWidget(self.lineEdit2)
        self.hlayout2.addWidget(self.folderCheck)
        
        self.button = QtGui.QPushButton("Convert *.dat")
        self.textEdit = QtGui.QTextEdit()
        
        self.vlayout = QtGui.QVBoxLayout(self.centralwidget)

        self.vlayout.addLayout(self.hlayout)
        self.vlayout.addLayout(self.hlayout2)
        self.vlayout.addWidget(self.button)
        self.vlayout.addWidget(self.textEdit)
        self.statusBar()
        self.setFocus()

        exit = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        exit.setShortcut('Ctrl+O')
        exit.setStatusTip('Open new File')
        self.connect(exit, QtCore.SIGNAL('triggered()'), self.showDialog)
        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.convert_dat)
        self.connect(self.folderCheck,  QtCore.SIGNAL('stateChanged(int)'),  self.testLoadFolder)

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)
        self.curDir = os.getcwd()
    
    def testLoadFolder(self, int):
        if int == 2:
            self.lineEdit.setEnabled(False)
        else:
            self.lineEdit.setEnabled(True)
        print int
    
    def convert_dat(self):
        try:
            fc = Fasta_Converter(self.filename,  self.lineEdit.text(),  self)
            if fc.converted:
                self.textEdit.setText("%s\nFile Successfully Converted"%(self.filename))
        except:
            self.textEdit.setText("Sorry, Error converting *.dat file:\n %s:%s"%(sys.exc_type, sys.exc_value))

    def showDialog(self):
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Select *.dat file to convert',self.curDir, 'UniProt dat (*.dat)')
        if self.filename:
            filenamelist= str(self.filename).split('.')
            self.fileType = filenamelist[-1]
            self.fileCore = filenamelist[:-1][0]
            if self.fileType == 'dat':
                convertFileStr = self.fileCore + ".fasta"
                self.lineEdit.setText(convertFileStr)
                self.textEdit.clear()
                

        
if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    cd = OpenFile()
    cd.show()
    sys.exit(app.exec_())
    
