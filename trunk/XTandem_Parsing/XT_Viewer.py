
"""
This is the explicit class for viewing Parsed XT Files
"""
#Importing built-in python modules and functions
import sys, os
from os import walk,  path
import base64
import struct
import string

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog,  QApplication

from matplotlib import rc, rcParams, use, interactive
use('Qt4Agg')

import numpy as N

#import matplotlib as mymat
from matplotlib.backends import backend_qt4, backend_qt4agg
backend_qt4.qApp = QtGui.qApp
#backend_qt4agg.matplotlib = mymat

    
#from io import hdfIO
from matplotlib.lines import Line2D
from matplotlib.widgets import SpanSelector
#import GUI scripts
import ui_main
from mpl_custom_widget import MPL_Widget
from xtandem_parser_class import XT_xml
import dbIO
#try:
#    import psyco
#    psyco.full()
#except:
#    print "Pysco not installed, try easy_install psyco at your command prompt"

class XTViewer(ui_main.Ui_MainWindow):
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        ui_main.Ui_MainWindow.setupUi(self,MainWindow)
        
        self.__additionalVariables__()
        self.__additionalConnections__()
        self.__setMessages__()
        self.__initContextMenus__()
        self.__setupPlot__()
        self.startup()
        
        self.drawProfile = True
    
 
    def startup(self):

        self.curFile = None
        self.curFileName = None
        self.pep_eVal=[]
        self.ppmlist=[]
        self.peplenlist=[]
        self.pepseqlist=[]
        self.deltascore=[]
        
        self.drawProfile = True
        
        self.plotTabWidget.setCurrentIndex(0)
        
        self.__setupPlot__()


        self.plotWidget.canvas.mpl_connect('pick_event', self.OnPickPlot)

    def loadFileXT(self,  filename):
        if filename:
            self.fileType= str(filename).split('.')[-1]
        if self.fileType == 'xml':
            self.curFile = XT_xml(filename)
            self.initiatePlot()
            self.firstLoad = False
            
        elif self.fileType == 'h5':
            self.curFile = XT_xml(filename,  parseFile = False)
            dbIO.load_XT_HDF5(str(filename), self.curFile)
            self.initiatePlot()
            self.firstLoad = False
            
        elif self.fileType == 'db':
            self.curFile = XT_xml(filename,  parseFile = False)      
            sqldb = dbIO.XTandemDB(str(filename), "testTables", createNew = False)#NEED TO FIX THE NAME
            sqldb.get_XTValues(sqldb.curTblName, self.curFile)
            sqldb.close()  
            self.initiatePlot()
            self.firstLoad = False
            
        else:
            return QtGui.QMessageBox.information(self.MainWindow,'', "Problem loading data, check file")
        

    def __readDataFile__(self):
        if self.firstLoad:
            dataFileName = QtGui.QFileDialog.getOpenFileName(self.MainWindow,\
                                                             self.OpenDataText,\
                                                             self.__curDir, 'X!Tandem XML (*.xml);; HDF5 File (*.h5);;SQLite Database (*.db)')
            if dataFileName:
                self.loadFileXT(dataFileName)
                
        else:
            if self.__askConfirm__("Data Reset",self.ResetAllDataText):
                self.plotWidget.canvas.ax.cla()
                #self.chromWidget.canvas.ax.cla()
                self.startup()
                dataFileName = QtGui.QFileDialog.getOpenFileName(self.MainWindow,\
                                                                 self.OpenDataText,\
                                                                 self.__curDir, 'X!Tandem XML (*.xml);; HDF5 File (*.h5);;SQLite Database (*.db)')
                if dataFileName:
                    self.loadFileXT(dataFileName)
    
    def __saveDataFile__(self):
        saveFileName = QtGui.QFileDialog.getSaveFileName(self.MainWindow,\
                                                             self.SaveDataText,\
                                                             self.__curDir, 'HDF5 File (*.h5);;SQLite Database (*.db)')
        if saveFileName:
            if self.curFile:
                #print "File name is: %s" % (str(self.curFileName))
                fileType= str(saveFileName).split('.')[-1]
                if fileType=='h5':
                    dbIO.save_XT_HDF5(str(saveFileName),  self.curFile)
                elif fileType == 'db':
                    sqldb = dbIO.XTandemDB(str(saveFileName), "testTables")#NEED TO FIX THE NAME
                    sqldb.INSERT_XT_VALUES(sqldb.curTblName, self.curFile)
                    sqldb.close()
            else:
                return QtGui.QMessageBox.information(self.MainWindow,'', "A X!Tandem File must be loaded first before saving")
    
    def OnPickPlot(self, event):
        self.pickIndex = event.ind[0]
        try:
            self.textHandle.remove()
        except:
            pass
        self.handleA.set_data(N.take(self.x, [self.pickIndex]), N.take(self.y, [self.pickIndex]))
        self.handleA.set_visible(True)
        showText = '%s'%(self.curFile.dataDict.get('pepIDs')[self.pickIndex])
        self.textHandle = self.plotWidget.canvas.ax.text(0.03, 0.95, showText, fontsize=9,\
                                        bbox=dict(facecolor='yellow', alpha=0.1),\
                                        transform=self.plotWidget.canvas.ax.transAxes, va='top')
        self.plotWidget.canvas.draw()

        
    def __setupPlot__(self):
        self.handleA,  = self.plotWidget.canvas.ax.plot([0], [0], 'o',\
                                        ms=8, alpha=.5, color='yellow', visible=False,  label = 'Cursor A')
        self.is_hZoomChrom = False

        self.is_hZoom = False
    
    def initiatePlot(self):
