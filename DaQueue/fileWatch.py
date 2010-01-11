#!/usr/bin/python

# gridlayout2.py

from os import walk, path, listdir
import uuid
from time import strftime, localtime
from binascii import hexlify

import sys
from PyQt4 import QtGui, QtCore
from dbInterface import sqliteIO

#WATCHDB = 'watchList.db'
QUEUEDB = 'labqueue.db'
QUEUETABLE = 'queueTable'
WATCHTABLE = 'watchTable'
CONFIGEXTENSION = '.cfgXML'

'''
This module is designed to add rows to a sqlite database when a watch directory is altered.
The sqlite db will then be polled by another threaded module to process the file
as directed by the configuration file.

The configuration files to be used now and in the future need to be xml files.
Currently this process is designed for X!Tandem (a proteomics data analysis package).

At present there are two actions that are ignored in the file structure.
One is the creation of results files and the other is modification or creation
of a log file.

By adding a new configuration file to the raw data folder the files will be processed again.

Config Files can have any primary name, however, the file extension must have
the cfgXML extension.

'''
STATUSIDS = [0,1,2,3]
STATUSTYPES = ['Queued', 'Processing', 'Finished', 'Failed']

JOBKEYS = [0, 1, 2, 3]
JOBTYPES = ['X!Tandem', 'File Conversion', 'Peak Picking', 'Polygraph']

class FileWatcher(QtGui.QWidget):
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


    def fileChanged(self, val):
        '''
        When a new file is added
        '''
        print "File String", str(val)
        for dir in self.watcher.directories():
            print '\t',str(dir)

    def dirChanged(self, val):
        '''
        When a file is added or the directory is changed then this is called.
        '''
        print "Dir String", str(val)
        for dir in self.watcher.directories():
            print '\t',str(dir)
        print '\n'

        self.updateDirs(self.startDir)
        #test to see if configuration file exists in the same directory

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


    def checkConfigFile(self, dataPath):
        '''
        Test to see if config file exists...

        MUST HAVE THE ".cfgXML" EXTENSION!!!!!!!!!!!!!!!!!!!!!!!!
        '''

        configList = []

        if path.isdir(dataPath):
            for i in listdir(dataPath):
                if CONFIGEXTENSION in i:
                    configList.append(path.abspath(i))

            return configList



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

    def __setupDB__(self, useMemory = True, newDB = False):
        '''
        Initialize DB
        The following methods from the sqlitIO.py module will create a table if one
        does not exist.  Otherwise the values will be added to the existing tables.

        INSERT_WATCH_VALUES
        INSERT_QUEUE_VALUES

        '''
        if useMemory:
            dbName =':memory:'
        elif newDB:
            dbName = self.__saveDataFile__()
        else:
            dbName = self.qDBName

        if dbName != None:
            self.qDB = queueDB(dbName)
#            self.qDB.CREATE_QUEUE_TABLE(self.qTableName)
#            self.qDB.CREATE_WATCH_TABLE(self.qWatchName)
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

#        self.watchDBName = WATCHDB
        self.qDBName = QUEUEDB

        self.qTableName = QUEUETABLE
        self.qWatchName = WATCHTABLE

        self.watchedFiles = []
        self.watchedFolders = []

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

def generateUUID(dataPathStr, configPathStr):
    '''
    Returns a uuid that is a combination of a datapath and a configuration file string
    The other marker is the time at which the configuration file was made
    '''
    if path.isfile(dataPathStr) and path.isfile(configPathStr):
            definerStr = ''
            startTime = str(path.getctime(configPathStr))
            definerStr+=dataPathStr
            definerStr+=configPathStr
            definerStr+=startTime
            hexStr = hexlify(definerStr)
            uuID = str(uuid.uuid5(uuid.NAMESPACE_DNS, hexStr))
            return True, uuID
    else:
        print "File paths provided are not valid"
        return False, None

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
    fw = FileWatcher()
    fw.show()
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
#    testStr = '/home/clowers/Sandbox/text.xml'
#    print generateUUID(testStr, testStr)
    run_main()
