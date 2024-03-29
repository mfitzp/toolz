
"""
This is the explicit class for viewing Parsed XT Files

/usr/bin/pyuic4 /home/clowers/workspace/XTandem_Parsing/main.ui  -o /home/clowers/workspace/XTandem_Parsing/ui_main.py

To Do:
Commit cross table peptide search with stats to DB
"""
#Importing built-in python modules and functions
import sys, os
from os import walk,  path

#import base64
import string
import time

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog,  QApplication

from matplotlib import rc, rcParams, use, interactive
use('Qt4Agg')

import numpy as N

from matplotlib.backends import backend_qt4, backend_qt4agg
backend_qt4.qApp = QtGui.qApp


#from io import hdfIO
from matplotlib.lines import Line2D
from matplotlib.widgets import SpanSelector

#import GUI scripts
import ui_main
from mpl_custom_widget import MPL_Widget
from xtandem_parser_class import XT_RESULTS
import dbIO
from customTable import DBTable
from rangeDialog import rangeDialog as RD
from FragmentPlot import FragPlotWidgets
import queryFunctions as QF

plot_colors = ['#297AA3','#A3293D','#3B9DCE','#293DA3','#5229A3','#8F29A3','#A3297A',
'#7AA329','#3DA329','#29A352','#29A38F','#A38F29','#3B9DCE','#6CB6DA','#CE6C3B','#DA916C',
'#0080FF','#0000FF','#7ABDFF','#8000FF','#FF0080','#FF0000','#FF8000','#FFFF00','#A35229','#80FF00',
'#00FF00','#00FF80','#00FFFF','#3D9EFF','#FF9E3D','#FFBD7A']

markers = ['o', 'd','>', 's', '^',  'p', '<', 'h', 'v']

#SAVE FIGURE TEST
from fig2xml import Figure2XML


class XTViewer(QtGui.QMainWindow,  ui_main.Ui_MainWindow):
    def __init__(self, parent = None):
        super(XTViewer,  self).__init__(parent)
        #self.ui = ui_main.Ui_MainWindow
        self.ui = self.setupUi(self)
        #self.MainWindow = MainWindow
        #ui_main.Ui_MainWindow.setupUi(self, self.MainWindow)

        self.__additionalVariables__()
        self.__additionalConnections__()
        self.__setMessages__()
        self.__initContextMenus__()
        self.__initVars__()
        self.startup()

    def __initVars__(self):
        self.openTableList = []
        self.openPlotList = []


    def startup(self, dbName = None, startDB = True):

        self.curFile = None
        self.curTbl = None
        self.curFileName = None
        self.xSelIndex = -1#used to keep track which index was selected
        self.ySelIndex = -1
        self.comboSelIndex = -1
        self.loVal = 0.0#value used for the range of selection in a query
        self.hiVal = 0.0#
        self.curDB = None
        self.loadOK = False
        self.ignoreSignal = False

        self.activeDict = {}
        self.activeData = None

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
        'Protein e-Value':None,
        'Seq Start':None,
        'Seq Stop':None
        }

        self.keyTypeMap = {}
        self.keyTypeMap['id'] = int
        self.keyTypeMap['pepID'] = str
        self.keyTypeMap['pep_eVal'] = float
        self.keyTypeMap['scanID'] = int
        self.keyTypeMap['ppm_error'] = float
        self.keyTypeMap['theoMZ'] = float
        self.keyTypeMap['hScore'] = float
        self.keyTypeMap['nextScore'] = float
        self.keyTypeMap['deltaH'] = float
        self.keyTypeMap['pepLen'] = int
        self.keyTypeMap['proID'] = str
        self.keyTypeMap['pro_eVal'] = float
        self.keyTypeMap['pepStart'] = int
        self.keyTypeMap['pepStop'] = int

        '''
        id INTEGER PRIMARY KEY AUTOINCREMENT,\
        pepID TEXT,\
        pep_eVal REAL,\
        scanID INTEGER,\
        ppm_error REAL,\
        theoMZ REAL,\
        hScore REAL,\
        nextScore REAL,\
        deltaH REAL,\
        pepLen INTEGER,\
        proID TEXT,\
        pro_eVal REAL)'''

        self.infoMap = {}
        self.infoMap['Index'] = 'id'
        self.infoMap['Peptide'] = 'pepID'
        self.infoMap['Peptide e-Value'] = 'pep_eVal'
        self.infoMap['Scan'] ='scanID'
        self.infoMap['ppm Error'] ='ppm_error'
        self.infoMap['Theoretical MZ'] ='theoMZ'
        self.infoMap['Hyperscore'] ='hScore'
        self.infoMap['Next Hyperscore'] = 'nextScore'
        self.infoMap['Delta Hyperscore'] = 'deltaH'
        self.infoMap['Peptide Length'] = 'pepLen'
        self.infoMap['Protein ID'] ='proID'
        self.infoMap['Protein e-Value'] = 'pro_eVal'
        self.infoMap['Seq Start'] = 'pepStart'
        self.infoMap['Seq Stop'] = 'pepStop'

        self.db_XCols.clear()
        self.db_YCols.clear()
        self.sizeArrayComboB.clear()

        if startDB:
            self.dbConnectedBtn.setEnabled(False)
            self.dbStatus = False
            if dbName != None:
                self.setDBConnection(dbName = dbName)
            else:
                self.setDBConnection()
        else:
            print "Startup called without DB Start Flag"
        self.__setupPlot__()

    def __testFunc__(self):
        print "TEST FUNCTION CALLED"
        
        xmlFig = Figure2XML(self.plotWidget.canvas.fig)
        xmlFig.print_xml('mplFig.xml')
#        self.UNIQUE_PEP_PRO_FULL()

#        if RD(self.loVal, self.hiVal, parent = self).exec_():
#            print self.loVal, self.hiVal
#            print "Ok"
#        else:
#            print self.loVal, self.hiVal
#            print "Cancel"

#        print self.curDB.LIST_COLUMNS(self.curDB.LIST_TABLES()[0])
#        print type(self.curDB.LIST_TABLES()[0]), self.curDB.LIST_TABLES()

    def closeOpenWindows(self):
        if len(self.openTableList)>0:
            for table in self.openTableList:
                try:
                    print "Closing %s"%str(table.windowTitle())
                    table.close()
                except:
                    pass
        if len(self.openPlotList)>0:
            for plot in self.openPlotList:
                try:
                    plot.close()
                except:
                    pass

    def __resetDB__(self):
        try:
            tblList = self.curDB.LIST_TABLES()
            print "DB Reset, Tables Contained: ", tblList
            for tbl in tblList:
                curResults = XT_RESULTS(parseFile = False)
                self.curDB.READ_CUSTOM_VALUES(tbl, curResults)
#                self.curDB.READ_XT_VALUES(tbl, curResults)
                self.activeDict[tbl] = curResults
                self.curTbl = tbl

        except:
            print 'DB Load Error'
            return True

        try:
            self.initiatePlot()
        except:
            print "initatePlot Failed"
        try:
            self.updatePlotOptionsGUI()
        except:
            print "updatePlotOptionsGUI Failed"
        try:
            self.updateQueryGUI()
        except:
            print "updateQueryGUI Failed"

        self.firstLoad = False


    def setColLists(self,  widgetItem):
        #The following three lines reset the parameters of the plotting mechanisms
        self.xSelIndex = self.db_XCols.currentRow()
        self.ySelIndex = self.db_YCols.currentRow()
        self.comboSelIndex = self.sizeArrayComboB.currentIndex()

        self.db_XCols.clear()
        self.db_YCols.clear()
        self.sizeArrayComboB.clear()

        activeData = self.activeDict[str(widgetItem.text())]
        colList = activeData.dataDict.keys()

        colNumList = []
        for col in colList:
            if self.keyTypeMap.has_key(col):
                if self.keyTypeMap[col] is str:
                    pass
                else:
                    colNumList.append(col)
        if len(colNumList) == 0:
            errMsg = ["Table format incompatible with Plot GUI"]
            self.db_XCols.addItems(errMsg)
