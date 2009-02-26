from PyQt4 import QtCore, QtGui
import os, os.path
import sys
from string import join
import subprocess as sub

import time

import ui_main

from LECO_IO import ChromaTOF_Reader as CR
from LECOFolderParse import getLECOFiles

import tables as T
import numpy as N


class LECOConvert(ui_main.Ui_MainWindow):
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        ui_main.Ui_MainWindow.setupUi(self,MainWindow)

        self.__setup__()
        self.__makeConnections__()

    def __setup__(self):
        self.LECODataOk = False
        self.LECOData = None

        self.outputFileOk = False
        self.outputFile = None

        self.outputTE.clear()

        self._curDir_ = os.getcwd()

        self.retCode = None
        self.err = False
        self.errMsg = None
        self.outMsg = None

        self.useSingleFile = True

        self.saveThread = saveThread(self)

        self.iterScroll = 0
        self.GCTime = None
        self.__updateGCTime__(5)
        #self.filePathError()

    def __updateGUI__(self):
        if self.LECODataOk and self.LECOData != None:
            self.LECOFolderLE.setText(self.LECOData)

        if self.outputFileOk and self.outputFile != None:
            self.outputFileLE.setText(self.outputFile)



    def __makeConnections__(self):
        QtCore.QObject.connect(self.actionClose,QtCore.SIGNAL("clicked()"),self.__mainClose__)
        QtCore.QObject.connect(self.selLECODataBtn,QtCore.SIGNAL("clicked()"),self.__getLECOData__)
        QtCore.QObject.connect(self.outputBtn,QtCore.SIGNAL("clicked()"),self.__setOutputFile__)
        QtCore.QObject.connect(self.cnvrtLECOBtn,QtCore.SIGNAL("clicked()"),self.__convertLECO__)
        QtCore.QObject.connect(self.GC2TimeSB,QtCore.SIGNAL("valueChanged(double)"),self.__updateGCTime__)
        QtCore.QObject.connect(self.actionConvert2HDF5,QtCore.SIGNAL("triggered()"),self.__convertLECO__)
        QtCore.QObject.connect(self.singleFileCB, QtCore.SIGNAL("stateChanged (int)"),self.__changeInputFile__)
        QtCore.QObject.connect(self.LECOFolderLE, QtCore.SIGNAL("editingFinished()"),self.__LECOLEChanged__)
        QtCore.QObject.connect(self.outputFileLE, QtCore.SIGNAL("editingFinished()"),self.__outputLEChanged__)
        QtCore.QObject.connect(self.action_About,QtCore.SIGNAL("triggered()"),self.__showAbout__)
        QtCore.QObject.connect(self.saveThread, QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"), self.updateOutputMsg)

    def __updateGCTime__(self, secs):
        '''
        This assumes a 10kHz sampling rate
        #NEED TO UPDATE GUI TO INCLUDE SAMPLING RATE
        '''
        self.GC2Time = secs*100


    def __LECOLEChanged__(self):
        self.LECODataOk = True
        self.LECOData = self.LECOFolderLE.text()

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
        self.LECOFolderLE.clear()
        self.LECODataOk = False

    def updateOutputMsg(self, outputStr):
        self.iterScroll+=1
        self.outputTE.insertPlainText(QtCore.QString(outputStr))
        scrollBar = self.outputTE.verticalScrollBar();
        scrollBar.setValue(scrollBar.maximum())

    def __convertLECO__(self):
        if self.LECODataOk:
            self.outputTE.clear()
            if self.useSingleFile == False:
                fileList = getLECOFiles(str(self.LECOData))
                if self.saveThread.updateThread(fileList):
                    self.saveThread.start()

            else:
                newFile = None
                if self.outputFileOk:
                    newFile =str(self.outputFile)

                fileList = [[str(self.LECOData), newFile]]
                if self.saveThread.updateThread(fileList):
                    self.saveThread.start()
                #self.msg = self.saveChroma2H5(item[0],  item[1])
                #self.updateOutputMsg(self.saveThread.saveChroma2H5(str(self.LECOData), newFile))
        else:
            reply = QtGui.QMessageBox.warning(self.MainWindow, "No Input File Set",  "An input file must be selected before continuing.")
            self.__getLECOData__()


    def __getLECOData__(self):
        if self.LECODataOk:
            try:
                if self.useSingleFile:
                    self.dir = os.path.dirname(str(self.LECOData))
                else:
                    self.dir = str(self.LECOData)
            except:
                print "Directory split didn't work"
                self.dir = self._curDir_
        else:
            self.dir = self._curDir_
        if self.LECODataOk and self.LECOData != None:
            if self.useSingleFile:
                self.dir = os.path.dirname(str(self.LECOData))
            else:
                self.dir = self.LECOData

        if self.useSingleFile:
            data = QtGui.QFileDialog.getOpenFileName(self.MainWindow,\
                                'Select LECO Data File',\
                                self.dir, 'netCDF (*.cdf);; All Files (*.*)')
        else:
            data= QtGui.QFileDialog.getExistingDirectory(self.MainWindow,\
                                                             "Select LECO Data Folder")
        if data:
#            if ' ' in data:
#                self.filePathError()
#            else:
            self.LECODataOk = True
            self.LECOData = data
            self.__updateGUI__()



    def __setOutputFile__(self):
        if self.LECODataOk and self.LECOData != None:
            if self.useSingleFile:
                outputFile = QtGui.QFileDialog.getSaveFileName(self.MainWindow,\
                            'Select Output File Name',\
                            self.dir, 'HDF5 (*.HDF5)')

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
            self.__getLECOData__()


    def filePathError(self):
        reply = QtGui.QMessageBox.warning(self.MainWindow, "File Naming Warning",  "This conversion utility requires the file path names to not have any spaces or special characters.  You've been warned!")

    def __showAbout__(self):
        return QtGui.QMessageBox.information(self.MainWindow,
                                            ("LECO2HDF5 V.0.9, November, 2008"),
                                            ("<p><b>LECO2HDF5</b> was written in Python by Brian H. Clowers (bhclowers@gmail.com).</p>"
        "<p>Please keep in mind that the entire effort is very much a"
        " work in progress and that Brian won't quit his day job for programming."
        " The original purpose of LECO2HDF5 was to provide a user-friendly interface to convert"
        " the LECO GC-GC-MS netCDF files output from the LECO Pegasus Software to a more compact "
        " and less memory intensive HDF5 file format."
        " At this time concatenation of the output files is not possible, though certainly feasible."
        " If you'd like the source code please let me know.  Please feel free to make modifications"
        " (preferably with documentation) and share your contributions with the rest of the community.</p>"))


    def __mainClose__(self):
        self.MainWindow.close()
############################


class saveThread(QtCore.QThread):

    def __init__(self, parent):
        QtCore.QThread.__init__(self, None)#parent)

        self.P = parent
        self.outputFile = None
        self.LECOData = None
        self.finished = False
        self.ready = False
        self.outFileType = None
        self.inFileType = None
        self.GCTime = None
        self.curFileNum = 0
        self.totalFiles = 1

    def updateThread(self, loadList):
        self.loadList = loadList
        self.numItems = len(loadList)
        self.totalFiles = len(loadList)
        self.outputFile = self.P.outputFile
        self.LECOData = self.P.LECOData
        self.GCTime = self.P.GCTime
        self.ready = True
        return True

    def run(self):
        if self.ready:
            while not self.finished and self.numItems > 0:
                self.curFileNum = 0
                for item in self.loadList:
                    self.msg = self.saveChroma2H5(item[0],  item[1])
                    #print item[0],  item[1]
                    #this following line is key to pass python object via the SIGNAL/SLOT mechanism of PyQt
                    self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),self.msg)#note PyQt_PyObject
                    self.numItems -=1

                    self.curFileNum+=1

    def __del__(self):
        self.exiting = True
        self.wait()

    def saveChroma2H5(self, file2Convert,  newFileName = None):
        t1 = time.clock()

        msg = 'Processing: %s\n'%str(file2Convert)
        self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),msg)

        self.LECOData = file2Convert
        self.outFileType = os.path.basename(str(self.LECOData)).split('.')[-1]
        self.dir = os.path.dirname(str(self.LECOData))
        if newFileName == None:
            newFileName = os.path.basename(str(self.LECOData)).split('.')[0]
        newFileName+='.h5'
        newPath = os.path.join(self.dir, newFileName)
        newPath = os.path.abspath(newPath)
