from PyQt4 import QtCore, QtGui
import os, os.path
import sys
from string import join
import subprocess as sub

import time

import ui_main

from BrukerFolderParse import getBrukerFiles
from PeakFolderParse import getPeakFiles, convert2mgf
from PeakExtract import brukerPeakList
from mzXML_reader import mzXMLDoc as MzR



class BrukerConvert(ui_main.Ui_MainWindow):
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        ui_main.Ui_MainWindow.setupUi(self,MainWindow)

        self.__setup__()
        self.__makeConnections__()

    def __setup__(self):
        self.fileDataOk = False
        self.fileData = None

        self.autoXFileOk = False
        self.autoXFile = None

        self.outputFileOk = False
        self.outputFile = None

        self.outputTE.clear()

        self._curDir_ = os.getcwd()

        self.retCode = None
        self.err = False
        self.errMsg = None
        self.outMsg = None

        self.useSingleFile = False
        self.writeCSV = False

        self.loadThread = LoadThread(self)

        self.iterScroll = 0
        #self.filePathError()

    def __updateGUI__(self):
        if self.fileDataOk and self.fileData != None:
            self.brukerFolderLE.setText(self.fileData)

        if self.autoXFileOk and self.autoXFile != None:
            self.autoExecuteLE.setText(self.autoXFile)

        if self.outputFileOk and self.outputFile != None:
            self.outputFileLE.setText(self.outputFile)

        #need to reset command sequence
        self.cmdOut = ['CompassXport']


    def __makeConnections__(self):
        QtCore.QObject.connect(self.actionClose,QtCore.SIGNAL("clicked()"),self.__mainClose__)
        QtCore.QObject.connect(self.selBrukerDataBtn,QtCore.SIGNAL("clicked()"),self.__getBrukerData__)
        QtCore.QObject.connect(self.autoXFileBtn,QtCore.SIGNAL("clicked()"),self.__getAutoXFile__)
        QtCore.QObject.connect(self.outputBtn,QtCore.SIGNAL("clicked()"),self.__setOutputFile__)
        QtCore.QObject.connect(self.cnvrtBrukerBtn,QtCore.SIGNAL("clicked()"),self.__convertBruker__)
        QtCore.QObject.connect(self.actionConvert2XML,QtCore.SIGNAL("triggered()"),self.__convertBruker__)
        QtCore.QObject.connect(self.singleFileCB, QtCore.SIGNAL("stateChanged (int)"),self.__changeInputFile__)
        QtCore.QObject.connect(self.toCSVCB, QtCore.SIGNAL("stateChanged (int)"),self.__write2csv__)
        QtCore.QObject.connect(self.brukerFolderLE, QtCore.SIGNAL("editingFinished()"),self.__brukerLEChanged__)
        QtCore.QObject.connect(self.autoExecuteLE, QtCore.SIGNAL("editingFinished()"),self.__autoXLEChanged__)
        QtCore.QObject.connect(self.outputFileLE, QtCore.SIGNAL("editingFinished()"),self.__outputLEChanged__)
        QtCore.QObject.connect(self.action_About,QtCore.SIGNAL("triggered()"),self.__showAbout__)
        QtCore.QObject.connect(self.loadThread, QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"), self.updateOutputMsg)
        QtCore.QObject.connect(self.agilent_CB, QtCore.SIGNAL("stateChanged (int)"),self.agilentToggle)

    def agilentToggle(self, state):
        if state == 2:
            self.makeMGF_CB.setCheckState(QtCore.Qt.Unchecked)
            self.toCSVCB.setCheckState(QtCore.Qt.Unchecked)
            self.makeMGF_CB.setEnabled(False)
            self.toCSVCB.setEnabled(False)
        else:
            self.makeMGF_CB.setEnabled(True)
            self.toCSVCB.setEnabled(True)

    def __brukerLEChanged__(self):
        self.fileDataOk = True
        self.fileData = self.brukerFolderLE.text()
        if os.path.isdir(str(self.fileData)):
            self.dir = str(self.fileData)

    def __autoXLEChanged__(self):
        self.autoXFileOk = True
        self.autoXFile = self.autoExecuteLE.text()

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
        self.brukerFolderLE.clear()
        self.fileDataOk = False

    def __write2csv__(self, state):
        if state == 2:
            self.writeCSV = True
        else:
            self.writeCSV = False

    def updateOutputMsg(self, outputStr):
        self.iterScroll+=1
        self.outputTE.insertPlainText(QtCore.QString(outputStr))
        scrollBar = self.outputTE.verticalScrollBar();
        scrollBar.setValue(scrollBar.maximum())

    def __convertBruker__(self):
        if self.fileDataOk:
            self.outputTE.clear()
            if self.makeMGF_CB.isChecked():
                fileList = getPeakFiles(str(self.fileData))
#                if self.outputFile != None:
#                    convert2mgf(str(self.outputFile))
#                else:
                filepath = os.path.abspath(str(self.fileData))
                coreDir = os.path.basename(filepath)
                coreDir+='.mgf'
                file2write = os.path.join(filepath, coreDir)
                self.updateOutputMsg(convert2mgf(fileList, file2write))



            else:
                if self.useSingleFile == False:
                    fileList = getBrukerFiles(str(self.fileData), getAgilent = self.agilent_CB.isChecked())
                    if self.loadThread.updateThread(fileList, convertAgilent = self.agilent_CB.isChecked()):
                        self.loadThread.start()

                else:
                    newFile = None
                    if self.outputFileOk:
                        newFile =str(self.outputFile)
                    self.updateOutputMsg(self.loadThread.exeCompassXport(str(self.fileData), newFile))
        else:
            reply = QtGui.QMessageBox.warning(self.MainWindow, "No Input File or Folder Set",  "An input file or folder must be selected before continuing.")
            self.__getBrukerData__()
#            exec_str = '-multi '+str(self.fileData)
#            self.cmdOut.append(exec_str)
#            file_str = ' -multiName '+'BrukerConvert.1231.test.mzXML'
#            self.cmdOut.append(file_str)


    def exeCompassXport(self, file2Convert,  newFileName = None):
        self.cmdOut = ['CompassXport']

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
            if filetype == 'None':
                newFileName+='.mzXML'
                newPath = os.path.join(str(self.fileData), newFileName)

            elif filetype != 'None' and self.useSingleFile == False:
                newFileName += '.mzXML'
                newPath = os.path.join(str(self.outputFile), newFileName)
            else:
                newPath=str(self.outputFile)
        else:
            newFileName='analysis.mzXML'
            self.dir = os.path.dirname(str(self.fileData))
            newPath = os.path.join(self.dir, newFileName)

        #this small code block writes a peak list to a csv file
        peakList = brukerPeakList(file2Convert)#used for csv
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


    def __getBrukerData__(self):
        if self.fileDataOk:
            try:
                if self.useSingleFile:
                    self.dir = os.path.dirname(str(self.fileData))
                else:
                    self.dir = str(self.fileData)
            except:
                print "Directory split didn't work"
                self.dir = self._curDir_
        else:
            self.dir = self._curDir_
        if self.fileDataOk and self.fileData != None:
            if self.useSingleFile:
                self.dir = os.path.dirname(str(self.fileData))
            else:
                self.dir = str(self.fileData)

        if self.useSingleFile:
            data = QtGui.QFileDialog.getOpenFileName(self.MainWindow,\
                                'Select Bruker Data File',\
                                self.dir, 'fid File (fid);; Agilent D Files (D);;All Files (*.*)')
        else:
            #you could parse the line edit if it is not empty and use that directory?
            data = QtGui.QFileDialog.getExistingDirectory(self.MainWindow,\
                                                        self.dir,
                                                        "Select Data Folder")
        if data:
            if ' ' in data:
                self.filePathError()
            else:
                if os.path.isdir(str(data)):
                    self.dir = str(data)
                self.fileDataOk = True
                self.fileData = data
                self.__updateGUI__()

    def __getAutoXFile__(self):

        dir = self._curDir_
        if self.fileDataOk and self.fileData != None:
            if not self.useSingleFile:
                dir = self.fileData

        autoXFileName = QtGui.QFileDialog.getOpenFileName(self.MainWindow,\
                            'Select Bruker AutoXecute File',\
                            dir, 'AutoXecute File (*.xml)')

        if autoXFileName:
            self.autoXFileOk = True
            self.autoXFile = autoXFileName
            self.__updateGUI__()


    def __setOutputFile__(self):
        if self.fileDataOk and self.fileData != None:
            if self.useSingleFile:
                outputFile = QtGui.QFileDialog.getSaveFileName(self.MainWindow,\
                            'Select Output File Name',\
                            self.dir, 'mzXML (*.mzXML);;mzData (*.mzDATA)')

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
            self.__getBrukerData__()


    def filePathError(self):
        reply = QtGui.QMessageBox.warning(self.MainWindow, "File Naming Warning",  "This conversion utility requires the file path names to not have any spaces or special characters.  You've been warned!")

    def __showAbout__(self):
        return QtGui.QMessageBox.information(self.MainWindow,
                                            ("Bruker2mzXML V.0.9, Octobert, 2008"),
                                            ("<p><b>Bruker2mzXML</b> was written in Python by Brian H. Clowers (bhclowers@gmail.com).</p>"
        "<p>Please keep in mind that the entire effort is very much a"
        " work in progress and that Brian won't quit his day job for programming."
        " The original purpose of Bruker2mzXML was to provide a user-friendly interface to the"
        " Bruker CompassXport conversion tool (which must be installed for this program to work)."
        " Bruker2mzXML also extends Bruker's original program by providing the ability to "
        " automatically rename files and place them in a directory of your choice.  At this time"
        " concatenation of the output files is not possible, though certainly feasible.  If you'd like "
        " the source code please let me know.  Please feel free to make modifications (preferably "
        " with documentation) and share your contributions with the rest of the community.</p>"
        " "
        " <p>Added support for Agilent *.D files and directories, October, 2009 BHC.</p>"))


    def __mainClose__(self):
        self.MainWindow.close()
############################


class LoadThread(QtCore.QThread):
        def __init__(self, parent):
            QtCore.QThread.__init__(self, None)#parent)

            self.P = parent
            self.outputFile = None
            self.fileData = None
            self.writeCSV = None
            self.finished = False
            self.convertAgilent = False
            self.ready = False

        def updateThread(self, loadList, convertAgilent = False):
            self.loadList = loadList
            self.numItems = len(loadList)
            self.totalFiles = len(loadList)
            self.outputFile = self.P.outputFile
            self.fileData = self.P.fileData
            self.writeCSV = self.P.writeCSV
            self.convertAgilent = convertAgilent
            self.ready = True
            return True

        def run(self):
            if self.ready:
                while not self.finished and self.numItems > 0:
                    self.curFileNum = 0
                    for item in self.loadList:
                        self.msg = self.exeCompassXport(item[0],  item[1])
                        #print item[0],  item[1]
                        #this following line is key to pass python object via the SIGNAL/SLOT mechanism of PyQt
                        self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),self.msg)#note PyQt_PyObject
                        self.numItems -=1

                        self.curFileNum+=1


        def __del__(self):
            self.exiting = True
            self.wait()

        def exeCompassXport(self, file2Convert,  newFileName = None):
            t1 = time.clock()
            self.cmdOut = ['CompassXport']

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
                if filetype == 'None':
                    newFileName+='.mzXML'
                    newPath = os.path.join(str(self.fileData), newFileName)

                elif filetype != 'None' and self.useSingleFile == False:
                    newFileName += '.mzXML'
                    newPath = os.path.join(str(self.outputFile), newFileName)
                else:
                    newPath=str(self.outputFile)
            else:
                newFileName='analysis.mzXML'
                self.dir = os.path.dirname(str(self.fileData))
                newPath = os.path.join(self.dir, newFileName)

            #this small code block writes a peak list to a csv file
            try:
                peakList = brukerPeakList(file2Convert)#used for csv
                peakList.saveCSV(os.path.splitext(newPath)[0])#used for csv
            except:
                print "Error converting Bruker peaklist for %s"%file2Convert

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

            ########BEGIN CONVERT TO CSV
                if self.writeCSV:
                    mzr = MzR(newPath)
                    mzr.saveCSV(os.path.splitext(newPath)[0])
            ###############################
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
                print cmdStr
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
    ui = BrukerConvert(MainWindow)
    MainWindow.show()
#    except:
#        errorMsg = "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
#        errorMsg+='\n Contact Clowers and try to remember what you did to make it crash!'
#        QtGui.QMessageBox.warning(MainWindow, "Fatal Error",  errorMsg)

    sys.exit(app.exec_())


if __name__ == "__main__":
    run_main()
