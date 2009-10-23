import os, sys
import sqlite3 as sql
import tables as T
import numpy as N

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog,  QApplication

import time

'''

Example Queries

SELECT LB8W1_1_Output.pepID, LB8W1_1_Output.pep_eVal, YP_TSB_1.pepID, YP_TSB_1.pep_eVal FROM LB8W1_1_Output, YP_TSB_1 WHERE LB8W1_1_Output.pepID = YP_TSB_1.pepID;

SELECT table1.column1, table2.column2 FROM table1, table2 WHERE table1.column1 = table2.column1;
SELECT LB8W1_1_Output.pepID, YP_TSB_1.pepID FROM LB8W1_1_Output, YP_TSB_1 WHERE LB8W1_1_Output.pepID = YP_TSB_1.pepID;

SELECT tbl1.ID, tbl1.fld1, tbl1.fld2 ... FROM tbl1
JOIN tbl2 ON tbl2.ParentID = tbl1.ID
JOIN tbl3 ON tbl3.ParentID = tbl2.ID
WHERE tbl1.ID = 4



tables = ['LB8W1_1_Output', 'YP_TSB_1']#, 'YP_TSB_2', 'GoJoe']
keyWordList = ['SELECT', 'FROM', 'WHERE', 'AND']
primKey = 'pepID'
execStr = ''
selectStr = 'SELECT '
whereStr = ' WHERE '
joinStr = ' JOIN '
fromStr = ' FROM '
andStr = ' AND '
querySep = ', '
numTables = len(tables)

for i,tableName in enumerate(tables):
    selectStr+=tableName
    selectStr+='.*'

    fromStr+=tableName



    if i == numTables-1:
        continue
    else:
        fromStr+=querySep

        selectStr+=querySep

        whereStr+=tables[0]
        whereStr+='.'
        whereStr+=primKey
        whereStr+= ' = '
        whereStr+=tables[i+1]
        whereStr+='.'
        whereStr+=primKey

    if i < numTables-2:
        whereStr+=andStr


selectStr += fromStr
selectStr += whereStr

print selectStr


Example: What customers have never ordered anything from us?

SELECT customers.* FROM customers LEFT JOIN orders ON customers.customer_id = orders.customer_id WHERE orders.customer_id IS NULL

More advanced example using a complex join: What customers have not ordered anything from us in the year 2004 - this one may not work in some lower relational databases (may have to use an IN clause)
SELECT customers.* FROM customers LEFT JOIN orders ON (customers.customer_id = orders.customer_id AND year(orders.order_date) = 2004) WHERE orders.order_id IS NULL


SELECT DISTINCT
  BSATest.pepID,
  BSATest.pep_eVal,
  BSATest.ppm_error,
  Oct_20_BSA.ppm_error,
  Oct_20_BSA.pepID,
  Oct_20_BSA.pep_eVal,
  bsa_Test.pepID,
  bsa_Test.pep_eVal,
  bsa_Test.ppm_error,
  BSATest.proID,
  Oct_20_BSA.proID,
  bsa_Test.proID
FROM
 BSATest
 INNER JOIN Oct_20_BSA ON (BSATest.pepID=Oct_20_BSA.pepID)
 INNER JOIN bsa_Test ON (Oct_20_BSA.pepID=bsa_Test.pepID)


'''

