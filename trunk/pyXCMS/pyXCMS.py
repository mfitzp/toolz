import sys, traceback
import os
import shutil
import time
from PyQt4 import QtCore, QtGui

#try:#this is done because sometimes there is an annoying message regard tk that come up
import rpy2
import rpy2.robjects as ro
import rpy2.rinterface as ri
#except:
#    pass

'''
ToDo:
Save File List
Save Param Dict
'''


import ui_main
import FolderParse as FP
from eicClass import EIC
from rpy2Thread import XCMSThread
from Python_Highlighter import PythonHighlighter as PH

import numpy as N
from scipy import rand

test_data = rand(10,2)

COLORS = ['#297AA3','#A3293D','#3B9DCE','#293DA3','#5229A3','#8F29A3','#A3297A',
'#7AA329','#3DA329','#29A352','#29A38F','#A38F29','#3B9DCE','#6CB6DA','#CE6C3B','#DA916C',
'#0080FF','#0000FF','#7ABDFF','#8000FF','#FF0080','#FF0000','#FF8000','#FFFF00','#A35229','#80FF00',
'#00FF00','#00FF80','#00FFFF','#3D9EFF','#FF9E3D','#FFBD7A']

def initRlibs(libList):
    libDict = {}

    for lib in libList:
        try:
            libDict[lib] = ro.r('library(%s)'%lib)
        except:
            errorMsg ='Error loading R library %s\nCheck Library Installation\n'%lib
            errorMsg += "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
            print errorMsg

    return libDict

def list2rpyFuntions(strList):
    funcDict = {}
    for entry in strList:
        try:
            funcDict[entry] = ro.r['%s'%entry]
        except:
            errorMsg ='Error creating function %s'%entry
            errorMsg += "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
            print errorMsg

    return funcDict


class pyXCMSWindow(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent = None):
        super(pyXCMSWindow, self).__init__(parent)
        self.ui = self.setupUi(self)

        self.__initVars()
        self.__initConnections()
        self._setContext_()
        self.setupGUI()
        self.setupR()


    def __initVars(self):
        self.firstLoad = True
        self.colorIndex = 0
        self.txtColor = None
        self.curDir = os.getcwd()
        self.peakTableName = None
        self.curParamDict = None
        self.curTypeDict = None
        self.fileList = None
#        self.Rliblist = ['xcms']
#        self.Rlibs = initRlibs(self.Rliblist)

        self.xcmsOK = False
        self.eicPlot = self.plotWidget.canvas.axDict['ax1']
        self.eicList = []
        self.eicDict = None
        self.eicClass = None
        self.curXSET = None
        self.plotIndex = 0
        self.initIndex = 0
        self.ignoreSignal = False
        self.highlighter = PH(self.batchScriptTE.document())


        self.rThread = XCMSThread()

