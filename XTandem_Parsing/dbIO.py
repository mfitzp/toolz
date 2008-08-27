import os, sys
import sqlite3 as sql
from tables import *
import numpy as N

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog,  QApplication

import time

#class dbError(object):
#    def __init__(self, msg):
#        self.msg = msg
#    
#    def __str__(self):
#        return self.msg
#        
class XT_DB(object):#X!Tandem Database Class
    '''Represents the interface to SQLite'''    
    def __init__(self,  db, tableName, createNew=True):#db is the path to the database on disk
        self.dbOK = True
        try:
            self.cnx = sql.connect(db)
            self.cur = self.cnx.cursor()
            self.curTblName = tableName
        except:
            self.errorMsg = "Sorry: %s:%s"%(sys.exc_type, sys.exc_value)
            self.dbOK = False
        try:
            if createNew:
                self.CREATE_RESULTS_TABLE(tableName)            
                self.cnx.commit()
        except:
            self.cnx.close()
            raise
    
    def getCurrentTableName(self):
        return self.curTblName
    
    def INSERT_XT_VALUES(self, tableName, XT_RESULTS):
        t1 = time.clock()
        for i in xrange(XT_RESULTS.iterLen):
            self.cur.execute(
                            'INSERT INTO "%s" VALUES (?,?,?,?,?,?,?,?,?,?,?)'%tableName,#again I know %s is not recommended but I don't know how to do this more elegantly.
                            (
                            i, 
                            XT_RESULTS.dataDict.get('pepIDs')[i], 
                            XT_RESULTS.dataDict.get('pep_eValues')[i], 
                            XT_RESULTS.dataDict.get('scanID')[i], 
                            XT_RESULTS.dataDict.get('ppm_errors')[i], 
                            XT_RESULTS.dataDict.get('theoMZs')[i], 
                            XT_RESULTS.dataDict.get('hScores')[i], 
                            XT_RESULTS.dataDict.get('nextScores')[i], 
                            XT_RESULTS.dataDict.get('pepLengths')[i], 
                            XT_RESULTS.dataDict.get('proIDs')[i], 
                            XT_RESULTS.dataDict.get('pro_eVals')[i] 
                            ))
        self.cnx.commit()
        t2 = time.clock()
        print "SQLite Commit Time (s): ", (t2-t1)
        
    def close(self):
        self.cnx.close()
        
    def CREATE_RESULTS_TABLE(self, tableName):
        self.curTblName = tableName
        self.cur.execute('CREATE TABLE IF NOT EXISTS "%s"(id INTEGER PRIMARY KEY AUTOINCREMENT,\
        pepID TEXT,\
        pep_eVal REAL,\
        scanID INTEGER,\
        ppm_error REAL,\
        theoMZ REAL,\
        hScore REAL,\
        nextScore REAL,\
        pepLen INTEGER,\
        proID TEXT,\
        pro_eVal REAL)'
            %tableName)
            
    def READ_XT_VALUES(self, tableName, XT_RESULTS):
        t1 = time.clock()
        
        pepIDs = []
        pep_eValues= []
        scanID = []
        ppm_errors = []
        theoMZs = []
        hScores = []
        nextScores = []
        pepLengths= []
        proIDs = []
        pro_eVals = []
        
        self.cur.execute('SELECT * FROM "%s"'%tableName)
        for row in self.cur.fetchall():
            pepIDs.append(row[1])
            pep_eValues.append(row[2])
            scanID.append(row[3])
            ppm_errors.append(row[4])
            theoMZs.append(row[5])
            hScores.append(row[6])
            nextScores.append(row[7])
            pepLengths.append(row[8])
            proIDs.append(row[9])
            pro_eVals.append(row[10])
            
        arrayDict = {
                'pepIDs': pepIDs, 
                'pep_eValues' : N.array(pep_eValues), 
                'scanID' : N.array(scanID), 
                'ppm_errors':N.array(ppm_errors),
                'theoMZs':N.array(theoMZs), 
                'hScores':N.array(hScores),
                'nextScores':N.array(nextScores),
                'pepLengths':N.array(pepLengths), 
                'proIDs':proIDs, 
                'pro_eVals':N.array(pro_eVals)
                }
        XT_RESULTS.setArrays(arrayDict)
        XT_RESULTS.setFN(tableName)    
        self.curTblName=tableName
        
        t2 = time.clock()
        print "SQLite Read Time (s): ", (t2-t1)
        
#############################################        
'''Begin HDF5 and PyTables Interface'''
#############################################
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
    
def save_XT_HDF5(filename, xtXML):
    #xtXML is an instance of XT_RESULTS found i xtandem_parse_class.py
    
    xtTbl = True
    
    hdf = openFile(filename, mode = "w", title = 'X!Tandem Results')
    varGroup = hdf.createGroup("/", 'pepGroup', 'Peptide Results')
    
    if xtTbl:
        pepTbl = hdf.createTable(varGroup, 'pepResults', XTResultsTable, "XT Peptides")
        pepTbl.attrs.origFileName = str(xtXML.fileName)
        xtTbl = False
        peptide = pepTbl.row
        for i in xrange(len(xtXML.dataDict.get('scanID'))):
            peptide['idnum'] = i
            peptide['pepID'] = xtXML.dataDict.get('pepIDs')[i]
            peptide['pep_eVal'] = xtXML.dataDict.get('pep_eValues')[i]
            peptide['scanID'] = xtXML.dataDict.get('scanID')[i]
            peptide['ppm_error'] = xtXML.dataDict.get('ppm_errors')[i]
            peptide['theoMZ'] = xtXML.dataDict.get('theoMZs')[i]
            peptide['hScore'] = xtXML.dataDict.get('hScores')[i]
            peptide['nextScore'] = xtXML.dataDict.get('nextScores')[i]
            peptide['pepLen'] = xtXML.dataDict.get('pepLengths')[i]
            peptide['proID'] = xtXML.dataDict.get('proIDs')[i]
            peptide['pro_eVal'] = xtXML.dataDict.get('pro_eVals')[i]

            peptide.append()

                    
    if xtTbl is False:
        pepTbl.flush()  
    hdf.close()

def load_XT_HDF5(filename,  xtXML):
    if os.path.isfile(filename):
        
        pepIDs = []
        pep_eValues= []
        scanID = []
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
                        scanID.append(row['scanID'])
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
                        'scanID' : N.array(scanID), 
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
