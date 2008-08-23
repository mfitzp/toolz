
import sqlite3 as sql
from tables import *

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog,  QApplication
    
#    def __saveDataFile__(self):
#        self.curFileName = QtGui.QFileDialog.getSaveFileName(self.MainWindow,\
#                                                             self.SaveDataText,\
#                                                             self.__curDir, 'SubPlot File (*.spf);;HDF5 File (*.h5)')
#        if self.curFileName:
#            #print "File name is: %s" % (str(self.curFileName))
#            hdfIO.save_workspace(str(self.curFileName),  self.localVars.getPubDict(),  self.userScratchDict,  self.plotScripts)
#    
#    def __saveDataFileAs__(self):
#        dataFileName = QtGui.QFileDialog.getSaveFileName(self.MainWindow,\
#                                                         self.SaveDataText,\
#                                                         self.__curDir,'Pqs data (*.pqs)')
#        if dataFileName:
#            print dataFileName
#            print "Currently this function does not do anything"

class dbError(Exeption):
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return self.msg
        
class XTandemDB(object):
    '''Represents the interface to SQLite'''
    CREATE_RESULTS_TABLE="""
        create table if not exists xtResults(
            id integer primary key autoincrement,
            """
#        ppm_errors = []
#        theoMZs = []
#        scanIndex = []
#        pro_eVals=[]
#        self.prot_IDs = []
#        pep_eValues=[]
#        self.pep_IDs = []
#        hScores = []
#        nextScores = []
#        pepLengths = []


#Row class for PyTables
class XTResults(IsDescription):
    idnum = Int64Col()
    pepID = StringCol() 
    pep_eVal = Float64Col()
    scanID = Int64Col()
    ppm_error = Float64Col()
    theoMZ = Float64Col()
    hScore = Float64Col()
    nextScore = Float64Col()
    proID = StringCol()
    pro_eVal = Float64Col()
    
    
