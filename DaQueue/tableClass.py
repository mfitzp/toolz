from PyQt4 import QtCore, QtGui
import sys
import time

##custom additions specific to DaQueue
from extraWidgets import cellComboBox, cellOFD, cellStatus


my_array = [['00','01','02'],
            ['10','11','12'],
            ['20','21','22'],
            ['30','31','32']]

def main():
    app = QtGui.QApplication(sys.argv)
    w = DataTableWindow()
    #w.show()
    sys.exit(app.exec_())

class EventFilter(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        if parent != None:
            self.parent = parent
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Enter:
            obj.focusEvent(self.parent)
            #print "got the focus"
        elif event.type() == QtCore.QEvent.Leave:
            obj.lossFocusEvent(self.parent)
            #print "lost the focus"
        return QtCore.QObject.eventFilter(self, obj, event)


class DataTableWindow(QtGui.QWidget):
#            super(Plot_Widget, self).__init__(None)#new  new^2:changed from parent
#        self.setAttribute(Qt.WA_DeleteOnClose)

    def __init__(self, dataList = None, colHeaderList = None, enableSort = False, title = None):
        QtGui.QWidget.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
#        self.installEventFilter(EventFilter(self))

        if title != None:
            self.title = title
            self.setWindowTitle(title)
        else:
            self.title = None
            self.setWindowTitle('Database Result')
        self.resize(900, 400)
        self.tableWidget = CustomTable(self)
        self.numRows = 5
        self.numCols = 5
        self.tableWidget.setRowCount(self.numRows)
        self.tableWidget.setColumnCount(self.numCols)
        self.sortOk = enableSort
        self.tableWidget.setSortingEnabled(False)
        if dataList:
            self.data = dataList
        else:
            self.data = my_array

        self.tableWidget.addData(self.data, enableSort = self.sortOk)
        if type(colHeaderList) == list:
            self.tableWidget.setHorizontalHeaderLabels(colHeaderList)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setCurrentCell(0, 0)#needed so selectedRanges does not fail initially

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.tableWidget)


        self.connect(self.tableWidget, QtCore.SIGNAL("itemSelectionChanged()"), self.tableSelect)



        self.setLayout(layout)
        self.show()

    def tableSelect(self):
        curRow = self.tableWidget.currentRow()
        curItem = self.tableWidget.item(curRow, 0)
        if curItem != None and self.title != None:
            curText = str(curItem.text())
            try:#using try here because if the table format is incorrect the first item may not be able to be converted to an integer
                curIndex = int(curText)
                curTable = self.title.split(',')[0]
                selList = [curIndex, curTable]
                self.emit(QtCore.SIGNAL("itemSelected(PyQt_PyObject)"),selList)
            except:
                return False

class CustomTable(QtGui.QTableWidget):
    def __init__(self, parent = None):
        QtGui.QTableWidget.__init__(self, parent)
        if parent:
            self.parent = parent


        '''
        These values are specific to the queue and should be changed
        '''
        self.methodFileInd = 1
        self.dataPathInd = 3
        self.outputPathInd = 5
        self.stateInd = 7
        self.taskIDInd = 8


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

    def addData(self, data, startrow=None,  startcol = None, enableSort = False):
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
        for row in data:
            n = sc
            for item in row:
#                print repr(str(item))
                newitem = QtGui.QTableWidgetItem(item)
                self.setItem(m,  n,  newitem)
                n+=1
            m+=1

        if enableSort:
            self.setSortingEnabled(enableSort)



    def __initActions__(self):
        self.pasteAction = QtGui.QAction("Paste",  self)
        self.pasteAction.setShortcut("Ctrl+V")
        self.addAction(self.pasteAction)
        self.connect(self.pasteAction, QtCore.SIGNAL("triggered()"), self.pasteClip)

        self.copyAction = QtGui.QAction("Copy",  self)
        self.copyAction.setShortcut("Ctrl+C")
        self.addAction(self.copyAction)
        self.connect(self.copyAction, QtCore.SIGNAL("triggered()"), self.copyCells)

#        self.insColAction = QtGui.QAction("Insert Column",  self)
#        self.addAction(self.insColAction)
#        self.connect(self.insColAction, QtCore.SIGNAL("triggered()"), self.addColumns)

        self.insRowAction = QtGui.QAction("Insert Row",  self)
        self.addAction(self.insRowAction)
        self.connect(self.insRowAction, QtCore.SIGNAL("triggered()"), self.addRows)

#        self.testAction = QtGui.QAction("Test Action",  self)
#        self.addAction(self.testAction)
#        self.connect(self.testAction, QtCore.SIGNAL("triggered()"), self.testFunc)

    def testFunc(self):
        if self.cb:
            #print sizeof(self.cb)
            self.cb.clear(QtGui.QClipboard.Clipboard)
    ###############################

    def addCustomRow(self, row):
        self.setCellWidget(row, 0, cellComboBox())
        self.setItem(row, self.methodFileInd+1, cellOFD())
        self.setItem(row, self.dataPathInd+1, cellOFD())
        self.setItem(row, self.outputPathInd+1, cellOFD())
        self.setItem(row, self.stateInd, cellStatus())

    def addRows(self):
        selRange  = self.selectedRanges()[0]
        topRow = selRange.topRow()
        bottomRow = selRange.bottomRow()
        for i in xrange(topRow, (bottomRow+1)):
            self.insRow(i)
        self.resizeRowsToContents()
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

    def insCol(self,  col = None):
        if type(col) is int:
            self.insertColumn(col)
        else:
            self.insertColumn(self.currentColumn())

    def insRow(self,  row = None):
        if type(row) is int:
            self.insertRow(row)
            self.addCustomRow(row)
        else:
            self.insertRow(self.currentRow())
            self.addCustomRow(self.currentRow())

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
        self.addData(clip2paste, topRow,  leftColumn)
        self.resizeColumnsToContents()
#        t3 = time.time()
#        print "Column set time:", (t3-t2)

#        print "Data Add Time:", (time.time()-t3)

    def splitClipboard(self,  clipText):
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
