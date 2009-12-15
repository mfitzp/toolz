from PyQt4 import QtCore, QtGui
import os, os.path
import sys
from string import join
import subprocess as sub

import time
from dbInterface import dbIO


class RAWConvert(ui_main.Ui_MainWindow):
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        ui_main.Ui_MainWindow.setupUi(self,MainWindow)

        self.__setup__()
        self.__makeConnections__()

    def __setup__(self):
        self.RAWDataOk = False
        self.RAWData = None

        self.outputFileOk = False
        self.outputFile = None

        self.outputTE.clear()

        self._curDir_ = os.getcwd()

        self.retCode = None
        self.err = False
        self.errMsg = None
        self.outMsg = None

        self.useSingleFile = False

        self.loadThread = LoadThread(self)

        self.iterScroll = 0
        #self.filePathError()

    def __updateGUI__(self):
        if self.RAWDataOk and self.RAWData != None:
            self.RAWFolderLE.setText(self.RAWData)



        if self.outputFileOk and self.outputFile != None:
            self.outputFileLE.setText(self.outputFile)

        #need to reset command sequence
        self.cmdOut = ['ReAdW']


    def __makeConnections__(self):
        QtCore.QObject.connect(self.actionClose,QtCore.SIGNAL("clicked()"),self.__mainClose__)
        QtCore.QObject.connect(self.selRAWDataBtn,QtCore.SIGNAL("clicked()"),self.__getRAWData__)
        QtCore.QObject.connect(self.outputBtn,QtCore.SIGNAL("clicked()"),self.__setOutputFile__)
        QtCore.QObject.connect(self.cnvrtRAWBtn,QtCore.SIGNAL("clicked()"),self.__convertRAW__)
        QtCore.QObject.connect(self.actionConvert2XML,QtCore.SIGNAL("triggered()"),self.__convertRAW__)
        QtCore.QObject.connect(self.singleFileCB, QtCore.SIGNAL("stateChanged (int)"),self.__changeInputFile__)
        QtCore.QObject.connect(self.RAWFolderLE, QtCore.SIGNAL("editingFinished()"),self.__RAWLEChanged__)
        QtCore.QObject.connect(self.outputFileLE, QtCore.SIGNAL("editingFinished()"),self.__outputLEChanged__)
        QtCore.QObject.connect(self.action_About,QtCore.SIGNAL("triggered()"),self.__showAbout__)
        QtCore.QObject.connect(self.loadThread, QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"), self.updateOutputMsg)

    def __RAWLEChanged__(self):
        self.RAWDataOk = True
        self.RAWData = self.RAWFolderLE.text()

    def __outputLEChanged__(self):
        self.outputFileOk = True
        self.outputFile = self.outputFileLE.text()

    def __changeInputFile__(self, state):
        if state == 2:
            self.useSingleFile = True
        else:
            self.useSingleFile = False
        self.outputFileLE.clear()
        self.outputFileOk = False
        self.RAWFolderLE.clear()
        self.RAWDataOk = False


    def updateOutputMsg(self, outputStr):
        self.iterScroll+=1
        self.outputTE.insertPlainText(QtCore.QString(outputStr))
        scrollBar = self.outputTE.verticalScrollBar();
        scrollBar.setValue(scrollBar.maximum())

    def __convertRAW__(self):
        if self.RAWDataOk:
            self.outputTE.clear()
            if self.useSingleFile == False:
                fileList = getRAWFiles(str(self.RAWData))
                if self.loadThread.updateThread(fileList):
                    self.loadThread.start()

            else:
                newFile = None
                if self.outputFileOk:
                    newFile =str(self.outputFile)
                else:
                    datadir = os.path.abspath(str(self.RAWData))
                    coreName = os.path.basename(datadir).split('.')[:-1][0]
                    newFile = coreName
#                    print "New File name: ", newFile, str(self.RAWData)
                curFile = os.path.abspath(str(self.RAWData))
                if self.loadThread.updateThread([(curFile, newFile)]):
                    self.loadThread.start()

#                self.updateOutputMsg(self.loadThread.exeRAW(str(self.RAWData), newFile))
        else:
            reply = QtGui.QMessageBox.warning(self.MainWindow, "No Input File Set",  "An input file must be selected before continuing.")
            self.__getRAWData__()
#            exec_str = '-multi '+str(self.RAWData)
#            self.cmdOut.append(exec_str)
#            file_str = ' -multiName '+'RAWConvert.1231.test.mzXML'
#            self.cmdOut.append(file_str)

    def __getRAWData__(self):
        if self.RAWDataOk:
            try:
                if self.useSingleFile:
                    self.dir = os.path.dirname(str(self.RAWData))
                else:
                    self.dir = str(self.RAWData)
            except:
                print "Directory split didn't work"
                self.dir = self._curDir_
        else:
            self.dir = self._curDir_
        if self.RAWDataOk and self.RAWData != None:
            if self.useSingleFile:
                self.dir = os.path.dirname(str(self.RAWData))
            else:
                self.dir = self.RAWData

        if self.useSingleFile:
            data = QtGui.QFileDialog.getOpenFileName(self.MainWindow,\
                                'Select RAW Data File',\
                                self.dir, 'Thermo RAW File (*.RAW)')
        else:
            data= QtGui.QFileDialog.getExistingDirectory(self.MainWindow,\
                                                             "Select RAW Data Folder")
        if data:
            if ' ' in data:
                self.filePathError()
            else:
                self.RAWDataOk = True
                self.RAWData = data
                self.__updateGUI__()



    def __setOutputFile__(self):
        if self.RAWDataOk and self.RAWData != None:
            if self.useSingleFile:
                outputFile = QtGui.QFileDialog.getSaveFileName(self.MainWindow,\
                            'Select Output File Name',\
                            self.dir, 'mzXML (*.mzXML);;mzML (*.mzML)')

                if outputFile:
                    if ' ' in outputFile:
                        self.filePathError()
                    else:
                        self.outputFileOk = True
                        self.outputFile = outputFile
                        self.__updateGUI__()
            else:
                outFolder= QtGui.QFileDialog.getExistingDirectory(self.MainWindow,\
                                                             "Select Output Folder")
                if outFolder:
                    if ' ' in outFolder:
                        self.filePathError()
                    else:
                        self.outputFileOk = True
                        self.outputFile = outFolder
                        self.__updateGUI__()
        else:
            reply = QtGui.QMessageBox.warning(self.MainWindow, "No Input File Set",  "An input file must be selected before continuing.")
            self.__getRAWData__()


    def filePathError(self):
        reply = QtGui.QMessageBox.warning(self.MainWindow, "File Naming Warning",  "This conversion utility requires the file path names to not have any spaces or special characters.  You've been warned!")

    def __showAbout__(self):
        return QtGui.QMessageBox.information(self.MainWindow,
                                            ("RAW2mzXML V.0.9, December, 2008"),
                                            ("<p><b>RAW2mzXML</b> was written in Python by Brian H. Clowers (bhclowers@gmail.com).</p>"
        "<p>Please keep in mind that the entire effort is very much a"
        " work in progress and that Brian won't quit his day job for programming."
        " The original purpose of RAW2mzXML was to provide a user-friendly interface to the"
        " ReAdW conversion tool (which must be installed for this program to work)."
        " At this time concatenation of the output files is not possible, though certainly "
        " feasible.  If you'd like the source code please let me know.  Please feel free to make "
        " modifications (preferably with documentation) and share your contributions with the "
        " rest of the community.</p>"))


    def __mainClose__(self):
        self.MainWindow.close()
############################


class runThread(QtCore.QThread):
        def __init__(self, parent):
            QtCore.QThread.__init__(self, None)#parent)
            '''
            Valid Process Types:
            XTandem
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

        def updateThread(self, inputDict):
            self.inputFile = inputDict['Input File']
            self.outputFile = inputDict['Output File']
            self.paramFile = inputDict['Param File']
            self.processType = inputDict['Process Type']
            self.execPath = inputDict['Executable Path']
            self.curInputDict = inputDict
            if os.path.isfile(self.execPath) and os.path.isfile(self.paramFile) and os.path.isfile(self.inputFile):
                self.ready = True
                return True
            else:
                self.ready = False
                return False

        def run(self):
            if self.ready:
                if self.processType == 'XTandem':
                    self.exeTandem()

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
                    self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),msg)
#                    self.__del__()
#                    return msg
                else:
                    msg = self.outMsg+'\n'+self.errMsg
                    msg += runTime
                    #print msg
                    self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),msg)
#                    self.__del__()
#                    return msg
            except:
                print "Error Log Start:\n",cmdStr
                raise



        def exeRAW(self, file2Convert,  newFileName = None):
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
                if filetype == 'None' and self.useSingleFile == False:
                    newFileName+='.mzXML'
                    newPath = os.path.join(str(self.RAWData), newFileName)

                elif filetype == 'None' and self.useSingleFile == True:
                    newFileName += '.mzXML'
                    coreDir = os.path.split(str(self.RAWData))[:-1][0]
                    newPath = os.path.join(coreDir, newFileName)
#                    print newPath

                else:
                    newPath=str(self.outputFile)

            else:
                erMsg = "No output file specified"
                print erMsg
                raise erMsg
#                bName = os.path.basename(file2Convert)
#                coreName = bName.split('.')[:-1][0]
#                newPath=coreName+'.mzXML '
#                self.dir = os.path.dirname(str(self.RAWData))

            newPath = os.path.abspath(newPath)
            outFile = newPath
            self.cmdOut.append(outFile)

            cmdStr = ' '
            for item in self.cmdOut:
                cmdStr += item
            cmdStr +='\n'
            print cmdStr
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
                    fileupdate = '%d of %d Finished\n'%(self.curFileNum+1, self.totalFiles)
                    msg +=fileupdate
                    msg += runTime
                    return msg
                else:
                    msg = self.outMsg+'\n'+self.errMsg
                    fileupdate = '%d of %d Finished\n'%(self.curFileNum+1, self.totalFiles)
                    msg +=fileupdate
                    msg += runTime
                    return msg
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


if __name__ == "__main__":
    run_main()


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
