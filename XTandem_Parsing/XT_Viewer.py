
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
from xtandem_parser_class import XT_RESULTS
import dbIO
#try:
#    import psyco
#    psyco.full()
#except:
#    print "Pysco not installed, try easy_install psyco at your command prompt"

plot_colors = ['#297AA3','#A3293D','#3B9DCE','#293DA3','#5229A3','#8F29A3','#A3297A','#A35229',
'#7AA329','#3DA329','#29A352','#29A38F','#A38F29','#3B9DCE','#6CB6DA','#CE6C3B','#DA916C',
'#0080FF','#0000FF','#8000FF','#FF0080','#FF0000','#FF8000','#FFFF00','#80FF00',
'#00FF00','#00FF80','#00FFFF','#3D9EFF','#7ABDFF','#FF9E3D','#FFBD7A']

markers = ['o', 'd', 's', '^', '>', 'v', '<', 'd', 'p', 'h']

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
        
 
    def startup(self):

        self.curFile = None
        self.curFileName = None
        self.curDB = None
        self.dbStatus = False
        
        self.plot_num = 0
        self.marker_index = 0
        self.mainTabWidget.setCurrentIndex(0)
        
        self.curSelectInfo = {
        'Index': None, 
        'Peptide': None, 
        'Peptide e-Value' : None, 
        'Scan' : None, 
        'ppm Error':None,
        'Theoretical MZ':None, 
        'Hyperscore':None,
        'Next Hyperscore':None,
        'Peptide Length':None, 
        'Protein ID':None, 
        'Protein e-Value':None
        }
        
        self.__setupPlot__()
        self.plotWidget.canvas.mpl_connect('pick_event', self.OnPickPlot)
        
        self.setDBConnection()

    def loadFileXT(self, filename):
        if filename:
            self.fileType= str(filename).split('.')[-1]
        if self.fileType == 'xml':
            self.curFile = XT_RESULTS(filename)
            self.initiatePlot()
            self.firstLoad = False
            
        elif self.fileType == 'h5':
            self.curFile = XT_RESULTS(filename,  parseFile = False)
            dbIO.load_XT_HDF5(str(filename), self.curFile)
            self.initiatePlot()
            self.firstLoad = False
            
        elif self.fileType == 'db':
            if not self.firstLoad:
                if self.__askConfirm__("Data Reset",self.ResetAllDataText):
                    self.resetData()
                    #self.resetDB()
                    self.startup()
            
            self.curFile = XT_RESULTS(filename,  parseFile = False)      
            sqldb = dbIO.XT_DB(str(filename), "testTables", createNew = False)#NEED TO FIX THE NAME
            sqldb.READ_XT_VALUES(sqldb.curTblName, self.curFile)
            sqldb.close()  
            self.initiatePlot()
            self.firstLoad = False
            
        else:
            return QtGui.QMessageBox.information(self.MainWindow,'', "Problem loading data, check file")
        

    def __readDataFile__(self):
        dataFileName = QtGui.QFileDialog.getOpenFileName(self.MainWindow,\
                                                         self.OpenDataText,\
                                                         self.__curDir, 'X!Tandem XML (*.xml);; HDF5 File (*.h5);;SQLite Database (*.db)')
        if dataFileName:
            self.loadFileXT(dataFileName)
                