#        self.rProcess = QtCore.QProcess()

        '''
        findPeaks.matchedFilter(object, fwhm = 30, sigma = fwhm/2.3548, max = 5,
        snthresh = 10, step = 0.1, steps = 2, mzdiff = 0.8 - step*steps,
        index = FALSE, sleep = 0)

        object   --xcmsRaw object
        fwhm     --full width at half maximum of matched filtration gaussian model peak
        sigma    --standard deviation of matched filtration model peak
        max      --maximum number of peaks per extracted ion chromatogram
        snthresh --signal to noise ratio cutoff
        step     --step size to use for profile generation
        steps    --number of steps to merge prior to filtration
        mzdiff   --minimum difference in m/z for peaks with overlapping retention times
        index    --return indicies instead of values for m/z and retention times
        sleep    --number of seconds to pause between plotting peak finding cycles


        '''
        self.matchedFilterParams = {'fwhm':30.,
                                    'sigma':30/2.3548,
                                    'max': 5.,
                                    'snthresh':10.,
                                    'step':0.01,
                                    'steps':2.,
                                    'mzdiff':0.01,
                                    }

        self.matchedFilterTypes = {'fwhm':float,
                                   'sigma':float,
                                   'max':float,
                                   'snthresh':float,
                                   'step':float,
                                   'steps':float,
                                   'mzdiff':float
                                    }

        ##########################
        '''
        CentWave

        object = "xcmsRaw"
        findPeaks.centWave(object, ppm=25, peakwidth=c(20,50),
        snthresh=10, prefilter=c(3,100), integrate=1, mzdiff=-0.001,
        fitgauss=FALSE, scanrange= numeric(), sleep=0, verbose.columns=FALSE)

        object     --xcmsSet objectprint methodHelp
        ppm        --maxmial tolerated m/z deviation in consecutive scans, in ppm (parts per million)
        peakwidth  --Chromatographic peak width, given as range (min,max) in seconds
        snthresh   --signal to noise ratio cutoff, definition see below.
        prefilter  --prefilter=c(k,I). Prefilter step for the first phase. Mass traces are only retained if they contain at least k peaks with intensity >= I.
        integrate  --Integration method. If =1 peak limits are found through descent on the mexican hat filtered data, if =2 the descent is done on the real data. Method 2 is very accurate but prone to noise, while method 1 is more robust to noise but less exact.
        mzdiff     --minimum difference in m/z for peaks with overlapping retention times, can be negative to allow overlap
        fitgauss   --logical, if TRUE a Gaussian is fitted to each peak
        scanrange  --scan range to process
        sleep      --number of seconds to pause between plotting peak finding cycles
        verbose.columns logical, if TRUE additional peak meta data columns are returned

        '''
        #this method is not working well yet for the ORBITRAP DATA ACQUIRED AT PNNL
        self.centWaveParams = {'ppm': 10.,
                               'peakwidth': str([20,50]),#this needs to be fixed, the new version of PyQt4 handles this better
                               'snthresh':10.,
                               'prefilter':str([3,100]),
                               'mzdiff':-0.001,
                               }
        self.centWaveTypes = {'ppm': float,
                               'peakwidth': str,
                               'snthresh':float,
                               'prefilter':str,
                               'mzdiff':float,
                               }
        ################################

        self.groupParams = {'bw':30.,
                            'minfrac':0.1,
                            'mzwid':0.1,
                            'max':3
                            }

        self.groupTypes = {'bw':float,
                            'minfrac':float,
                            'mzwid':float,
                            'max':int
                            }
        ##############################

        self.retcorParams = {'extra':2,
                             'span':0.5,
                             'f':'symmetric',
                             'plottype':'none',
                             'missing':2
                             }
        self.retcorTypes = {'extra':int,
                            'span':float,
                            'f':str,
                            'plottype':str,
                            'missing':str
                            }

        #########################
        self.xcmsParamDict = {'Matched Filter':self.matchedFilterParams,
                              'Group Params':self.groupParams,
                              'Retcor Params':self.retcorParams,
                              'CentWave':self.centWaveParams}

        self.xcmsTypeDict = {'Matched Filter':self.matchedFilterTypes,
                             'Group Params':self.groupTypes,
                             'Retcor Params':self.retcorTypes,
                             'CentWave':self.centWaveTypes}


    def __initConnections(self):
        QtCore.QObject.connect(self.getFolderBtn, QtCore.SIGNAL("clicked()"), self.initFileList)
        QtCore.QObject.connect(self.xcmsMethodCB, QtCore.SIGNAL("currentIndexChanged(QString)"), self.updateParamTable)
        QtCore.QObject.connect(self.paramTableWidget, QtCore.SIGNAL("itemDoubleClicked(QTableWidgetItem*)"), self.paramTableEntered)
        QtCore.QObject.connect(self.paramTableWidget, QtCore.SIGNAL("itemChanged(QTableWidgetItem*)"), self.paramTableChanged)
        QtCore.QObject.connect(self.paramTableWidget, QtCore.SIGNAL("helpRequested(PyQt_PyObject)"), self.showParamHelp)
        QtCore.QObject.connect(self.actionTest_XCMS, QtCore.SIGNAL("triggered()"), self.testXCMS)
        QtCore.QObject.connect(self.actionSave_HDF5, QtCore.SIGNAL("triggered()"), self.saveEICs2HDF5)
        QtCore.QObject.connect(self.actionLoad_HDF5, QtCore.SIGNAL("triggered()"), self.loadHDF52EICs)
        QtCore.QObject.connect(self.actionSave_Results_Table, QtCore.SIGNAL("triggered()"), self.saveXCMSResultsCSV)
        QtCore.QObject.connect(self.getEICBtn, QtCore.SIGNAL("clicked()"), self.fetchEIC)
        QtCore.QObject.connect(self.runXCMSBtn, QtCore.SIGNAL("clicked()"), self.startXCMSRun)

        QtCore.QObject.connect(self.loadRPY2BatchBtn, QtCore.SIGNAL("clicked()"), self.loadRPY2Batch)


        QtCore.QObject.connect(self.eicIndexSB, QtCore.SIGNAL("valueChanged(int)"), self.indexChanged)

        QtCore.QObject.connect(self.rThread, QtCore.SIGNAL("xcmsOutUpdate(PyQt_PyObject)"), self.updateROutput)
        QtCore.QObject.connect(self.rThread, QtCore.SIGNAL("xcmsGetEIC(PyQt_PyObject)"), self.getThreadEIC)
        QtCore.QObject.connect(self.rThread, QtCore.SIGNAL("xcmsSet(PyQt_PyObject)"), self.setXCMSGroup)

        self.removeFileAction = QtGui.QAction("Remove File", self)
        self.dirListWidget.addAction(self.removeFileAction)
        QtCore.QObject.connect(self.removeFileAction,QtCore.SIGNAL("triggered()"), self.removeFile)


    def removeFile(self):
        selItem = self.dirListWidget.selectedItems()[0]
        curRow = self.dirListWidget.row(selItem)
        print curRow
        self.dirListWidget.takeItem(curRow)
        self.dirList.pop(curRow)
        print len(self.dirList)


    def _setContext_(self):
        self.plotWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.plotWidget.connect(self.plotWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self._plotContext_)
        self.dirListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.dirListWidget.connect(self.dirListWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self._dirListContext_)

    def _dirListContext_(self, point):
        ct_menu = QtGui.QMenu("File List Menu", self.dirListWidget)
        ct_menu.addAction(self.removeFileAction)
        ct_menu.exec_(self.dirListWidget.mapToGlobal(point))

    def _plotContext_(self, point):
        ct_menu = QtGui.QMenu("Plot Menu", self.plotWidget)
        ct_menu.addAction(self.plotWidget.zoomAction)
        ct_menu.addAction(self.plotWidget.actionAutoScale)
        ct_menu.addSeparator()
        ct_menu.addAction(self.plotWidget.saveCSVAction)
        ct_menu.addAction(self.plotWidget.mpl2ClipAction)
        ct_menu.exec_(self.plotWidget.mapToGlobal(point))


    def setupR(self):
        peakTableName = 'tempPeakTable.csv'
        self.peakTableName = os.path.join(self.curDir, peakTableName)
        try:
            ro.r('source("xcmsFuncs.R")')
        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