#class dbError(object):
#    def __init__(self, msg):
#        self.msg = msg
#
#    def __str__(self):
#        return self.msg
#
class XT_DB(object):#X!Tandem Database Class
    '''Represents the interface to SQLite'''
    def __init__(self,  db, createNew=False,  tableName = None, parent = None):#db is the path to the database on disk
        if parent:
            self.parent = parent
        self.dbOK = True
        self.dbName = db
        try:
            self.cnx = sql.connect(db)
            self.cur = self.cnx.cursor()
            #self.curTblName = tableName
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

    def READ_CUSTOM_VALUES(self, tableName, XT_RESULTS):
        '''This is for processed query of an XT run'''
        t1 = time.clock()
        tableExists =self.cnx.execute("SELECT COUNT(*) FROM sqlite_master WHERE name=?", (tableName,)).fetchone()[0]
        if tableExists == 0:
            print "Table %s does not exist, ignoring"%tableName
        else:
            tempDict = {}
            self.LIST_COLUMNS(tableName)
            self.colList
            for col in self.colList:
                tempDict[col]=[]

        self.cur.execute('SELECT * FROM "%s"'%tableName)
        for row in self.cur.fetchall():
            '''I don't like this, what if the rows are not in the same order as the columns
            '''
            for i,col in enumerate(self.colList):
                tempDict[col].append(row[i])


        for key in tempDict.iterkeys():
            tempDict[key] = N.array(tempDict[key])

        XT_RESULTS.setArrays(tempDict)
        XT_RESULTS.setFN(tableName)
        self.curTblName=tableName

        t2 = str(time.clock()-t1)
        print "SQLite Read Time for %s (s): %s"%(tableName, t2)


    def INSERT_XT_VALUES(self, tableName, XT_RESULTS):
        '''This is for filling data for a full XT data run, but may not
        be appropriate for a custom table as they may not have all of the appropriate
        keys'''
        t1 = time.clock()
        tableExists =self.cnx.execute("SELECT COUNT(*) FROM sqlite_master WHERE name=?", (tableName,)).fetchone()[0]
        if tableExists == 0:
            self.CREATE_RESULTS_TABLE(tableName)
        else:
            reply = QtGui.QMessageBox.question(self.parent, "Table Already Exists in Database",  "Overwrite existing Table and Overwite?", QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            if reply:
                dropOK = self.DROP_TABLE(tableName)
                if dropOK:
                    self.CREATE_RESULTS_TABLE(tableName)
                    pass
                else:
                    return False
            else:
                return False
        for i in xrange(XT_RESULTS.iterLen):
            self.cur.execute(
                            'INSERT INTO "%s" VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'%tableName,#again I know %s is not recommended but I don't know how to do this more elegantly.
                            (
                            i,
                            XT_RESULTS.dataDict.get('pepID')[i],
                            XT_RESULTS.dataDict.get('pep_eVal')[i],
                            XT_RESULTS.dataDict.get('scanID')[i],
                            XT_RESULTS.dataDict.get('ppm_error')[i],
                            XT_RESULTS.dataDict.get('theoMZ')[i],
                            XT_RESULTS.dataDict.get('hScore')[i],
                            XT_RESULTS.dataDict.get('nextScore')[i],
                            XT_RESULTS.dataDict.get('deltaH')[i],
                            XT_RESULTS.dataDict.get('pepLen')[i],
                            XT_RESULTS.dataDict.get('proID')[i],
                            XT_RESULTS.dataDict.get('pro_eVal')[i]
                            ))
        self.cnx.commit()
        t2 = time.clock()
        print "SQLite Commit Time (s): ", (t2-t1)
        return True

    def close(self):
        self.cnx.close()
        self.dbOK = False

    def LIST_TABLES(self):
        self.tblList = []
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence' ORDER BY name")
        for row in self.cur.fetchall():
            self.tblList.append(str(row[0]))#row[0] by itself produces a unicode object, and row itself is a tuple

        return self.tblList

#    def COPY_DB(self, ):
#        def dump_to_disk(con, filename):
#    """
#    Dumps the tables of an in-memory database into a file-based SQLite database.
#
#    @param con:         Connection to in-memory database.
#    @param filename:    Name of the file to write to.
#    """
#    cur = con.cursor()
#    cur.execute("attach '%s' as __extdb" % filename)
#    cur.execute("select name from sqlite_master where type='table'")
#    table_names = cur.fetchall()
#    for table_name, in table_names:
#        cur.execute("create table __extdb.%s as select * from %s" %
#(table_name, table_name))
#    cur.execute("detach __extdb")


    def LIST_COLUMNS(self,  tableName):
        self.colList = []
        self.cur.execute('PRAGMA table_info(%s)'%tableName)
        for row in self.cur.fetchall():
            self.colList.append(str(row[1]))#row[1] by itself produces a unicode object, and row itself is a tuple, row[1] is the column name
        return self.colList

    def DROP_TABLE(self, tableName):
        try:
            self.cur.execute('DROP TABLE %s'%tableName)
            self.cnx.commit()
            print tableName,  "Dropped"
            return True
        except:
            self.errorMsg = "Sorry: %s:%s"%(sys.exc_type, sys.exc_value)
            msg = self.errorMsg + '\nCheck File Name! No Funky Characters'
            error = QtGui.QMessageBox.warning(self.parent, "Table Drop Error!",  msg)
            return False


    def CREATE_RESULTS_TABLE(self, tableName,  overWrite = False):
        if overWrite:
            self.DROP_TABLE(tableName)

        self.curTblName = tableName

        self.cur.execute('CREATE TABLE IF NOT EXISTS "%s"(id INTEGER PRIMARY KEY AUTOINCREMENT,\
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
        pro_eVal REAL)'
            %tableName)

    #def CREATE_CUSTOM_TABLE(self, tableName, overWrite = False):

    def GET_CURRENT_QUERY(self,  truncate = False):
        result = []
        if truncate:
            lim = 25
            i = 0
            for row in self.cur.fetchall():
                rowList = []
                for item in row:
                    rowList.append(str(item))
                result.append(rowList)#row[0] by itself produces a unicode object, and row itself is a tuple
                i+=1
                if i == lim:#if true then the loop terminates
                    return result
            return result
        else:
            for row in self.cur.fetchall():
                rowList = []
                for item in row:
                    rowList.append(str(item))
                result.append(rowList)
            return result

    def GET_VALUE_BY_TYPE(self, tableName, fieldType, fieldValue, savePrompt = False):
        if savePrompt:
            '''Saves query to the database--only if the user commits to the database upon close of the application'''
            newTableName , ok = QtGui.QInputDialog.getText(self.parent, 'Create New Database Table',\
                                            'Enter New Table Name: ', QtGui.QLineEdit.Normal, 'newTable')
            if ok:
                newTableName = str(newTableName)
                self.LIST_TABLES()#updates self.tblList
                if newTableName in self.tblList:
                    reply = QtGui.QMessageBox.question(self.parent, "Table Creation Conflict", "A table by that name already exists. Do you want to overwrite that table?", QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        self.DROP_TABLE(newTableName)
                    else:
                        return None, []#this will be captured by the len condition on the receiving end...


                self.cur.execute("CREATE TABLE %s AS SELECT * FROM %s WHERE %s LIKE '%s'"%(newTableName, tableName, fieldType, fieldValue))
                self.cur.execute("SELECT * FROM %s"%(newTableName))
                #print "CREATE TABLE %s AS SELECT * FROM %s WHERE %s LIKE '%s'"%(newTableName, tableName, fieldType, fieldValue)
                result = self.GET_CURRENT_QUERY()
                print 'The table named: "%s" created in current database.'%newTableName
                return newTableName, result
            else:#this is the case if the user cancels the input of the new table
                return None, []

        else:
            '''Simply returns the selected query but does not save it to the database'''
            self.cur.execute("SELECT * FROM %s WHERE %s LIKE '%s'"%(tableName, fieldType, fieldValue))
            print "SELECT * FROM %s WHERE %s LIKE '%s'"%(tableName, fieldType, fieldValue)
            result = self.GET_CURRENT_QUERY()
            return None, result

    def GET_VALUE_BY_RANGE(self, tableName, fieldType, loVal, hiVal, savePrompt = False):
        if savePrompt:
            '''Saves query to the database--only if the user commits to the database upon close of the application'''
            newTableName , ok = QtGui.QInputDialog.getText(self.parent, 'Create New Database Table',\
                                            'Enter New Table Name: ', QtGui.QLineEdit.Normal, 'newTable')
            if ok:
                newTableName = str(newTableName)
                self.LIST_TABLES()#updates self.tblList
                if newTableName in self.tblList:
                    reply = QtGui.QMessageBox.question(self.parent, "Table Creation Conflict", "A table by that name already exists. Do you want to overwrite that table?", QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        self.DROP_TABLE(newTableName)
                    else:
                        return False#this will be captured by the len condition on the receiving end...


                self.cur.execute("CREATE TABLE %s AS SELECT * FROM %s WHERE %s > %s AND %s < %s"%(newTableName, tableName, fieldType, str(loVal), fieldType, str(hiVal)))
                self.cur.execute("SELECT * FROM %s"%(newTableName))
                #print "CREATE TABLE %s AS SELECT * FROM %s WHERE %s LIKE '%s'"%(newTableName, tableName, fieldType, fieldValue)
                result = self.GET_CURRENT_QUERY()
                print 'The table named: "%s" created in current database.'%newTableName
                return result
            else:#this is the case if the user cancels the input of the new table
                return False

        else:
            '''Simply returns the selected query but does not save it to the database'''
            self.cur.execute("SELECT * FROM %s WHERE %s > %s AND %s < %s"%(tableName, fieldType, str(loVal), fieldType, str(hiVal)))
            print "SELECT * FROM %s WHERE %s > %s AND %s < %s"%(tableName, fieldType, str(loVal), fieldType, str(hiVal))
            result = self.GET_CURRENT_QUERY()
            return result

    def READ_XT_VALUES(self, tableName, XT_RESULTS):
        '''The XT_RESULTS in this case is empty instance that will be filled, however, it could be one that needs to be updated too.'''
        t1 = time.clock()

        pepID = []
        pep_eValue= []
        scanID = []
        ppm_error = []
        theoMZ = []
        hScores = []
        nextScore = []
        pepLen= []
        proID = []
        pro_eVal = []
        deltaH = []

        self.cur.execute('SELECT * FROM "%s"'%tableName)
        for row in self.cur.fetchall():
            pepID.append(row[1])
            pep_eValue.append(row[2])
            scanID.append(row[3])
            ppm_error.append(row[4])
            theoMZ.append(row[5])
            hScores.append(row[6])
            nextScore.append(row[7])
            deltaH.append(row[8])
            pepLen.append(row[9])
            proID.append(row[10])
            pro_eVal.append(row[11])

        arrayDict = {
                'pepID': pepID,
                'pep_eVal' : N.array(pep_eValue),
                'scanID' : N.array(scanID),
                'ppm_error':N.array(ppm_error),
                'theoMZ':N.array(theoMZ),
                'hScore':N.array(hScores),
                'nextScore':N.array(nextScore),
                'pepLen':N.array(pepLen),
                'proID':proID,
                'pro_eVal':N.array(pro_eVal),
                'deltaH':N.array(deltaH)
                }
        XT_RESULTS.setArrays(arrayDict)
        XT_RESULTS.setFN(tableName)
        self.curTblName=tableName

        t2 = str(time.clock()-t1)
        print "SQLite Read Time for %s (s): %s"%(tableName, t2)

#############################################
'''Begin HDF5 and PyTables Interface'''
#############################################
#Row class for PyTables
class XTResultsTable(T.IsDescription):
    idnum = T.Int32Col()
    pepID = T.StringCol(64)
    pep_eVal = T.Float64Col()
    scanID = T.Int32Col()
    ppm_error = T.Float64Col()
    theoMZ = T.Float64Col()
    hScore = T.Float64Col()
    nextScore = T.Float64Col()
    deltaH = T.Float64Col()
    pepLen = T.Int32Col()
    proID = T.StringCol(64)
    pro_eVal = T.Float64Col()

def save_XT_HDF5(filename, xtXML):
    #xtXML is an instance of XT_RESULTS found i xtandem_parse_class.py

    xtTbl = True
    hdf = T.openFile(filename, mode = "w", title = 'X!Tandem Results')
    try:
        varGroup = hdf.createGroup("/", 'pepGroup', 'Peptide Results')

        if xtTbl:
            pepTbl = hdf.createTable(varGroup, 'pepResults', XTResultsTable, "XT Peptides")
            pepTbl.attrs.origFileName = str(xtXML.fileName)
            xtTbl = False
            peptide = pepTbl.row
            for i in xrange(len(xtXML.dataDict.get('scanID'))):
                peptide['idnum'] = i
                peptide['pepID'] = xtXML.dataDict.get('pepID')[i]
                peptide['pep_eVal'] = xtXML.dataDict.get('pep_eVal')[i]
                peptide['scanID'] = xtXML.dataDict.get('scanID')[i]
                peptide['ppm_error'] = xtXML.dataDict.get('ppm_error')[i]
                peptide['theoMZ'] = xtXML.dataDict.get('theoMZ')[i]
                peptide['hScore'] = xtXML.dataDict.get('hScore')[i]
                peptide['nextScore'] = xtXML.dataDict.get('nextScore')[i]
                peptide['pepLen'] = xtXML.dataDict.get('pepLen')[i]
                peptide['proID'] = xtXML.dataDict.get('proID')[i]
                peptide['pro_eVal'] = xtXML.dataDict.get('pro_eVal')[i]
                peptide['deltaH'] = xtXML.dataDict.get('deltaH')[i]

                peptide.append()


        if xtTbl is False:
            pepTbl.flush()
        hdf.close()
    except:
        hdf.close()

def load_XT_HDF5(filename,  xtXML):
    if os.path.isfile(filename):

        pepID = []
        pep_eValue= []
        scanID = []
        ppm_error = []
        theoMZ = []
        hScore = []
        nextScore = []
        pepLen= []
        proID = []
        pro_eVal = []
        deltaH = []

        origFileName = None

        hdf = T.openFile(filename, mode = "r")
        groupDict = hdf.root._v_groups
        if groupDict.has_key('pepGroup'):
            for node in hdf.root.pepGroup._f_iterNodes():
                if node._c_classId is 'TABLE':
                    origFileName = node.attrs.origFileName
                    for row in node.iterrows():
                        pepID.append(row['pepID'])
                        pep_eValue.append(row['pep_eVal'])
                        scanID.append(row['scanID'])
                        ppm_error.append(row['ppm_error'])
                        theoMZ.append(row['theoMZ'])
                        hScore.append(row['hScore'])
                        nextScore.append(row['nextScore'])
                        pepLen.append(row['pepLen'])
                        proID.append(row['proID'])
                        pro_eVal.append(row['pro_eVal'])
                        deltaH.append(row['deltaH'])


        hdf.close()
        arrayDict = {
                        'pepID': pepID,
                        'pep_eVal' : N.array(pep_eValue),
                        'scanID' : N.array(scanID),
                        'ppm_error':N.array(ppm_error),
                        'theoMZ':N.array(theoMZ),
                        'hScore':N.array(hScore),
                        'nextScore':N.array(nextScore),
                        'pepLen':N.array(pepLen),
                        'proID':proID,
                        'pro_eVal':N.array(pro_eVal),
                        'deltaH':N.array(deltaH)
                        }
        xtXML.setArrays(arrayDict)
        xtXML.setFN(origFileName)