#            return QtGui.QMessageBox.warning(self, "Database Table Error",  "No numerical data exist in the selected table!")
        else:
            self.db_XCols.addItems(colNumList)
            self.db_YCols.addItems(colNumList)
            self.sizeArrayComboB.addItems(colNumList)

            if self.xSelIndex != -1 and self.xSelIndex <= self.db_XCols.count():
                self.db_XCols.setCurrentRow(self.xSelIndex)
            if self.ySelIndex != -1 and self.ySelIndex <= self.db_YCols.count():
                self.db_YCols.setCurrentRow(self.ySelIndex)
            if self.comboSelIndex != -1 and self.comboSelIndex <= self.sizeArrayComboB.count():
                self.sizeArrayComboB.setCurrentIndex(self.comboSelIndex)

    def executeSQLQuery(self):
        if self.dbStatus:
            queryStr = str(self.sqlQueryString.toPlainText())
            self.outTableWidget.clear()
            self.outTableWidget.setRowCount(5)
            self.outTableWidget.setColumnCount(5)
            if queryStr != None:
                try:
                    self.curDB.cur.execute(queryStr)
                    self.sqlErrorMessage.setText('No Error')
                    result = self.curDB.GET_CURRENT_QUERY(truncate = True)
                    colNames = self.curDB.GET_COLUMN_NAMES()
                    if len(result) != 0:
                        self.outTableWidget.setHorizontalHeaderLabels(colNames)
                        self.outTableWidget.setSortingEnabled(False)
                        self.outTableWidget.addData(result)
                        self.outTableWidget.resizeColumnsToContents()
                        self.outTableWidget.setSortingEnabled(True)
                except:
                    self.sqlErrorMessage.setText(str(sys.exc_value))
#                    errorMsg = "Error: %s\n\n%s\n"%(sys.exc_type, sys.exc_value)
#                    errorMsg+='\n There was an error executing the SQL Query.'
#                    return QtGui.QMessageBox.information(self,'SQL Execute Error', errorMsg)

    def viewQueryResults(self):
        if self.dbStatus:
            queryStr = str(self.sqlQueryString.toPlainText())
            if queryStr != None:
                try:
                    self.curDB.cur.execute(queryStr)
                    self.sqlErrorMessage.setText('No Error')
                    result = self.curDB.GET_CURRENT_QUERY(truncate = False)
                    colNames = self.curDB.GET_COLUMN_NAMES()
                    if len(result) != 0:
                        if len(queryStr) > 50:
                            tempTitle = queryStr[0:50]+'...'
                        else:
                            tempTitle = queryStr
                        self.openTableList.append(DBTable(result, enableSort = True, title = tempTitle, colHeaderList = colNames))
                        self.curDBTable = self.openTableList[-1]#append adds to the end of the list so adding the most recent addition
                    else:
                        self.sqlErrorMessage.setText('No Error, but query returned no results')
                except:
                    self.sqlErrorMessage.setText(str(sys.exc_value))
#                    errorMsg = "Error: %s\n\n%s\n"%(sys.exc_type, sys.exc_value)
#                    errorMsg+='\n There was an error executing the SQL Query.'
#                    return QtGui.QMessageBox.information(self,'SQL Execute Error', errorMsg)


    def setQueryLists(self,  widgetItem):
        self.queryFieldList.clear()
        activeData = self.activeDict[str(widgetItem.text())]
        colList = activeData.dataDict.keys()
        if len(colList) == 0:
            return QtGui.QMessageBox.warning(self, "Database Table Error",  "No data exist in the selected table!")
        else:
            self.queryFieldList.addItems(colList)

    def updateQueryGUI(self):
        self.queryTblList.clear()