#                    print 'Error saving figure data'
            errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
            return QtGui.QMessageBox.warning(self, "R Source Error", errorMsg)
            print errorMsg
        #print peakTableName

    def setXCMSGroup(self, xcmsSetObject):
        if xcmsSetObject != None:
            self.curXSET = xcmsSetObject
            ro.r.writePeakTable(self.curXSET, self.peakTableName)
            if os.path.isfile(self.peakTableName):
                self.RoutputTE.append('xcms peak table written to: %s'%self.peakTableName)

    def saveXCMSResultsCSV(self):
        if self.curXSET != None:
            if os.path.isfile(self.peakTableName):
                fileName = str(self.SaveCSVDialog())
                if fileName != None:
                    shutil.copy(self.peakTableName, fileName)
                    if os.path.isfile(fileName):
                        self.RoutputTE.append('xcms peak table written to: %s'%fileName)
        else:
            Msg = 'No XSET Exists\nTry Again!'
            return QtGui.QMessageBox.warning(self, "There is no xset instance, hence no table!", Msg )

    def fetchEIC(self):
        if self.curXSET != None:
            if self.rtTypeCB.isChecked():
                rtType = "corrected"
            else:
                rtType = "raw"
            mzlo = self.mzStartSB.value()
            mzhi = self.mzStopSB.value()
            if mzlo > mzhi:
                Msg = 'm/z start must be lower than m/z stop!'
                return QtGui.QMessageBox.warning(self, "Try Again Slick", Msg )
            mzRange = ro.r.cbind(mzmin=mzlo,mzmax=mzhi)
            if self.rtWidthSB_Stop.value() == -1:
                usrRTrange = self.rtWidthSB.value()
            else:
                usrRTrange = ro.r.cbind(self.rtWidthSB.value(),self.rtWidthSB_Stop.value())
            eic = ro.r.getEIC(self.curXSET, mzRange, rtrange=usrRTrange,rt=rtType)
            self.eicClass.appendEIC(eic)
            self.updateGUI()
            self.eicIndexSB.setValue(self.eicIndexSB.maximum())

            #self.RoutputTE.append('xcms peak table written to: %s'%fileName)
        else:
            Msg = 'No XSET Exists\nTry Again!'
            return QtGui.QMessageBox.warning(self, "No xset. No EIC.", Msg )



    def SaveCSVDialog(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self, "Select File to Save", self.curDir,"csv (*.csv)")
        if not fileName.isEmpty():
            print fileName
            return fileName
        else:
            return None


    def SFDialog(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self, "Select File to Save", self.curDir,"HDF5 Files (*.h5)")
        if not fileName.isEmpty():
            print fileName
            return fileName
        else:
            return None

    def LFDialog(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,\
                                                    "Select File to Load",\
                                                    self.curDir, 'HDF5 File (*.h5)')
        if not fileName.isEmpty():
            print fileName
            return fileName
        else:
            return None

    def loadHDF52EICs(self):
        #need qualifier to wipe out old one....
        msgTitle = 'Overwrite existing EIC set'
        overWriteStr = 'Clear current EIC and load a new set?'
        if self.__askConfirm__(msgTitle,overWriteStr):
            fileName = str(self.LFDialog())
            if fileName != None:
                self.eicClass = EIC()
                t1 = time.clock()
                self.eicClass.loadHDF5(fileName)
                t2 = time.clock()-t1
                self.RoutputTE.append('HDF5 Read Time: %.4f seconds'%t2)
                self.updateGUI()

    def saveEICs2HDF5(self):
        fileName = str(self.SFDialog())
        if fileName != None:
            if self.eicClass != None:
                t1 = time.clock()
                self.eicClass.save2HDF5(fileName)
                t2 = time.clock()-t1
                self.RoutputTE.append('HDF5 Write Time: %.4f seconds'%t2)
            else:
                rMsg = 'No xcms Data Exists to Save'
                return QtGui.QMessageBox.warning(self, "Run XCMS or Load a File!", rMsg )

    def loadRPY2Batch(self):
        print "Batch Button Load Clicked"

    def getThreadEIC(self, eicClass):
        if eicClass != None:
            self.eicClass = eicClass
            self.updateGUI()

    def indexChanged(self, index):
        if self.ignoreSignal:
            return
        else:
            self.plotIndex = index
