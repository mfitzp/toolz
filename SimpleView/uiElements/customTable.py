from PyQt4 import QtCore, QtGui
import os, sys, traceback
import time

from pylab import load as L
import numpy as N
from mpl_pyqt4_widget import MPL_Widget

my_array = [['00','01','50'],
            ['10','11','12'],
            ['20','21','22'],
            ['30','31','32']]
#my_data = L('Z.csv', delimiter = ',')


def main():
    app = QtGui.QApplication(sys.argv)
    w = DataTable()
    w.show()
    sys.exit(app.exec_())

class DataTable(QtGui.QWidget):
    def __init__(self, data = None,  colHeaderList = None, rowHeaderList = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle('Fingerprint Meta Data')
        self.resize(650, 500)
        if data != None:
            self.data = data
        else:
            self.data = my_array
            print my_array[0]
#            self.numRows = my_array.shape[0]
#            self.numCols = my_array.shape[1]


#        self.tableWidget.setRowCount(self.numRows)
#        self.tableWidget.setColumnCount(self.numCols)



        self.vLayout = QtGui.QVBoxLayout(self)
        self.tabWidget = QtGui.QTabWidget(self)
        self.tab = QtGui.QWidget()

        self.tableWidget = CustomTable(self.tab)
        self.tabLayout = QtGui.QHBoxLayout(self.tab)
        self.tabLayout.addWidget(self.tableWidget)

        self.tableWidget.addData(self.data)
        if type(colHeaderList) == list:
            self.tableWidget.setHorizontalHeaderLabels(colHeaderList)
        if type(rowHeaderList) == list:
            self.tableWidget.setVerticalHeaderLabels(rowHeaderList)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setCurrentCell(0, 0)#needed so selectedRanges does not fail initially

        self.tabWidget.addTab(self.tab, "Table")

        self.tab2 = QtGui.QWidget()
        self.plotWidget = MPL_Widget(self.tab2, enableAutoScale = True, enableCSV = True, enableEdit = True)
#        self.axisLayout = QtGui.QHBoxLayout
#        self.setLimitsBtn = QtGui.QPushButton(self.tab2)
#        self.setLimitsBtn.setText('Set X Scale')
        self.tab2Layout = QtGui.QHBoxLayout(self.tab2)
        self.tab2Layout.addWidget(self.plotWidget)

        self.tabWidget.addTab(self.tab2, "Plot")
        self.tabWidget.setCurrentIndex(1)

        self.vLayout.addWidget(self.tabWidget)
#        self.resize(500,700)

class CustomTable(QtGui.QTableWidget):
    def __init__(self, parent = None):
        QtGui.QTableWidget.__init__(self, parent)
        if parent:
            self.parent = parent
        self.__initActions__()
        self.__initContextMenus__()

    def __initContextMenus__(self):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.tableWidgetContext)

    def tableWidgetContext(self, point):
        '''Create a menu for the tableWidget and associated actions'''
        tw_menu = QtGui.QMenu("Menu", self)
        tw_menu.addAction(self.pasteAction)
        tw_menu.addAction(self.copyAction)
