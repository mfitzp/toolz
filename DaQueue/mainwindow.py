# -*- coding: utf-8 -*-

'''
/usr/bin/pyuic4 /home/clowers/workspace/DaQueue/mainwindow.ui  -o /home/clowers/workspace/DaQueue/ui_mainwindow.py

NEED TO ADD A THE FOLLOWING JOB STATES
QUEUED
PROCESSING
FINISHED
FAILED
'''


"""
This module contains the class MainWindow.
"""
import os
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignature
from ui_mainwindow import Ui_MainWindow
from extraWidgets import cellComboBox, cellOFD, cellStatus
from time import strftime, localtime
#strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())
from dbInterface import dbIO
import time

DBNAME = 'labqueue'
ROOTUSER = 'clowers'

try:
    USERNAME = os.login()
except:
    USERNAME = 'TestUser'

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
        self.initDB()

    def getTaskType(self, row):
        curWidget = self.taskTable.cellWidget(row, 0)
        if isinstance(curWidget, cellComboBox):
            return str(curWidget.currentText())

    def updateTaskType(self, row, comboIndex):
        curItem = self.taskTable.cellWidget(row, 0)
        if isinstance(curItem, cellComboBox):
#            print type(curItem)
            curItem.setCurrentIndex(comboIndex)

    def testTable(self):
        for row in xrange(self.taskTable.rowCount()):
            print type(self.taskTable.item(row, 0))

    def deleteJob(self, row = None):
        if row == None:
            row = self.taskTable.currentRow()
        jobItem = self.taskTable.item(row, self.taskIDInd)
        userItem = self.taskTable.item(row, self.uidInd)

        if jobItem != None and userItem != None:
            jobID = str(jobItem.text())
            userID = str(userItem.text())
            if len(jobID)>0 and len(userID)>0:
                if userID == USERNAME or USERNAME == ROOTUSER:
                    print jobID
                    self.db.delDocument(jobID)
                    self.taskTable.removeRow(row)
                else:
                    return QtGui.QMessageBox.warning(self, "Job Deletion Error",  self.wrongUserText)
            else:
                print "JobID or User is empty"
        else:
            print "JobItem or UserItem is empty"



    def submitJob(self, row = None):
        '''
        Submit Individual Job
        There needs to be a better way of detecting a
        problem in the dictionary parameters and aborting the job
        '''
        dbKeys = ['Task Type', 'Method File', 'Data Path', 'Output Path', 'State', 'User', 'Submit Time']
        indDict = {'Task Type':0, 'Method File':self.methodFileInd, 'Data Path':self.dataPathInd,
                   'Output Path':self.outputPathInd, 'State':self.stateInd, 'User':self.uidInd, 'Submit Time':self.timeInd}
        #self.taskTypeDict = {'File Conversion':0, 'X!Tandem Run':1, 'Peak Picking':2}

        if row == None:
            row = self.taskTable.currentRow()

        jobOK = True#assume job is ok to start
        jobID = str(self.taskTable.item(row, self.taskIDInd).text())
        #if the job already has been loaded to the couchdb server
        #then it will have a job ID and we only want to submit new jobs
        if len(jobID) == 0:
            '''
            Need to verify paths
            '''
            jobDict = {}#initiate an empty job
            for key in dbKeys:
                curCol = indDict[key]
                if curCol == self.methodFileInd or curCol == self.dataPathInd or curCol == self.outputPathInd:
                    curItem = self.taskTable.item(row, curCol)
                    if curItem != None:
                        dictParam = str(curItem.text())
                        if os.path.isfile(dictParam) or os.path.isdir(dictParam):
                            jobDict[key] = dictParam
                            curItem.setBackgroundColor(QtGui.QColor(255, 255, 255))
                        else:
                            jobOK = False
                            print "Parameter Error, Row %s, Column %s is not a valid path or file"%(row, curCol)
                            curItem.setBackgroundColor(QtGui.QColor(255, 106, 106))
                    else:
                        jobOK = False
                        print "Parameter Error, Row %s, Column %s is not a valid path or file"%(row, curCol)
                        newItem = QtGui.QTableWidgetItem('')
                        newItem.setBackgroundColor(QtGui.QColor(255, 106, 106))
                        self.taskTable.setItem(row, curCol, newItem)
                elif curCol == 0:
                    #this is the column for the task type
                    jobDict[key] = self.getTaskType(row)

                elif curCol == self.timeInd:
                    jobDict[key] = strftime("%a, %d %b %Y %H:%M:%S", localtime())

                elif curCol == self.uidInd:
                    curItem = self.taskTable.item(row, curCol)
                    if curItem != None:
                        dictParam = str(curItem.text())
                        if dictParam != None:
                            if len(dictParam)>0:
                                jobDict[key] = dictParam
                            else:
                                jobOK = False
                                print "Parameter Error, Row %s, Column %s is not a valid user"%(row, curCol)
                                curItem.setBackgroundColor(QtGui.QColor(255, 106, 106))
                        else:
                            jobOK = False
                            print "Parameter Error, Row %s, Column %s is not a valid user"%(row, curCol)
                            curItem.setBackgroundColor(QtGui.QColor(255, 106, 106))
                    else:
                        jobOK = False
                        print "Parameter Error, Row %s, Column %s is not a valid user"%(row, curCol)
                        curItem.setBackgroundColor(QtGui.QColor(255, 106, 106))

                elif curCol == self.stateInd:
                    curItem = self.taskTable.item(row, curCol)
                    if curItem != None:
                        dictParam = self.getTableJobStatus(row)
                        if dictParam != None:
                            if len(dictParam)>0:
                                jobDict[key] = dictParam
                            else:
                                jobOK = False
                                print "Parameter Error, Row %s, Column %s State Error"%(row, curCol)
                                curItem.setBackgroundColor(QtGui.QColor(255, 106, 106))
                        else:
                            jobOK = False
                            print "Parameter Error, Row %s, Column %s State Error"%(row, curCol)
                            curItem.setBackgroundColor(QtGui.QColor(255, 106, 106))
                    else:
                        jobOK = False
                        print "Parameter Error, Row %s, Column %s State Error"%(row, curCol)
                        curItem.setBackgroundColor(QtGui.QColor(255, 106, 106))

            if jobOK:
                ans = self.db.addDocument(jobDict)
                #boolean, jobID
                if ans[0]:
                    self.taskTable.setItem(row, self.taskIDInd, QtGui.QTableWidgetItem(ans[1]))
                    self.taskTable.setItem(row, self.timeInd, QtGui.QTableWidgetItem(jobDict['Submit Time']))
                    print jobDict
                else:
                    curItem = QtGui.QTableWidgetItem('Error submitting job!')
                    self.taskTable.setItem(row, self.taskIDInd, curItem)
                    curItem.setBackgroundColor(QtGui.QColor(255, 106, 106))
                    print "There was an error submitting job....contact Clowers"
            else:
                print "Job Error at Row %s"%row

    def submitQueue(self):
        '''
        self.methodFileInd = 1
        self.dataPathInd = 3
        self.outputPathInd = 5
        self.stateInd = 7
        self.uidInd = 8
        self.taskIDInd = 9
        self.timeInd = 10
        '''
        for i in xrange(self.taskTable.rowCount()):#iterate through the table of jobs
            self.submitJob(i)


    def updateQueue(self):
        '''
        I don't like to double "db".  Need to find a more elegant way of interfacing
        i.e. subclass
        '''
        if self.dbOK:
            self.taskTable.setRowCount(0)#need this otherwise there may duplicates added
            #alternatively, one could test to see if item exists....but right now I'm feeling lazy
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
                            elif curDoc[key] == 'Queued':
                                self.updateStatus(i, 3)
                        elif key == 'Task Type':
                            taskKey = curDoc[key]
                            self.updateTaskType(i, self.taskTypeDict[taskKey])
                        elif key == 'User':
                            newTableItem = QtGui.QTableWidgetItem(curDoc[key])
                            self.makeItemReadOnly(newTableItem)
                            self.taskTable.setItem(i,j, newTableItem)
                        else:
                            newTableItem = QtGui.QTableWidgetItem(curDoc[key])
                            self.taskTable.setItem(i,j, newTableItem)

                    elif key == 'Task ID':
                        newTableItem = QtGui.QTableWidgetItem(docID)
                        self.makeItemReadOnly(newTableItem)
                        self.taskTable.setItem(i,j, newTableItem)

            self.updateColumnSizes()
            self.sortTable()


    def __setVariables__(self):
        '''Variables that are utilized by other functions'''
        self.__curDir = getHomeDir()
        self.server = None
        self.serverStatus = False
        self.serverAddress = None
        self.serverPort = None
        self.db = None
        self.dbOK = False

        self.taskHeaders = ['Task Type', 'Method File', '', 'Data Path', '','Output Path', '', 'State', 'User', 'Task ID', 'Submit Time']
        self.dbKeys = ['Task Type', 'Method File', 'Data Path', 'Output Path', 'State', 'User', 'Task ID', 'Submit Time']
        self.taskOptions = ['File Conversion', 'X!Tandem Run', 'Peak Picking']
        self.taskTypeDict = {'File Conversion':0, 'X!Tandem Run':1, 'Peak Picking':2}

        self.methodFileInd = 1
        self.dataPathInd = 3
        self.outputPathInd = 5
        self.stateInd = 7
        self.uidInd = 8
        self.taskIDInd = 9
        self.timeInd = 10

        self.taskTable.setSortingEnabled(True)

    def sortTable(self):
        self.taskTable.sortItems(self.timeInd, QtCore.Qt.AscendingOrder)
        self.taskTable.scrollToBottom()

    def dbStatusUpdate(self):
        '''
        Updates the server status on the GUI and attempts
        connection with couchDB server
        '''
        if self.serverStatus and self.dbOK:
            self.serverStatusBtn.setIcon(QtGui.QIcon('images/clean.png'))
        else:
            self.serverStatusBtn.setIcon(QtGui.QIcon('images/exit.png'))

        if self.serverStatus:
            if self.dbOK:
                pass
            else:
                return QtGui.QMessageBox.warning(self, "Database Error",  self.dbErrorText)
        else:
            return QtGui.QMessageBox.warning(self, "Server Connection Error",  self.serverErrorText)


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

        self.serverErrorText = "There was an error connecting to the server.  Please try the number and dial again."
        self.dbErrorText = "There was an error connecting to the 'labqueue' database. Does the database exist?"
        self.wrongUserText = "You do not have the permissions to delete this job as you are not the owner."

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
        QtCore.QObject.connect(self.submitQueueBtn, QtCore.SIGNAL("clicked()"),self.submitQueue)

        QtCore.QObject.connect(self.actionFill_Column_with_Current_Value, QtCore.SIGNAL("triggered()"),self.fillColumnWithCurrent)
        QtCore.QObject.connect(self.actionUpdate_Queue, QtCore.SIGNAL("triggered()"),self.updateQueue)
        QtCore.QObject.connect(self.actionSubmit_Queue, QtCore.SIGNAL("triggered()"),self.submitQueue)
        QtCore.QObject.connect(self.actionAdd_Multiple_Rows, QtCore.SIGNAL("triggered()"),self.addRows)
        QtCore.QObject.connect(self.actionAdd_Row, QtCore.SIGNAL("triggered()"),self.addSingleRow)
        QtCore.QObject.connect(self.actionDelete_Job, QtCore.SIGNAL("triggered()"),self.deleteJob)
        QtCore.QObject.connect(self.deleteQueueRowBtn, QtCore.SIGNAL("clicked()"),self.deleteJob)

        '''
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL("triggered()"),self.testFunc)
        actionSubmit_Job
        '''
        QtCore.QObject.connect(self.actionTestAction, QtCore.SIGNAL("triggered()"),self.testFunc)

    def testFunc(self):
        print "Test Function Triggered"
