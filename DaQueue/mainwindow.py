# -*- coding: utf-8 -*-

'''
/usr/bin/pyuic4 /home/clowers/workspace/DaQueue/mainwindow.ui  -o /home/clowers/workspace/DaQueue/ui_mainwindow.py
'''


"""
This module contains the class MainWindow.
"""
import os, sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignature
from ui_mainwindow import Ui_MainWindow
from extraWidgets import cellComboBox, cellOFD, cellStatus

from dbInterface import dbIO
import time

DBNAME = 'labqueue'
ROOTUSER = 'clowers'

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """
    MainWindow: this is the class that manages all the functionality of receiving input from the user, and navigating the internet.
    """
    def __init__(self, parent = None):
        """
        Default Constructor. It can receive a top window as parent.
        """
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.__setMessages__()
        self.__setVariables__()
        self.__resetTaskTable__()
        self.__setConnections__()
        self.initServer()
        self.initDB()

    def initDB(self):
        if self.serverStatus:
            self.db = dbIO.DB(self.server, DBNAME, self.dbKeys)
            self.dbOK = self.db.OK
            self.dbStatusUpdate()

    def initServer(self):
        self.serverAddress = str(self.serverAddressLE.text())
        self.serverPort = self.portSB.value()
#        print "Server Address, Port: %s:%s"%(self.serverAddress, self.serverPort)
        self.server = dbIO.CouchDBServer(self.serverAddress, self.serverPort)
        self.serverStatus = self.server.OK

    def updateTaskType(self, row, comboIndex):
        curItem = self.taskTable.cellWidget(row, 0)
        if isinstance(curItem, cellComboBox):
#            print type(curItem)
            curItem.setCurrentIndex(comboIndex)

    def testTable(self):
        for row in xrange(self.taskTable.rowCount()):
            print type(self.taskTable.item(row, 0))

    def updateQueue(self):
        '''
        I don't like to double "db".  Need to find a more elegant way of interfacing
        i.e. subclass
        '''
        if self.dbOK:
            self.taskTable.setRowCount(0)
            for i,docID in enumerate(self.db.db):
                self.taskTable.insRow(i)
                curDoc = self.db.db[docID]
                for j, key in enumerate(self.taskHeaders):
                    if curDoc.has_key(key):
                        if key == 'State':
                            if curDoc[key] == 'Processing':
                                self.updateStatus(i, 0)
                            elif curDoc[key] == 'Finished':
                                self.updateStatus(i, 1)
                            elif curDoc[key] == 'Failed':
                                self.updateStatus(i, 2)
                        elif key == 'Task Type':
                            taskKey = curDoc[key]
                            self.updateTaskType(i, self.taskTypeDict[taskKey])
                        else:
                            newTableItem = QtGui.QTableWidgetItem(curDoc[key])
                            self.taskTable.setItem(i,j, newTableItem)

                    elif key == 'Task ID':
                        newTableItem = QtGui.QTableWidgetItem(docID)
                        self.taskTable.setItem(i,j, newTableItem)

            self.updateColumnSizes()


    def __setVariables__(self):
        '''Variables that are utilized by other functions'''
        self.__curDir = getHomeDir()
        self.server = None
        self.serverStatus = False
        self.serverAddress = None
        self.serverPort = None
        self.db = None
        self.dbOK = False

        self.taskHeaders = ['Task Type', 'Method File', '', 'Data Path', '','Output Path', '', 'State', 'User', 'Task ID']
        self.dbKeys = ['Task Type', 'Method File', 'Data Path', 'Output Path', 'State', 'Task ID', 'User']
        self.taskOptions = ['File Conversion', 'X!Tandem Run', 'Peak Picking']
        self.taskTypeDict = {'File Conversion':0, 'X!Tandem Run':1, 'Peak Picking':2}

        self.methodFileInd = 1
        self.dataPathInd = 3
        self.outputPathInd = 5
        self.stateInd = 7
        self.taskIDInd = 8


    def dbStatusUpdate(self):
        '''
        Updates the server status on the GUI and attempts
        connection with couchDB server
        '''
        if self.serverStatus and self.dbOK:
            self.serverStatusBtn.setIcon(QtGui.QIcon('images/clean.png'))
        else:
            self.serverStatusBtn.setIcon(QtGui.QIcon('images/exit.png'))

    def toggleServerEdit(self, state = None):
        if state == 2:
            self.serverAddressLE.setEnabled(True)
            self.portSB.setEnabled(True)
            self.resetServerBtn.setEnabled(True)
        elif state == 0:
            self.serverAddressLE.setEnabled(False)
            self.portSB.setEnabled(False)
            self.resetServerBtn.setEnabled(False)

    def __setMessages__(self):
        '''This function is obvious'''
        self.ClearTableText = "Are you sure you want to erase\nthe entire table content?"
        self.ClearAllDataText = "Are you sure you want to erase\nthe entire data set?"
        self.NotEditableText = "Sorry, this data format is not table-editable."
        self.OpenScriptText = "Choose a python script to launch:"
        self.SaveDataText = "Choose a name for the data file to save:"
        self.ScratchSavePrompt = "Choose file name to save the scratch pad:"
        self.OpenDataText = "Choose a data file to open:"
        self.ResetAllDataText = "This operation will reset all your data.\nWould you like to continue?"
        self.EmptyArrayText = "There is no data in the array selected.  Perhaps the search criteria are too stringent.  Check ppm and e-Value cutoff values.\n"

    def __getDataFile__(self):
        dataFileName = QtGui.QFileDialog.getOpenFileName(self,\
                                                         self.OpenDataText,\
                                                         self.__curDir, '*.* (*.*);;X!Tandem XML (*.xml);;SQLite Database (*.db)')
        if dataFileName:
            self.__curDir = getCurDir(dataFileName)
            return str(dataFileName)
        else:
            return None
