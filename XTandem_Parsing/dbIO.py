
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

#class dbError(object):
#    def __init__(self, msg):
#        self.msg = msg
#    
#    def __str__(self):
#        return self.msg
#        
#class XTandemDB(object):
#    '''Represents the interface to SQLite'''
#    CREATE_RESULTS_TABLE="""
#        create table if not exists xtResults(
#            id integer primary key autoincrement,
#            """


#Row class for PyTables
class XTResultsTable(IsDescription):
    idnum = Int32Col()
    pepID = StringCol(64) 
    pep_eVal = Float64Col()
    scanID = Int32Col()
    ppm_error = Float64Col()
    theoMZ = Float64Col()
    hScore = Float64Col()
    nextScore = Float64Col()
    pepLen = Int32Col()
    proID = StringCol(64)
    pro_eVal = Float64Col()
    
def save_workspace(filename, xtXML):
    #xtXML is an instance of XT_xml found i xtandem_parse_class.py
    
    xtTbl = True
    
    hdf = openFile(filename, mode = "w", title = 'X!Tandem Results')
    varGroup = hdf.createGroup("/", 'pepGroup', 'Peptide Results')
    
    if xtTbl:
        pepTbl = hdf.createTable(varGroup, 'pepResults', XTResultsTable, "XT Peptides")
        xtTbl = False
        peptide = pepTbl.row
        for i in xrange(len(xtXML.scanIndex)):
            peptide['idnum'] = i
            peptide['pepID'] = xtXML.pep_IDs[i]
            peptide['pep_eVal'] = xtXML. pep_eValues[i]
            peptide['scanID'] = xtXML.scanIndex[i]
            peptide['ppm_error'] = xtXML.ppm_errors[i]
            peptide['theoMZ'] = xtXML.theoMZs[i]
            peptide['hScore'] = xtXML.hScores[i]
            peptide['nextScore'] = xtXML.nextScores[i]
            peptide['pepLen'] = xtXML.pepLengths[i]
            peptide['proID'] = xtXML.prot_IDs[i]
            peptide['pro_eVal'] = xtXML.pro_eVals[i]

            peptide.append()

                    
    if xtTbl is False:
        pepTbl.flush()  
    hdf.close()      
