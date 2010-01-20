#!/usr/bin/python

import os
from os import walk, path, listdir
import uuid
from time import strftime, localtime
from binascii import hexlify
import time

import sys
from PyQt4 import QtGui, QtCore
from dbInterface import sqliteIO

#WATCHDB = 'watchList.db'
QUEUEDB = 'labqueue.db'
QUEUEDIR = '/workspace/DaQueue'
QUEUETABLE = 'queueTable'
WATCHTABLE = 'watchTable'
CONFIGEXTENSION = '.cfgXML'#, '.db']

#1SRef is a Bruker File Folder Structure that should be ignored
EXCLUDE = ['.svn', '.db', '.cfgXML']

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

TODO:

Modify database to catch when a file is deleted and adjust appropriately...
Optimize...currently there are too many call to the database which I don't like.

'''
STATUSIDS = [0,1,2,3,4]
STATUSTYPES = ['Queued', 'Processing', 'Finished', 'Failed', 'Waiting for User Action']

JOBKEYS = [0,1,2,3,4]
JOBTYPES = ['X!Tandem', 'File Conversion', 'Peak Picking', 'Polygraph', 'Unspecified']

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
        self.__setupDB__(useMemory = False)
        self.updateWatcher()
        self.pollWatcher()


    def pollWatcher(self):
        watcherDirs = self.watcher.directories()
        watcherFiles = self.watcher.files()
        for dir in watcherDirs:
            print str(dir)

        for f in watcherFiles:
            print str(f)

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
        jobID INTEGER)'
        '''
        if self.dbOK:
            '''
            Need to test if table exists
            '''
            #SELECT THE QUEUED FILES
            self.qDB.cur.execute(("SELECT * FROM %s WHERE %s LIKE '%s'"%(QUEUETABLE, 'statusID', str(STATUSIDS[0]))))
            self.queryResult = self.qDB.GET_CURRENT_QUERY_AS_DICT()#GET_CURRENT_QUERY()
            for row in self.queryResult:
                print row

    def dummyFunc(self):
        '''
        dummy function for QTimer Slot
        Useful as QTimer runs in a separate thread.
        '''
        print "\t DummyFunc Called"
        return True

    def checkStable(self, targetFile):
        '''
        Takes an input file and checks to see if it is stable
        i.e. not changing from a file transfer process.
        '''
        print "CheckStable Called"
        stable = False
        curSize = os.path.getsize(targetFile)
        time.sleep(1)
#        QtCore.QTimer.singleShot(2000, self.dummyFunc)
        nextSize = os.path.getsize(targetFile)
        #While Loop to check if the file is changing
        while (curSize != nextSize):
            curSize = os.path.getsize(targetFile)
            time.sleep(1)
#            QtCore.QTimer.singleShot(2000, self.dummyFunc)
            nextSize = os.path.getsize(targetFile)

        if curSize == nextSize:
            stable = True

        return stable

    def fileChanged(self, val):
        '''
        When a new file is added
        '''
        if self.ignoreSignal:
            return False
        else:
            print "File String", str(val)
            for dir in self.watcher.directories():
                print '\t',str(dir)

    def dirChanged(self, val):
        '''
        When a file is added or the directory is changed then this is called.


        print "Dir String", str(val)
        for dir in self.watcher.directories():
        print '\t',str(dir)
        print '\n'

        '''
        self.increment+=1
        print "dir Changed Called ",self.increment
        if self.ignoreSignal:
            return False
        else:

            self.updateDirs(self.startDir)
            self.updateFiles(self.startDir)
            self.updateDB()


    def updateDirs(self, startDir, firstRun = False, debug = False, exclude = EXCLUDE):
        '''
        update the watch dir list

        Do I need to exclude special character directories?
        How best to do this
        '''
        if startDir:
            numFiles = 0
            for root, dirs, files in walk(startDir):
                if firstRun:
                    if len(dirs) > 0:
                        for dir in dirs:
                            newDir = os.path.join(root,dir)
                            if '.svn' not in dir and '.svn' not in root:
                                print "updateDirs added %s"%newDir, os.path.isdir(newDir)
                                self.watcher.addPath(newDir)
                else:
                    for dir in dirs:
                        newDir = os.path.join(root,dir)
                        if QtCore.QString(newDir) not in self.watcher.directories():
                            if '.svn' not in dir and '.svn' not in root:
                                print "updateDirs added %s"%os.path.join(root,dir), os.path.isdir(os.path.join(root,dir))
                                self.watcher.addPath(os.path.join(root,dir))


    def checkConfigFile(self, dataPath):
        '''
        Test to see if config file exists...

        MUST HAVE THE ".cfgXML" EXTENSION!!!!!!!!!!!!!!!!!!!!!!!!
        '''
