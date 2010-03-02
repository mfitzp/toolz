
import os, sys, traceback
import time
import numpy as N
import scipy as S

from PyQt4 import QtCore, QtGui

from mpl_pyqt4_widget import MPL_Widget
from mzXMLReader import mzXMLDoc
from xtandemParser import XT_RESULTS


import main_ui

'''
/usr/bin/pyuic4 /home/clowers/workspace/SpecDigger/src/main.ui  -o /home/clowers/workspace/SpecDigger/src/main_ui.py
'''

COLORS = ['#A3293D','#3B9DCE','#293DA3','#5229A3','#297AA3','#8F29A3','#A3297A',
'#7AA329','#3DA329','#29A352','#29A38F','#A38F29','#3B9DCE','#6CB6DA','#CE6C3B','#DA916C',
'#0080FF','#0000FF','#7ABDFF','#8000FF','#FF0080','#FF0000','#FF8000','#FFFF00','#A35229','#80FF00',
'#00FF00','#00FF80','#00FFFF','#3D9EFF','#FF9E3D','#FFBD7A']



class specDigger(main_ui.Ui_MainWindow):
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        main_ui.Ui_MainWindow.setupUi(self,MainWindow)

        #self.__updatePlotScripts__()
        self.__addWidgets__()
        #self.__additionalVariables__()
        self.__setConnections__()
        self.__setMessages__()
        #self.__initContextMenus__()
#        self.__setupChrom__()
#        self.__setupMZ__()
        self.startup()
        self.__testFunc__()
        self.drawProfile = False

    def __testFunc__(self):
        self.setDataFile()
        self.setXTResults()
        self.plotMZXML()
        self.plotXTVals()
        self.updatePlotWidget()

    def __addWidgets__(self):
        self.plotTabLayout = QtGui.QHBoxLayout(self.plotTab)
        self.plotWidget = MPL_Widget(parent = self.MainWindow, enableAutoScale = False, doublePlot = True, enableEdit = True, shareAxis = True)
        self.plotTabLayout.addWidget(self.plotWidget)

    def __setConnections__(self):
#        self.hZoom = QtGui.QAction("Horizontal Zoom",  self.MainWindow)
#        self.hZoom.setShortcut("Ctrl+Z")
#        self.spectrumTabWidget.addAction(self.hZoom)
#        QtCore.QObject.connect(self.hZoom,QtCore.SIGNAL("triggered()"), self.hZoomToggle)
#
#        self.actionAutoScale = QtGui.QAction("AutoScale",  self.MainWindow)
#        self.actionAutoScale.setShortcut("Ctrl+A")
#        self.spectrumTabWidget.addAction(self.actionAutoScale)
#        QtCore.QObject.connect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)
#
#        self.actionAutoScaleChrom = QtGui.QAction("Autoscale",  self.chromWidget)
#        self.chromWidget.addAction(self.actionAutoScaleChrom)
#        self.actionAutoScaleChrom.setShortcut("Ctrl+Shift+A")
#        QtCore.QObject.connect(self.actionAutoScaleChrom,QtCore.SIGNAL("triggered()"), self.autoscaleChrom)
#
#        self.hZoomChrom = QtGui.QAction("Horizontal Zoom",  self.chromWidget)
#        self.chromWidget.addAction(self.hZoomChrom)
#        self.hZoomChrom.setShortcut("Ctrl+Shift+Z")
#        QtCore.QObject.connect(self.hZoomChrom,QtCore.SIGNAL("triggered()"), self.hZoomToggleChrom)

#        self.removeFileAction = QtGui.QAction("Remove File",  self.spectra_CB)
#        self.spectra_CB.addAction(self.removeFileAction)
#        QtCore.QObject.connect(self.removeFileAction, QtCore.SIGNAL("triggered()"), self.removeFile)

#        self.actionToggleDraw = QtGui.QAction("Toggle Draw Style",  self.spectrumTabWidget)
#        self.spectrumTabWidget.addAction(self.actionToggleDraw)
#        self.actionToggleDraw.setShortcut("Ctrl+D")
#        QtCore.QObject.connect(self.actionToggleDraw,QtCore.SIGNAL("triggered()"), self.toggleDraw)
#
#        self.actionScanUp = QtGui.QAction("",  self.chromWidget)
#        self.chromWidget.addAction(self.actionScanUp)
#        self.actionScanUp.setShortcut("Up")
#        QtCore.QObject.connect(self.actionScanUp,QtCore.SIGNAL("triggered()"), self.scanUp)
#
#        self.actionScanDown = QtGui.QAction("",  self.chromWidget)
#        self.chromWidget.addAction(self.actionScanDown)
#        self.actionScanDown.setShortcut("Down")
#        QtCore.QObject.connect(self.actionScanDown,QtCore.SIGNAL("triggered()"), self.scanDown)


        '''File menu actions slots'''
        QtCore.QObject.connect(self.action_Open,QtCore.SIGNAL("triggered()"),self.__openDataFile__)
