#!/usr/bin/python

import os, sys, traceback
from PyQt4 import QtGui, QtCore
import time

'''
The Question:
Do we kill the process and respawn a new one or keep regenerating...
I vote for kill and respawn

'''
class QUEUEJOB(QtCore.QObject):
    def __init__(self, execCmd = "", optionStr = "", execPath = None, parent = None):
        QtCore.QObject.__init__(self, parent)
        self.execPath = execPath
        self.optionStr = optionStr
        self.execCmd = execCmd
        self.outStr = None
        self.returnStr = None
        self.startTime = None
        self.stopTime = None
        self.process = QtCore.QProcess(self)
        #self.__resetConnections__()

    def run(self):
        self.__resetConnections__()

    def setExecCmd(self, execCmd):
        self.execCmd = ""
        if type(execCmd) == str:
            if len(execCmd)>0:
                self.execCmd = execCmd

    def setExecPath(self, execPath):
        self.execPath = os.getcwd()
        if type(execPath) == str:
            if len(execPath)>0:
                if os.path.isdir(execPath):
                    self.execPath = execPath
                    self.process.setWorkingDirectory(self.execPath)

    def setOptionStr(self, optionStr):
        self.optionStr = ""
        if type(optionStr) == str:
            if len(optionStr) >0:
                self.optionStr = optionStr
            else:
                print "Option Str is Empty"

    def __resetConnections__(self):
        if self.execCmd != None:
            if len(self.execCmd)>0:
                QtCore.QObject.connect(self.process, QtCore.SIGNAL("finished(int)"), self.finished)
                QtCore.QObject.connect(self.process, QtCore.SIGNAL("readyReadStandardOutput()"), self.OnProcessOutputReady)
                QtCore.QObject.connect(self.process, QtCore.SIGNAL("readyReadStandardError()"), self.OnProcessOutputError)
                QtCore.QObject.connect(self.process, QtCore.SIGNAL("error(QProcess::ProcessError)"), self.processError)


                self.processList = []
                self.execCmd = " ".join([self.execCmd, self.optionStr])
                self.processList.append(self.execCmd)

                sublist = self.processList[0]
                del self.processList[0]
                print(sublist)
                if len(sublist) > 1:
                    #print "GO"
                    self.startTime = time.ctime()
                    self.process.start(sublist)

#                elif len(sublist) == 1:
#                    self.startTime = time.ctime()
#                    self.process.start(sublist[0])
            else:
                print "Empty execution string"
        else:
            print "Exectable path is not defined"

    def processRead(self):
        errMsg = self.process.readAllStandardOutput().data()
        #print len(errMsg), str(errMsg)
        errMsg = self.process.readAllStandardError().data()
        #print len(errMsg), str(errMsg)

    def stopProcess(self):
        if self.process:
            self.disconnect(self.process, QtCore.SIGNAL('error(QProcess::ProcessError)'), self.processError)
            self.disconnect(self.process, QtCore.SIGNAL('finished(int)'), self.finished)
            self.disconnect(self.process, QtCore.SIGNAL("finished(int)"), self.finished)
            self.disconnect(self.process, QtCore.SIGNAL("readyReadStandardOutput()"), self.OnProcessOutputReady)
            self.disconnect(self.process, QtCore.SIGNAL("readyReadStandardError()"), self.OnProcessOutputError)

            if self.process.state() != QtCore.QProcess.NotRunning:
                self.process.terminate()
                if not self.process.waitForFinished(5000):
                    self.process.kill()
            self.process = None
            self.stopTime = time.ctime()

    def processError(self, error):
        if error == QtCore.QProcess.FailedToStart:
            print "Process failed to start: %s" % self.process.errorString()
        elif error == QtCore.QProcess.Crashed:
            print "Process crashed with exit code %s." % self.process.exitCode()
        else:
            print "Process failed with error %s." % error

        self.processRead()
        #codec = QTextCodec.codecForName("UTF-8")
        #errMsg = self.process.readAllStandardError()
#        print len(errMsg), errMsg
        #self.txt.setText(self.txt.toPlainText() + codec.toUnicode(self.process.readAllStandardError().data()))

        self.stopProcess()

    def OnProcessOutputError(self):
        print "OutputError\n\t"
        codec = QtCore.QTextCodec.codecForName("UTF-8")
        self.returnStr = self.process.readAllStandardError().data()
        print self.returnStr
        #self.txt.setText(self.txt.toPlainText() + codec.toUnicode(self.process.readAllStandardError().data()))
        #self.processRead()

    def OnProcessOutputReady(self):
        print "StandardOutput\n\t"
        codec = QtCore.QTextCodec.codecForName("UTF-8")
        self.returnStr = self.process.readAllStandardOutput().data()
        print self.returnStr
        #self.txt.setText(self.txt.toPlainText() + codec.toUnicode(self.process.readAllStandardOutput().data()))
        #self.processRead()

    def finished(self, rv):
        print "Return Code: ",rv
        #self.processRead()

        #errMsg = self.process.readAllStandardOutput().data()
#        encoding = sys.getfilesystemencoding() or 'utf-8'
#        errMsg = str(self.process.readAllStandardOutput()).decode(encoding, 'replace')

        #print len(errMsg), errMsg
        if (len(self.processList) == 0):
            self.process = None
            self.stopTime = time.ctime()
            return
        sublist = self.processList[0]
        del self.processList[0]
        print(sublist)
        self.process.start(sublist[0], sublist[1])

if __name__ == "__main__":

    jq = QUEUEJOB()
    #jq.setExecCmd('CompassXPort')
    if os.sys.platform == 'linux2':
        jq.setExecCmd('ls')
        jq.setOptionStr('-l')
    elif os.sys.platform == 'win32':
        jq.setExecPath('C:\\Documents and Settings\\d3p483\\My Documents\\Python\\DaQueue')
        jq.setExecCmd('ReAdW.exe')
    jq.run()
    jq.process.waitForFinished()

    print jq.startTime
    print jq.stopTime
