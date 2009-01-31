import sys
import os, os.path
from PyQt4 import QtCore, QtGui

#try:#this is done because sometimes there is an annoying message regard tk that come up
import rpy2.robjects as ro
import rpy2.rinterface as ri
#except:
#    pass



import ui_main
import FolderParse as FP

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
            errorMsg ='Error loading R library %s\nCheck Library Installation'%lib
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
#        self.MainWindow = MainWindow
#        ui_main.Ui_MainWindow.setupUi(self, MainWindow)

        self.__initVars()
        self.__initConnections()
        self.setupGUI()

#        self.paramTableWidget.addData(test_data)
#        ro.r.library("xcms")
#        print ro.r.help("xcmsSet")


    def __initVars(self):
        self.firstLoad = True
        self.colorIndex = 0
        self.txtColor = None
        self.curDir = os.getcwd()
        self.Rliblist = ['xcms']
        self.Rlibs = initRlibs(self.Rliblist)
        self.EICList = None
        self.xcmsOK = False

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
                                    'step':0.1,
                                    'steps':2.,
                                    'mzdiff':0.1
                                    }
        self.matchedFilterTypes = {'fwhm':float,
                                   'sigma':float,
                                   'max':float,
                                   'snthresh':float,
                                   'step':float,
                                   'steps':float,
                                   'mzdiff':float
                                    }
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
        self.xcmsGroupDict = {'Matched Filter':self.matchedFilterParams,
                               'CentWave':self.centWaveParams}
        self.xcmsTypeDict = {'Matched Filter':self.matchedFilterTypes,
                               'CentWave':self.centWaveTypes}


    def __initConnections(self):
        QtCore.QObject.connect(self.getFolderBtn, QtCore.SIGNAL("clicked()"), self.initFileList)
        QtCore.QObject.connect(self.xcmsMethodCB, QtCore.SIGNAL("currentIndexChanged(QString)"), self.updateParamTable)
        QtCore.QObject.connect(self.paramTableWidget, QtCore.SIGNAL("itemDoubleClicked(QTableWidgetItem*)"), self.paramTableEntered)
        QtCore.QObject.connect(self.paramTableWidget, QtCore.SIGNAL("itemChanged(QTableWidgetItem*)"), self.paramTableChanged)
        QtCore.QObject.connect(self.paramTableWidget, QtCore.SIGNAL("helpRequested(PyQt_PyObject)"), self.showParamHelp)

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
        self.xcmsMethodCB.addItems(self.xcmsGroupDict.keys())
        self.eicIndexSlider.setMaximum(0)
        self.eicIndexSB.setMaximum(0)

    def paramTableEntered(self, tableItem):
        if self.paramTableWidget.currentColumn() == 0:
            QtGui.QTableWidget
            nextItem = self.paramTableWidget.item(self.paramTableWidget.currentRow(), 1)
            self.paramTableWidget.editItem(nextItem)
#            self.paramTableWidget.releaseMouse()
#            self.paramTableWidget.setCurrentCell(self.paramTableWidget.currentRow(), 1)
            return QtGui.QMessageBox.warning(self, "",  "Don't do that Dave.")
#            self.dirListWidget.setFocus()
        else:
            pass

    def paramTableChanged(self, tableItem):
        if self.paramTableWidget.currentColumn() > 0:
            curMethod = str(self.xcmsMethodCB.currentText())
            curTypeDict = self.xcmsTypeDict[curMethod]
            curParam = str(self.paramTableWidget.item(tableItem.row(), 0).text())
            curType = curTypeDict[curParam]
            try:
                tempVal = curType(str(tableItem.text()))
            except:
                origVal = self.xcmsGroupDict[curMethod][curParam]
                tableItem.setText(str(origVal))
#            tempType = type()
#            tempVal = curType(str(tableItem.text()))
            print curMethod, curParam
#        curParam = str(self.paramTableWidget.item(self.paramTableWidget.currentRow(), 0).text())
#        curType = curTypeDict[curParam]
#        tempVal = curType(tableItem.text())
#        print tempVal, type(tempVal)
#        print tableItem.text()
#        self.item(self.currentRow(),0).text()

    def updateParamTable(self, selectText):
        curParams = self.xcmsGroupDict[str(selectText)].items()
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