#        tw_menu.addAction(self.insRowAction)
#        tw_menu.addAction(self.insColAction)
#        tw_menu.addAction(self.testAction)
        tw_menu.exec_(self.mapToGlobal(point))

    def addData(self, data, startrow=None,  startcol = None):
        if data != None:
            try:
                if (len(data[0])) >= self.columnCount():
                    self.setColumnCount(len(data[0]))
                if (len(data)) >= self.rowCount():
                    self.setRowCount(len(data))

                if startcol:
                    sc = startcol#start column
                else:
                    sc = 0 # n is for columns
                if startrow:
                    sr = startrow
                else:
                    sr = 0

                m = sr
                #print "Row, Col Commit:", sr, n
                if type(data) is N.ndarray:
                    for row in data:
                        n = sc
                        for item in row:
                            #print repr(str(item))
                            newitem = QtGui.QTableWidgetItem(0)#'%.3f'%item)
                            newitem.setData(0,QtCore.QVariant(item))
                            self.setItem(m,  n,  newitem)
                            n+=1
                        m+=1
        #            print type(item)
                else:
                    for row in data:
                        n = sc
                        for item in row:
                            #print repr(str(item))
                            newitem = QtGui.QTableWidgetItem(0)#'%.3f'%item)
                            newitem.setData(0,QtCore.QVariant(item))
                            self.setItem(m,  n,  newitem)
                            n+=1
                        m+=1
    #                for row in data:
    #                    n = sc
    #                    for item in row:
    #                        #print repr(str(item))
    #                        newitem = QTableWidgetItem(item)
    #                        self.setItem(m,  n,  newitem)
    #                        n+=1
    #                    m+=1
            except:
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
                errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
                return QMessageBox.warning(self, "Adding Data Error", errorMsg)
                print errorMsg

        else:
            print "Error adding entry to table, there is no data!!!"



    def __initActions__(self):
        self.pasteAction = QtGui.QAction("Paste",  self)
        self.pasteAction.setShortcut("Ctrl+Alt+V")
        self.addAction(self.pasteAction)
        self.connect(self.pasteAction, QtCore.SIGNAL("triggered()"), self.pasteClip)

        self.copyAction = QtGui.QAction("Copy",  self)
        self.copyAction.setShortcut("Ctrl+Alt+C")
        self.addAction(self.copyAction)
        self.connect(self.copyAction, QtCore.SIGNAL("triggered()"), self.copyCells)

        self.insColAction = QtGui.QAction("Insert Column",  self)
        self.addAction(self.insColAction)
        self.connect(self.insColAction, QtCore.SIGNAL("triggered()"), self.addColumns)

        self.insRowAction = QtGui.QAction("Insert Row",  self)
        self.addAction(self.insRowAction)
        self.connect(self.insRowAction, QtCore.SIGNAL("triggered()"), self.addRows)

        self.testAction = QtGui.QAction("Test Action",  self)
        self.addAction(self.testAction)
        self.connect(self.testAction, QtCore.SIGNAL("triggered()"), self.testFunc)

    def testFunc(self):
        if self.cb:
            #print sizeof(self.cb)
            self.cb.clear(QtGui.QClipboard.Clipboard)
    ###############################

    def addRows(self):
        selRange  = self.selectedRanges()[0]
        topRow = selRange.topRow()
        bottomRow = selRange.bottomRow()
        for i in xrange(topRow, (bottomRow+1)):
            self.insRow(i)
        #print topRow,  bottomRow
        #print selRange

    def addColumns(self):
        selRange  = self.selectedRanges()[0]
        rightColumn = selRange.rightColumn()
        leftColumn = selRange.leftColumn()
        for i in xrange(leftColumn, (rightColumn+1)):
            self.insCol(i)
        #print topRow,  bottomRow
        #print selRange

    def inCol(self,  col = None):
        if type(col) is int:
            self.insertColumn(col)
        else:
            self.insertColumn(self.currentColumn())

    def insRow(self,  row = None):
        if type(row) is int:
            self.insertRow(row)
        else:
            self.insertRow(self.currentRow())

    ####################################


    def pasteClip(self):

        self.cb = QtGui.QApplication.clipboard()
        clipText = self.cb.text()
        t0 = time.time()
        clip2paste = self.splitClipboard(clipText)

        selRange  = self.selectedRanges()[0]#just take the first range
        topRow = selRange.topRow()
        bottomRow = selRange.bottomRow()
        rightColumn = selRange.rightColumn()
        leftColumn = selRange.leftColumn()

        #test to ensure pasted area fits in table
        t1 = time.time()
        print "Clipboard split time:",  (t1-t0)
        if (len(clip2paste)+topRow) >= self.rowCount():
            self.setRowCount(len(clip2paste)+topRow)
        t2 = time.time()
        print "Row set time:",  (t2-t1)

        if (len(clip2paste[0])+rightColumn) >= self.columnCount():
            self.setColumnCount(len(clip2paste[0])+rightColumn)
        t3 = time.time()
        print "Column set time:", (t3-t2)
        self.addData(clip2paste, topRow,  leftColumn)
        print "Data Add Time:", (time.time()-t3)

    def splitClipboard(self, clipText):
        #create list to be returned
        returnClip = []
        #split by carriage return which makes the rows
        clipList = clipText.split("\r\n")
        #split each item by tab (aka columns)
        for item in clipList:
            returnClip.append(item.split("\t"))

        return returnClip

 ######################################

    def copyCells(self):
#        print "COPY"
        selRange  = self.selectedRanges()[0]#just take the first range
        topRow = selRange.topRow()
        bottomRow = selRange.bottomRow()
        rightColumn = selRange.rightColumn()
        leftColumn = selRange.leftColumn()
        #item = self.tableWidget.item(topRow, leftColumn)
        clipStr = QtCore.QString()
        for row in xrange(topRow, bottomRow+1):
            for col in xrange(leftColumn, rightColumn+1):
                cell = self.item(row, col)
                if cell:
                    clipStr.append(cell.text())
                else:
                    clipStr.append(QtCore.QString(""))
                clipStr.append(QtCore.QString("\t"))
            clipStr.chop(1)
            clipStr.append(QtCore.QString("\r\n"))

#        if self.cb:
#            self.cb.clear()
        self.cb = QtGui.QApplication.clipboard()
        self.cb.setText(clipStr)


if __name__ == "__main__":
    main()
