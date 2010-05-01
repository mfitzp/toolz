#!/usr/bin/python

import os, sys, traceback
from PyQt4 import QtGui, QtCore
import time

'''
The Question:
Do we kill the process and respawn a new one or keep regenerating...
I vote for kill and respawn

'''


class XTandem:
    def __init__(self, exePath = "", taxPath = "", 
                 defaultPath = "", inputPath = ""):
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

        #need to adjust the modified input file so that the correct
        #data files and output files are used
        '''
        def modXML(fileName, inputFile, outputPath):

            modifies a standard x!tandem input file to utilize a different input and output path
            inputFile = Raw Data File
            outputPath = Output Path File Name
            returns Success and XT input file path
            
        '''
        
        self.setupOk = False
        self.exePath = exePath
        self.taxPath = taxPath
        self.defaultPath = defaultPath
        self.inputPath = inputPath
        self.rtnCode = 99
        self.outputStr = ''
        self.qj = None #queuejob
        self.sanityCheck()
        
    def setExePath(self, exePath):
        if os.path.isfile(exePath):
            self.exePath = exePath
            self.defaultPath = os.path.dirname(exePath)
            self.sanityCheck()
    
    def setTaxPath(self, taxPath):
        if os.path.isfile(taxPath):
            self.taxPath = taxPath
            self.sanityCheck()
               
    def setInputPath(self, inputPath):
        if os.path.isfile(inputPath):
            self.inputPath = inputPath  
            self.sanityCheck()             
               
    def sanityCheck(self):
        self.setupOk = True
        if not os.path.isfile(self.exePath):
            print "X!Tandem Executable not defined"
            self.setupOk = False
        if not os.path.isfile(self.taxPath):
            print "X!Tandem taxonomy file not defined"
            self.setupOk = False
        if not os.path.isfile(self.inputPath):
            print "X!Tandem input file not defined"
            self.setupOk = False
            
    def start(self):
        if self.setupOk:
            self.qj = QUEUEJOB(self.exePath, self.inputPath, self.defaultPath)
            self.qj.run()
        else:
            print "Setup Failed, check file paths"
            print self.exePath
            print self.inputPath
            print self.taxPath
    
    def killProcess(self):
        if self.qj != None:
            self.qj.stopProcess()
            self.qj.finished(-1)

class QUEUEJOB(QtCore.QObject):
    def __init__(self, execCmd = "", optionStr = "", execPath = None, parent = None):
        QtCore.QObject.__init__(self, parent)
        self.process = QtCore.QProcess(self)
        self.setExecPath(execPath)
        self.optionStr = optionStr
        self.execCmd = execCmd
        self.outStr = None
        self.returnStr = None
        self.startTime = None
        self.stopTime = None        
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
        #print "StandardOutput\n\t"
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
        #sublist = self.processList[0]
        #del self.processList[0]
        #print(sublist)
        #self.process.start(sublist[0], sublist[1])

if __name__ == "__main__":
    testQueue = False
    if testQueue:
        jq = QUEUEJOB()
        #jq.setExecCmd('CompassXPort')
        if os.sys.platform == 'linux2':
            jq.setExecCmd('ls')
            jq.setOptionStr('-l')
        elif os.sys.platform == 'win32':
            #jq.setExecPath('C:\\Documents and Settings\\d3p483\\My Documents\\Python\\DaQueue')
            #jq.setExecCmd('ReAdW.exe')
            execPath = "C:\\BUGS\\tornado\\thegpm\\thegpm-cgi\\tandem.exe"
            jq.setExecPath(os.path.dirname(execPath))
            jq.setExecCmd(os.path.basename(execPath))
            jq.setOptionStr("C:\\BUGS\\tornado\\thegpm\\tandem\\test.xml")
            #"C:\\BUGS\\tornado\\thegpm\\tandem\\taxonomy.xml"
            #"C:\\BUGS\\tornado\\test_spectra\\chicken\\gt1.tmp"
        jq.run()
        jq.process.waitForFinished()
    
        print jq.startTime
        print jq.stopTime
    else:
        xtJob = XTandem()
        xtJob.setExePath("C:\\BUGS\\tornado\\thegpm\\thegpm-cgi\\tandem.exe")
        xtJob.setInputPath("C:\\BUGS\\tornado\\thegpm\\tandem\\test.xml")
        xtJob.setTaxPath("C:\\BUGS\\tornado\\thegpm\\tandem\\taxonomy.xml")
        xtJob.start()
        xtJob.qj.process.waitForFinished(4000)
        
        
