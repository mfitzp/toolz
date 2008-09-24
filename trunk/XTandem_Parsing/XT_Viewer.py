
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


#try:
#    import psyco
#    psyco.full()
#except:
#    print "Pysco not installed, try easy_install psyco at your command prompt"

plot_colors = ['#297AA3','#A3293D','#3B9DCE','#293DA3','#5229A3','#8F29A3','#A3297A',
'#7AA329','#3DA329','#29A352','#29A38F','#A38F29','#3B9DCE','#6CB6DA','#CE6C3B','#DA916C',
'#0080FF','#0000FF','#7ABDFF','#8000FF','#FF0080','#FF0000','#FF8000','#FFFF00','#A35229','#80FF00',
'#00FF00','#00FF80','#00FFFF','#3D9EFF','#FF9E3D','#FFBD7A']

markers = ['o', 'd','>', 's', '^',  'p', '<', 'h', 'v']

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
        self.startup()
        
 
    def startup(self):

        self.curFile = None
        self.curTbl = None
        self.curFileName = None
        self.curDB = None
        self.loadOK = False
        
        self.activeDict = {}
        
        self.dbConnectedBtn.setEnabled(False)
        self.dbStatus = False
        self.setDBConnection()
        
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
        
        self.infoMap = {}
        self.infoMap['Index'] = 'id'
        self.infoMap['Peptide'] = 'pepID'
        self.infoMap['Peptide e-Value'] = 'pep_eValue'
        self.infoMap['Scan'] ='scanID'
        self.infoMap['ppm Error'] ='ppm_error'
        self.infoMap['Theoretical MZ'] ='theoMZ'
        self.infoMap['Hyperscore'] ='hScore'
        self.infoMap['Next Hyperscore'] = 'nextScore'
        self.infoMap['Delta Hyperscore'] = 'deltaH'
        self.infoMap['Peptide Length'] = 'pepLen'
        self.infoMap['Protein ID'] ='proID'
        self.infoMap['Protein e-Value'] = 'pro_eVal'
        
        
        self.__setupPlot__()
        
    
    def __testFunc__(self):
        if self.loadOK:
            print self.curDB.LIST_TABLES()
            print self.curDB.LIST_COLUMNS(self.curDB.LIST_TABLES()[0])
            print type(self.curDB.LIST_TABLES()[0])
            
            activeData = self.activeDict[self.curTbl]
            print activeData.dataDict.keys()
           
    
    
    def setColLists(self,  widgetItem):
        self.db_XCols.clear()
        self.db_YCols.clear()
        self.sizeArrayComboB.clear()
        
        activeData = self.activeDict[str(widgetItem.text())]
        colList = activeData.dataDict.keys()
        colNumList = []
        for col in colList:
            if type(activeData.dataDict[col][0]) is str:
                pass
            else:
                colNumList.append(col)
        if len(colNumList) == 0:
            return QtGui.QMessageBox.warning(self, "Database Table Error",  "No numerical data exist in the selected table!")
        else:
            self.db_XCols.addItems(colNumList)
            self.db_YCols.addItems(colNumList)
            
            self.sizeArrayComboB.addItems(colNumList)

    def executeSQLQuery(self):
        if self.dbStatus:
            queryStr = str(self.sqlQueryString.toPlainText())
            if queryStr != None:
                try:
                    self.curDB.cur.execute(queryStr)
                    self.sqlErrorMessage.setText('No Error')
                    result = self.curDB.GET_CURRENT_QUERY(truncate = True)
                    if len(result) != 0:
                        self.outTableWidget.addData(result)        
                        self.outTableWidget.resizeColumnsToContents()
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
                    result = self.curDB.GET_CURRENT_QUERY(truncate = True)
                    if len(result) != 0:
                        self.curDBTable = DBTable(result)
                        #self.outTableWidget.addData(result)        
                        #self.outTableWidget.resizeColumnsToContents()
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
        self.queryFieldList.clear()
        activeTbls = self.activeDict.keys()
        self.queryTblList.addItems(activeTbls)
        self.queryTblList.setCurrentRow(0)
        self.setQueryLists(self.queryTblList.currentItem())
    
    def updatePlotOptionsGUI(self):
        self.db_TableList.clear()
        self.sizeArrayComboB.clear()
        activeTbls = self.activeDict.keys()
        self.db_TableList.addItems(activeTbls)
        self.db_TableList.setCurrentRow(0)
        self.setColLists(self.db_TableList.currentItem())
        
    
    def setDBConnection(self):#would this be better if you added an old db reference in case it fails?
        if self.useMemDB_CB.isChecked() == True and self.dbStatus == False:
            self.setMemDB(2)
        else:
            dbName = QtGui.QFileDialog.getSaveFileName(self,\
                                             'Select Database: ',\
                                             self.__curDir, 'SQLite Database (*.db)', "", QtGui.QFileDialog.DontConfirmOverwrite)
            if not dbName.isEmpty():
                if self.dbStatus:#(i.e a connection already exists)
                    reply = QtGui.QMessageBox.question(self, "Database Conneciton Exists", "A Database Connection already exists.  Do you want to close the current connection and establish the one just selected?",
                                                   QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        self.curDB.close()
                        self.dbStatus == False
                        if self.useMemDB_CB.isChecked():
                            self.useMemDB_CB.setChecked(False)
                        self.curDBpathname.setText(dbName)
                        self.curDB = dbIO.XT_DB(str(dbName),  parent = self)
                        self.dbStatus = self.curDB.dbOK
                        if self.dbStatus:
                            self.dbConnectedBtn.setEnabled(True)
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
            self.dbStatus = False
    
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
        #state == 2 if checked
        if state == 0:
            return False
        if self.useMemDB_CB.isChecked() and self.dbStatus == False:
            dbName=':memory:'
            self.curDBpathname.setText(dbName)#updates the DB GUI
            self.curDB = dbIO.XT_DB(str(dbName),  parent = self)
            self.dbStatus = self.curDB.dbOK
            if self.dbStatus:
                self.dbConnectedBtn.setEnabled(True)
            else:
                self.setDBError()
                    
        elif self.useMemDB_CB.isChecked() and self.dbStatus == True:
            reply = QtGui.QMessageBox.question(self, "Database Conneciton Exists", "A Database Connection already exists.  Do you want to close the current connection and establish an in-memory database?",
                                           QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.curDB.close()
                self.dbStatus == False
                dbName=':memory:'
                self.curDBpathname.setText(dbName)
                self.curDB = dbIO.XT_DB(str(dbName),  parent = self)
                self.dbStatus = self.curDB.dbOK
                if self.dbStatus:
                    self.dbConnectedBtn.setEnabled(True)
                else:
                    self.setDBError()
            elif reply == QtGui.QMessageBox.No:
                self.useMemDB_CB.setChecked(False)
                
        else:
            self.dbStatus = False
            self.setDBError()
            
    def loadFileXT(self, filename):
        if filename:
            self.fileType= str(filename).split('.')[-1]
        if self.fileType == 'xml':
            if self.dbStatus:
                fnCore = self.getFNCore(str(filename))
                self.curTbl = fnCore
#                try:
                results = XT_RESULTS(filename)
                if results.dataDict == False:
                    raise Exception,  self.EmptyArrayText
                    
                else:
                    self.activeDict[fnCore] = results
                    insertOK = self.curDB.INSERT_XT_VALUES(fnCore, self.activeDict[fnCore])
                    self.loadOK = True
                    if insertOK:
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
            try:
                self.curFile = XT_RESULTS(filename,  parseFile = False)
                dbIO.load_XT_HDF5(str(filename), self.curFile)
                self.initiatePlot()
                self.firstLoad = False
                self.loadOK = True
            except:
                self.loadOK = False
                return QtGui.QMessageBox.information(self,'', "Error reading hfdf5 File.  Are you sure it was created by this program?")
            
        elif self.fileType == 'db':
            try:
                if not self.firstLoad:
                    if self.__askConfirm__("Data Reset",self.ResetAllDataText):
                        self.resetData()
                        #self.resetDB()#Need to implement
                        self.startup()
                
                self.curFile = XT_RESULTS(filename,  parseFile = False)      
                sqldb = dbIO.XT_DB(str(filename), "testTables", createNew = False)#NEED TO FIX THE NAME
                sqldb.READ_XT_VALUES(sqldb.curTblName, self.curFile)
                sqldb.close()
                self.loadOK = True
                self.initiatePlot()
                self.firstLoad = False
            except:
                self.loadOK = False
                return QtGui.QMessageBox.information(self,'', "Error reading db File.  Are you sure it was created by this program?")
            
        else:
            return QtGui.QMessageBox.information(self,'', "Problem loading data, check file")

        
    def __loadDataFolder__(self):
#        if self.dbStatus:
        directory= QtGui.QFileDialog.getExistingDirectory(self,\
                                                         "Select X!Tandem XML Data Folder")
        print directory
        #from os.path import join, abspath
        for root, dirs, files in walk(str(directory)):
            for file in files:
                if '.xml' in file:
                    ##full file path name
                    ffpn=path.abspath(path.join(root, file))
                    print ffpn
                    print file.split('.')[0]
#        if self.filename:
#            if os.sys.platform == 'win32':
#                self.path2write = (self.filename.split('\\'))[-1].replace(".xml", "")+'.ms2'
#            else:
#                self.path2write = (self.filename.split('//'))[-1].replace(".xml", "")+'.ms2'#assumes linux2 and or OSX (win32 uses the 'bad' kind of slash)
            
#        else:
#            self.retryDBConnection()
    
    
    def __readDataFile__(self):
        if self.dbStatus:
            dataFileName = QtGui.QFileDialog.getOpenFileName(self,\
                                                             self.OpenDataText,\
                                                             self.__curDir, 'X!Tandem XML (*.xml);; HDF5 File (*.h5);;SQLite Database (*.db)')
            if dataFileName:
                self.loadFileXT(dataFileName)
        else:
            if self.memDB:
                self.setDBConnection()
                dataFileName = QtGui.QFileDialog.getOpenFileName(self,\
                                            self.OpenDataText,\
                                            self.__curDir, 'X!Tandem XML (*.xml);; HDF5 File (*.h5);;SQLite Database (*.db)')
                if dataFileName:
                    self.loadFileXT(dataFileName)
            else:
                self.retryDBConnection()   

    def __saveDataFile__(self):
        saveFileName = QtGui.QFileDialog.getSaveFileName(self,\
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
                return QtGui.QMessageBox.information(self,'', "A X!Tandem File must be loaded first before saving")
                
    
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
        self.plotWidget.canvas.draw()

        
    def __setupPlot__(self):
        '''Sets up the plot variables used for interaction'''
        self.handleA,  = self.plotWidget.canvas.ax.plot([0], [0], 'o',\
                                        ms=8, alpha=.5, color='yellow', visible=False,  label = 'Cursor A')
        self.is_hZoom = False
        self.plotWidget.canvas.mpl_connect('pick_event', self.OnPickPlot)
    
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
            
            self.plotScatter = self.plotWidget.canvas.ax.scatter(self.x, self.y,  s = sizeList,  color = self.getPlotColor(),  marker = self.getPlotMarker(), alpha = 0.3,  label = self.curTbl,  picker = 5)
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
            
            self.mainTabWidget.setCurrentIndex(0)
        except:
            errorMsg = "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
            errorMsg+='\n Perhaps a "log" axis is checked or a large number is being used for the size modifier?'
            QtGui.QMessageBox.warning(self, "Plot Update",  errorMsg)
            
    def initiatePlot(self):
        self.plotWidget.canvas.ax.cla()
        self.__setupPlot__()
        activeData = self.activeDict[self.curTbl]
        self.x = activeData.dataDict.get('pep_eValue')
        #self.x = self.curFile.dataDict.get('hScores')
        self.y = activeData.dataDict.get('deltaH')#(activeData.dataDict.get('hScores')-activeData.dataDict.get('nextScores'))
        sizeList = activeData.dataDict.get('pepLen')**1.5
        self.plotScatter = self.plotWidget.canvas.ax.scatter(self.x, self.y,  s = sizeList,  color = self.getPlotColor(),  marker = self.getPlotMarker(), alpha = 0.3,  label = self.curTbl,  picker = 5)#add label = ??
        self.plotWidget.canvas.ax.set_xscale('log')
        xmin = N.min(self.x)/10
        xmax = N.max(self.x)*10
        self.plotWidget.canvas.ax.set_xlim(xmin, xmax)        
        
        self.plotWidget.canvas.xtitle="Peptide e-Value"
        self.plotWidget.canvas.ytitle="Delta Hyperscore"
        self.plotWidget.canvas.PlotTitle = self.curTbl
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
        activeData = self.activeDict[activeKey]
        self.curSelectInfo['Index'] = str(index)
        self.curSelectInfo['Peptide'] = activeData.dataDict.get('pepID')[index]
        self.curSelectInfo['Peptide e-Value'] = str(activeData.dataDict.get('pep_eValue')[index])
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
                newitem = QtGui.QTableWidgetItem(entry)
                self.SelectInfoWidget.setItem(n, m, newitem)
                m+=1
            n+=1
        
        self.SelectInfoWidget.resizeColumnsToContents()

    
    def onselect(self, xmin, xmax):
            #print xmin,  xmax
            if self.is_hZoom:
                self.plotWidget.canvas.ax.set_xlim(xmin,  xmax)
                self.plotWidget.canvas.draw()
                
    
            
    def __initContextMenus__(self):
        self.plotWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.SelectInfoWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.queryFieldList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.plotWidget.connect(self.plotWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.plotTabContext)
        self.SelectInfoWidget.connect(self.SelectInfoWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.SelectInfoTabContext)
        self.queryFieldList.connect(self.queryFieldList, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.queryFieldContext)
    
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
                    result = self.curDB.GET_VALUE_BY_TYPE(curTbl, curType, curVal,  savePrompt = True)
                else:
                    result = self.curDB.GET_VALUE_BY_TYPE(curTbl, curType, curVal)
                if result == False:
                    print "User aborted query"
                else:
                    if len(result) == 0:
                        result = ['No data was found...', ]
                    #print result
                    #else:
                    colHeaders = self.curDB.LIST_COLUMNS(curTbl)
                    self.curDBTable = DBTable(result,  colHeaders)
                
            except:
                errorMsg = "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
                errorMsg+='\n GET_VALUE_BY_TYPE Failed!\nThere was a problem retrieving the information from the database.'
                QtGui.QMessageBox.warning(self, "Select Database Field Error",  errorMsg)
                
        
    def saveQueryTable(self):
        self.selectDBField(saveTable = True)         
    
    def queryByType(self):
        curField = str(self.queryFieldList.currentItem().text())
        curTbl = str(self.queryTblList.currentItem().text())
        if curField != None and curTbl != None:
            queryValue , ok = QtGui.QInputDialog.getText(self, 'Enter Query Value',\
                                'Enter %s to Query From %s: '%(curField, curTbl), QtGui.QLineEdit.Normal, '')
            if ok:
                queryValue = str(queryValue)
                if len(queryValue) != 0:#make sure the user didn't leave the prompt blank
                    result = self.curDB.GET_VALUE_BY_TYPE(curTbl,  curField,  queryValue)
                    if len(result) == 0:
                        result = ['No data was found...', ]
                    colHeaders = self.curDB.LIST_COLUMNS(curTbl)
                    self.curDBTable = DBTable(result,  colHeaders)
                    
            #print curField,  curTbl
   
    def queryFieldContext(self, point):
        queryCT_menu = QtGui.QMenu("Menu",  self.queryFieldList)
        queryCT_menu.addAction(self.queryByTypeAction)
        queryCT_menu.exec_(self.queryFieldList.mapToGlobal(point))
        #queryCT_menu
    
    def SelectInfoTabContext(self,  point):
        '''Create a context menu for the SelectInfoWidget which is a QTableWidget'''
        infoCT_menu = QtGui.QMenu("Menu",  self.SelectInfoWidget)
        infoCT_menu.addAction(self.selectDBFieldAction)
        infoCT_menu.addAction(self.saveDBFieldAction)
        infoCT_menu.exec_(self.SelectInfoWidget.mapToGlobal(point))
    
    def plotTabContext(self, point):
        '''Create a menu for mainTabWidget'''
        plotCT_menu = QtGui.QMenu("Menu", self.plotWidget)
        plotCT_menu.addAction(self.plotWidget.hZoom)
        plotCT_menu.addAction(self.plotWidget.actionAutoScale)
        #plotCT_menu.addAction(self.actionToggleDraw)
        plotCT_menu.exec_(self.plotWidget.mapToGlobal(point))
      
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
        self.__curDir = os.getcwd()
        self.firstLoad = True


        
    def __additionalConnections__(self):
        '''SelectInfoWidget context menu actions'''
        self.selectDBFieldAction = QtGui.QAction("Select Table By Field",  self)#self)
        self.SelectInfoWidget.addAction(self.selectDBFieldAction)
        QtCore.QObject.connect(self.selectDBFieldAction,QtCore.SIGNAL("triggered()"), self.selectDBField)
        
        self.saveDBFieldAction = QtGui.QAction("Save New Table By Field",  self)#self)
        self.SelectInfoWidget.addAction(self.saveDBFieldAction)
        QtCore.QObject.connect(self.saveDBFieldAction,QtCore.SIGNAL("triggered()"), self.saveQueryTable)
        
        '''Plot GUI Interaction slots'''
        QtCore.QObject.connect(self.db_TableList, QtCore.SIGNAL("itemPressed (QListWidgetItem *)"), self.setColLists)
        QtCore.QObject.connect(self.updatePlotBtn, QtCore.SIGNAL("clicked()"), self.updatePlot)
        
        '''Query GUI slots'''
        QtCore.QObject.connect(self.queryTblList, QtCore.SIGNAL("itemPressed (QListWidgetItem *)"), self.setQueryLists)
        QtCore.QObject.connect(self.dbExecuteQuery,QtCore.SIGNAL("clicked()"),self.executeSQLQuery)        
        QtCore.QObject.connect(self.viewQueryBtn,QtCore.SIGNAL("clicked()"),self.viewQueryResults)
        QtCore.QObject.connect(self.dumpDBBtn,QtCore.SIGNAL("clicked()"),self.dumpCurDB)
        
        self.queryByTypeAction=QtGui.QAction("Query By Type Value",  self)
        self.queryFieldList.addAction(self.queryByTypeAction)
        QtCore.QObject.connect(self.queryByTypeAction,QtCore.SIGNAL("triggered()"), self.queryByType)
        
        
        '''Database Connection slots'''
        QtCore.QObject.connect(self.openDBButton, QtCore.SIGNAL("clicked()"), self.setDBConnection)
        QtCore.QObject.connect(self.useMemDB_CB, QtCore.SIGNAL("stateChanged (int)"), self.setMemDB)
        
        '''File menu actions slots'''
        QtCore.QObject.connect(self.action_Open,QtCore.SIGNAL("triggered()"),self.__readDataFile__)
        QtCore.QObject.connect(self.actionLoad_Folder,QtCore.SIGNAL("triggered()"),self.__loadDataFolder__)
        QtCore.QObject.connect(self.action_Save,QtCore.SIGNAL("triggered()"),self.__saveDataFile__)
        QtCore.QObject.connect(self.actionFileOpen,QtCore.SIGNAL("triggered()"),self.__readDataFile__)
        QtCore.QObject.connect(self.actionAbout,QtCore.SIGNAL("triggered()"),self.__showAbout__)
        QtCore.QObject.connect(self.actionTools, QtCore.SIGNAL("triggered()"),self.__testFunc__)
        QtCore.QObject.connect(self.actionHints,QtCore.SIGNAL("triggered()"),self.__showHints__)
        QtCore.QObject.connect(self.action_Exit,QtCore.SIGNAL("triggered()"),self.__exitProgram__)
        #QtCore.QObject.connect(self.MainWindow,QtCore.SIGNAL("close()"),self.__exitProgram__)
        

        QtCore.QMetaObject.connectSlotsByName(self)#MainWindow)
    
###########################################################

    def closeEvent(self,  event = None):
        if self.okToExit():
            pass
        else:
            event.ignore()

    def resetData(self):
        self.plotWidget.canvas.ax.cla()
        self.startup()
        
    def __exitProgram__(self):
        self.close()
    
    def okToExit(self):
        if self.dbStatus:
            reply = QtGui.QMessageBox.question(self, "Save Changes & Exit?", "Commit changes to database and exit? Press discard to exit without saving.",\
                                               QtGui.QMessageBox.Yes|QtGui.QMessageBox.Discard|QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Yes:
                if self.dbStatus:
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
                                             ("<p> 1.	For files that contain spectra with a high degree of detail (i.e. not stick mass spectra) use the profile mode for drawing (Ctrl+D).  Otherwise, the plotting will be slow.</p>"
                                             "<p> 2. I haven't incorporated MS^n (where n >= 3) spectrum views at this point--I didn't have an example file to test.</p>"
                                             "<p>3.  If the program is too slow, remember python is not or ever intended to be C.</p>"
                                             "<p>4.  I have not incorporated a reader for mzData files as this format does not explictly store base peak and TIC values for chromatogram generation.  In order to do this each scan must be read simply to construct the TIC/BPC.  This is very slow.  The new mzML format will be supported in the very near future.</p>"))
  
    def __showAbout__(self):
        return QtGui.QMessageBox.information(self,
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
    ui = XTViewer()
    ui.show()
    #ui = XTViewer(MainWindow)
    #MainWindow.show()
    sys.exit(app.exec_())


'''CREATE TABLE test AS SELECT * FROM Vlad_Test WHERE theoMZ > 700 --Creates a new table from the selection criteria
SELECT DISTINCT proID FROM Vlad_Test
CREATE TABLE dualTest AS SELECT DISTINCT proID, pepID FROM Vlad_Test;
'''


if __name__ == "__main__":
    run_main()