#            print self.plotIndex
            QtCore.QTimer.singleShot(750,  self.plotByIndex)

    def add2ROutput(self, rVector):
        for item in rVector:
            self.RoutputTE.append(item)
        self.RoutputTE.append("\n")

    def plotByIndex(self):
        self.curIndex = self.plotIndex#need to do this because the slider is going from 1 and python counts from 0
        self.curEIC = self.eicClass.eicTraces[self.curIndex]
        self.plotEIC(self.curEIC)

    def plotEIC(self, eicTrace):
        self.eicPlot.cla()
        curGroup = eicTrace.keys()[0]
        dataList = eicTrace.values()[0]
        metaDict = dataList[0]
        dataDict = dataList[1]
        mzlo = metaDict['mzlo']
        mzhi = metaDict['mzhi']
        sampNames = dataDict.keys()

        for name in sampNames:
            eic = dataDict[name]
            xdata = eic['xdata']
            ydata = eic['ydata']
            self.eicPlot.plot(xdata, ydata, label = name)
        if self.plotLegendCB.isChecked():
            self.eicPlot.legend(axespad = 0.03, pad=0.25)
        self.eicPlot.set_title('EIC from %.2f to %.2f m/z'%(mzlo, mzhi))
        self.plotWidget.canvas.xtitle = 'Time (s)'
        self.plotWidget.canvas.ytitle ='Arbitrary Intensity'
        self.plotWidget.canvas.format_labels()
        self.plotWidget.canvas.draw()
        self.plotWidget.setFocus()


    def updateROutput(self, StrOutput):
        if  len(StrOutput)>5:
            self.RoutputTE.append(StrOutput)
        else:
            self.RoutputTE.insertPlainText(StrOutput)
            self.RoutputTE.insertPlainText('\t')

    def updateGUI(self):
        numEICs = self.eicClass.numEICs
        self.eicIndexSlider.setMaximum(numEICs-1)
        self.eicIndexSB.setMaximum(numEICs-1)
        self.eicIndexSB.setValue(0)

    def startXCMSRun(self):
        self.dirListWidget.selectAll()
        fileList = self.dirListWidget.selectedItems()
        if len(fileList)>0:
            self.fileList = []
            for entry in fileList:
                self.fileList.append(str(entry.toolTip()))#we use the tooltip as it contains the full path
            if self.rtTypeCB.isChecked():
                if self.rThread.updateThread(self.fileList, self.xcmsParamDict, self.rtWidthSB.value()):
                    self.rThread.start()
            else:
                if self.rThread.updateThread(self.fileList, self.xcmsParamDict, self.rtWidthSB.value(), corType = 'raw'):
                    self.rThread.start()