#        print "Checking Config File in %s\n"%dataPath
        configList = []

        if path.isdir(dataPath):
            for i in listdir(dataPath):
                if self.configExt in i:
                    configList.append(path.join(dataPath,i))

            return configList
        else:
            print "Not a valid directory to check for config files!!!!!!!!!!"
            return configList


    def updateFiles(self, startDir, firstRun = False, debug = False, exclude = EXCLUDE):
        '''
        self.configFiles = []
        self.queuedFiles = []
        self.finishedFiles = []
        self.outputFiles = []
        self.failedFiles = []
        self.fileStatus = []
        self.statusIDs = []
        self.jobIDs = []
        self.uuIDs = []

        I know this is not as efficient as it could be but I'm looking
        for a solution NOW

        STATUSIDS = [0,1,2,3,4]
        STATUSTYPES = ['Queued', 'Processing', 'Finished', 'Failed', 'Waiting for User Action']

        JOBKEYS = [0, 1, 2, 3, 4]
        JOBTYPES = ['X!Tandem', 'File Conversion', 'Peak Picking', 'Polygraph', 'Unspecified']
        '''
        self.__resetLists__()
        if startDir:
            numFiles = 0
            for root, dirs, files in walk(startDir):
                for basename in dirs + files:
                    if basename in exclude:
                        if basename in dirs:
                            dirs.remove(basename)
                        continue

                    excluded = False
                    for ignoreStr in EXCLUDE:
                        if ignoreStr in basename:
                            excluded = True


                    workingPath = os.path.join(root, basename)
                    if not excluded:#CONFIGEXTENSION not in workingPath:#don't add config files to queue