#            self.loadFileXT(dataFileName)

    def __loadDataFolder__(self):
        directory= QtGui.QFileDialog.getExistingDirectory(self, self.__curDir,
                                                          "Select Output Data Folder")
        if os.path.isdir(str(directory)):
            self.__curDir = str(directory)
            return str(directory)
#            for root, dirs, files in walk(str(directory)):
#                for file in files:
#                    if '.xml' in file:
#                        ##full file path name
#                        ffpn=path.abspath(path.join(root, file))#file full path name
        else:
            return None

    def __setConnections__(self):
        '''establishes connections between GUI Slots and Actions'''
        QtCore.QObject.connect(self.taskTable, QtCore.SIGNAL("itemClicked (QTableWidgetItem *)"), self.updateCellValue)
        QtCore.QObject.connect(self.taskTable, QtCore.SIGNAL("itemEntered (QTableWidgetItem *)"), self.updateCellValue)

        QtCore.QObject.connect(self.editServerCB, QtCore.SIGNAL("stateChanged(int)"),self.toggleServerEdit)
        QtCore.QObject.connect(self.resetServerBtn, QtCore.SIGNAL("clicked()"),self.initServer)

        QtCore.QObject.connect(self.updateQueueBtn, QtCore.SIGNAL("clicked()"),self.updateQueue)