#            print fileList
        print 'Start XCMS'

    def testXCMS(self):
        r = ro.r
        a = r('cdfpath = system.file("cdf", package = "faahKO")')
        cdfpath = ri.globalEnv.get("cdfpath")
        r('cdffiles = list.files(cdfpath, recursive = TRUE, full.names = TRUE)')
        r('cdffiles = cdffiles[1:3]')
        cdffiles = ri.globalEnv.get("cdffiles")
        cdfList = list(cdffiles)

        if len(cdffiles) == 0:
            rMsg = 'Open R and enter the following:\nsource("http://bioconductor.org/biocLite.R")\nbiocLite("faahKO")'
            return QtGui.QMessageBox.warning(self, "Error with Test Data", rMsg )
        if self.rThread.updateThread(cdfList, self.xcmsParamDict, self.rtWidthSB.value()):
            self.rThread.start()

    def showParamHelp(self, emitString):
        curMethod = str(self.xcmsMethodCB.currentText())
        xcmsSetHelp = ro.r.help("xcmsSet", htmlhelp = True)
        print xcmsSetHelp
        if curMethod == 'Matched Filter':
            methodHelp = ro.r.help("findPeaks.matchedFilter", htmlhelp = True)
            print methodHelp
        elif curMethod == 'CentWave':
            methodHelp = ro.r.help("findPeaks.centWave", htmlhelp = True)
            print methodHelp

    def _getDir_(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, '', self.curDir)
        directory = str(directory)
        if directory != None:
            self.curDir = directory
        else:
            self.curDir = os.getcwd()

    def setupGUI(self):
        self.xcmsMethodCB.addItems(self.xcmsParamDict.keys())
        self.eicIndexSlider.setMaximum(0)
        self.eicIndexSB.setMaximum(0)

    def paramTableEntered(self, tableItem):
        if self.paramTableWidget.currentColumn() == 0:
            QtGui.QTableWidget
            nextItem = self.paramTableWidget.item(self.paramTableWidget.currentRow(), 1)
            self.paramTableWidget.editItem(nextItem)
            return QtGui.QMessageBox.warning(self, "",  "Don't do that Dave.")
        else:
            pass

    def paramTableChanged(self, tableItem):
        '''
        This method accepts the new value for a given parameter
        checkes to see if it is the same type as the original,
        if not then return to the original value.
        '''
        if self.paramTableWidget.currentColumn() > 0:
            curParam = str(self.paramTableWidget.item(tableItem.row(), 0).text())
            curType = self.curTypeDict[curParam]
            try:
                tempVal = curType(str(tableItem.text()))
            except:
                origVal = self.curParamDict[curParam]
                tableItem.setText(str(origVal))
            tempVal = curType(str(tableItem.text()))
            self.curParamDict[curParam] = tempVal
            print self.curParamDict

    def updateParamTable(self, selectText):
        self.curParamDict = self.xcmsParamDict[str(selectText)]
        self.curTypeDict = self.xcmsTypeDict[str(selectText)]
        curParams = self.curParamDict.items()
        curParams.sort()
        self.paramTableWidget.clear()
        self.paramTableWidget.addData(curParams)


    def initFileList(self):
        if not self.firstLoad:
            #reinitialize GUI and spectrumList
            #need to reset GUI
            print "Need to reset GUI"