#        self.addRows()
        self.fillColumnWithCurrent()
#        self.updateStatus(2, 2)

    def makeItemReadOnly(self, tableItem):
        tableItem.setFlags(QtCore.Qt.ItemIsSelectable)
        tableItem.setFlags(QtCore.Qt.ItemIsEnabled)

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
            userItem = QtGui.QTableWidgetItem(USERNAME)
            self.makeItemReadOnly(userItem)
            self.taskTable.setItem(row, self.uidInd, userItem)
            taskIDItem = QtGui.QTableWidgetItem('')
            self.makeItemReadOnly(taskIDItem)
            self.taskTable.setItem(row, self.uidInd+1, taskIDItem)

        self.taskTable.resizeColumnsToContents()
        self.taskTable.resizeRowsToContents()
        self.taskTable.setColumnWidth(0, 150)

    def getTableJobStatus(self, row):
        '''
        Returns the state of processing from the table NOT THE DATABASE
        '''
        curItem = self.taskTable.item(row, self.stateInd)
        if isinstance(curItem, cellStatus):
            return curItem.getStatusText()


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
            self.sortTable()


    def addSingleRow(self):
        '''
        Adds a single row to the job queue
        '''
        curRow = self.taskTable.rowCount()
        self.taskTable.insRow(curRow)
        self.taskTable.scrollToBottom()

    def addRows(self):
        '''
        Adds the user specified number of rows
        '''
        val, ansOK = QtGui.QInputDialog.getInteger(self, 'Modify Table', 'Specify number of rows to add:', 0)
        if ansOK:
            curRow = self.taskTable.currentRow()
            for i in xrange(val):
                self.addSingleRow()
#                self.taskTable.insRow(i+curRow)
            return val

    def fillColumnWithCurrent(self):
        '''
        Fills all rows below the current column value for the user specified number of rows
        '''
        curRow = self.taskTable.currentRow()
        maxRows = self.taskTable.rowCount()
        numRows = maxRows - curRow
        if numRows == 0:
            return False

        curCol = self.taskTable.currentColumn()
        if curCol == self.methodFileInd or curCol == self.dataPathInd or curCol == self.outputPathInd:
#            numRows = self.addRows()
            curItem = self.taskTable.currentItem()
            if curItem != None:
                curText = str(curItem.text())
                if curText != None:
                    for i in xrange(numRows):
                        self.taskTable.setItem(curRow+i, curCol, QtGui.QTableWidgetItem(curText))




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