#        else:
#
#            dataFileName = QtGui.QFileDialog.getOpenFileName(self.MainWindow,\
#                                                             self.OpenDataText,\
#                                                             self.__curDir, 'X!Tandem XML (*.xml);; HDF5 File (*.h5);;SQLite Database (*.db)')
#            if dataFileName:
#                self.loadFileXT(dataFileName)

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
                    sqldb = dbIO.XT_DB(str(saveFileName), "testTables")#NEED TO FIX THE NAME
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
        self.updateSelectInfo(self.pickIndex)
        self.plotWidget.canvas.draw()

        
    def __setupPlot__(self):
        self.handleA,  = self.plotWidget.canvas.ax.plot([0], [0], 'o',\
                                        ms=8, alpha=.5, color='yellow', visible=False,  label = 'Cursor A')
        self.is_hZoomChrom = False

        self.is_hZoom = False
    
    def initiatePlot(self):
        
        self.x = self.curFile.dataDict.get('pep_eValues')
        #self.x = self.curFile.dataDict.get('hScores')
        self.y = (self.curFile.dataDict.get('hScores')-self.curFile.dataDict.get('nextScores'))
        sizeList = self.curFile.dataDict.get('pepLengths')**1.5
        #self.y = self.y**4
        self.plotScatter = self.plotWidget.canvas.ax.scatter(self.x, self.y,  s = sizeList,  color = self.getPlotColor(),  alpha = 0.3,  picker = 5)
        self.plotWidget.canvas.ax.set_xscale('log')
        xmin = N.min(self.curFile.dataDict.get('pep_eValues'))/10
        xmax = N.max(self.curFile.dataDict.get('pep_eValues'))*10
        self.plotWidget.canvas.ax.set_xlim(xmin, xmax)        
        
        self.plotWidget.canvas.xtitle="Peptide e-Value"
        self.plotWidget.canvas.ytitle="Delta Hyperscore"
        self.plotWidget.canvas.PlotTitle = self.curFile.fileName
        self.plotWidget.canvas.format_labels()
        self.plotWidget.canvas.draw()
    
    def getPlotColor(self):
        color = plot_colors[self.plot_num]
        if self.plot_num is len(plot_colors)-1:
            self.plot_num = 0
        else:
            self.plot_num+=1
        return color
    
    def updateSelectInfo(self,  index):

        self.curSelectInfo['Index'] = str(index)
        self.curSelectInfo['Peptide'] = self.curFile.dataDict.get('pepIDs')[index]
        self.curSelectInfo['Peptide e-Value'] = str(self.curFile.dataDict.get('pep_eValues')[index])
        self.curSelectInfo['Scan'] =str(self.curFile.dataDict.get('scanID')[index])
        self.curSelectInfo['ppm Error'] =str(self.curFile.dataDict.get('ppm_errors')[index])
        self.curSelectInfo['Theoretical MZ'] =str(self.curFile.dataDict.get('theoMZs')[index])
        self.curSelectInfo['Hyperscore'] =str(self.curFile.dataDict.get('hScores')[index])
        self.curSelectInfo['Next Hyperscore'] =str(self.curFile.dataDict.get('nextScores')[index])
        self.curSelectInfo['Peptide Length'] =str(self.curFile.dataDict.get('pepLengths')[index])
        self.curSelectInfo['Protein ID'] =self.curFile.dataDict.get('proIDs')[index]
        self.curSelectInfo['Protein e-Value'] =str(self.curFile.dataDict.get('pro_eVals')[index])
        
        n = 0
        for item in self.curSelectInfo.iteritems():
            m = 0
            for entry in item:
                newitem = QtGui.QTableWidgetItem(entry)
                self.SelectInfoWidget.setItem(n, m, newitem)
                m+=1
            n+=1
        
        self.SelectInfoWidget.resizeColumnsToContents()

    
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
    
            
    def __initContextMenus__(self):
        #self.mzWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.mainTabWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.chromWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.mzWidget.connect(self.mzWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.mzWidgetContext)
        #self.chromWidget.connect(self.chromWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.chromWidgetContext)
        self.mainTabWidget.connect(self.mainTabWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.plotTabContext)
    
    def plotTabContext(self, point):
        '''Create a menu for mainTabWidget'''
        plotCT_menu = QtGui.QMenu("Menu", self.mainTabWidget)
        plotCT_menu.addAction(self.hZoom)
        plotCT_menu.addAction(self.actionAutoScale)
        #plotCT_menu.addAction(self.actionToggleDraw)
        plotCT_menu.exec_(self.mainTabWidget.mapToGlobal(point))
      
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
        self.mainTabWidget.addAction(self.hZoom)
        QtCore.QObject.connect(self.hZoom,QtCore.SIGNAL("triggered()"), self.ZoomToggle)
        
        self.actionAutoScale = QtGui.QAction("AutoScale",  self.MainWindow)
        self.actionAutoScale.setShortcut("Ctrl+A")
        self.mainTabWidget.addAction(self.actionAutoScale)
        QtCore.QObject.connect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)

#        self.actionSave = QtGui.QAction("Save File",  self.MainWindow)
#        self.actionSave.setShortcut("Ctrl+S")
#        self.MainWindow.addAction(self.actionSave)
#        QtCore.QObject.connect(self.actionSave,QtCore.SIGNAL("triggered()"), self.__saveDataFile__)