#            self.setupGUI()
        self._getDir_()
        dirList, startDir = FP.Load_mzXML_Folder(self.curDir)
        if startDir != None:
            if os.path.exists(startDir):
                self.curDir = startDir
                self.curFolderLE.setText(self.curDir)
                self.eicCurFolderLE.setText(self.curDir)
#        print startDir
        if len(dirList) !=0:
            self.dirList = dirList
            self.loadOk = True
            self.firstLoad = False
            self.addFiles()
#            self.dirListWidget.addItems(self.dirList)
#            if self.readThread.updateThread(dirList,  loadmzXML = True):
#                self.readThread.start()
        elif startDir != None:
            return QtGui.QMessageBox.warning(self, "No Data Found",  "Check selected folder, does it have any data?")

    def addFiles(self):
        self.dirListWidget.clear()
        for item in self.dirList:
            #####Text Color Handler
            if self.colorIndex%len(COLORS) == 0:
                self.colorIndex = 0
                self.txtColor = COLORS[self.colorIndex]
                self.colorIndex +=1
            else:
                self.txtColor = COLORS[self.colorIndex]
                self.colorIndex +=1

            fileName = os.path.basename(item)
            tempItem = QtGui.QListWidgetItem(fileName)
            tempColor = QtGui.QColor(self.txtColor)
            tempItem.setTextColor(tempColor)
            tempItem.setToolTip(item)
            #self.specListWidget.addItem(loadedItem.name)
            self.dirListWidget.addItem(tempItem)

    def __askConfirm__(self,title,message):
        clickedButton = QtGui.QMessageBox.question(self,\
                                                   title,message,\
                                                   QtGui.QMessageBox.Yes,QtGui.QMessageBox.Cancel)
        if clickedButton == QtGui.QMessageBox.Yes: return True
        return False

    def closeEvent(self,  event = None):
        try:
            ri.endr()
        except:
            pass

##########Begin Ashoka Progress Bar Code....
    def layoutStatusBar(self):
        self.progressBar = QtGui.QProgressBar()
        self.statusLabel = QtGui.QLabel("Ready")
#        self.statusLabel.setMinimumSize(self.statusLabel.sizeHint())
        self.statusLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.statusLabel.setText("Ready")
        self.statusbar.addPermanentWidget(self.statusLabel)
        self.progressBar.setTextVisible(False)
        self.progressBar.setRange(0,100)
        self.progressBar.setValue(0)
        self.progressBar.setFixedHeight(15)
        self.progressBar.setFixedWidth(100)
        self.toggleProgressBar(False)
        self.statusbar.addWidget(self.progressBar)

    def resetProgressBar(self):
        self.setProgressValue(0)
        self.toggleProgressBar(False)

    def setStatusLabel(self, text):
        self.statusLabel.setText(text)

    def showStatusMessage(self, text, stime):
        self.statusBar().showMessage(text, stime)

    def setProgressValue(self, val):
        self.progressBar.setValue(val)

    def toggleProgressBar(self, toggle):
        self.progressBar.setVisible(toggle)

    def threadProgress(self, progVal):
        self.setStatusLabel("Fitting Peaks, %d segments completed." % progVal)
        newVal = int(100*(progVal/self.progressMax))
        self.setProgressValue(newVal)
#        self.AddMessage2Tab("  %d Iterations Done." % progVal)
#        print progVal, newVal, self.progressMax

    def PCTProgress(self, updateString):
        self.setStatusLabel(updateString)


def run_main():
    app = QtGui.QApplication(sys.argv)
    ui = pyXCMSWindow()
#    plot = Plot_Widget()
    ui.show()
    sys.exit(app.exec_())
#    app = QtGui.QApplication(sys.argv)
#    MainWindow = QtGui.QMainWindow()
##    try:
#    ui = pyXCMSWindow(MainWindow)
#    MainWindow.show()
#    except:
#        errorMsg = "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
#        errorMsg+='\n Contact Clowers and try to remember what you did to make it crash!'
#        QtGui.QMessageBox.warning(MainWindow, "Fatal Error",  errorMsg)

    sys.exit(app.exec_())


if __name__ == "__main__":
    run_main()