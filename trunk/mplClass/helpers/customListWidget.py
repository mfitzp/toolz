# -*- coding: utf-8 -*-

"""The user interface for our app"""

import os,sys

# Import Qt modules
from PyQt4 import QtCore,QtGui

# Create a class for our main window
class DictTreeWidget(QtGui.QDialog):
    def __init__(self, userDict = None, returnCall = None, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        if len(userDict) < 1:
            self.close()
            
        self.userDict = userDict
        self.returnCall = returnCall
        
        self.setWindowTitle('Data Dictionary')
        self.vbox = QtGui.QVBoxLayout()
        self.treeWidget = QtGui.QTreeWidget(self)
        self.treeWidget.setColumnCount(3)
        self.columnLabels = ['Key Name', 'Data Type', 'Data Length']
        self.treeWidget.setHeaderLabels(self.columnLabels)
        
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),self.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),self.reject)
      
        self.vbox.addWidget(self.treeWidget)
        self.vbox.addWidget(self.buttonBox)
        self.setLayout(self.vbox)
        
        self.populateDict()
        self.resize(500,250)
    
    def populateDict(self, userDict = None):
        if userDict:
            self.userDict = userDict
            
        if self.userDict != None:
            if len(self.userDict) > 0:
                for key in self.userDict.keys():
                    itemTags = []
                    itemTags.append(key)
                    itemTags.append(str(type(self.userDict[key])))
                    itemTags.append(str(len(self.userDict[key])))
                    newItem = QtGui.QTreeWidgetItem(itemTags)
                    newItem.setCheckState(0, QtCore.Qt.Unchecked)
                    self.treeWidget.addTopLevelItem(newItem)
                
                for i in xrange(len(itemTags)):
                    self.treeWidget.resizeColumnToContents(i)
                
                self.treeWidget.sortItems(0, QtCore.Qt.AscendingOrder)
                
    def accept(self):
        selectedKeys = []
        for i in xrange(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)
            if item.checkState(0) == 2:#2 is a checked item, 0 is unchecked
                selectedKeys.append(str(item.text(0)))
                
        print selectedKeys
        if self.returnCall != None:
            self.returnCall(selectedKeys)
        #~ self.setVisible(False)
        #~ QtCore.QTimer.singleShot(2000, self.testFunc)
        #~ self.setVisible(True)
        #~ QtCore.QTimer.singleShot(5000, self.testFunc)
        self.close()

    def testFunc(self):
        print "TEST FUNCTION"
    
def main():
    import numpy as N
    
    userDict = {}
    for i in xrange(10):
        userDict['Array%s'%i] = N.arange(20)
    
        
    
    # Again, this is boilerplate, it's going to be the same on
    # almost every app you write
    app = QtGui.QApplication(sys.argv)
    window=DictTreeWidget(userDict)
    window.show()
    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()
