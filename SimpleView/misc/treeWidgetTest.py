from PyQt4 import QtCore, QtGui
import sys
import time

from pylab import load as L
import numpy as N

my_array = N.array([['00','01','02'],
                    ['10','11','12'],
                    ['20','21','22'],
                    ['30','31','32']])

headers = ['Planets', 'Plants']
planetNames = ['Earth', 'Mars', 'Venus']
plantNames = ['corn', 'cactus', 'spinach']
#my_data = L('Z.csv', delimiter = ',')


def main():
    app = QtGui.QApplication(sys.argv)
    w = TWidget()
    #w.show()
    sys.exit(app.exec_())

class TWidget(QtGui.QWidget):
#            super(Plot_Widget, self).__init__(None)#new  new^2:changed from parent
#        self.setAttribute(Qt.WA_DeleteOnClose)

    def __init__(self, dataList = None,  colHeaderList = None):
        QtGui.QWidget.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle('Database Result')
        self.resize(900, 400)
        self.treeWidget = CustomTree(self)
        self.connect(self.treeWidget, QtCore.SIGNAL("itemClicked(QTreeWidgetItem *,int)"), self.testFunc)
        if dataList:
            self.data = dataList
        else:
            self.data = my_array
            print my_array[0]
            self.numRows = self.data.shape[0]
            self.numCols = self.data.shape[1]

#        QtGui.QTreeWidget
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(['Parent','Child'])

        self.plantItems = QtGui.QTreeWidgetItem(self.treeWidget)
        self.plantItems.setText(0,'Plants')
        for i,plant in enumerate(plantNames):
            curPlant = QtGui.QTreeWidgetItem()
            curPlant.setText(0,plant)
            self.plantItems.addChild(curPlant)

        self.planetItems = QtGui.QTreeWidgetItem(self.treeWidget)
        self.planetItems.setText(0,'Planets')
        for i,planet in enumerate(planetNames):
#            QtGui.QTreeWidget
            curPlanet = QtGui.QTreeWidgetItem()
            curPlanet.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsUserCheckable)
            curPlanet.setCheckState(0, QtCore.Qt.Unchecked)
#            curPlanet.setFlags(curPlanet.flags()|QtCore.Qt.ItemIsEnabled)
            curPlanet.setText(0,planet)
            self.planetItems.addChild(curPlanet)



        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.treeWidget)
        self.setLayout(layout)
        self.show()



    def testFunc(self, item=None, index = None):
        if item != None:
            print item.text(index)
#            print item.childCount()
            if item.parent() != None:
                print item.parent().text(index)
            print item.checkState(0)
#        if index != None:
#            print index

class CustomTree(QtGui.QTreeWidget):
    def __init__(self, parent = None):
        QtGui.QTableWidget.__init__(self, parent)
        if parent:
            self.parent = parent
        self.__initActions__()
        #self.__initContextMenus__()

    def __initContextMenus__(self):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.connect(self, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.treeWidgetContext)

    def treeWidgetContext(self, point):
        '''Create a menu for the treeWidget and associated actions'''
        tw_menu = QMenu("Menu", self)
        tw_menu.addAction(self.pasteAction)
        tw_menu.addAction(self.copyAction)
        tw_menu.addAction(self.insRowAction)
        tw_menu.addAction(self.insColAction)
        tw_menu.addAction(self.testAction)
        tw_menu.exec_(self.mapToGlobal(point))

    def addData(self, data, startrow=None,  startcol = None):
        if data != None:
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
                        newitem = QtGui.QTreeWidgetItem(0)#'%.3f'%item)
                        newitem.setData(0,QVariant(item))
                        self.setItem(m,  n,  newitem)
                        n+=1
                    m+=1
    #            print type(item)
            else:
                for row in data:
                    n = sc
                    for item in row:
                        #print repr(str(item))
                        newitem = QtGui.QTreeWidgetItem(0)#'%.3f'%item)
                        newitem.setData(0,QVariant(item))
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
        else:
            print "Error adding entry to table, there is no data!!!"



    def __initActions__(self):
        self.pasteAction = QtGui.QAction("Paste",  self)
        self.pasteAction.setShortcut("Ctrl+V")
        self.addAction(self.pasteAction)
        self.connect(self.pasteAction, QtCore.SIGNAL("triggered()"), self.pasteClip)

        self.copyAction = QtGui.QAction("Copy",  self)
        self.copyAction.setShortcut("Ctrl+C")
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
        #item = self.treeWidget.item(topRow, leftColumn)
        clipStr = QtCore.QString()
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