#        self.queryFieldList.clear()
        if len(self.activeDict) > 0:
            activeTbls = self.activeDict.keys()
            for tbl in activeTbls:
                if tbl[0] != '_':#ignore special tables
                    curTbl = QtGui.QListWidgetItem()
                    curTbl.setText(tbl)
                    curTbl.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsSelectable)
                    curTbl.setCheckState(QtCore.Qt.Unchecked)
                    self.queryTblList.addItem(curTbl)
            self.queryTblList.setCurrentRow(0)
            self.setQueryLists(self.queryTblList.currentItem())


    def updatePlotOptionsGUI(self):
        self.db_TableList.clear()
        self.sizeArrayComboB.clear()
        if len(self.activeDict) > 0:
            activeTbls = self.activeDict.keys()
            self.db_TableList.addItems(activeTbls)
            self.db_TableList.setCurrentRow(0)
            self.setColLists(self.db_TableList.currentItem())


    def setDBConnection(self, dbName = None):#would this be better if you added an old db reference in case it fails?
        if self.useMemDB_CB.isChecked() == True and self.dbStatus == False and dbName is None:
            #this is for the inital startup so that this connection is established
            print "Using :memory: DB"
            self.setMemDB(2)
        else:
            if dbName is None:
                dbName = QtGui.QFileDialog.getSaveFileName(self,\
                                                 'Select Database: ',\
                                                 self.__curDir, 'SQLite Database (*.db)', "", QtGui.QFileDialog.DontConfirmOverwrite)

            if not dbName.isEmpty():
                self.__curDir = getCurDir(dbName)
                print self.dbStatus, dbName
                if self.dbStatus:#(i.e a connection already exists)
                    reply = QtGui.QMessageBox.question(self, "Database Conneciton Exists", "A Database Connection already exists.  Do you want to close the current connection and establish the one just selected?",
                                                   QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        self.curDB.close()
                        self.startup(startDB = False)#need to reset variables
                        self.dbStatus == False
                        if self.useMemDB_CB.isChecked():
                            self.useMemDB_CB.setChecked(False)
                        self.curDBpathname.setText(dbName)
                        self.curDB = dbIO.XT_DB(str(dbName),  parent = self)
                        self.dbStatus = self.curDB.dbOK
                        if self.dbStatus:
                            self.dbConnectedBtn.setEnabled(True)
                            self.__resetDB__()
                        else:
                            self.setDBError()
                else:
                    return False
            elif self.useMemDB_CB.isChecked() == False:
                self.retryDBConnection()

    def retryDBConnection(self):
        reply = QtGui.QMessageBox.question(self, "Database Connection Needed", "You Must Select a Valid SQLite DB Before Proceeding.  Establish Connection Now?",
                                           QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.setDBConnection()
        else:
            self.useMemDB_CB.setCheckState(QtCore.Qt.Checked)
#            self.dbStatus = False

    def updateDBGUI(self):
        if self.useMemDB_CB.isChecked():
            self.memDB = True
        else:
            self.memDB = False

    def setDBError(self):
        try:
            errorMsg = self.curDB.errorMsg
        except:
            errorMsg = "No database establed. Try again?"
        reply = QtGui.QMessageBox.warning(self, "Database Connection Error",  errorMsg)
        if reply == QtGui.QMessageBox.OK:
            self.retryDBConnection()

    def setMemDB(self, state):
        '''This function initializes a memory data base for sqlite if the GUI checkbox is marked'''
        if self.ignoreSignal:
            return True
        else:

            #state == 2 if checked
            if state == 0:
                return False
            if self.useMemDB_CB.isChecked() and self.dbStatus == False:
                self.startup(startDB = False)
                dbName=':memory:'
                self.curDBpathname.setText(dbName)#updates the DB GUI
                self.curDB = dbIO.XT_DB(str(dbName),  parent = self)
                self.dbStatus = self.curDB.dbOK
                if self.dbStatus:
                    self.dbConnectedBtn.setEnabled(True)
                    if not self.firstLoad:
                        self.initiatePlot()
                        self.updatePlotOptionsGUI()
                        self.updateQueryGUI()
                else:
                    self.setDBError()

            elif self.useMemDB_CB.isChecked() and self.dbStatus == True:
                reply = QtGui.QMessageBox.question(self, "Database Conneciton Exists", "A Database Connection already exists.  Do you want to close the current connection and establish an in-memory database?",
                                               QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    self.curDB.close()
                    self.startup(startDB = False)
                    self.dbStatus == False
                    dbName=':memory:'
                    self.curDBpathname.setText(dbName)
                    self.curDB = dbIO.XT_DB(str(dbName),  parent = self)
                    self.dbStatus = self.curDB.dbOK
                    if self.dbStatus:
                        self.dbConnectedBtn.setEnabled(True)
                        if not self.firstLoad:
                            self.initiatePlot()
                            self.updatePlotOptionsGUI()
                            self.updateQueryGUI()
                    else:
                        self.setDBError()
                elif reply == QtGui.QMessageBox.No:
                    dbName=':memory:'
                    if str(self.curDBpathname.text()) == dbName:
                        print "Memory DB already Established"
                        self.ignoreSignal = True
                        self.useMemDB_CB.setCheckState(QtCore.Qt.Checked)
                        self.ignoreSignal = False
                    else:
#                        self.setDBConnection()
                        self.useMemDB_CB.setChecked(False)

            else:
                self.dbStatus = False
                self.setDBError()

    def loadFileXT(self, filename):
        if filename:
            self.fileType= str(filename).split('.')[-1]
        if self.fileType == 'xml':
            if self.dbStatus:
                fnCore = os.path.basename(str(filename)).split('.')[0]#self.getFNCore(str(filename))
                self.curTbl = fnCore
#                try:
#                    print filename
                results = XT_RESULTS(filename)
                if results.dataDict == False:
                    raise Exception,  self.EmptyArrayText

                else:
                    insertOK = self.curDB.INSERT_XT_VALUES(fnCore, results)
                    self.loadOK = True
                    if insertOK:
                        self.activeDict[fnCore] = results
                        self.initiatePlot()
                        self.updatePlotOptionsGUI()
                        self.updateQueryGUI()
                        self.firstLoad = False
#                except:
#                    errorMsg = "Error: %s\n\n%s\n"%(sys.exc_type, sys.exc_value)
#                    errorMsg+='\n There was an error reading the xml file.  Are you sure it is an X!Tandem output file?'
#                    return QtGui.QMessageBox.information(self,'Error Reading File', errorMsg)
#
        elif self.fileType == 'h5':
#            try:
            self.curFile = XT_RESULTS(filename,  parseFile = False)
            dbIO.load_XT_HDF5(str(filename), self.curFile)
            self.initiatePlot()
            self.firstLoad = False
            self.loadOK = True
#            except:
#                self.loadOK = False
#                return QtGui.QMessageBox.information(self,'', "Error reading hfdf5 File.  Are you sure it was created by this program?")

        elif self.fileType == 'db':
#            try:

            print filename, type(filename)
#            self.startup(dbName = filename)#, startDB)
            self.setDBConnection(dbName = filename)
#            self.resetData(dbName = filename)
#            if self.dbStatus:
            self.loadOK = True
#            except:
#                self.loadOK = False
#                return QtGui.QMessageBox.information(self,'', "Error reading db File.  Are you sure it was created by this program?")

        else:
            return QtGui.QMessageBox.information(self,'', "Problem loading data, check file")


    def __loadDataFolder__(self):
#        if self.dbStatus:
        directory= QtGui.QFileDialog.getExistingDirectory(self, self.__curDir,
                                                          "Select X!Tandem XML Data Folder")
        if os.path.isdir(str(directory)):
            self.__curDir = str(directory)
            if self.dbStatus:
                for root, dirs, files in walk(str(directory)):
                    for file in files:
                        if '.xml' in file:
                            ##full file path name
                            ffpn=path.abspath(path.join(root, file))#file full path name

                            if self.dbStatus:

                                if ffpn:
                                    self.loadFileXT(str(ffpn))
                            else:
                                if self.memDB:
                                    self.setDBConnection()
                                    if ffpn:
                                        self.loadFileXT(str(ffpn))
                                else:
                                    self.retryDBConnection()



    def __readDataFile__(self):
        if self.dbStatus:
            dataFileName = QtGui.QFileDialog.getOpenFileName(self,\
                                                             self.OpenDataText,\
                                                             self.__curDir, 'X!Tandem XML (*.xml);;SQLite Database (*.db)')
            if dataFileName:
                self.loadFileXT(dataFileName)
                self.__curDir = getCurDir(dataFileName)
        else:
            if self.memDB:
                self.setDBConnection()
                dataFileName = QtGui.QFileDialog.getOpenFileName(self,\
                                            self.OpenDataText,\
                                            self.__curDir, 'X!Tandem XML (*.xml);;SQLite Database (*.db)')
                if dataFileName:
                    self.loadFileXT(dataFileName)
                    self.__curDir = getCurDir(dataFileName)
            else:
                self.retryDBConnection()

    def __saveDataFile__(self):
        return QtGui.QMessageBox.information(self,'', "This feature is not implemented yet.  Use a database outside of memory")
#        saveFileName = QtGui.QFileDialog.getSaveFileName(self,\
#                                                             self.SaveDataText,\
#                                                             self.__curDir, 'HDF5 File (*.h5);;SQLite Database (*.db)')
#        if saveFileName:
#            if self.curFile:
#                #print "File name is: %s" % (str(self.curFileName))
#                fileType= str(saveFileName).split('.')[-1]
#                if fileType=='h5':
#                    print self.curFile, type(self.curFile)
##                    dbIO.save_XT_HDF5(str(saveFileName),  self.curFile)
#                elif fileType == 'db':
#                    sqldb = dbIO.XT_DB(str(saveFileName), "testTables")#NEED TO FIX THE NAME
#                    sqldb.INSERT_XT_VALUES(sqldb.curTblName, self.curFile)
#                    sqldb.close()
#            else:
#                return QtGui.QMessageBox.information(self,'', "A X!Tandem File must be loaded first before saving")


    def getFNCore(self, filename):
        '''This function parses the filename to get a simple name for the table to be entered into memory and the database'''
        self.sysType = os.sys.platform
        if self.sysType == 'win32':
            fs = filename.split('/')[-1]#fs = file split
            fileCore = fs.split('.')[0]
        else:
            fs = filename.split('/')[-1]#fs = file split
            fileCore = fs.split('.')[0]
        return fileCore

    def OnPickPlot(self, event):
        t1 = time.clock()
        self.pickIndex = event.ind[0]
        try:
            self.textHandle.remove()
        except:
            pass
        self.curTbl = event.artist.get_label()
        if self.clearPlotCB.isChecked():
            #I'd rather do the following ALWAYS but it seems difficult to do in terms of keeping track of which arrays were plotted when multiple plots are present
            self.handleA.set_data(N.take(self.x, [self.pickIndex]), N.take(self.y, [self.pickIndex]))
        else:
            self.handleA.set_data([event.mouseevent.xdata], [event.mouseevent.ydata])

        self.handleA.set_visible(True)
        showText = '%s'%(self.activeDict[self.curTbl].dataDict.get('pepID')[self.pickIndex])
        self.textHandle = self.plotWidget.canvas.ax.text(0.03, 0.95, showText, fontsize=9,\
                                        bbox=dict(facecolor='yellow', alpha=0.1),\
                                        transform=self.plotWidget.canvas.ax.transAxes, va='top')
        self.updateSelectInfo(self.pickIndex,  self.curTbl)
        t2 = time.clock()
#        print t2-t1
        self.plotWidget.canvas.draw()

    def tableSelChanged(self, selList):
#        updateSelectInfo(self,  index,  activeKey)
        selIndex, activeKey = selList
        if type(selIndex) == int and self.activeDict.has_key(activeKey):
            self.updateSelectInfo(selIndex, activeKey)
#            print selList

    def __setupPlot__(self):
        '''Sets up the plot variables used for interaction'''
        self.handleA,  = self.plotWidget.canvas.ax.plot([0], [0], 'o',\
                                        ms=8, alpha=.5, color='yellow', visible=False,  label = '_nolegend_')
        self.is_hZoom = False
        self.plotWidget.canvas.mpl_connect('pick_event', self.OnPickPlot)

    def clearPlot(self):
        self.plotWidget.canvas.ax.cla()
        self.__setupPlot__()
        self.plotWidget.canvas.format_labels()
        self.plotWidget.canvas.draw()
        self.mainTabWidget.setCurrentIndex(1)

    def updatePlot(self):
        try:
            if self.clearPlotCB.isChecked():
                self.plotWidget.canvas.ax.cla()
            self.__setupPlot__()

            self.curTbl = str(self.db_TableList.currentItem().text())
            xKey = str(self.db_XCols.currentItem().text())
            yKey = str(self.db_YCols.currentItem().text())

            activeData = self.activeDict[self.curTbl]
            self.x = activeData.dataDict[xKey]
            self.y = activeData.dataDict[yKey]

            sizeModifier = self.sizeModSpinBox.value()
            sizeArray = activeData.dataDict[str(self.sizeArrayComboB.currentText())]#this is used to adjust the size of the marker
            sizeList = sizeArray**sizeModifier

            self.plotScatter = self.plotWidget.canvas.ax.scatter(self.x, self.y,  color = self.getPlotColor(),  marker = self.getPlotMarker(), alpha = 0.3,  label = self.curTbl,  picker = 5,  s = sizeList)
            #self.plotScatter = self.plotWidget.canvas.ax.plot(self.x, self.y,  color = self.getPlotColor(),  marker = self.getPlotMarker(), alpha = 0.3,  label = self.curTbl,  picker = 5)
            if self.showLegendCB.isChecked():
                self.plotWidget.canvas.ax.legend(borderaxespad = 0.03, axespad=0.25)
                if self.plotWidget.canvas.ax.get_legend() != None:
                    texts = self.plotWidget.canvas.ax.get_legend().get_texts()
                    for text in texts:
                        text.set_fontsize(8)
                
            if self.cb_logx.isChecked():
                self.plotWidget.canvas.ax.set_xscale('log')
                xmin = N.min(self.x)/10
                xmax = N.max(self.x)*10
                self.plotWidget.canvas.ax.set_xlim(xmin, xmax)

            if self.cb_logy.isChecked():
                self.plotWidget.canvas.ax.set_yscale('log')
                ymin = N.min(self.y)/10
                ymax = N.max(self.y)*10
                self.plotWidget.canvas.ax.set_ylim(ymin, ymax)

            self.plotWidget.canvas.xtitle=xKey
            self.plotWidget.canvas.ytitle=yKey
            self.plotWidget.canvas.PlotTitle = self.curTbl
            self.plotWidget.canvas.format_labels()
            self.plotWidget.canvas.draw()

            self.mainTabWidget.setCurrentIndex(1)
        except:
            errorMsg = "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
            errorMsg+='\n Perhaps a "log" axis is checked or a large number is being used for the size modifier?'
            QtGui.QMessageBox.warning(self, "Plot Update",  errorMsg)

    def initiatePlot(self):
        self.plotWidget.canvas.ax.cla()
        self.__setupPlot__()
        if self.curTbl != None:
            activeData = self.activeDict[self.curTbl]
            self.x = activeData.dataDict.get('pep_eVal')
            #self.x = self.curFile.dataDict.get('hScores')
            self.y = activeData.dataDict.get('deltaH')#(activeData.dataDict.get('hScores')-activeData.dataDict.get('nextScores'))
            sizeList = activeData.dataDict.get('pepLen')**1.5
            self.plotScatter = self.plotWidget.canvas.ax.scatter(self.x, self.y,  s = sizeList,  color = self.getPlotColor(),  marker = self.getPlotMarker(), alpha = 0.3,  label = self.curTbl,  picker = 5)#add label = ??
            #self.plotScatter = self.plotWidget.canvas.ax.plot(self.x, self.y,  color = self.getPlotColor(),  marker = self.getPlotMarker(), alpha = 0.3,  label = self.curTbl,  picker = 5)#add label = ??
            self.plotWidget.canvas.ax.set_xscale('log')
            xmin = N.min(self.x)/10
            xmax = N.max(self.x)*10
            self.plotWidget.canvas.ax.set_xlim(xmin, xmax)

            self.plotWidget.canvas.xtitle="Peptide e-Value"
            self.plotWidget.canvas.ytitle="Delta Hyperscore"
            self.plotWidget.canvas.PlotTitle = self.curTbl
        else:
            self.plotWidget.canvas.xtitle="X-Axis"
            self.plotWidget.canvas.ytitle="Y-Axis"
            self.plotWidget.canvas.PlotTitle = " "
        self.plotWidget.canvas.format_labels()
        self.plotWidget.canvas.draw()

    def getPlotColor(self):
        color = plot_colors[self.plot_num]
        if self.plot_num is len(plot_colors)-1:
            self.plot_num = 0
        else:
            self.plot_num+=1
        return color

    def getPlotMarker(self):
        marker = markers[self.marker_index]
        if self.marker_index is len(markers)-1:
            self.marker_index = 0
        else:
            self.marker_index+=1
        return marker

    def updateSelectInfo(self,  index,  activeKey):
        '''
        Accepts the index to the current dictionary and the activeKey is the hook to
        grab that dictionary
        '''
        activeData = self.activeDict[activeKey]
        self.curSelectInfo['Index'] = str(index)
        self.curSelectInfo['Peptide'] = activeData.dataDict.get('pepID')[index]
        self.curSelectInfo['Peptide e-Value'] = str(activeData.dataDict.get('pep_eVal')[index])
        self.curSelectInfo['Scan'] =str(activeData.dataDict.get('scanID')[index])
        self.curSelectInfo['ppm Error'] =str(activeData.dataDict.get('ppm_error')[index])
        self.curSelectInfo['Theoretical MZ'] =str(activeData.dataDict.get('theoMZ')[index])
        self.curSelectInfo['Hyperscore'] =str(activeData.dataDict.get('hScore')[index])
        self.curSelectInfo['Next Hyperscore'] =str(activeData.dataDict.get('nextScore')[index])
        self.curSelectInfo['Delta Hyperscore'] =str(activeData.dataDict.get('deltaH')[index])
        self.curSelectInfo['Peptide Length'] =str(activeData.dataDict.get('pepLen')[index])
        self.curSelectInfo['Protein ID'] =activeData.dataDict.get('proID')[index]
        self.curSelectInfo['Protein e-Value'] =str(activeData.dataDict.get('pro_eVal')[index])

        newitem = QtGui.QTableWidgetItem('Table')
        self.SelectInfoWidget.setItem(0, 0, newitem)
        newitem = QtGui.QTableWidgetItem(activeKey)
        self.SelectInfoWidget.setItem(0, 1, newitem)

        n = 1
        for item in self.curSelectInfo.iteritems():
            m = 0
            for entry in item:
                if entry != None:
                    #print type(entry), str(entry)
                    newitem = QtGui.QTableWidgetItem(entry)
                    self.SelectInfoWidget.setItem(n, m, newitem)
                    m+=1
            n+=1

        self.SelectInfoWidget.resizeColumnsToContents()
        self.activeData = activeData.dataDict


    def onselect(self, xmin, xmax):
            #print xmin,  xmax
            if self.is_hZoom:
                self.plotWidget.canvas.ax.set_xlim(xmin,  xmax)
                self.plotWidget.canvas.draw()



    def __initContextMenus__(self):
        self.plotWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.SelectInfoWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.queryFieldList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.queryTblList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.plotWidget.connect(self.plotWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.plotTabContext)
        self.SelectInfoWidget.connect(self.SelectInfoWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.selectInfoTabContext)
        self.queryFieldList.connect(self.queryFieldList, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.queryFieldContext)
        self.queryTblList.connect(self.queryTblList, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.queryTableContext)

    def dumpCurDB(self):
        if self.dbStatus:
            saveFileName = QtGui.QFileDialog.getSaveFileName(self,\
                                                     self.SaveDataText,\
                                                     self.__curDir, 'SQLite Text Database (*.sql)')
            if saveFileName:
                warnMsg = "This feature will be enabled with the release of Python 2.6"
                print warnMsg
                return QtGui.QMessageBox.warning(self, "Database Dump Error",  warnMsg)

#                con = self.curDB.cnx
#                full_dump = os.linesep.join([line for line in con.iterdump()])
#                f = open(str(saveFileName), 'w')
#                f.writelines(full_dump)
#                f.close()


    def selectDBField(self,  saveTable = None):
        curCol = self.SelectInfoWidget.currentColumn()
        if self.SelectInfoWidget.currentItem() == None:
            return False
            #print "Current index: ",  self.SelectInfoWidget.currentRow(), curCol
        else:
            try:
                curItem = self.SelectInfoWidget.item(self.SelectInfoWidget.currentRow(), 0)
                curType = self.infoMap[str(curItem.text())]
                curVal = self.curSelectInfo[str(curItem.text())]
                curTbl = self.curTbl
                if saveTable:
                    tblName, result, colNames, execStr = self.curDB.GET_VALUE_BY_TYPE(curTbl, curType, curVal, savePrompt = True)

                    if len(result)>0 and tblName != None:
                        self.sqlQueryString.setText(execStr)
                        curResults = XT_RESULTS(parseFile = False)
                        self.curDB.READ_CUSTOM_VALUES(tblName, curResults)
                        self.activeDict[tblName] = curResults
                        self.__resetDB__()


                else:
                    tblName, result, colNames, execStr = self.curDB.GET_VALUE_BY_TYPE(curTbl, curType, curVal)
                if result == False:
                    print "User aborted query"
                else:
                    if len(result) == 0:
                        result = ['No data was found...', ]
                    #print result
                    #else:
                    tempTitle = curTbl+' '+curType
                    colHeaders = self.curDB.LIST_COLUMNS(curTbl)
                    self.openTableList.append(DBTable(result, colHeaders, enableSort = True, title = tempTitle))
                    self.curDBTable = self.openTableList[-1]#append adds to the end of the list so adding the most recent addition
                    self.sqlQueryString.setText(execStr)

            except:
                errorMsg = "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
                errorMsg+='\n GET_VALUE_BY_TYPE Failed!\nThere was a problem retrieving the information from the database.'
                QtGui.QMessageBox.warning(self, "Select Database Field Error",  errorMsg)



    def saveQueryTable(self):
        self.selectDBField(saveTable = True)

    def queryByType(self):
        curField = str(self.queryFieldList.currentItem().text())
        curTbl = str(self.queryTblList.currentItem().text())
        if self.keyTypeMap.has_key(curField):
            result = []
            tempTitle = 'Database Query'
            if self.keyTypeMap[curField] == str:
                if curField != None and curTbl != None:
                    queryValue, ok = QtGui.QInputDialog.getText(self, 'Enter Query Value',\
                                        'Enter %s to Query From %s: '%(curField, curTbl), QtGui.QLineEdit.Normal, '')
                    if ok:
                        queryValue = str(queryValue)
                        if len(queryValue) != 0:#make sure the user didn't leave the prompt blank
                            tempName, result, colNames, execStr = self.curDB.GET_VALUE_BY_TYPE(curTbl,  curField,  queryValue)
                            tempTitle = curTbl+', '+curField+', '+queryValue

            elif self.keyTypeMap[curField] == int:
                self.loVal = 0.0
                self.hiVal = 0.0
                if RD(self.loVal, self.hiVal, parent = self).exec_():
#                    print self.loVal, self.hiVal
                    self.loVal = int(self.loVal)
                    self.hiVal = int(self.hiVal)
                    result, colNames, execStr = self.curDB.GET_VALUE_BY_RANGE(curTbl, curField, self.loVal, self.hiVal)
                    tempTitle = curTbl+', '+curField+', '+str(self.loVal)+' to '+str(self.hiVal)

            elif self.keyTypeMap[curField] == float:
                if RD(self.loVal, self.hiVal, parent = self).exec_():
#                    print self.loVal, self.hiVal
                    result, colNames, execStr = self.curDB.GET_VALUE_BY_RANGE(curTbl, curField, self.loVal, self.hiVal)
                    tempTitle = curTbl+', '+curField+', '+str(self.loVal)+' to '+str(self.hiVal)

#            if len(result) == 0:
#                result = ['No data was found...', ]
#            colHeaders = self.curDB.LIST_COLUMNS(curTbl)

            curTableWin = DBTable(result, colNames, enableSort = True, title = tempTitle)
            QtCore.QObject.connect(curTableWin,QtCore.SIGNAL("itemSelected(PyQt_PyObject)"), self.tableSelChanged)
            self.openTableList.append(curTableWin)
            self.curDBTable = self.openTableList[-1]#append adds to the end of the list so adding the most recent addition
            self.sqlQueryString.setText(execStr)
#            QtCore.QObject.connect(self.curDBTable, QtCore.SIGNAL("itemSelected(PyQt_PyObject)"), self.tableSelChange)

    def queryFieldContext(self, point):
        queryCT_menu = QtGui.QMenu("Menu",  self.queryFieldList)
        queryCT_menu.addAction(self.queryByTypeAction)
        queryCT_menu.exec_(self.queryFieldList.mapToGlobal(point))
        #queryCT_menu

    def selectInfoTabContext(self,  point):
        '''Create a context menu for the SelectInfoWidget which is a QTableWidget'''
        infoCT_menu = QtGui.QMenu("Menu",  self.SelectInfoWidget)
        infoCT_menu.addAction(self.selectDBFieldAction)
        infoCT_menu.addAction(self.saveDBFieldAction)
        infoCT_menu.addAction(self.getFragAction)
        infoCT_menu.exec_(self.SelectInfoWidget.mapToGlobal(point))

    def plotTabContext(self, point):
        '''Create a menu for mainTabWidget'''
        plotCT_menu = QtGui.QMenu("Menu", self.plotWidget)
        plotCT_menu.addAction(self.plotWidget.hZoom)
        plotCT_menu.addAction(self.plotWidget.actionAutoScale)
        #plotCT_menu.addAction(self.actionToggleDraw)
        plotCT_menu.exec_(self.plotWidget.mapToGlobal(point))

    def queryTableContext(self, point):
        queryList_menu = QtGui.QMenu("Menu", self.queryTblList)
        queryList_menu.addAction(self.showTableAction)
        queryList_menu.addSeparator()
        queryList_menu.addAction(self.uniquePeptidesAction)
        queryList_menu.addAction(self.uniqueProteinsAction)
        queryList_menu.addAction(self.uniquePepByProtAction)
        queryList_menu.addSeparator()
        queryList_menu.addAction(self.uniqueMultiPepAction)
        queryList_menu.addAction(self.uniqueMultiPepStatsAction)
        queryList_menu.addAction(self.uniquePepProAction)
        queryList_menu.addSeparator()
        queryList_menu.addAction(self.dumpTableAction)#this is a save function
        queryList_menu.addSeparator()
        queryList_menu.addAction(self.removeTableAction)
        queryList_menu.exec_(self.queryTblList.mapToGlobal(point))

    def removeTable(self):
        curItem = self.queryTblList.currentItem()
        if curItem != None:
            curTbl = str(curItem.text())
            if self.__askConfirm__('Remove File from Database?','This action will permanently remove the following table: %s'%curTbl):
                if self.curDB.DROP_TABLE(curTbl):
                    if self.activeDict.has_key(curTbl):
                        self.activeDict.pop(curTbl)
                        self.__resetDB__()


                else:
                    return QtGui.QMessageBox.information(self, ("Error Deleting Table %s"%curTbl), ('Check the database'))

    def copyCurrentDatabase(self):
        if self.dbStatus:
            saveFileName = QtGui.QFileDialog.getSaveFileName(self,\
                                                                 self.SaveDataText,\
                                                                 self.__curDir, 'SQLite Database (*.db)')
            if saveFileName:
                self.curDB.COPY_DATABASE(str(saveFileName))
                self.__curDir = getCurDir(saveFileName)

    def saveCSVTable(self, tableName = None, saveFileName = None):
        if tableName is None and saveFileName is None:
            saveFileName = QtGui.QFileDialog.getSaveFileName(self,\
                                                     self.SaveDataText,\
                                                     self.__curDir, 'CSV Text File (*.csv)')
            if saveFileName:
                curTbl = str(self.queryTblList.currentItem().text())
                if len(curTbl)>0:
                    self.curDB.DUMP_TABLE(curTbl, saveFileName)
                    self.__curDir = getCurDir(saveFileName)
        else:
            self.curDB.DUMP_TABLE(tableName, saveFileName)
            self.__curDir = getCurDir(saveFileName)

    def dumpAllCSVTables(self):
        reply = QtGui.QMessageBox.question(self, "Save All Tables", "Do you want to save all the tables to CSV?\nThis could take a while depending on the size of your database.",\
                                           QtGui.QMessageBox.Yes|QtGui.QMessageBox.Cancel)
        if reply == QtGui.QMessageBox.Yes:
            if self.dbStatus:
                tblList = self.curDB.LIST_TABLES()
                if len(tblList)>0:
                    for tbl in tblList:
                        #need to add a place to save to a directory
                        fileName = os.path.join(self.__curDir, (tbl+'.csv'))
                        self.saveCSVTable(tbl, fileName)

    def getFragSpectrum(self):
        curCol = self.SelectInfoWidget.currentColumn()
        if self.SelectInfoWidget.currentItem() == None:
            return False
            #print "Current index: ",  self.SelectInfoWidget.currentRow(), curCol
        else:
            try:
                curItem = self.SelectInfoWidget.item(1, 1)
                indexVal = int(curItem.text())
                #indexVal +=-1#this is because we are counting from zero, but the index table counts from 1
                curSeq = self.activeData['pepID'][indexVal]
                xData = self.activeData['xFrags'][indexVal]#this is text and needs to be converted
                yData = self.activeData['yFrags'][indexVal]
                tableText = str(self.SelectInfoWidget.item(0, 1).text())
                eValText = str(self.activeData['pep_eVal'][indexVal])
                theoMZText = '%.2f'%self.activeData['theoMZ'][indexVal]
                ppmText = '%d'%self.activeData['ppm_error'][indexVal]
                fragTitle = tableText+', '+'Index: '+str(indexVal)+', '+curSeq
                textTag='\n'
                textTag+='e-Val: '
                textTag+= eValText
                textTag+='\n'
                textTag+='m/z: '
                textTag+=theoMZText
                textTag+='\n'
                textTag+='ppm error: '
                textTag+=ppmText

                tempXList = xData.split()
                tempYList = yData.split()
#                print type(tempXList), type(tempYList)
#                print tempXList
                xData = N.array(tempXList, dtype = N.float)#conver to array with dtype set or it will default to string types
                yData = N.array(tempYList, dtype = N.float)
                curFragPlot = FragPlotWidgets.FragPlot(curSeq, xData, yData, title = fragTitle, annotation = textTag)
                curFragPlot.show()
                self.openPlotList.append(curFragPlot)
#                print indexVal
#                print curSeq
#                print xData
#                print yData

#                curType = self.infoMap[str(curItem.text())]
#                curVal = self.curSelectInfo[str(curItem.text())]
#                curTbl = self.curTbl
            except:
                raise

    def showTable(self):
        curItem = self.queryTblList.currentItem()
        if curItem != None:
            curTbl = str(curItem.text())
            if self.dbStatus:
                ok, result, colNames = self.curDB.GET_TABLE(curTbl)
                if ok:
                    self.openTableList.append(DBTable(result, enableSort = True, title = curTbl, colHeaderList = colNames))
                    self.curDBTable = self.openTableList[-1]#append adds to the end of the list so adding the most recent addition

    def commitFullQuery(self):
        '''
        Writes the result of the current query to the database
        '''
        if self.dbStatus:
            queryStr = str(self.sqlQueryString.toPlainText())
            if queryStr != None:
                try:
                    newTableName, result, colNames = self.curDB.EXEC_QUERY_W_NEW_TABLE(queryStr)
                    #EXEC_QUERY_W_NEW_TABLE asks for a table name unless it is give
                    self.sqlErrorMessage.setText('No Error')
                    print len(result)
                    if len(result) > 0 and newTableName != None:
                        if len(queryStr) > 50:
                            tempTitle = queryStr[0:50]+'...'
                        else:
                            tempTitle = queryStr

                        self.openTableList.append(DBTable(result, enableSort = True, title = newTableName, colHeaderList = colNames))
                        self.curDBTable = self.openTableList[-1]#append adds to the end of the list so adding the most recent addition

                        curResults = XT_RESULTS(parseFile = False)
                        self.curDB.READ_CUSTOM_VALUES(newTableName, curResults)
                        self.activeDict[newTableName] = curResults
                        self.__resetDB__()

                except:
                    self.sqlErrorMessage.setText(str(sys.exc_value))
#                    errorMsg = "Error: %s\n\n%s\n"%(sys.exc_type, sys.exc_value)
#                    errorMsg+='\n There was an error executing the SQL Query.'
#                    return QtGui.QMessageBox.information(self,'SQL Execute Error', errorMsg)

    def parseCombined(self, combinedResults, headerList = None, tblNames = None):
        '''
        Parses and formats the combined results from UNIQUE_PEP_PRO_FULL
        How to commit to database?
        '''
        newResults = []
        print "Col Names ", headerList
        for i,result in enumerate(combinedResults):
            curTable = tblNames[i]
            newResults.append([curTable])
            print "\n\n%s"%curTable
            for row in result:
                #print row
                newResults.append(row)
        tblTitle = 'Cross Table Peptide Stats'
        self.openTableList.append(DBTable(newResults, enableSort = False, title = tblTitle, colHeaderList = headerList))
        self.curDBTable = self.openTableList[-1]#append adds to the end of the list so adding the most recent addition

    def UNIQUE_PEP_PRO_FULL(self):
        '''
        The idea here is to get a full on list of peptides
        across tables along with the status associated with each
        Using a _CommonList the peptides for each table are compared and
        the stats computed
        '''
        cmnTableName = '_CommonList'
        tblList = []
        for i in xrange(self.queryTblList.count()):
            curItem = self.queryTblList.item(i)
            if curItem.checkState() == 2:# Item is selected: QtCore.Qt.Checked
                tblList.append(str(curItem.text()))
        if len(tblList)>1:
            if self.dbStatus:
                self.sqlQueryString.clear()
                queryStr = QF.GET_UNIQUE_PEPTIDE_GROUP_SIMPLE(tblList)
                self.sqlQueryString.setText(queryStr)
                #commit _CommonList to database and use this for
                #future searches for each
                ANS = self.curDB.EXEC_QUERY_W_NEW_TABLE(queryStr, newTableName = cmnTableName, overWrite = True)
                newTableName, result, colNames = ANS
                ##FIX THIS?????
                self.activeDict[newTableName] = result
                self.__resetDB__()

                if len(result) == 0:
                    #Terminate call if an empty string is returned
                    self.sqlErrorMessage.setText('No Error, but an empty result was returned')
                    return False
                combinedResults = []#used to hold combined stats for each table
                for tblName in tblList:
                    queryStr = QF.GET_COMMON_WITH_STATS(tblName, cmnTableName)
                    self.curDB.cur.execute(queryStr)
                    result = self.curDB.GET_CURRENT_QUERY()
                    colNames = self.curDB.GET_COLUMN_NAMES()
                    if len(result) == 0:
                        #Terminate call if an empty string is returned
                        self.sqlErrorMessage.setText('No Error, but an empty result was returned')
                        return False
                    else:
                        combinedResults.append(result)

                self.parseCombined(combinedResults, headerList = colNames, tblNames = tblList)


#                self.viewQueryResults()
        elif len(tblList) == 1:#need to just show for a single table....
            curTbl = tblList[0]
            queryStr = QF.GET_UNIQUE_PEPTIDES_BY_PROTEIN(curTbl)
            self.sqlQueryString.setText(queryStr)
#            self.viewQueryResults()

    def UNIQUE_PEP_PRO(self):
        tblList = []
        for i in xrange(self.queryTblList.count()):
            curItem = self.queryTblList.item(i)
            if curItem.checkState() == 2:# QtCore.Qt.Checked:
                tblList.append(str(curItem.text()))
        if len(tblList)>1:
            if self.dbStatus:
                self.sqlQueryString.clear()
                queryStr = QF.GET_UNIQUE_PEP_PRO_GROUP(tblList)
                self.sqlQueryString.setText(queryStr)
#                self.viewQueryResults()
        elif len(tblList) == 1:#need to just show for a single table....
            curTbl = tblList[0]
            queryStr = QF.GET_UNIQUE_PEPTIDES_BY_PROTEIN(curTbl)
            self.sqlQueryString.setText(queryStr)
#            self.viewQueryResults()

    def UNIQUE_PROTEINS(self):
        curItem = self.queryTblList.currentItem()
        if curItem != None:
            curTbl = str(curItem.text())
            if self.dbStatus:
                self.sqlQueryString.clear()
                queryStr = QF.GET_UNIQUE_PROTEINS(curTbl)
                self.sqlQueryString.setText(queryStr)
#                self.viewQueryResults()

    def UNIQUE_PEPTIDES(self):
        curItem = self.queryTblList.currentItem()
        if curItem != None:
            curTbl = str(curItem.text())
            if self.dbStatus:
                self.sqlQueryString.clear()
                queryStr = QF.GET_UNIQUE_PEPTIDES(curTbl)
                self.sqlQueryString.setText(queryStr)
#                self.viewQueryResults()

    def GROUP_UNIQUE_PEPTIDES_BY_PROTEIN(self):
        curItem = self.queryTblList.currentItem()
        if curItem != None:
            curTbl = str(curItem.text())
            if self.dbStatus:
                self.sqlQueryString.clear()
                queryStr = QF.GET_UNIQUE_PEPTIDES_BY_PROTEIN(curTbl)
                self.sqlQueryString.setText(queryStr)
#                self.viewQueryResults()

    def MULTI_UNIQUE_PEPTIDE_GROUP(self):
        tblList = []
        for i in xrange(self.queryTblList.count()):
            curItem = self.queryTblList.item(i)
            if curItem.checkState() == 2:# QtCore.Qt.Checked:
                tblList.append(str(curItem.text()))
        if len(tblList)>1:
            if self.dbStatus:
                self.sqlQueryString.clear()
#                queryStr = QF.GET_UNIQUE_PEPTIDE_GROUP(tblList)
                queryStr = QF.GET_UNIQUE_PEPTIDE_GROUP_SIMPLE(tblList)
                self.sqlQueryString.setText(queryStr)
#                self.viewQueryResults()
        elif len(tblList) == 1:#need to just show for a single table....
            curTbl = tblList[0]
            queryStr = QF.GET_UNIQUE_PEPTIDES_BY_PROTEIN(curTbl)
            self.sqlQueryString.setText(queryStr)
#            self.viewQueryResults()


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
        self.EmptyArrayText = "There is no data in the array selected.  Perhaps the search criteria are too stringent.  Check ppm and e-Value cutoff values.\n"

    def __additionalVariables__(self):
        '''Extra variables that are utilized by other functions'''
        self.__curDir = getHomeDir()
        self.firstLoad = True

    def __additionalConnections__(self):
        '''SelectInfoWidget context menu actions'''
        self.selectDBFieldAction = QtGui.QAction("Select Table By Field", self)
        self.SelectInfoWidget.addAction(self.selectDBFieldAction)
        QtCore.QObject.connect(self.selectDBFieldAction,QtCore.SIGNAL("triggered()"), self.selectDBField)

        self.saveDBFieldAction = QtGui.QAction("Save New Table By Field", self)
        self.SelectInfoWidget.addAction(self.saveDBFieldAction)
        QtCore.QObject.connect(self.saveDBFieldAction,QtCore.SIGNAL("triggered()"), self.saveQueryTable)

        '''Database View, Add, Remove Tools'''
        self.removeTableAction = QtGui.QAction("Remove Table from Database", self)
        self.queryTblList.addAction(self.removeTableAction)
        QtCore.QObject.connect(self.removeTableAction, QtCore.SIGNAL("triggered()"), self.removeTable)

        self.dumpTableAction = QtGui.QAction("Save Table to CSV", self)
        self.queryTblList.addAction(self.dumpTableAction)
        QtCore.QObject.connect(self.dumpTableAction, QtCore.SIGNAL("triggered()"), self.saveCSVTable)

        self.showTableAction = QtGui.QAction("Show Table", self)
        self.queryTblList.addAction(self.showTableAction)
        QtCore.QObject.connect(self.showTableAction, QtCore.SIGNAL("triggered()"), self.showTable)

        QtCore.QObject.connect(self.actionSave_All_Tables, QtCore.SIGNAL("triggered()"), self.dumpAllCSVTables)
        QtCore.QObject.connect(self.actionCopy_Current_Database, QtCore.SIGNAL("triggered()"), self.copyCurrentDatabase)

        '''Fragment Display Tools'''
        self.getFragAction = QtGui.QAction("Display Fragment Spectrum", self)
        self.queryTblList.addAction(self.getFragAction)
        QtCore.QObject.connect(self.getFragAction, QtCore.SIGNAL("triggered()"), self.getFragSpectrum)

        '''Plot GUI Interaction slots'''
        QtCore.QObject.connect(self.db_TableList, QtCore.SIGNAL("itemPressed (QListWidgetItem *)"), self.setColLists)
        QtCore.QObject.connect(self.updatePlotBtn, QtCore.SIGNAL("clicked()"), self.updatePlot)
        QtCore.QObject.connect(self.clearPlotBtn, QtCore.SIGNAL("clicked()"), self.clearPlot)

        '''Query GUI slots'''
        QtCore.QObject.connect(self.queryTblList, QtCore.SIGNAL("itemPressed (QListWidgetItem *)"), self.setQueryLists)
        QtCore.QObject.connect(self.dbExecuteQuery,QtCore.SIGNAL("clicked()"),self.executeSQLQuery)
        QtCore.QObject.connect(self.viewQueryBtn,QtCore.SIGNAL("clicked()"),self.viewQueryResults)
        QtCore.QObject.connect(self.dumpDBBtn,QtCore.SIGNAL("clicked()"),self.dumpCurDB)

        self.queryByTypeAction=QtGui.QAction("Query By Type Value",  self)
        self.queryFieldList.addAction(self.queryByTypeAction)
        QtCore.QObject.connect(self.queryByTypeAction,QtCore.SIGNAL("triggered()"), self.queryByType)

        '''Peptide and Protein Query slots'''
        self.uniquePeptidesAction = QtGui.QAction("Get Unique Peptides", self)
        self.queryTblList.addAction(self.uniquePeptidesAction)
        QtCore.QObject.connect(self.uniquePeptidesAction, QtCore.SIGNAL("triggered()"), self.UNIQUE_PEPTIDES)

        self.uniqueProteinsAction = QtGui.QAction("Get Unique Proteins", self)
        self.queryTblList.addAction(self.uniqueProteinsAction)
        QtCore.QObject.connect(self.uniqueProteinsAction, QtCore.SIGNAL("triggered()"), self.UNIQUE_PROTEINS)

        self.uniquePepProAction = QtGui.QAction("Get Unique Proteins and Peptides Across Tables", self)
        self.queryTblList.addAction(self.uniquePepProAction)
        QtCore.QObject.connect(self.uniquePepProAction, QtCore.SIGNAL("triggered()"), self.UNIQUE_PEP_PRO)

        self.uniquePepByProtAction = QtGui.QAction("Get Unique Peptides by Protein", self)
        self.queryTblList.addAction(self.uniquePepByProtAction)
        QtCore.QObject.connect(self.uniquePepByProtAction, QtCore.SIGNAL("triggered()"), self.GROUP_UNIQUE_PEPTIDES_BY_PROTEIN)

        self.uniqueMultiPepAction = QtGui.QAction("Group Unique Peptides Across Tables", self)
        self.queryTblList.addAction(self.uniqueMultiPepAction)
        QtCore.QObject.connect(self.uniqueMultiPepAction, QtCore.SIGNAL("triggered()"), self.MULTI_UNIQUE_PEPTIDE_GROUP)

        self.uniqueMultiPepStatsAction = QtGui.QAction("Group Unique Peptides Across Tables with Stats", self)
        self.queryTblList.addAction(self.uniqueMultiPepStatsAction)
        QtCore.QObject.connect(self.uniqueMultiPepStatsAction, QtCore.SIGNAL("triggered()"), self.UNIQUE_PEP_PRO_FULL)

        '''Database Connection slots'''
        QtCore.QObject.connect(self.openDBButton, QtCore.SIGNAL("clicked()"), self.setDBConnection)
        QtCore.QObject.connect(self.useMemDB_CB, QtCore.SIGNAL("stateChanged (int)"), self.setMemDB)
        QtCore.QObject.connect(self.dbCommitQuery, QtCore.SIGNAL("clicked()"), self.commitFullQuery)


        '''File menu actions slots'''
        QtCore.QObject.connect(self.action_Open,QtCore.SIGNAL("triggered()"),self.__readDataFile__)
        QtCore.QObject.connect(self.actionLoad_Folder,QtCore.SIGNAL("triggered()"),self.__loadDataFolder__)
        QtCore.QObject.connect(self.action_Save,QtCore.SIGNAL("triggered()"),self.__saveDataFile__)
        QtCore.QObject.connect(self.actionFileOpen,QtCore.SIGNAL("triggered()"),self.__readDataFile__)
        QtCore.QObject.connect(self.actionAbout,QtCore.SIGNAL("triggered()"),self.__showAbout__)

        QtCore.QObject.connect(self.actionHints,QtCore.SIGNAL("triggered()"),self.__showHints__)
        QtCore.QObject.connect(self.action_Exit,QtCore.SIGNAL("triggered()"),self.__exitProgram__)

        QtCore.QObject.connect(self.actionTools, QtCore.SIGNAL("triggered()"),self.__testFunc__)
        #QtCore.QObject.connect(self.MainWindow,QtCore.SIGNAL("close()"),self.__exitProgram__)


        QtCore.QMetaObject.connectSlotsByName(self)#MainWindow)

###########################################################

    def closeEvent(self,  event = None):
        if self.okToExit():
            self.closeOpenWindows()
            pass
        else:
            event.ignore()

    def resetData(self, dbName = None):
#        self.plotWidget.canvas.ax.cla()
        if dbName != None:
            self.startup(dbName = dbName)
        else:
            self.startup()

    def __exitProgram__(self):
        self.close()

    def okToExit(self):
        #add a question to save memory database to file
        if self.dbStatus:
            reply = QtGui.QMessageBox.question(self, "Save Changes & Exit?", "Commit changes to database and exit? Press discard to exit without saving.",\
                                               QtGui.QMessageBox.Yes|QtGui.QMessageBox.Discard|QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Yes:
                if self.dbStatus:
                    if self.curDB.dbName == ':memory:':
                        self.copyCurrentDatabase()
                    self.curDB.cnx.commit()
                    self.curDB.close()
                return True

            elif reply == QtGui.QMessageBox.Discard:
                if self.dbStatus:
                    self.curDB.close()
                return True

            elif reply == QtGui.QMessageBox.Cancel:
                return False
        else:
            return False

    def __askConfirm__(self,title,message):
        clickedButton = QtGui.QMessageBox.question(self,\
                                                   title,message,\
                                                   QtGui.QMessageBox.Yes,QtGui.QMessageBox.Cancel)
        if clickedButton == QtGui.QMessageBox.Yes: return True
        return False

    def __showHints__(self):
        return QtGui.QMessageBox.information(self,
                                             ("Hints and known Issues"),
                                             ("<p>1.  More soon! </p>"))

    def __showAbout__(self):
        return QtGui.QMessageBox.information(self,
                                            ("X!Tandem Viewer v0.8, November, 2009"),
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
    #MainWindow = QtGui.QMainWindow()
    ui = XTViewer()
    ui.show()
    #ui = XTViewer(MainWindow)
    #MainWindow.show()
    sys.exit(app.exec_())


def getCurDir(dirString):
    tempStr = str(dirString)#incase it is a QString
    if os.path.isfile(tempStr):
        return os.path.dirname(tempStr)
    else:
        return os.getcwd()

def valid(path):
    if path and os.path.isdir(path):
        return True
    return False

def env(name):
    return os.environ.get( name, '' )

def getHomeDir():
    if sys.platform != 'win32':
        return os.path.expanduser( '~' )

    homeDir = env( 'USERPROFILE' )
    if not valid(homeDir):
        homeDir = env( 'HOME' )
        if not valid(homeDir) :
            homeDir = '%s%s' % (env('HOMEDRIVE'),env('HOMEPATH'))
            if not valid(homeDir) :
                homeDir = env( 'SYSTEMDRIVE' )
                if homeDir and (not homeDir.endswith('\\')) :
                    homeDir += '\\'
                if not valid(homeDir) :
                    homeDir = 'C:\\'
    return homeDir


if __name__ == "__main__":
    run_main()