#        for item in self.curFile.pep_results:
#            self.pep_eVal.append(item.pep_eVal)
#            self.ppmlist.append(item.ppm)
#            self.peplenlist.append(len(item.pep_seq)**1.5)
#            self.pepseqlist.append(item.pep_seq)
#            self.deltascore.append((item.hscore - item.nextscore))
#            
#        self.pep_eVal = N.array(self.pep_eVal)
#        self.ppmlist = N.array(self.ppmlist)
#        self.peplenlist = N.array(self.peplenlist)
#        self.deltascore = N.array(self.deltascore)
#        self.pep_results = []
#        self.ppm_errors = []
#        self.theoMZs = []
#        self.scanID = []
#        self.pro_eVals=[]
#        self.prot_IDs = []
#        self.pep_eValues=[]
#        self.pep_seqs = []
#        self.hScores = []
#        self.nextScores = []
        
        self.x = self.curFile.dataDict.get('pep_eValues')
        self.y = (self.curFile.dataDict.get('hScores')-self.curFile.dataDict.get('nextScores'))
        sizeList = self.curFile.dataDict.get('pepLengths')**1.5
        self.plotScatter = self.plotWidget.canvas.ax.scatter(self.x, self.y,  s = sizeList,  alpha = 0.3,  picker = 5)
        
        self.plotWidget.canvas.ax.set_xscale('log')
        xmin = N.min(self.curFile.dataDict.get('pep_eValues'))/10
        xmax = N.max(self.curFile.dataDict.get('pep_eValues'))*10
        self.plotWidget.canvas.ax.set_xlim(xmin, xmax)        
        
        self.plotWidget.canvas.xtitle="Peptide e-Value"
        self.plotWidget.canvas.ytitle="Delta e-Value"
        self.plotWidget.canvas.PlotTitle = self.curFile.fileName
        self.plotWidget.canvas.format_labels()
        self.plotWidget.canvas.draw()
    
   
    
    def updateScanInfo(self):
        n = 0
        for item in self.curScanInfo.iteritems():
            m = 0
            for entry in item:
                newitem = QtGui.QTableWidgetItem(entry)
                self.tableWidget.setItem(n,  m,  newitem)
                m+=1
            n+=1

    
    def ZoomToggle(self):
        self.plotWidget.toolbar.zoom()
    
    def onselect(self, xmin, xmax):
            #print xmin,  xmax
            if self.is_hZoom:
                self.plotWidget.canvas.ax.set_xlim(xmin,  xmax)
                self.plotWidget.canvas.draw()
                
    def autoscale_plot(self):
        self.plotWidget.toolbar.home()
        #self.rescale_plot()
        #self.plotWidget.canvas.ax.autoscale_view(tight = False, scalex=True, scaley=True)
        #self.mzWidget.canvas.ax.set_ylim(self.mzYScale[0], self.mzYScale[1])
        #self.plotWidget.canvas.draw()
    
    def toggleDraw(self):
        if self.drawProfile:
            self.drawProfile = False
            self.getMZScan(self.indexA)
            print "Profile Draw Disabled"
        else:
            self.drawProfile = True
            self.getMZScan(self.indexA)
            print "Profile Draw Enabled"
            
    def __initContextMenus__(self):
        #self.mzWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.plotTabWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.chromWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.mzWidget.connect(self.mzWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.mzWidgetContext)
        #self.chromWidget.connect(self.chromWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.chromWidgetContext)
        self.plotTabWidget.connect(self.plotTabWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.plotTabContext)

