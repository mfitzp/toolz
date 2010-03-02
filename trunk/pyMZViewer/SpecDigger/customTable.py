from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import time
import webbrowser as W

import numpy as N

my_array = [['00','01','02'],
            ['10','11','12'],
            ['20','21','22'],
            ['30','31','32']]

def main():
    import scipy as S
    app = QApplication(sys.argv)
    
    a = S.rand(20)
    ans = calc_dist_matrix(a,a)
    #print ans
    w = MainTable(dataList = ans)
    #w.show()
    sys.exit(app.exec_())

def calc_dist_matrix(array_one, array_two) :
    """Returns a matrix of C-alpha distances between two chains"""
    answer = N.zeros((len(array_one), len(array_two)), N.float)
    for row, elem_one in enumerate(array_one) :
        for col, elem_two in enumerate(array_two) :
            answer[row, col] = N.abs(elem_one-elem_two)
    return answer



#class EventFilter(QtCore.QObject):
#    def __init__(self, parent=None):
#        QtCore.QObject.__init__(self, parent)
#        if parent != None:
#            self.parent = parent
#    def eventFilter(self, obj, event):
#        if event.type() == QtCore.QEvent.Enter:
#            obj.focusEvent(self.parent)
#            #print "got the focus"
#        elif event.type() == QtCore.QEvent.Leave:
#            obj.lossFocusEvent(self.parent)
#            #print "lost the focus"
#        return QtCore.QObject.eventFilter(self, obj, event)


class MainTable(QWidget):
    def __init__(self, dataList = None, colHeaderList = None, enableSort = False, title = None):
        QWidget.__init__(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
#        self.installEventFilter(EventFilter(self))

        if title != None:
            self.title = title
            self.setWindowTitle(title)
        else:
            self.title = None
            self.setWindowTitle('Database Result')
        #self.resize(900, 400)
        self.tableWidget = CustomTable(self)
        self.numRows = 5
        if colHeaderList != None:
            self.numCols = len(colHeaderList)
        else:
            self.numCols = 5
        self.tableWidget.setRowCount(self.numRows)
        self.tableWidget.setColumnCount(self.numCols)
        self.sortOk = enableSort
        self.tableWidget.setSortingEnabled(False)
        if dataList != None:
            self.data = dataList
        else:
            self.data = my_array

        self.tableWidget.addData(self.data, enableSort = self.sortOk)
        if type(colHeaderList) == list:
            self.tableWidget.setHorizontalHeaderLabels(colHeaderList)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setCurrentCell(0, 0)#needed so selectedRanges does not fail initially

        layout = QVBoxLayout(self)
        layout.addWidget(self.tableWidget)

        self.connect(self.tableWidget, SIGNAL("itemSelectionChanged()"), self.tableSelect)
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
                self.emit(SIGNAL("itemSelected(PyQt_PyObject)"),selList)
            except:
                return False

class CustomTable(QTableWidget):
    def __init__(self, parent = None):
        QTableWidget.__init__(self, parent)
        if parent:
            self.parent = parent
        self.__initActions__()
        self.__initContextMenus__()

    def __initContextMenus__(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self, SIGNAL("customContextMenuRequested(QPoint)"), self.tableWidgetContext)

    def tableWidgetContext(self, point):
        '''Create a menu for the tableWidget and associated actions'''
        tw_menu = QMenu("Menu", self)
        tw_menu.addAction(self.pasteAction)
        tw_menu.addAction(self.copyAction)
        tw_menu.addAction(self.insRowAction)
        tw_menu.addAction(self.insColAction)
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
                #print repr(str(item))
                newitem = QTableWidgetItem(str(item))
                self.setItem(m,  n,  newitem)
                n+=1
            m+=1

        if enableSort:
            self.setSortingEnabled(enableSort)

    def __initActions__(self):
        self.pasteAction = QAction("Paste",  self)
        self.pasteAction.setShortcut("Ctrl+V")
        self.addAction(self.pasteAction)
        self.connect(self.pasteAction, SIGNAL("triggered()"), self.pasteClip)

        self.copyAction = QAction("Copy",  self)
        self.copyAction.setShortcut("Ctrl+C")
        self.addAction(self.copyAction)
        self.connect(self.copyAction, SIGNAL("triggered()"), self.copyCells)

        self.insColAction = QAction("Insert Column",  self)
        self.addAction(self.insColAction)
        self.connect(self.insColAction, SIGNAL("triggered()"), self.addColumns)

        self.insRowAction = QAction("Insert Row",  self)
        self.addAction(self.insRowAction)
        self.connect(self.insRowAction, SIGNAL("triggered()"), self.addRows)

        self.testAction = QAction("Test Action",  self)
        self.addAction(self.testAction)
        self.connect(self.testAction, SIGNAL("triggered()"), self.testFunc)

        #customFunction to perform web query based upon cell text
        #self.connect(self, SIGNAL("itemDoubleClicked (QTableWidgetItem *)"), self.getWebProID)


    def getWebProID(self, selectedItem = None):
        '''
        Used to select the proID from a protein
        Table.  If this is the case, fire up the web browser and run
        the query for that protein.
        '''
        if selectedItem != None:
            matchVar = 'proID'
            webStr = 'http://www.uniprot.org/uniprot/?query='
            curCol = self.column(selectedItem)
#            print curCol, type(curCol)
            curColHeader = self.horizontalHeaderItem(curCol)
            if curColHeader != None:
                colText = str(curColHeader.text())
                if colText == 'proID':#column is the protein ID
                    cellStr = str(selectedItem.text())
                    if len(cellStr)>0:
                        if '|' in cellStr:#example: sp|ALBU_BOVIN|
                            queryStr = cellStr.split('|')[1]
                        else:
                            queryStr = cellStr
                        if len(queryStr)>0:
                            webStr+=queryStr
                            try:
                                W.open_new_tab(webStr)
                            except:
                                print "Web Search Error: %s"%webStr
#                print "Col Header", str(curColHeader.text())

    def testFunc(self, var = None):
        print "Test Function"
        if self.cb:
            print sizeof(self.cb)
            self.cb.clear(QClipboard.Clipboard)
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
        self.cb = QApplication.clipboard()
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
        clipStr = QString()
        for row in xrange(topRow, bottomRow+1):
            for col in xrange(leftColumn, rightColumn+1):
                cell = self.item(row, col)
                if cell:
                    clipStr.append(cell.text())
                else:
                    clipStr.append(QString(""))
                clipStr.append(QString("\t"))
            clipStr.chop(1)
            clipStr.append(QString("\r\n"))

#        if self.cb:
#            self.cb.clear()
        self.cb = QApplication.clipboard()
        self.cb.setText(clipStr)


if __name__ == "__main__":
    main()