#            print self.outFileType
        if self.outFileType == 'cdf':
            try:
                cdf = CR(self.LECOData,  fileType = 'NetCDF', GC2Time = self.GCTime)
                self.saveChromaTOF(newPath, cdf, dataType = 'NetCDF' )

                t2 = time.clock()
                msg = '%s written\n'%newPath
                runTime= '%s sec\n\n'%(t2-t1)

                fileupdate = '%d of %d Finished\n'%(self.curFileNum+1, self.totalFiles)
                msg +=fileupdate
                msg += runTime
                return msg

            except:
                errorMsg = "Error: %s\n\n%s\n"%(sys.exc_type, sys.exc_value)
                return errorMsg


        return "%s,%s"%(newPath, newFileName)


    def saveChromaTOF(self, fileName,  cdf, numCols=None,  numRows = None, dataType = 'NetCDF'):
        t1 = time.clock()

        mzMax = 401 #rows
        colCount = len(cdf.scanIndex)
        hdf = T.openFile(fileName, mode = "w", title = 'Data_Array')
        filters = T.Filters(complevel=5, complib='zlib')
        atom = T.Int32Atom()
        chunkS = (400, 5)
        #chunkMZ = (20, 401)
        dataCube = hdf.createEArray(hdf.root, 'dataCube', atom, (0,mzMax), filters = filters,  expectedrows = colCount)#,  chunkshape = chunkMZ)
        dataCube.attrs.rowPoints = cdf.rowPoints
        dataCube.attrs.colPoints = cdf.colPoints

        data = cdf.TIC
        shape = data.shape
        tic = hdf.createCArray(hdf.root, 'TIC', atom, shape,  filters = filters)
        tic[0:shape[0]] = data
        tic.flush()
        #print "TIC OK"

        bpc = hdf.createCArray(hdf.root, 'BPC', atom, shape,  filters = filters)
        bpcMZ = hdf.createCArray(hdf.root, 'BPCmz', atom, shape,  filters = filters)


        #sicCube = hdf.createEArray(hdf.root, 'sicCube', atom, (mzMax,0), filters = filters,  expectedrows = mzMax)#,  chunkshape = chunkS)
        #print "Sic Chunk", sicCube.chunkshape
        #print "MZ Chunk",  dataCube.chunkshape

        try:
            if dataType == 'NetCDF':
                m=0
                for i in cdf.scanIndex:

                    localMaxIndex = i+cdf.pntCount[m]#index for current mass spectrum
                    mz2Write = N.zeros(mzMax)#ADDING 1 so that indicies work out!!!!!!!!!!!!!!!DOUBLE CHECK THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    mzLocal = N.array(cdf.vars['mass_values'].data[i:localMaxIndex])#the current mz values
                    mzLocal +=1 #!!!!!!!!!!!!!!DOUBLE CHECK THIS
                    intLocal = cdf.vars['intensity_values'].data[i:localMaxIndex]#the current mz intensity values
                    N.put(mz2Write,  mzLocal, intLocal)
                    dataCube.append(mz2Write[N.newaxis,:])
                    bpc[m] = mz2Write.max()
                    bpcMZ[m] = mz2Write.argmax()


                    if m%10000 == 0:
                        msg = "%s mass spectra\n"%m
                        self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),msg)
                        #print m
                    m+=1

