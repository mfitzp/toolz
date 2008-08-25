import os
import sqlite3 as sql
from tables import *
import numpy as N

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
class XTandemDB(object):
    '''Represents the interface to SQLite'''
    CREATE_RESULTS_TABLE="""
        CREATE TABLE IF NOT EXISTS xtResults(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pepID TEXT,
            pep_eVal REAL,
            scanID INTEGER,
            ppm_error REAL,
            theoMZ REAL,
            hScore REAL,
            nextScore REAL,
            pepLen INTEGER,
            propsID TEST,
            pro_eVal REAL            
            """
    
    GET_ALL_RESULTS = '''SELECT * FROM xtResults'''
    GET_ITEM_RANGE = '''SELECT * FROM xtResults WHERE ?>=? and ?<=?'''
    
    def __init__(self,  db):#db is the path to the database on disk
        self. cnx = sqlite3.connect(db)
        self.cur = self.cnx.cursor()
        self.cur.execute(self.CREATE_RESULTS_TABLE)


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
        pepTbl.attrs.origFileName = str(xtXML.fileName)
        xtTbl = False
        peptide = pepTbl.row
        for i in xrange(len(xtXML.scanIndex)):
            peptide['idnum'] = i
            peptide['pepID'] = xtXML.pepIDs[i]
            peptide['pep_eVal'] = xtXML. pep_eValues[i]
            peptide['scanID'] = xtXML.scanIndex[i]
            peptide['ppm_error'] = xtXML.ppm_errors[i]
            peptide['theoMZ'] = xtXML.theoMZs[i]
            peptide['hScore'] = xtXML.hScores[i]
            peptide['nextScore'] = xtXML.nextScores[i]
            peptide['pepLen'] = xtXML.pepLengths[i]
            peptide['proID'] = xtXML.proIDs[i]
            peptide['pro_eVal'] = xtXML.pro_eVals[i]

            peptide.append()

                    
    if xtTbl is False:
        pepTbl.flush()  
    hdf.close()

def load_workspace(filename,  xtXML):
    if os.path.isfile(filename):
        
        pepIDs = []
        pep_eValues= []
        scanIndex = []
        ppm_errors = []
        theoMZs = []
        hScores = []
        nextScores = []
        pepLengths= []
        proIDs = []
        pro_eVals = []
        
        origFileName = None
        
        hdf = openFile(filename, mode = "r")
        groupDict = hdf.root._v_groups
        if groupDict.has_key('pepGroup'):
            for node in hdf.root.pepGroup._f_iterNodes():
                if node._c_classId is 'TABLE':
                    origFileName = node.attrs.origFileName
                    for row in node.iterrows():
                        pepIDs.append(row['pepID'])
                        pep_eValues.append(row['pep_eVal'])
                        scanIndex.append(row['scanID'])
                        ppm_errors.append(row['ppm_error'])
                        theoMZs.append(row['theoMZ'])
                        hScores.append(row['hScore'])
                        nextScores.append(row['nextScore'])
                        pepLengths.append(row['pepLen'])
                        proIDs.append(row['proID'])
                        pro_eVals.append(row['pro_eVal'])
                
        
        hdf.close()
        arrayDict = {
                        'pepIDs': pepIDs, 
                        'pep_eValues' : N.array(pep_eValues), 
                        'scanIndex' : N.array(scanIndex), 
                        'ppm_errors':N.array(ppm_errors),
                        'theoMZs':N.array(theoMZs), 
                        'hScores':N.array(hScores),
                        'nextScores':N.array(nextScores),
                        'pepLengths':N.array(pepLengths), 
                        'proIDs':proIDs, 
                        'pro_eVals':N.array(pro_eVals)
                        }
        xtXML.setArrays(arrayDict)
        xtXML.setFN(origFileName)