#        
#        self.hZoomChrom = QtGui.QAction("Horizontal Zoom",  self.chromWidget)
#        self.chromWidget.addAction(self.hZoomChrom)
#        self.hZoomChrom.setShortcut("Ctrl+Shift+Z")
#        QtCore.QObject.connect(self.hZoomChrom,QtCore.SIGNAL("triggered()"), self.hZoomToggleChrom)
        
        '''Database Connection slots'''
        QtCore.QObject.connect(self.openDBButton, QtCore.SIGNAL("clicked()"), self.setDBConnection)
        
        
        '''File menu actions slots'''
        QtCore.QObject.connect(self.action_Open,QtCore.SIGNAL("triggered()"),self.__readDataFile__)
        QtCore.QObject.connect(self.action_Save,QtCore.SIGNAL("triggered()"),self.__saveDataFile__)
        QtCore.QObject.connect(self.actionFileOpen,QtCore.SIGNAL("triggered()"),self.__readDataFile__)
        QtCore.QObject.connect(self.actionAbout,QtCore.SIGNAL("triggered()"),self.__showAbout__)
        QtCore.QObject.connect(self.actionHints,QtCore.SIGNAL("triggered()"),self.__showHints__)
        QtCore.QObject.connect(self.action_Exit,QtCore.SIGNAL("triggered()"),self.__exitProgram__)

        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
    
    def setDBConnection(self):    
        dbName = QtGui.QFileDialog.getOpenFileName(self.MainWindow,\
                                         'Select Database: ',\
                                         self.__curDir, 'SQLite Database (*.db)')
        if not dbName.isEmpty():
            self.curDBpathname.setText(dbName)
            self.curDB = dbIO.XT_DB(str(dbName), 'test',  createNew = False)
            self.dbStatus = self.curDB.dbOK
            if self.dbStatus:
                self.dbConnect_RB.setChecked(True)
                self.dbConnect_RB.setDown(True)
                #self.dbConnect_RB.setCheckable(False)
                
            else:
                reply = QtGui.QMessageBox.warning(self.MainWindow, "Database Connection Error",  self.curDB.errorMsg)
                if reply == QtGui.QMessageBox.OK:
                    self.retryDBConnection()
        else:
            self.retryDBConnection()
    
    
    def retryDBConnection(self):
        reply = QtGui.QMessageBox.question(self.MainWindow, "You Must Select a Valid SQLite DB Before Proceeding", "Retry Connection Now?",\
                                           QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.setDBConnection()
        else:
            self.dbStatus = False
###########################################################    \
    def resetData(self):
        self.plotWidget.canvas.ax.cla()
        self.startup()
        
    def __exitProgram__(self):
        if self.okToExit():
            self.MainWindow.close()
    
    def okToExit(self):
        reply = QtGui.QMessageBox.question(self.MainWindow, "Commit changes to database and exit? Discard to exit without saving.", "Save Changes & Exit?",\
                                           QtGui.QMessageBox.Yes|QtGui.QMessageBox.Discard|QtGui.QMessageBox.Cancel)
        if reply == QtGui.QMessageBox.Yes:
            if self.dbStatus:
                self.curDB.cnx.commit()
                self.curDB.cnx.close()
            return True
            
        elif reply == QtGui.QMessageBox.Discard:
            if self.dbStatus:
                self.curDB.cnx.close()
            return True
            
        elif reply == QtGui.QMessageBox.Cancel:
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
                                            ("X!Tandem Viewer V.0.1, August, 2008"),
                                            ("<p><b>X!Tandem Viewer</b> was written in Python by Brian H. Clowers (bhclowers@gmail.com).</p>"
        "<p>Please keep in mind that the entire effort is very much a"
        " work in progress and that Brian won't quit his day job for programming."
        " The original purpose of X!Tandem Viewer was to provide a user-friendly, open-source tool"
        " for examining X!Tandem xml files and link them to a SQLite Database for further exploration "
        " and concatenation of replicate experiments.  Please feel free to update X!Tandem Viewer"
        " (preferably with documentation) and please share your contributions"
        " with the rest of the community.</p>"))
        

def run_main():
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = XTViewer(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    run_main()