#    def mzWidgetContext(self, point):
#        '''Create a menu for mzWidget'''
#        mzct_menu = QtGui.QMenu("Menu", self.mzWidget)
#        mzct_menu.addAction(self.hZoom)
#        mzct_menu.addAction(self.actionAutoScale)
#        mzct_menu.exec_(self.mzWidget.mapToGlobal(point))
#    
#    def chromWidgetContext(self, point):
#        '''Create a menu for mzWidget'''
#        chromct_menu = QtGui.QMenu("Menu", self.chromWidget)
#        chromct_menu.addAction(self.hZoomChrom)
#        chromct_menu.addAction(self.actionAutoScaleChrom)
#        chromct_menu.exec_(self.chromWidget.mapToGlobal(point))
    
    def plotTabContext(self, point):
        '''Create a menu for plotTabWidget'''
        plotCT_menu = QtGui.QMenu("Menu", self.plotTabWidget)
        plotCT_menu.addAction(self.hZoom)
        plotCT_menu.addAction(self.actionAutoScale)
        #plotCT_menu.addAction(self.actionToggleDraw)
        plotCT_menu.exec_(self.plotTabWidget.mapToGlobal(point))
      
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

    def __additionalVariables__(self):
        '''Extra variables that are utilized by other functions'''
        self.__curDir = os.getcwd()
        self.firstLoad = True

    def __additionalConnections__(self):
        self.hZoom = QtGui.QAction("Zoom",  self.MainWindow)
        self.hZoom.setShortcut("Ctrl+Z")
        self.plotTabWidget.addAction(self.hZoom)
        QtCore.QObject.connect(self.hZoom,QtCore.SIGNAL("triggered()"), self.ZoomToggle)
        
        self.actionAutoScale = QtGui.QAction("AutoScale",  self.MainWindow)
        self.actionAutoScale.setShortcut("Ctrl+A")
        self.plotTabWidget.addAction(self.actionAutoScale)
        QtCore.QObject.connect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)

#        self.actionSave = QtGui.QAction("Save File",  self.MainWindow)
#        self.actionSave.setShortcut("Ctrl+S")
#        self.MainWindow.addAction(self.actionSave)
#        QtCore.QObject.connect(self.actionSave,QtCore.SIGNAL("triggered()"), self.__saveDataFile__)

#        self.actionAutoScaleChrom = QtGui.QAction("Autoscale",  self.chromWidget)
#        self.chromWidget.addAction(self.actionAutoScaleChrom)
#        self.actionAutoScaleChrom.setShortcut("Ctrl+Shift+A")
#        QtCore.QObject.connect(self.actionAutoScaleChrom,QtCore.SIGNAL("triggered()"), self.autoscaleChrom)
#        
#        self.hZoomChrom = QtGui.QAction("Horizontal Zoom",  self.chromWidget)
#        self.chromWidget.addAction(self.hZoomChrom)
#        self.hZoomChrom.setShortcut("Ctrl+Shift+Z")
#        QtCore.QObject.connect(self.hZoomChrom,QtCore.SIGNAL("triggered()"), self.hZoomToggleChrom)
        
