import os, sys, traceback
import sqlite3 as sql
import numpy as N
import csv

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog,  QApplication

import time

'''

Basic usgae

start new DB
q = queueDB('newDatabase.db')
qTableName = 'queueTable'
q.CREATE_QUEUE_TABLE(qTableName)
q.INSERT_QUEUE_VALUES(qTableName, newQueueDictInstance)


'''

#class dbError(object):
#    def __init__(self, msg):
#        self.msg = msg
#
#    def __str__(self):
#        return self.msg
#
class queueDB(object):#DaQueue Database Class
    '''Represents the interface to SQLite'''
    def __init__(self, db, createNew=False, tableName = None, parent = None):#db is the path to the database on disk
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
            print self.errorMsg
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

    def UPDATEROWBYKEY(self, tableName, updateField, updateValue, keyField, keyValue):

        #UPDATE queueTable SET jobID = 5 WHERE uuID LIKE 'f065ec40-839b-5022-a528-b5764845f20d'
        '''This inserts the specified values into the identified row'''
        t1 = time.clock()
        tableExists =self.cnx.execute("SELECT COUNT(*) FROM sqlite_master WHERE name=?", (tableName,)).fetchone()[0]
        if tableExists == 0:
            print "Table %s does not exist, ignoring"%tableName
        else:
            self.cur.execute('UPDATE %s SET %s = %s WHERE %s LIKE "%s"'%(tableName, updateField, updateValue, keyField, keyValue))
            self.cnx.commit()
            t2 = str(time.clock()-t1)
            print "SQLite Row Update Time for %s (s): %s"%(tableName, t2)



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

    def INSERT_WATCH_VALUES(self, tableName, watchDict):
        '''This is for filling data for a file queue run, but may not
        be appropriate for a custom table as they may not have all of the appropriate
        keys'''
        t1 = time.clock()
        tableExists =self.cnx.execute("SELECT COUNT(*) FROM sqlite_master WHERE name=?", (tableName,)).fetchone()[0]
        if tableExists == 0:
            self.CREATE_WATCH_TABLE(tableName)
        else:
            reply = QtGui.QMessageBox.question(self.parent, "Table Already Exists in Database",  "Overwrite existing Table and Overwite?", QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            if reply:
                dropOK = self.DROP_TABLE(tableName)
                if dropOK:
                    self.CREATE_WATCH_TABLE(tableName)
                    pass
                else:
                    return False
            else:
                return False
        try:

            for i in xrange(watchDict.iterLen):
                self.cur.execute(
                                'INSERT INTO "%s" VALUES (?,?,?,?,?,?,?,?)'%tableName,#again I know %s is not recommended but I don't know how to do this more elegantly.
                                (
                                i,
                                watchDict.dataDict['watchFields'][i],
                                watchDict.dataDict['watchTypes'][i],
                                queueDict.dataDict['uuIDs'][i]
                                ))
            self.cnx.commit()
            t2 = time.clock()
            print "SQLite Commit Time (s): ", (t2-t1)
            return True
        except:
            print "Insert into Table False"
            return False

    def INSERT_QUEUE_VALUES(self, tableName, queueDict):
        '''This is for filling data for a file queue run, but may not
        be appropriate for a custom table as they may not have all of the appropriate
        keys'''
        t1 = time.clock()
        tableExists =self.cnx.execute("SELECT COUNT(*) FROM sqlite_master WHERE name=?", (tableName,)).fetchone()[0]
        if tableExists == 0:
            self.CREATE_QUEUE_TABLE(tableName)
#        else:
#            print "%s already exists, will simply add to existing."%tableName

#        else:
#            reply = QtGui.QMessageBox.question(self.parent, "Table Already Exists in Database",  "Overwrite existing Table and Overwite?", QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
#            if reply:
#                dropOK = self.DROP_TABLE(tableName)
#                if dropOK:
#                    self.CREATE_QUEUE_TABLE(tableName)
#                    pass
#                else:
#                    return False
#            else:
#                return False
        try:
#            print "Row Count", self.cur.rowcount
            for i in xrange(len(queueDict[queueDict.keys()[0]])):
                try:
                    self.cur.execute(
                                    'INSERT INTO "%s" VALUES (?,?,?,?,?,?,?,?)'%tableName,#again I know %s is not recommended but I don't know how to do this more elegantly.
                                    (
                                    queueDict['uuIDs'][i],
                                    queueDict['dataFiles'][i],
                                    queueDict['cfgFiles'][i],
                                    queueDict['outputFiles'][i],
                                    queueDict['statuses'][i],
                                    queueDict['statusIDs'][i],
                                    queueDict['jobIDs'][i],
                                    queueDict['timeIDs'][i]
                                    ))
                except:
                    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                    if exceptionValue[0] == 'column uuID is not unique':#exceptionValue is a tuple
                        #this is specific to Sqlite Tables with uuid as the primary key
#                        print "Not a unique UUID...skipping"
                        continue
#                    traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
#                    errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
#                    print errorMsg
            self.cnx.commit()
            t2 = time.clock()
            print "SQLite Commit Time (s): ", (t2-t1)
            return True
        except:
            print "Insert into Table False"
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
            errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
            print errorMsg
            return False

    def close(self):
        self.cur.close()
        self.cnx.close()
        self.dbOK = False

    def LIST_TABLES(self):
        self.tblList = []
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence' ORDER BY name")
        for row in self.cur.fetchall():
            self.tblList.append(str(row[0]))#row[0] by itself produces a unicode object, and row itself is a tuple

        return self.tblList

    def COPY_DATABASE(self, filename = None):

        """
        def dump_to_disk(con, filename):
        Dumps the tables of an in-memory database into a file-based SQLite database.

        @param con:         Connection to in-memory database.
        @param filename:    Name of the file to write to.
        """
        if filename is None:
            filename = 'test.db'
        self.cur.execute("attach '%s' as __extdb" % filename)
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        table_names = self.cur.fetchall()
        try:
            for table_name, in table_names:#the comma is because the cursor returns tuples
                if table_name != 'sqlite_sequence':
                    self.cur.execute("CREATE TABLE __extdb.%s AS SELECT * FROM %s"%(table_name, table_name))
            self.cur.execute("DETACH __extdb")
        except:
            self.cur.execute("DETACH __extdb")
            self.errorMsg = "Sorry: %s:%s"%(sys.exc_type, sys.exc_value)
            msg = self.errorMsg + '\nSave Error'
            error = QtGui.QMessageBox.warning(self.parent, "Copy DB Error!",  msg)


    def DUMP_TABLE(self, tblName, fileName = None):
        selectStr= "SELECT * FROM %s"%tblName
        fileName= fileName
        if fileName != None:
            self.cur.execute(selectStr)
            result = self.cur.fetchall()
            self.LIST_COLUMNS(tblName)

            if len(result)>0:
                dumpWriter = csv.writer(open(fileName, 'w'), delimiter = ',', quotechar= "'")
                try:
                    dumpWriter.writerow(self.colList)
                    for record in result:
                        dumpWriter.writerow(record)

                except:
                    self.errorMsg = "Sorry: %s:%s"%(sys.exc_type, sys.exc_value)
                    msg = self.errorMsg + '\nSave Error'
                    error = QtGui.QMessageBox.warning(self.parent, "CSV Table Save Error!",  msg)


    def LIST_COLUMNS(self,  tableName):
        self.colList = []
        self.cur.execute('PRAGMA TABLE_INFO(%s)'%tableName)
        for row in self.cur.fetchall():
            self.colList.append(str(row[1]))#row[1] by itself produces a unicode object, and row itself is a tuple, row[1] is the column name
            #the 0 - id, 1 - column name, 2 - data type
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
            print msg
            if self.parent:
                error = QtGui.QMessageBox.warning(self.parent, "Table Drop Error!",  msg)
            return False

    def CREATE_WATCH_TABLE(self, tableName,  overWrite = False):
        if overWrite:
            self.DROP_TABLE(tableName)

        self.curTblName = tableName

        self.cur.execute('CREATE TABLE IF NOT EXISTS "%s"(id INTEGER PRIMARY KEY AUTOINCREMENT,\
        watchField TEXT,\
        watchType INTEGER,\
        uuID TEXT)'
        %tableName)

#    def CREATE_QUEUE_TABLE(self, tableName,  overWrite = False):
#        if overWrite:
#            self.DROP_TABLE(tableName)
#
#        self.curTblName = tableName
#
#        self.cur.execute('CREATE TABLE IF NOT EXISTS "%s"(id INTEGER PRIMARY KEY AUTOINCREMENT,\
#        dataFile TEXT,\
#        cfgFile TEXT,\
#        outputFile TEXT,\
#        status TEXT,\
#        statusID INTEGER,\
#        jobID INTEGER,\
#        uuID TEXT)'
#        %tableName)

    def CREATE_QUEUE_TABLE(self, tableName,  overWrite = False):
        '''
        ,\
        uuID TEXT)'
        '''
        if overWrite:
            self.DROP_TABLE(tableName)

        self.curTblName = tableName

        self.cur.execute('CREATE TABLE IF NOT EXISTS "%s"(uuID TEXT PRIMARY KEY NOT NULL,\
        dataFile TEXT,\
        cfgFile TEXT,\
        outputFile TEXT,\
        status TEXT,\
        statusID INTEGER,\
        jobID INTEGER,\
        timeID TEXT)'
        %tableName)
        '''
        http://stackoverflow.com/questions/811548/sqlite-and-python-return-a-dictionary-using-fetchone
        def dict_factory(cursor, row):
            d = {}
            for idx,col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        from pysqlite2 import dbapi2 as sqlite
        conn = sqlite.connect(...)
        conn.row_factory = dict_factory
        '''
    def DICT_FACTORY(self, cursor, row):
        '''
        http://stackoverflow.com/questions/811548/sqlite-and-python-return-a-dictionary-using-fetchone
        '''
        d={}
        for idx,col in enumerate(cursor.description):
            d[col[0]] = str(row[idx])
        return d

    def GET_CURRENT_QUERY_AS_DICT(self):
        result = []
        for row in self.cur.fetchall():
            result.append(self.DICT_FACTORY(self.cur, row))
        return result

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

    def EXEC_QUERY_W_NEW_TABLE(self, queryStr):
        '''Saves query to the database--only if the user commits to the database upon close of the application'''
        newTableName, ok = QtGui.QInputDialog.getText(self.parent, 'Create New Database Table',\
                                        'Enter New Table Name: ', QtGui.QLineEdit.Normal, 'newTable')
        if ok:
            execStr = "CREATE TABLE %s AS "%str(newTableName)
            execStr += queryStr
            print execStr
            self.cur.execute(execStr)
            self.cur.execute("SELECT * FROM %s"%(str(newTableName)))
            result = self.GET_CURRENT_QUERY()
            colNames = self.LIST_COLUMNS(str(newTableName))

            print 'The table named: "%s" created in current database.'%str(newTableName)

            return str(newTableName), result, colNames
        else:
            return None, [], []

    def GET_TABLE(self, tblName):
        self.cur.execute("SELECT * FROM %s"%(tblName))
        result = self.GET_CURRENT_QUERY()
        colNames = self.GET_COLUMN_NAMES()
        if len(result)>0:
            return True, result, colNames
        else:
            return False, [], []

    def EXEC_QUERY(self, execStr):
        self.cur.execute(execStr)
        self.cnx.commit()
#        result = self.GET_CURRENT_QUERY()
#        if len(result)>0:
#            colNames = self.GET_COLUMN_NAMES()
#            return newTableName, result, colNames


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
                colNames = self.GET_COLUMN_NAMES()
                return newTableName, result, colNames
            else:#this is the case if the user cancels the input of the new table
                return None, []

        else:
            '''Simply returns the selected query but does not save it to the database'''
            self.cur.execute("SELECT * FROM %s WHERE %s LIKE '%s'"%(tableName, fieldType, fieldValue))
            print "SELECT * FROM %s WHERE %s LIKE '%s'"%(tableName, fieldType, fieldValue)
            result = self.GET_CURRENT_QUERY()
            colNames = self.GET_COLUMN_NAMES()
            return None, result, colNames

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
                colNames = self.GET_COLUMN_NAMES()
                print 'The table named: "%s" created in current database.'%newTableName
                return result, colNames

            else:#this is the case if the user cancels the input of the new table
                return False

        else:
            '''Simply returns the selected query but does not save it to the database'''
            self.cur.execute("SELECT * FROM %s WHERE %s > %s AND %s < %s"%(tableName, fieldType, str(loVal), fieldType, str(hiVal)))
            print "SELECT * FROM %s WHERE %s > %s AND %s < %s"%(tableName, fieldType, str(loVal), fieldType, str(hiVal))
            result = self.GET_CURRENT_QUERY()
            colNames = self.GET_COLUMN_NAMES()
            return result, colNames

    def GET_COLUMN_NAMES(self):
        colNames = [tuple[0] for tuple in self.cur.description]
        if len(colNames)>0:
            return colNames
        else:
            return []

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
        xFrags = []
        yFrags = []

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
            xFrags.append(row[12])
            yFrags.append(row[13])

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
                'deltaH':N.array(deltaH),
                'xFrags':xFrags,
                'yFrags':yFrags
                }
        XT_RESULTS.setArrays(arrayDict)
        XT_RESULTS.setFN(tableName)
        self.curTblName=tableName

        t2 = str(time.clock()-t1)
        print "SQLite Read Time for %s (s): %s"%(tableName, t2)