#        QtCore.QObject.connect(self.deleteQueueRowBtn, QtCore.SIGNAL("clicked()"),self.deleteQueueRow)
#        QtCore.QObject.connect(self.submitQueueBtn, QtCore.SIGNAL("clicked()"),submitQueue)





        QtCore.QObject.connect(self.actionTestAction, QtCore.SIGNAL("triggered()"),self.testFunc)

    def __resetTaskTable__(self):
        self.taskTable.clear()
        self.taskTable.setColumnCount(len(self.taskHeaders))
        self.taskTable.setRowCount(3)
        self.taskTable.setHorizontalHeaderLabels(self.taskHeaders)

        for row in xrange(self.taskTable.rowCount()):
            self.taskTable.setCellWidget(row, 0, cellComboBox())
            self.taskTable.setItem(row, self.methodFileInd+1, cellOFD())
            self.taskTable.setItem(row, self.dataPathInd+1, cellOFD())
            self.taskTable.setItem(row, self.outputPathInd+1, cellOFD())
            self.taskTable.setItem(row, self.stateInd, cellStatus())

        self.taskTable.resizeColumnsToContents()
        self.taskTable.resizeRowsToContents()
        self.taskTable.setColumnWidth(0, 150)

    def updateStatus(self, row, state):
        curItem = self.taskTable.item(row, self.stateInd)
        if isinstance(curItem, cellStatus):
            curItem.switchStatus(state)

    def updateColumnSizes(self):
        self.taskTable.resizeColumnsToContents()
        self.taskTable.setColumnWidth(0, 150)

    def updateCellValue(self, tableItem = None):
        if isinstance(tableItem, cellOFD):
            if tableItem.column() == self.outputPathInd+1:
                dataPath = self.__loadDataFolder__()
                if dataPath != None:
                    prevTableItem = QtGui.QTableWidgetItem(dataPath)
                    self.taskTable.setItem(tableItem.row(), tableItem.column()-1, prevTableItem)

            else:
                dataFileName = self.__getDataFile__()
                if dataFileName != None:
                    prevTableItem = QtGui.QTableWidgetItem(dataFileName)
                    self.taskTable.setItem(tableItem.row(), tableItem.column()-1, prevTableItem)

                    if tableItem.column() == self.dataPathInd+1:
                        nextItem = self.taskTable.item(tableItem.row(), tableItem.column()+1)
                        baseDir = os.path.dirname(dataFileName)
                        if nextItem == None:
                            nextItem = QtGui.QTableWidgetItem()
                        curText = str(nextItem.text())
                        if os.path.isdir(curText) or os.path.isfile(curText):
                            return True
                        else:
                            nextItem.setText(baseDir)
                            self.taskTable.setItem(tableItem.row(), tableItem.column()+1, nextItem)

            self.updateColumnSizes()

    def fillColumnWithCurrent(self):
        '''
        Fills all rows below the current column value
        '''


    def testFunc(self):
        print "Test Function Triggered"
        self.updateStatus(2, 2)

    @pyqtSignature("")
    def on_btnNavigate_released(self):
        """
        Public slot invoked when the user clicks the Navigate Button
        """
        #TODO: check out this code, ensure it does cover all the posibilities
        theUrl = self.txtUrl.text()
        if theUrl[0:7] != 'http://':
            theUrl = 'http://' + theUrl
        self.webView.setUrl(QtCore.QUrl(theUrl))

    @pyqtSignature("QString")
    def on_webView_titleChanged(self, title):
        """
        Public Slot invoked when the title of the page changes. All we do is to display it as the main window title.
        """
        self.setWindowTitle(title)

    @pyqtSignature("QUrl")
    def on_webView_urlChanged(self, url):
        """
        Public Slot invoked when the url changes. All we do is display the current url in txtUrl.
        """
        self.txtUrl.setText(url.toString())

def getCurDir(dirString):
    tempStr = str(dirString)#incase it is a QString
    if os.path.isfile(tempStr):
        return os.path.dirname(tempStr)
    else:
        return os.getcwd()

def valid(path):
    if path and os.path.isdir(path):
        return True
    return False

def env(name):
    return os.environ.get( name, '' )

def getHomeDir():
    if sys.platform != 'win32':
        return os.path.expanduser( '~' )

    homeDir = env( 'USERPROFILE' )
    if not valid(homeDir):
        homeDir = env( 'HOME' )
        if not valid(homeDir) :
            homeDir = '%s%s' % (env('HOMEDRIVE'),env('HOMEPATH'))
            if not valid(homeDir) :
                homeDir = env( 'SYSTEMDRIVE' )
                if homeDir and (not homeDir.endswith('\\')) :
                    homeDir += '\\'
                if not valid(homeDir) :
                    homeDir = 'C:\\'
    return homeDir


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())