#        self.actionToggleDraw = QtGui.QAction("Toggle Draw Style",  self.spectrumTabWidget)
#        self.spectrumTabWidget.addAction(self.actionToggleDraw)
#        self.actionToggleDraw.setShortcut("Ctrl+D")
#        QtCore.QObject.connect(self.actionToggleDraw,QtCore.SIGNAL("triggered()"), self.toggleDraw)
        
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
        QtCore.QObject.connect(self.action_Open,QtCore.SIGNAL("triggered()"),self.__readDataFile__)
        QtCore.QObject.connect(self.action_Save,QtCore.SIGNAL("triggered()"),self.__saveDataFile__)
        QtCore.QObject.connect(self.actionFileOpen,QtCore.SIGNAL("triggered()"),self.__readDataFile__)
        QtCore.QObject.connect(self.actionAbout,QtCore.SIGNAL("triggered()"),self.__showAbout__)
        QtCore.QObject.connect(self.actionHints,QtCore.SIGNAL("triggered()"),self.__showHints__)
        QtCore.QObject.connect(self.action_Exit,QtCore.SIGNAL("triggered()"),self.__exitProgram__)
        #QtCore.QObject.connect(self.spectrumTabWidget,QtCore.SIGNAL("currentChanged(int)"),self.updateMZTab)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
    
#    def scanUp(self):
#        if self.curScanId:
#            #self.curScanId+=1
#            #self.getMZScan(self.curScanId, 1)
#            #self.scanSBox.setValue(self.curScanId)
#            print "Up"
#    
#    def scanDown(self):
#        if self.curScanId:
#            #self.curScanId-=1
#            #self.getMZScan(self.curScanId,  0)
#            #self.scanSBox.setValue(self.curScanId)
#            print "Down"
    
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
                                             ("Hints and known Issues"), 
                                             ("<p> 1.	For files that contain spectra with a high degree of detail (i.e. not stick mass spectra) use the profile mode for drawing (Ctrl+D).  Otherwise, the plotting will be slow.</p>"
                                             "<p> 2. I haven't incorporated MS^n (where n >= 3) spectrum views at this point--I didn't have an example file to test.</p>"
                                             "<p>3.  If the program is too slow, remember python is not or ever intended to be C.</p>"
                                             "<p>4.  I have not incorporated a reader for mzData files as this format does not explictly store base peak and TIC values for chromatogram generation.  In order to do this each scan must be read simply to construct the TIC/BPC.  This is very slow.  The new mzML format will be supported in the very near future.</p>"))
  
    def __showAbout__(self):
        return QtGui.QMessageBox.information(self.MainWindow,
                                            ("mzViewer V.0.1, July, 2008"),
                                            ("<p><b>mzViewer</b> was written in Python by Brian H. Clowers (bhclowers@gmail.com).</p>"
        "<p>Please keep in mind that the entire effort is very much a"
        " work in progress and that Brian won't quit his day job for programming."
        " The original purpose of mzViewer was to provide a user-friendly, open-source tool"
        " for examining common mass spectrometry data formats (e.g. mzXML, mzData, and mzML"
        " using numpy and matplotlib.  Feel free to update"
        " (preferably with documentation) mzViewer and please share your contributions"
        " with the rest of the community.</p>"))
        


#class precursorTabWidget(QtGui.QWidget):
#    def __init__(self, precursorScan,  parent, name=None):
#        QtGui.QWidget.__init__(self,  parent.mzTab)
#        #def makePrecursorTab(self, fragScan, tabName):
#        #fragTab = QtGui.QWidget()
#        self.parent = parent
#        self.scan = precursorScan
#        self.setWindowModality(QtCore.Qt.NonModal)
#        self.setEnabled(True)
#        if name:
#            self.setObjectName(name)
#        self.fragPlot = MPL_Widget(self)
#        self.horizontalLayout = QtGui.QHBoxLayout()
#        self.horizontalLayout.addWidget(self.fragPlot)
#        self.precursorSpec = None
#        self.scanInfo = None
#        
#        
#    def updatePlot(self):
#        self.precursorSpec, self.scanInfo = self.parent.curFile.getPreSpectrum(self.scan)
#        self.fragPlot.canvas.ax.vlines(self.precursorSpec[0], 0, self.precursorSpec[1])
#        self.fragPlot.canvas.PlotTitle = "Scan #%s"%(self.scanInfo.get('id'))
#        self.fragPlot.canvas.draw()


def run_main():
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = XTViewer(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    run_main()