#        QtCore.QObject.connect(self.actionFileOpen,QtCore.SIGNAL("triggered()"),self.__readDataFile__)
#        QtCore.QObject.connect(self.actionAbout,QtCore.SIGNAL("triggered()"),self.__showAbout__)
#        QtCore.QObject.connect(self.actionHints,QtCore.SIGNAL("triggered()"),self.__showHints__)
#        QtCore.QObject.connect(self.actionRunScript,QtCore.SIGNAL("triggered()"),self.__showHints__)
#        QtCore.QObject.connect(self.action_Exit,QtCore.SIGNAL("triggered()"),self.__exitProgram__)
#        QtCore.QObject.connect(self.spectrumTabWidget,QtCore.SIGNAL("currentChanged(int)"),self.updateMZTab)
#        #this method is called when spectrum index is changed
#        QtCore.QObject.connect(self.spectra_CB,QtCore.SIGNAL("currentIndexChanged (QString)"),self.setupDataFile)
#
#        QtCore.QObject.connect(self.xicList_CB,QtCore.SIGNAL("currentIndexChanged (QString)"),self.setupXIC)
#        QtCore.QObject.connect(self.getXIC_Btn,QtCore.SIGNAL("clicked()"),self.getXIC)
#
#
#        #I know this scaling mechanism is a hack but in order to allow for the axvlines to work appropriately this will have to do.
#        QtCore.QObject.connect(self.mzWidget,QtCore.SIGNAL("autoScaleAxis(bool)"),self.scaleYAxis)

        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

        #self.xicList_CB.setDuplicatesEnabled(False)

    def __openDataFile__(self):
#        if self.firstLoad:
        dataFileName = QtGui.QFileDialog.getOpenFileName(self.MainWindow,\
                                                         self.OpenDataText,\
                                                         self.__curDir, 'mzXML (*.mzXML);;mzML (*.mzML)')
        if dataFileName:
            self.loadFile(dataFileName)


#        else:
##            if self.__askConfirm__("Data Reset",self.ResetAllDataText):
#            self.startup()
#            dataFileName = QtGui.QFileDialog.getOpenFileName(self.MainWindow,\
#                                                                 self.OpenDataText,\
#                                                                 self.__curDir, 'mzXML (*.mzXML);;mzML (*.mzML)')
#            if dataFileName:
#                self.loadFile(dataFileName)

    def updatePlotWidget(self):
        self.plotWidget.canvas.format_labels()
        self.plotWidget.canvas.draw()

    def plotXTVals(self):
        self.XTax.vlines(self.xtScanVals, 0, self.scanScores*-1, color='k', lw = 2.0, linestyles='solid')#, alpha = 0.1)
        self.XTax.vlines(self.xtScanVals, 0, self.nextScores*-1, color='r', lw = 2.0, linestyles='solid')#, alpha = 0.7)
        self.XTax.set_ylim((-100,0))
        self.XTax.grid(True)

    def plotMZXML(self):
        if len(self.BPC)>=1:
            self.mzXMLax.plot(self.scanVals, self.BPC, '-ob', ms =2, picker = 5, alpha = 0.5)
            hitIND = []
            for scan in self.xtScanVals:
                curHit = N.where(self.scanVals<scan)[0][-1]#xtXML.dataDict['scanID'] == scanVals)
                #print 'CurHit', curHit
                hitIND.append(curHit)
            self.handleA,  = self.mzXMLax.plot([0], [0], 'o', ms=8, alpha=0.5, color='yellow', visible=False, label = 'Cursor A')
            self.mzXMLax.plot(self.xtScanVals, self.BPC[N.array(hitIND)], 'og', ms = 5, alpha = 0.6)
            self.mzXMLax.grid(True)

    def setDataFile(self):
        self.curDataFileName = 'R19.mzXML'
        if os.path.isfile(self.curDataFileName):

    #        try:
            t0 = time.clock()
            self.curDataFile = mzXMLDoc(self.curDataFileName, sumBool = False)
            print "%s Load Time: %.4f s"%(self.curDataFileName, time.clock()-t0)
            self.BPC = N.array(self.curDataFile.data.get('BPC'))
            self.scanVals = N.array(self.curDataFile.data.get('expTime'), dtype = N.int32)
    #        except:
    #            print "mzXML Failure"
        else:
            print "%s is not a File"%self.curDataFileName

    def setXTResults(self):
        self.curXTFileName = 'R19.xml'
#        try:
        t0 = time.clock()
        self.curXTResults = XT_RESULTS(self.curXTFileName)
        self.xtScanVals = self.curXTResults.dataDict['scanID']
        self.scanScores = self.curXTResults.dataDict['hScore']
        self.nextScores = self.curXTResults.dataDict['deltaH']
        print "%s Load Time %.4f s"%(self.curXTFileName, time.clock()-t0)