#                    if m == 10000:
#                        print time.clock()-t1, 'seconds'
#                        hdf.close()
#                        return
                dataCube.flush()
                bpc.flush()
                bpcMZ.flush()
                print time.clock()-t1, 'seconds'
                hdf.close()

            if dataType == 'HDF5':
                m=0
                for i in cdf.scanIndex:

                    localMaxIndex = i+cdf.pntCount[m]
                    mz2Write = N.zeros(mzMax)#ADDING 1 so that indicies work out!!!!!!!!!!!!!!!DOUBLE CHECK THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    mzLocal = N.array(cdf.vars['mass_values'][i:localMaxIndex])
                    mzLocal +=1 #!!!!!!!!!!!!!!DOUBLE CHECK THIS
                    intLocal = cdf.vars['intensity_values'][i:localMaxIndex]
                    N.put(mz2Write,  mzLocal, intLocal)
                    dataCube.append(mz2Write[N.newaxis,:])
                    dataCube.flush()

                    if m%10000 == 0:
                        msg = "%s mass spectra\n"%m
                        self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),msg)
                        #print m
                    m+=1
                print time.clock()-t1, 'seconds'
                hdf.close()


        except:
            errorMsg = "Error: %s\n\n%s\n"%(sys.exc_type, sys.exc_value)
            print errorMsg
            hdf.close()

#            try:
#
#                t2 = time.clock()
#                runTime= '%s sec\n\n'%(t2-t1)
#
#                fileupdate = '%d of %d Finished\n'%(self.curFileNum+1, self.totalFiles)
#                msg +=fileupdate
#                msg += runTime
#                return msg
#            except:
#                errorMsg = "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
#                print errorMsg
#                raise


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
    try:
        ui = LECOConvert(MainWindow)
        MainWindow.show()
    except:
        errorMsg = "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
        errorMsg+='\n Contact Clowers and try to remember what you did to make it crash!'
        QtGui.QMessageBox.warning(MainWindow, "Fatal Error",  errorMsg)

    sys.exit(app.exec_())


if __name__ == "__main__":
    run_main()
