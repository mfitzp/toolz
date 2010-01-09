#!/usr/bin/python

# gridlayout2.py

from os import walk, path
import uuid

import sys
from PyQt4 import QtGui, QtCore
from dbInterface import sqliteIO


class GridLayout(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setWindowTitle('grid layout')

        title = QtGui.QLabel('Title')
        author = QtGui.QLabel('Author')
        review = QtGui.QLabel('Review')

        titleEdit = QtGui.QLineEdit()
        authorEdit = QtGui.QLineEdit()
        reviewEdit = QtGui.QTextEdit()

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)

        self.setLayout(grid)
        self.resize(350, 300)

        self.__setupVars__()
        self.__setupDB__(useMemory = True)
        self.updateWatcher()


#    def fileChanged(self, val):
#        print "File String", str(val)
#        for dir in self.watcher.directories():
#            print '\t',str(dir)

    def dirChanged(self, val):
        print "Dir String", str(val)
        for dir in self.watcher.directories():
            print '\t',str(dir)
        print '\n'

        self.updateDirs(self.startDir)
        self.updateFiles(self.startDir)
#        for f in self.watcher.files():
#            print '\t\t',str(f)

    def updateDirs(self, startDir, firstRun = False, debug = False):
        '''update the watch dir list'''
        if startDir:
            numFiles = 0
            for root, dirs, files in walk(startDir):
                if firstRun:
                    if len(dirs) > 0:
                        for dir in dirs:
                            self.watcher.addPath(dir)
                else:
                    for dir in dirs:
                        if QtCore.QString(dir) not in self.watcher.directories():
                            self.watcher.addPath(dir)

    def checkConfigFile(self):
        '''
        Test to see if config file exists...
        '''

    def updateFiles(self, startDir, firstRun = False, debug = False):
        '''
        dataFile TEXT,\
        cfgFile TEXT,\
        outputFile TEXT,\
        status TEXT,\
        statusID INTEGER,\
        jobID INTEGER,\
        uuID INTEGER)'


        self.queuedFiles = []
        self.finishedFiles = []
        self.failedFiles = []
        self.fileStatus = []
        self.statusIDs = []
        self.jobIDs = []
        self.uuIDs = []

        '''
        if startDir:
            numFiles = 0
            for root, dirs, files in walk(startDir):
                for f in files:

                    self.queuedFiles.append(path.abspath(f))

    def updateWatcher(self, useDefault = True):
        if useDefault:
            self.watcher.addPath(self.startDir)
        else:
            newDir = self.__getDataFolder__()
            if newDir != None:
                self.watcher.addPath(newDir)
        self.updateDirs(self.startDir, firstRun = True)
        self.updateFiles(self.startDir, firstRun = True)

    def __setupDB__(self, useMemory = True):
        '''
        Initialize DB
        '''
        if useMemory:
            dbName=':memory:'
        else:
            dbName = self.__saveDataFile__()

        if dbName != None:
            self.qDB = queueDB(dbName)
            qTableName = 'queueTable'
            self.qDB.CREATE_QUEUE_TABLE(qTableName)
        else:
            errorMsg = 'There was an error establishing a connection to the data base.  Contact Clowers'
            return QtGui.QMessageBox.warning(self, "DB Error",  errorMsg)


    def __setupVars__(self):

        self.__setMessages__()
        self.startDir = getHomeDir()

        self.queuedFiles = []
        self.finishedFiles = []
        self.failedFiles = []
        self.fileStatus = []
        self.statusIDs = []
        self.jobIDs = []
        self.uuIDs = []

        self.statusID = [0,1,2,3]
        self.statusType = ['Queued', 'Processing', 'Finished', 'Failed']

        self.jobKey = [0, 1, 2, 3]
        self.jobTypes = ['X!Tandem', 'File Conversion', 'Peak Picking', 'Polygraph']


        self.watcher = QtCore.QFileSystemWatcher(self)

#        QtCore.QObject.connect(self.watcher,QtCore.SIGNAL("fileChanged(const QString&)"), self.fileChanged)
        QtCore.QObject.connect(self.watcher,QtCore.SIGNAL("directoryChanged(const QString&)"), self.dirChanged)


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

    def __saveDataFile__(self):
#        return QtGui.QMessageBox.information(self,'', "This feature is not implemented yet.  Use a database outside of memory")
        saveFileName = QtGui.QFileDialog.getSaveFileName(self,\
                                                             self.SaveDataText,\
                                                             self.startDir, 'SQLite Database (*.db);;HDF5 File (*.h5)')
    def __getDataFile__(self):
        dataFileName = QtGui.QFileDialog.getOpenFileName(self,\
                                                         self.OpenDataText,\
                                                         self.startDir, '*.* (*.*);;X!Tandem XML (*.xml);;SQLite Database (*.db)')
        if dataFileName:
            self.startDir = getCurDir(dataFileName)
            return str(dataFileName)
        else:
            return None

    def __getDataFolder__(self):
        directory= QtGui.QFileDialog.getExistingDirectory(self, "Select Folder", self.startDir)
        if os.path.isdir(str(directory)):
            self.startDir = str(directory)
            print self.startDir, str(directory)
            return str(directory)
        else:
            return None


class queueDict(object):
    def __init__(self):
        self.dataDict = {'cfgFiles':[],
                         'dataFiles':[],
                         'outputFiles':[],
                         'statuses':[],
                         'statusIDs':[],
                         'jobIDs':[],
                         'uuIDs':[]}


    def popluateDict(self, configFileList, dataFileList, outputFileList, statsList, statusIDList, jobIDList, uuIDList):
            self.dataDict['cfgFiles'] = configFileList
            self.dataDict['dataFiles'] = dataFileList
            self.dataDict['outputFiles'] = outputFileList
            self.dataDict['statuses'] = statsList
            self.dataDict['statusIDs'] = statusIDList
            self.dataDict['jobIDs'] = jobIDList
            self.dataDict['uuIDs'] = uuIDList

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


def run_main():
    app = QtGui.QApplication(sys.argv)
    qb = GridLayout()
    qb.show()
    sys.exit(app.exec_())


'''
class MyOutput():
    def __init__(self, logfile):
        self.stdout = sys.stdout
        self.log = open(logfile, 'w')

    def write(self, text):
        self.stdout.write(text)
        self.log.write(text)
        self.log.flush()

    def close(self):
        self.stdout.close()
        self.log.close()

sys.stdout = MyOutput("log.txt")
print "blah blah blah"
'''

if __name__ == "__main__":
    run_main()
