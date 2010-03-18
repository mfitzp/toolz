14#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
/usr/bin/pyuic4 /home/clowers/workspace/DaQueue/workerGUI.ui  -o /home/clowers/workspace/DaQueue/ui_workerGUI.py

NEED TO ADD A THE FOLLOWING JOB STATES
QUEUED
PROCESSING
FINISHED
FAILED

Need to add logging
'''


"""
This module contains the class MainWindow.
"""
import os
from os import walk
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignature
from ui_workerGUI import Ui_MainWindow
from extraWidgets import cellComboBox, cellOFD, cellStatus
from time import strftime, localtime, sleep
#strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())
from dbInterface import sqliteIO#, dbIO
import time

from string import join
import subprocess as sub

from uiSupport import STATUSIDS, STATUSTYPES, JOBKEYS, JOBTYPES,\
                      JOBDICT, DBNAME, QUEUETABLE, ROOTUSER, XT_EXE_PATH,\
                      USERNAME, STATUSDICT
#STATUSIDS = [0,1,2,3,4]
#STATUSTYPES = ['Queued', 'Processing', 'Finished', 'Failed', 'Waiting for User Action']
#
#JOBKEYS = [0,1,2,3,4,5,6]
#JOBTYPES = ['X!Tandem', 'RAW File Conversion', 'Bruker File Conversion', 'Peak Picking', 'Polygraph', 'Unspecified', 'Ignored']
#JOBDICT = {'X!Tandem':0, 'RAW File Conversion':1, 'Bruker File Conversion':2, 'Peak Picking':3, 'Polygraph':4, 'Unspecified':5, 'Ignored':6}
#
#DBNAME = 'labqueue.db'
#QUEUETABLE = 'queueTable'
#ROOTUSER = 'clowers'
#
#XT_EXE_PATH = ''
#
#try:
#    USERNAME = os.login()
#except:
#    USERNAME = 'TestUser'

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
        self.initDB()
        self.getUnprocessedTask()

    def initDB(self):
        self.db = sqliteIO.queueDB(DBNAME, parent = self)
        self.dbOK = self.db.dbOK
        self.dbStatusUpdate()

    def dbStatusUpdate(self):
        '''
        Updates the status on the GUI and attempts
        connection with sqlite server
        '''
        if self.dbOK:
            self.serverStatusBtn.setIcon(QtGui.QIcon('images/clean.png'))
        else:
            self.serverStatusBtn.setIcon(QtGui.QIcon('images/exit.png'))
            return QtGui.QMessageBox.warning(self, "Database Error",  self.dbErrorText)

    def getUnprocessedTask(self):
        '''
        starts the next unprocessed task in queue

        look at existing table
        if there are any unprocessed jobs
        get that job
        run it
        change status upon thread completion
        if there are no unprocessed jobsthat should be called ONLY once
        updated from database and repeat
        '''
        if len(self.unprocessedRows) == 0:
            self.pollDB()
            self.updateQueue()#clears and resets tables and checks for new values
            self.taskLoop()
        elif len(self.unprocessedRows) > 0:
            self.curDBRow = self.unprocessedRows.pop(0)
            if self.curDBRow.has_key('uuID'):
                uiID = self.curDBRow['uuID']
#                print jobID
                if uiID != None:
                    self.curRow = self.getRowFromTaskID(uiID)
                    self.updateStatus(self.curRow, 1)#1 is Processing
                    self.updateDB(uiID, 'status', 'Processing')
                    self.submitJob(self.curDBRow)
#                    print "DBROW", self.curDBRow
                else:
                    print "JobID Empty"
                #update database
                #prepare thread
                #run thread

    def getRowFromTaskID(self, uiID):
        for row in xrange(self.taskTable.rowCount()):
            tableID = str(self.taskTable.item(row,self.uuIDInd).text())
            #print tableID, uiID, type(tableID), type(uiID)
            if tableID == uiID:
                return row

    def updateStatus(self, row, state):
        curItem = self.taskTable.item(row, self.stateIconInd)
        if isinstance(curItem, cellStatus):
            curItem.switchStatus(state)
#            print row, self.stateInd
            textItem = self.taskTable.setItem(row, self.stateInd, QtGui.QTableWidgetItem(STATUSDICT[state]))


    def pollDB(self):
        if self.dbOK:
            self.getQueued()

    def getQueued(self):
        '''
        dataFile TEXT,\
        cfgFile TEXT,\
        outputFile TEXT,\
        status TEXT,\
        statusID INTEGER,\
        jobID INTEGER,\
        timeID TEXT)'
        '''
        if self.dbOK:
            #SELECT THE QUEUED FILES
            self.db.cur.execute(("SELECT * FROM %s WHERE %s LIKE '%s'"%(QUEUETABLE, 'statusID', str(STATUSIDS[0]))))
            self.unprocessedRows = self.db.GET_CURRENT_QUERY_AS_DICT()


    def updateQueue(self):
        '''
        Example DB Row from sqlite database

        DBROW {
        'status': 'Queued',
        'dataFile': 'C:\\Documents and Settings\\d3p483\\workspace\\DaQueue\\testData\\0_E7.mzXML',
        'outputFile': 'None',
        'uuID': '4a7a3f62-ce14-5389-be92-d836d89fd17e',
        'cfgFile': 'C:\\Documents and Settings\\d3p483\\workspace\\DaQueue\\testData\\pyInput.cfgXML',
        'timeID': 'Mon, 25 Jan 2010 11:18:09',
        'jobID': '5',
        'statusID': '0'}

        '''
        if self.dbOK:
            self.taskTable.setRowCount(0)#need this otherwise there may duplicates added
            #alternatively, one could test to see if item exists....but right now I'm feeling lazy
            for i, dbRow in enumerate(self.unprocessedRows):
                self.taskTable.insRow(i)#REMEBER THIS USES A CUSTOM CALL in tableClass.py
                for j, key in enumerate(self.dbKeys):
                    if dbRow.has_key(key):
                        if key == 'statusID':
                            if dbRow[key] == '1':
                                self.updateStatus(i, 1)
                            elif dbRow[key] == '2':
                                self.updateStatus(i, 2)
                            elif dbRow[key] == '3':
                                self.updateStatus(i, 3)
                            elif dbRow[key] == '0':
                                self.updateStatus(i, 0)
                        elif key == 'jobID':
                            jobKey = dbRow[key]
#                            self.taskTypeDict = {'X!Tandem Run':0, 'Peak Picking':1, 'File Conversion':2}
                            self.updateTaskType(i, int(jobKey))
                        elif key == 'User':
                            newTableItem = QtGui.QTableWidgetItem(curDoc[key])
                            self.makeItemReadOnly(newTableItem)
                            self.taskTable.setItem(i,j, newTableItem)
                        else:
                            newTableItem = QtGui.QTableWidgetItem(dbRow[key])
                            self.taskTable.setItem(i,j, newTableItem)

                    elif key == 'uuID':
                        newTableItem = QtGui.QTableWidgetItem(dbRow[uuID])
                        self.makeItemReadOnly(newTableItem)
                        self.taskTable.setItem(i,j, newTableItem)

            self.updateColumnSizes()
            self.sortTable()
#            self.setTaskList()

    def updateColumnSizes(self):
        self.taskTable.resizeColumnsToContents()
        self.taskTable.setColumnWidth(0, 150)

    def sortTable(self):
        self.taskTable.sortItems(self.timeIDInd, QtCore.Qt.AscendingOrder)
        self.taskTable.scrollToBottom()

    def taskLoop(self):
        '''
        This is the main worker loop that is called whenever a job finishes are there
        are no more jobs to run
        '''
        print "Task Loop Called"

        waitTime = 2000
        QtCore.QTimer.singleShot(waitTime, self.getUnprocessedTask)


        #waitTime = 2
        #sleep(waitTime)
        #self.getUnprocessedTask()


    def taskTest(self, val = None):
        print "taskTest Called"
        self.taskFinished(val, "Ok")

    def updateDB(self, jobID, updateField, updateValue):
        '''
        This is not working the way I want....
        STATUSIDS = [0,1,2,3,4]
        STATUSTYPES = ['Queued', 'Processing', 'Finished', 'Failed', 'Waiting for User Action']

        JOBKEYS = [0,1,2,3,4]
        JOBTYPES = ['X!Tandem', 'File Conversion', 'Peak Picking', 'Polygraph', 'Unspecified']

        uuID TEXT,\
        dataFile TEXT,\
        cfgFile TEXT,\
        outputFile TEXT,\
        status TEXT,\
        statusID INTEGER,\
        jobID INTEGER,\
        timeID TEXT)'

        '''
        keyField = 'uuID'
        keyValue = jobID

        nextField = 'statusID'
        #self.updateDB(jobID, 'State', 'Processing')
        #UPDATE queueTable SET jobID = 7, status = 'YOGI' WHERE uuID LIKE "f065ec40-839b-5022-a528-b5764845f20d"
        for i,val in enumerate(STATUSTYPES):
            if updateValue == val:
                nextValue = i
                continue

        execStr = 'UPDATE %s SET %s = "%s", %s = %d WHERE %s LIKE "%s"'%(QUEUETABLE,updateField, updateValue, nextField, nextValue, keyField, keyValue)
        print execStr

        self.db.EXEC_QUERY(execStr)

    def getTaskID(self, dbRow):
        '''
        dbRow is a dictionary format with the following keys
        uuID TEXT,\
        dataFile TEXT,\
        cfgFile TEXT,\
        outputFile TEXT,\
        status TEXT,\
        statusID INTEGER,\
        jobID INTEGER,\
        timeID TEXT)'

        '''
        jobItem = self.taskTable.item(row, self.taskIDInd)
        if jobItem != None:
            jobID = str(jobItem.text())
            return jobID

    def taskFinished(self, retObject):
        '''
        To be called when the thread finishes

        update table
        update database
        process next task
        '''
        retVal, retStr = retObject
        print "Task Finished, RetVal: %s"%retVal
        if retVal == 1:
            self.updateStatus(self.curRow, 3)#failed State
            self.updateDB(self.curDBRow['uuID'], 'status', 'Failed')
            #process retStr
            #update DB
            #add to log
        elif retVal == 0:
            self.updateStatus(self.curRow, 2)#finished State
            self.updateDB(self.curDBRow['uuID'], 'status', 'Finished')
            #process retStr
            #update DB
            #add to log
        self.taskLoop()
#        self.getUnprocessedTask()

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
                self.taskTable.removeRow(row)
                print "JobID or User is empty"
        else:
            self.taskTable.removeRow(row)
            print "JobItem or UserItem is empty"


    def submitJob(self, dbRowDict, tableRow = None):
        '''
        Submit Individual Job
        There needs to be a better way of detecting a
        problem in the dictionary parameters and aborting the job

        DBROW {
        'status': 'Queued',
        'dataFile': 'C:\\Documents and Settings\\d3p483\\workspace\\DaQueue\\testData\\0_E7.mzXML',
        'outputFile': 'None',
        'uuID': '4a7a3f62-ce14-5389-be92-d836d89fd17e',
        'cfgFile': 'C:\\Documents and Settings\\d3p483\\workspace\\DaQueue\\testData\\pyInput.cfgXML',
        'timeID': 'Mon, 25 Jan 2010 11:18:09',
        'jobID': '5',
        'statusID': '0'}
        inputDict['Param File']

                self.execPath =

        '''
        dbRowKeys = ['status', 'dataFile', 'outputFile', 'uuID', 'cfgFile', 'timeID', 'jobID', 'statusID']

        #Get Job Type
        jobType = JOBTYPES[int(dbRowDict['jobID'])]
        inputDict = {}
        if jobType == None:
            print "Submit JobType error!"
            return False
        inputDict['Process Type'] = jobType
        #Get Input File
        inputFile = dbRowDict['dataFile']
        if os.path.isfile(inputFile):
            inputDict['Input File'] = inputFile
        else:
            print "Input File is not a valid path!"
            return False
        #Get Config File
        cfgFile = dbRowDict['cfgFile']
        if os.path.isfile(cfgFile):
            inputDict['Param File'] = cfgFile
        else:
            inputDict['Param File'] = None

        #Need to add a check for whether a config file is required
        inputDict['Executable Path'] = None

        #Get Output File
        outputFile = dbRowDict['outputFile']
        inputDict['Output File'] = outputFile#do I need a check for this

        if self.thread.updateThread(inputDict):
            self.thread.start()
        else:
            msg = "Update Thread Failed\n"
            msg += str(inputDict)
            print msg
            #call taskFinished with failed error
            self.taskFinished([1,msg])

    def submitQueue(self):
        '''
        self.methodFileInd = 1
        self.dataPathInd = 3
        self.outputPathInd = 5
        self.stateInd = 7
        self.uidInd = 8
        self.taskIDInd = 9
        self.timeIDInd = 10
        '''
        for i in xrange(self.taskTable.rowCount()):#iterate through the table of jobs
            self.submitJob(i)


    def setTaskList(self):
        '''
        Fills up the variable containing the rows to process
        '''
        self.unprocessedRows = []
        # self.stateList = ['Processing', 'Finished', 'Failed', 'Queued']
        # States = 0, 1, 2, 3
        for row in xrange(self.taskTable.rowCount()):
            if self.getTableJobStatus(row) == 'Queued':#third value
                self.unprocessedRows.append(row)

    def __setVariables__(self):
        '''Variables that are utilized by other functions'''
        self.__curDir = getHomeDir()
        self.server = None
        self.serverStatus = False
        self.serverAddress = None
        self.serverPort = None
        self.db = None
        self.dbOK = False
        self.queryResult = []#will hold a list of dictionaries from the sqlite DB
        self.thread = runThread(parent = self)

        '''
        uuID TEXT,\
        dataFile TEXT,\
        cfgFile TEXT,\
        outputFile TEXT,\
        status TEXT,\
        statusID INTEGER,\
        jobID INTEGER,\
        timeID INTEGER)'
        '''

        #OLD self.taskHeaders = ['Task Type', 'Method File', '', 'Data Path', '','Output Path', '', 'State', 'User', 'Task ID', 'Submit Time']
        self.taskHeaders = ['Task Type', 'State', 'Method File', 'Data Path','Output Path','State ID','Task ID', 'Submit Time']
        self.dbKeys = ['jobID', 'statusID', 'cfgFile', 'dataFile', 'outputFile', 'status', 'uuID', 'timeID']
        self.taskOptions = ['X!Tandem Run', 'Peak Picking','File Conversion']
        self.taskTypeDict = {'X!Tandem Run':0, 'Peak Picking':1, 'File Conversion':2}

        self.curRow = 0
        self.curDBRow = {}

        self.taskSelectorInd = 0
        self.stateIconInd = 1
        self.methodFileInd = 2
        self.dataPathInd = 3
        self.outputPathInd = 4
        self.stateInd = 5
        self.uuIDInd = 6
        self.timeIDInd = 7

#        self.taskIDInd = 9
#        self.timeIDInd = 10

        self.unprocessedRows = []

        self.taskTable.setSortingEnabled(True)


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
        directory= QtGui.QFileDialog.getExistingDirectory(self, "Select Output Data Folder", self.__curDir)
        if os.path.isdir(str(directory)):
            self.__curDir = str(directory)
            print self.__curDir, str(directory)
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
#        QtCore.QObject.connect(self.resetServerBtn, QtCore.SIGNAL("clicked()"),self.initServer)

        QtCore.QObject.connect(self.updateQueueBtn, QtCore.SIGNAL("clicked()"),self.updateQueue)
#        QtCore.QObject.connect(self.submitQueueBtn, QtCore.SIGNAL("clicked()"),self.submitQueue)

#        QtCore.QObject.connect(self.actionFill_Column_with_Current_Value, QtCore.SIGNAL("triggered()"),self.fillColumnWithCurrent)
#        QtCore.QObject.connect(self.actionAdd_Entire_Data_Folder, QtCore.SIGNAL("triggered()"),self.processEntireFolder)
        QtCore.QObject.connect(self.actionUpdate_Queue, QtCore.SIGNAL("triggered()"),self.updateQueue)
#        QtCore.QObject.connect(self.actionSubmit_Queue, QtCore.SIGNAL("triggered()"),self.submitQueue)
#        QtCore.QObject.connect(self.actionAdd_Multiple_Rows, QtCore.SIGNAL("triggered()"),self.addRows)
#        QtCore.QObject.connect(self.actionAdd_Row, QtCore.SIGNAL("triggered()"),self.addSingleRow)
        QtCore.QObject.connect(self.actionDelete_Job, QtCore.SIGNAL("triggered()"),self.deleteJob)
        QtCore.QObject.connect(self.deleteQueueRowBtn, QtCore.SIGNAL("clicked()"),self.deleteJob)

        '''
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL("triggered()"),self.testFunc)
        actionSubmit_Job
        '''
        QtCore.QObject.connect(self.actionTestAction, QtCore.SIGNAL("triggered()"), self.testFunc)
        QtCore.QObject.connect(self.runJobBtn, QtCore.SIGNAL("clicked()"), self.testFunc)

        QtCore.QObject.connect(self.thread, QtCore.SIGNAL("threadFinished(PyQt_PyObject)"),self.taskFinished)

    def testFunc(self):
        print "Test Function Triggered"
#        self.addRows()
#        self.fillColumnWithCurrent()
#        self.updateStatus(0,0)
#        self.processEntireFolder()
        self.updateQueue()#FIX
        self.getUnprocessedTask()

    def parseFolder(self, directory, debug = False):
        '''
        At this point this just looks for mzXML and mgf files for X!Tandem to examine
        '''
        fileList = []
        startDir = []
        for root, dirs, files in walk(directory):
            #for dir in dirs:
            for file in files:
                if '.mzXML' in file or '.mgf' in file:
                    #temptime = time.clock()
                    filePath = os.path.abspath(os.path.join(root, file))
                    fileList.append(filePath)

                    if debug:
                        i+=1
                        if i == 30:
                            t2 = time.clock()
                            for item in dirList:
                                print item
                                print ''
                            print t2-t1,  " sec Total"
                            return fileList

#        for item in fileList:
#            print item
        return fileList

    def processEntireFolder(self):
        '''
        Goes through an entire folder and adds the acceptable files to a input file list
        '''
        folderName = self.__loadDataFolder__()
        if folderName != None:
            fileList = self.parseFolder(folderName)
            if len(fileList)>0:
                rowStart = self.taskTable.rowCount()
                self.addRows(len(fileList))
                for i,dataFile in enumerate(fileList):
                    self.taskTable.setItem(rowStart+i, self.dataPathInd, QtGui.QTableWidgetItem(dataFile))
                self.updateColumnSizes()


    def makeItemReadOnly(self, tableItem):
        tableItem.setFlags(QtCore.Qt.ItemIsSelectable)
        tableItem.setFlags(QtCore.Qt.ItemIsEnabled)

    def __resetTaskTable__(self):
        self.taskTable.clear()
        self.taskTable.setColumnCount(len(self.taskHeaders))
        self.taskTable.setRowCount(3)
        self.taskTable.setHorizontalHeaderLabels(self.taskHeaders)

        for row in xrange(self.taskTable.rowCount()):
            self.taskTable.setCellWidget(row, self.taskSelectorInd, cellComboBox())
#            self.taskTable.setItem(row, self.methodFileInd+1, cellOFD())
#            self.taskTable.setItem(row, self.dataPathInd+1, cellOFD())
#            self.taskTable.setItem(row, self.outputPathInd+1, cellOFD())
            self.taskTable.setItem(row, self.stateIconInd, cellStatus())
#            userItem = QtGui.QTableWidgetItem(USERNAME)
#            self.makeItemReadOnly(userItem)
#            self.taskTable.setItem(row, self.uidInd, userItem)
            taskIDItem = QtGui.QTableWidgetItem('')
            self.makeItemReadOnly(taskIDItem)
            self.taskTable.setItem(row, self.uuIDInd, taskIDItem)

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

    def addRows(self, val = None):
        '''
        Adds the user specified number of rows
        '''
        if val == None:
            val, ansOK = QtGui.QInputDialog.getInteger(self, 'Modify Table', 'Specify number of rows to add:', 0)
        elif type(val) == int:
            ansOK = True
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

class runThread(QtCore.QThread):
        def __init__(self, parent):
            QtCore.QThread.__init__(self, None)#parent)
            '''
            Valid Process Types:
            XTandem
            RAW File Conversion
            '''
            self.P = parent
            self.processType = None
            self.inputFile = None
            self.outputFile = None
            self.paramFile = None
            self.execPath = None
            self.inputDict = {}
            self.retCode = None
            self.finished = False
            self.ready = False

            self.retCode = None #0 is succesful, any other integer is a failure.

        def updateThread(self, inputDict):
            self.processType = inputDict['Process Type']
            print "Thread Process Type: ", self.processType, type(self.processType)
            if self.processType == 'RAW File Conversion':
                self.inputFile = inputDict['Input File']
                self.outputFile = inputDict['Output File']
                print 'ReAdW Params:\t',self.inputFile, self.outputFile
                if os.path.isfile(self.inputFile):
                    self.curInputDict = inputDict
                    self.ready = True
                    return True
                else:
                    self.ready = False
                    return False
            elif self.processType == 'Bruker File Conversion':
                '''
                This is not implemented yet
                '''
                print "Bruker File Conversion Not Implemented"
                self.ready = False
                return False

            elif self.processType == 'X!Tandem':
                self.paramFile = inputDict['Param File']

                self.execPath = inputDict['Executable Path']
                self.curInputDict = inputDict
                if os.path.isfile(self.execPath) and os.path.isfile(self.paramFile) and os.path.isfile(self.inputFile):
                    self.ready = True
                    return True
                else:
                    print "X!Tandem Thread Update Failed"
                    self.ready = False
                    return False
            else:
                '''
                This is not implemented yet
                '''
                print "%s Job Type is Not Implemented"%self.processType
                self.ready = False
                return False

        def run(self):
            if self.ready:
                if self.processType == 'X!Tandem':
                    self.emit(QtCore.SIGNAL("threadFinished(PyQt_PyObject)"),[99,'None Implemented'])
#                    self.exeTandem()
                if self.processType == 'RAW File Conversion':
                    self.exeRAW(self.inputFile, self.outputFile)
                self.ready = False


        def updateMsg(self, outputStr = None):
            print self.outMsg
            self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),self.outMsg)

        def __del__(self):
            self.exiting = True
            self.wait()

        def exeTandem(self):
            '''
            USAGE: tandem filename

            where filename is any valid path to an XML input file.

            +-+-+-+-+-+-+

            X! TANDEM TORNADO (2008.02.01.3)

            Copyright (C) 2003-2008 Ronald C Beavis, all rights reserved
            This software is a component of the GPM  project.
            Use of this software governed by the Artistic license.
            If you do not have this license, you can get a copy at
            http://www.perl.com/pub/a/language/misc/Artistic.html

            +-+-+-+-+-+-+

            Because XTandem puts the output file in the directory of the executable, we need to move it to the
            appropriate place, i.e. The Data Repository

            Also to be done is the create a database (i.e. sqlite3 db) to store the processed info and have a log!!!

            '''
            t1 = time.clock()
            self.cmdOut = [self.execPath]
            self.cmdOut.append(self.inputFile)

            cmdStr = ''
            for item in self.cmdOut:
                cmdStr += item
                cmdStr += ' ' #add space
            cmdStr +='\n'
            print cmdStr
            try:
                subHandle = sub.Popen(cmdStr, bufsize = 0, shell = True,  cwd = self.cwd, stdout=sub.PIPE, stderr=sub.PIPE,  stdin=sub.PIPE)

#                print subHandle.poll()
#                timer = QtCore.QTimer()
#                while subHandle.poll() == None:
#                    timer.start(10)
#                    msg = subHandle.stdout.read()
#                    self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),msg)

#                    print subHandle.stderr.read()


#                    msg = subHandle.stderr.readline()
#                    self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),msg)
#                    msg = subHandle.stdout.readline()
#                    self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),msg)
#                    self.outMsg = subHandle.stdout.read()
#                    print subHandle.stderr.read()
#                    QtCore.QTimer.singleShot(20, self.updateMsg)


                self.outMsg = subHandle.stdout.read()
                self.errMsg = subHandle.stderr.read()
                subHandle.stderr.close()
                subHandle.stdout.close()
                subHandle.stdin.close()
                self.retCode = subHandle.wait()

                t2 = time.clock()
                runTime= '%s sec\n\n'%(t2-t1)
                if self.retCode != 0:
                    msg = self.outMsg+'\n'+self.errMsg
                    msg += runTime
                    #print msg
                    self.emit(QtCore.SIGNAL("threadFinished(PyQt_PyObject)"),[self.retCode,msg])
#                    self.__del__()
#                    return msg
                else:
                    msg = self.outMsg+'\n'+self.errMsg
                    msg += runTime
                    #print msg
                    self.emit(QtCore.SIGNAL("threadFinished(PyQt_PyObject)"),[self.retCode,msg])
#                    self.__del__()
#                    return msg
            except:
                print "Error Log Start:\n",cmdStr
                raise



        def exeRAW(self, file2Convert, newFileName = None):
            '''
            ReAdW 4.0.1(build Jun 13 2008 11:45:07)

            Usage: ReAdW [options] <raw file path> [<output file>]

             Options
              --mzXML:         mzXML mode (default)
              --mzML:          mzML mode (EXPERIMENTAL)
                  one of --mzXML or --mzML must be selected

              --centroid, -c: Centroid all scans (MS1 and MS2)
                  meaningful only if data was acquired in profile mode;
                  default: off
              --compress, -z: Use zlib for compressing peaks
                  default: off
              --verbose, -v:   verbose

              output file: (Optional) Filename for output file;
                  if not supplied, the output file will be created
                  in the same directory as the input file.


            Example: convert input.raw file to output.mzXML, centroiding MS1 and MS2 scans

                  ReAdW --mzXML -c C:\test\input.raw c:\test\output.mzXML

            Author: Josh Tasman (SPC/ISB), with Jimmy Eng, Brian Pratt, and Matt Chambers,
                  based on orignal work by Patrick Pedriolli.
            '''

            #############HARD CODED OPTIONS###########
            self.centroidOK = True

            t1 = time.clock()
            self.cmdOut = ['ReAdW']

            filetype = str(self.outputFile).split('.')[-1]
#            print filetype, type(filetype)

            if filetype == 'mzXML':
                self.cmdOut.append(' --mzXML')
            elif filetype == 'None':
                self.cmdOut.append(' --mzXML')
            elif filetype == 'mzML':
                self.cmdOut.append(' --mzML')

            if self.centroidOK:
                processMods = ' -v -c '# v is for verbose output
            else:
                processMods = ' -v ' #add a space
            self.cmdOut.append(processMods)

            if self.centroidOK:
                inputFile = file2Convert+' '# v is for verbose output
            else:
                inputFile = file2Convert+' ' #add a space
            self.cmdOut.append(inputFile)


            if newFileName != None:
#                if filetype == 'None' and self.useSingleFile == False:
#                    newFileName+='.mzXML'
#                    newPath = os.path.join(str(self.RAWData), newFileName)
#
#                elif filetype == 'None' and self.useSingleFile == True:
#                    newFileName += '.mzXML'
#                    coreDir = os.path.split(str(self.RAWData))[:-1][0]
#                    newPath = os.path.join(coreDir, newFileName)
##                    print newPath
#
#                else:
                newPath=str(self.outputFile)

            else:
                erMsg = "No output file specified"
                print erMsg
                raise erMsg

            newPath = os.path.abspath(newPath)
            outFile = newPath
            self.cmdOut.append(outFile)

            cmdStr = ''
            for item in self.cmdOut:
                cmdStr += item
            cmdStr +='\n'
            print cmdStr
            print os.getcwd()
            try:

                subHandle = sub.Popen(cmdStr, bufsize = 0, shell = True,  stdout=sub.PIPE, stderr=sub.PIPE,  stdin = sub.PIPE)

                self.outMsg = subHandle.stdout.read()
                self.errMsg = subHandle.stderr.read()
                subHandle.stderr.close()
                subHandle.stdout.close()
                subHandle.stdin.close()
                self.retCode = subHandle.wait()

                t2 = time.clock()
                runTime= '%s sec\n\n'%(t2-t1)
                if self.retCode != 0:
                    msg = self.outMsg+'\n'+self.errMsg
#                    fileupdate = '%d of %d Finished\n'%(self.curFileNum+1, self.totalFiles)
#                    msg +=fileupdate
                    msg += runTime
                    self.emit(QtCore.SIGNAL("threadFinished(PyQt_PyObject)"),[self.retCode,msg])
                    return msg
                else:
                    msg = self.outMsg+'\n'+self.errMsg
#                    fileupdate = '%d of %d Finished\n'%(self.curFileNum+1, self.totalFiles)
#                    msg +=fileupdate
                    msg += runTime
                    self.emit(QtCore.SIGNAL("threadFinished(PyQt_PyObject)"),[self.retCode,msg])
                    return msg
                #######Need to Emit Signal###########
            except:
                print "Error Log Start:\n",cmdStr
                raise


############################
class ProgressBar(QtGui.QWidget):
    def __init__(self, maxRange, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setWindowTitle('File Conversion Progress')

        self.pbar = QtGui.QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.maxRange = maxRange
        self.pbar.setRange(0, self.maxRange)
        self.pbar.setValue(0)
        self.step = 0;

    def barUpdate(self, value):
        if self.step >= self.maxRange:
            return

        self.step +=1
        self.pbar.setValue(value)

def run_main():
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
#    try:
    ui = RAWConvert(MainWindow)
    MainWindow.show()
#    except:
#        errorMsg = "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
#        errorMsg+='\n Contact Clowers and try to remember what you did to make it crash!'
#        QtGui.QMessageBox.warning(MainWindow, "Fatal Error",  errorMsg)

    sys.exit(app.exec_())

def run_main2():
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
#    run_main()
    run_main2()


'''    def exeRAW(self, file2Convert,  newFileName = None):
        self.cmdOut = ['ReAdW']

        filetype = str(self.outputFile).split('.')[-1]

        if filetype == 'mzXML':
            self.cmdOut.append(' -mode 0 ')
        elif filetype == 'None':
            self.cmdOut.append(' -mode 0 ')
        elif filetype == 'mzDATA':
            self.cmdOut.append(' -mode 1 ')

        inputFile = ' -a '+file2Convert
        self.cmdOut.append(inputFile)

        if newFileName != None:
            if filetype == 'None' and self.useSingleFile == False:
                newFileName+='.mzXML'
                newPath = os.path.join(str(self.RAWData), newFileName)

            elif filetype != 'None' and self.useSingleFile == True:
                newFileName += '.mzXML'
                coreDir = os.path.split(str(self.RAWData))[:-1][0]
                newPath = os.path.join(coreDir, newFileName)
                print newPath
            else:
                newPath=str(self.outputFile)
        else:
            newFileName='analysis.mzXML'
            self.dir = os.path.dirname(str(self.RAWData))
            newPath = os.path.join(self.dir, newFileName)

        #this small code block writes a peak list to a csv file
        peakList = RAWPeakList(file2Convert)#used for csv
        peakList.saveCSV(os.path.splitext(newPath)[0])#used for csv

        outFile = ' -o '+newPath
        self.cmdOut.append(outFile)

        cmdStr = ''
        for item in self.cmdOut:
            cmdStr += item
        cmdStr +='\n'
        try:

            subHandle = sub.Popen(cmdStr, bufsize = 0, shell = True,  stdout=sub.PIPE, stderr=sub.PIPE,  stdin = sub.PIPE)

            self.outMsg = subHandle.stdout.read()
            self.errMsg = subHandle.stderr.read()
            subHandle.stderr.close()
            subHandle.stdout.close()
            subHandle.stdin.close()
            self.retCode = subHandle.wait()

            if self.retCode != 0:
                self.outputTE.insertPlainText(QtCore.QString(cmdStr))
                msg = self.outMsg+'\n'+self.errMsg
                self.outputTE.insertPlainText(QtCore.QString(msg))
                self.outputTE.update()
            else:
                msg = self.outMsg+'\n'+self.errMsg
                self.outputTE.insertPlainText(QtCore.QString(msg))
                self.outputTE.update()
        except:
            print cmdStr
            raise
'''