#                        print "Basename", basename, workingPath
                        configList = self.checkConfigFile(root)
                        if len(configList)>0:
                            if self.checkStable(workingPath):
                                for cfgFile in configList:
                                    boolAns, tempUUID = generateUUID(path.abspath(workingPath), cfgFile)
                                    if boolAns:
                                         if tempUUID not in self.uuIDs:
                                            self.uuIDs.append(tempUUID)
                                            self.configFiles.append(cfgFile)
                                            self.queuedFiles.append(path.abspath(workingPath))
                                            self.fileStatus.append(STATUSTYPES[0])
                                            self.statusIDs.append(STATUSIDS[0])
                                            #need to add a function to discern what kind of job is to be run
                                            #hard-coding to XTandem initially
                                            self.outputFiles.append('None at this Time')
                                            self.jobIDs.append(JOBKEYS[0])
                                            self.timeIDs.append(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
                #                            self.jobIDs.append(STATUSIDS[0])
    #                                else:
    #                                    self.uuIDs.append('UUID Error')
    #                        else:
    #                            '''
    #                            I don't like this.  Need to catch the case where the file has been
    #                            added WIHTOUT a config file and then overwrite the entry when a config file
    #                            is added.  Or don't add that file to begin with?
    #                            '''
    #                            print "No Configuration Files"
    #                            boolAns, tempUUID = generateStrUUID(path.abspath(f))
    #                            if boolAns:
    #                                if tempUUID not in self.uuIDs:
    #                                    self.configFiles.append('Not Specified')
    #                                    self.queuedFiles.append(path.abspath(f))
    #                                    self.fileStatus.append(STATUSTYPES[4])
    #                                    self.statusIDs.append(STATUSIDS[4])
    #                                    self.jobIDs.append(JOBKEYS[4])
    #                                    self.uuIDs.append(tempUUID)


    def updateWatcher(self, useDefault = True):
        if useDefault:
            self.watcher.addPath(self.startDir)
        else:
            newDir = self.__getDataFolder__()
            if newDir != None:
                self.watcher.addPath(newDir)
        self.updateDirs(self.startDir, firstRun = True)
        self.updateFiles(self.startDir, firstRun = True)
        self.updateDB()

    def updateDB(self):
        '''
        Need to check for unique ids
        need to check for unique keys
        '''
        self.ignoreSignal = True
        qDict = queueDict()
        qDict.popluateDict(self.configFiles, self.queuedFiles, self.outputFiles,
                           self.fileStatus, self.statusIDs, self.jobIDs, self.uuIDs, self.timeIDs)
        self.qDB.INSERT_QUEUE_VALUES(QUEUETABLE, qDict.dataDict)
#        time.sleep(5)
        self.ignoreSignal = False
        self.pollDB()

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
#            print self.startDir, self.qDBName, type(self.startDir), type(self.qDBName)
#            print path.join(self.startDir, self.qDBName)
            dbName = path.join(self.queueDir, self.qDBName) #Defined Globally in self.__setupVars__()
            print "DB Name:", dbName

        if dbName != None:
            '''
            Explicit creation of tables is not necessary as when the tables are updated
            if they do not exist they are created
            '''
            self.qDB = sqliteIO.queueDB(dbName, parent = self)
            self.dbOK = True
#            self.qDB.CREATE_QUEUE_TABLE(self.qTableName)
#            self.qDB.CREATE_WATCH_TABLE(self.qWatchName)
        else:
            errorMsg = 'There was an error establishing a connection to the data base.  Contact Clowers'
            return QtGui.QMessageBox.warning(self, "DB Error",  errorMsg)


    def __resetLists__(self):
        self.configFiles = []
        self.queuedFiles = []
        self.finishedFiles = []
        self.outputFiles = []
        self.failedFiles = []
        self.fileStatus = []
        self.statusIDs = []
        self.jobIDs = []
        self.uuIDs = []
        self.timeIDs = []

    def __setupVars__(self):

        self.ignoreSignal = False #used to block directory changes and signal registers

        self.increment = 0

        self.__setMessages__()
        self.startDir = getHomeDir()
        ##################
        self.startDir +='/workspace/DaQueue/testData'
        self.queueDir = getHomeDir()+QUEUEDIR
        ##################

        self.startDir = path.abspath(self.startDir)
#        print self.startDir, path.isdir(self.startDir)

        self.configFiles = []
        self.queuedFiles = []
        self.finishedFiles = []
        self.outputFiles = []
        self.failedFiles = []
        self.fileStatus = []
        self.statusIDs = []
        self.jobIDs = []
        self.uuIDs = []
        self.timeIDs = []

#        self.watchDBName = WATCHDB
        self.qDBName = QUEUEDB
        self.qDB = None
        self.dbOK = False
        self.numQueuedFiles = 0

        self.qTableName = QUEUETABLE
        self.qWatchName = WATCHTABLE

        self.watchedFiles = []
        self.watchedFolders = []

        self.configExt = CONFIGEXTENSION

        self.watcher = QtCore.QFileSystemWatcher()

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
        '''

        '''
        self.dataDict = {'cfgFiles':[],
                         'dataFiles':[],
                         'outputFiles':[],
                         'statuses':[],
                         'statusIDs':[],
                         'jobIDs':[],
                         'uuIDs':[],
                         'timeIDs':[]}

    def popluateDict(self, configFileList, dataFileList, outputFileList, statusList, statusIDList, jobIDList, uuIDList, timeIDList):
        '''

        '''
        self.dataDict['cfgFiles'] = configFileList
        self.dataDict['dataFiles'] = dataFileList
        self.dataDict['outputFiles'] = outputFileList
        self.dataDict['statuses'] = statusList
        self.dataDict['statusIDs'] = statusIDList
        self.dataDict['jobIDs'] = jobIDList
        self.dataDict['uuIDs'] = uuIDList
        self.dataDict['timeIDs'] = timeIDList


def generateStrUUID(definerStr):
    if type(definerStr) is str:
        if len(definerStr)>=0:
            hexStr = hexlify(definerStr)
            uuID = str(uuid.uuid5(uuid.NAMESPACE_DNS, hexStr))
            return True, uuID
        else:
            return False, None
    else:
        return False, None

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
        print dataPathStr, configPathStr, '\n'
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