#        except:
#            print "XT Result Failure"

    def __setMessages__(self):
        '''This function is obvious'''
        self.SaveDataText = "Choose a name for the data file to save:"
        self.ScratchSavePrompt = "Choose file name to save the scratch pad:"
        self.OpenDataText = "Choose a data file to open:"
        self.ResetAllDataText = "This operation will reset all your data.\nWould you like to continue?"

    def __exitProgram__(self):
        if self.okToExit():
            self.MainWindow.close()

    def okToExit(self):
        reply = QtGui.QMessageBox.question(self.MainWindow, "Confirm Quit", "Exit now?",\
                                           QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            return True
        else:
            return False

    def __askConfirm__(self,title,message):
        clickedButton = QtGui.QMessageBox.question(self.MainWindow,\
                                                   title,message,\
                                                   QtGui.QMessageBox.Yes,QtGui.QMessageBox.Cancel)
        if clickedButton == QtGui.QMessageBox.Yes: return True
        return False

    def __showHints__(self):
        return QtGui.QMessageBox.information(self.MainWindow,
                                             ("Hints and Known Issues"),
                                             ("<p> 1.    For files that contain spectra with a high degree of detail (i.e. not centroided (stick) mass spectra) use the profile mode for drawing (Ctrl+D).  Otherwise, the plotting will be slow.</p>"
                                             "<p> 2. I haven't incorporated MS^n (where n >= 3) spectrum views at this point--I didn't have an example file to test.</p>"
                                             "<p>3.  If the program is too slow, remember python is not or ever intended to be C.</p>"
                                             "<p>4.  I have not incorporated a reader for mzData files as this format does not explictly store base peak and TIC values for chromatogram generation.  In order to do this each scan must be read simply to construct the TIC/BPC.  This is very slow.  The new mzML format will be supported in the very near future.</p>"
                                             "<p>4.  Ctrl+Z enables/disables zooming, Ctrl+A zooms out entirely (i.e. autoscale).  These shortcuts are by far the easiest way to navigate</p>"
                                             ""))

    def __showAbout__(self):
        return QtGui.QMessageBox.information(self.MainWindow,
                                            ("mzViewer V.0.5, October, 2009"),
                                            ("<p><b>mzViewer</b> was written in Python by Brian H. Clowers (bhclowers@gmail.com).</p>"
        "<p>Please keep in mind that the entire effort is very much a"
        " work in progress and that Brian won't quit his day job for programming."
        " The original purpose of mzViewer was to provide a user-friendly, open-source tool"
        " for examining common mass spectrometry data formats (e.g. mzXML and mzML* (*in the future)"
        " using numpy and matplotlib.  Feel free to update"
        " (preferably with documentation) mzViewer and please share your contributions"
        " with the rest of the community.</p>"))


    def startup(self):

        self.mzXMLax = self.plotWidget.canvas.ax
        self.XTax = self.plotWidget.canvas.ax2

        self.BPC = None#base peak chromatogram from the mzXML file
        self.expTime = None#experiment time


        self.xtScanVals = None#indices from the main scan where a DB hit was found
        self.hitScans = None#indices from the main scan where a DB hit was found
        self.scanScores = None#primary score values from the DB
        self.nextScores = None#the next closets score from the DB
#        self.curFile = None
#        self.curFileName = None
#        self.basePeak = True
#        self.TIC = False
#        self.curParentScan = None
#        self.chromLine = None
#        self.bpcOk = True
#        self.curLine = None
#        self.curScanInfo = None
#        self.curScanId = None
#        self.curIndex = None
#        self.ignoreSignal = False
#        self.tempIndex = None
#        self.yMax = 1.0#will be the maximum for the Y scale after autozoom
#        self.fragScanList = []
#        self.fragPlotList = []
#        self.fragTabDict = {}
#        self.xicDict = {}
#        self.scanInfoList = []
#        self.fragPlotted = 0#used to keep track of whether or not a fragment has been plotted
#        self.fragIndex = None
#
#        self.drawProfile = False
#        self.tableWidget.clear()
#
#        self.spectrumTabWidget.setCurrentIndex(0)
#        numTabs = self.spectrumTabWidget.count()
#        j=1
#        for i in range(1, numTabs):#this is a weird loop because each time you kill a tab it reorders the whole bunch
#            self.spectrumTabWidget.removeTab(j)
#
#        self.__setupChrom__()
#        self.__setupMZ__()
#
#        self.chromWidget.canvas.mpl_connect('pick_event', self.OnPickChrom)
#        self.mzWidget.canvas.mpl_connect('pick_event', self.OnPickMZ)





def run_main():
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = specDigger(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_main()