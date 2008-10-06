#!/usr/bin/env python

import os
import time

from PyQt4 import QtCore,  QtGui

import numpy as N
import scipy as S

from FolderParse import __loadDataFolder__ as LF
from flexReader import brukerFlexDoc as FR

from ui_main import Ui_Form

class LoadThread(QtCore.QThread):
        def __init__(self, parent = None):    
            QtCore.QThread.__init__(self, parent)
            
            self.finished = False
            self.ready = False
         
        def updateThread(self, loadList):
            self.loadList = loadList
            self.numItems = len(loadList)
            self.ready = True
            return True
        
        def run(self):
            if self.ready:
                while not self.finished and self.numItems > 0:
                    for item in self.loadList:
                        tempFlex = FR(item)
                        tempSpec = tempFlex.data['spectrum']
                        data2plot = DataPlot(tempSpec[:, 0],  tempSpec[:, 1])
                        #this following line is key to pass python object via the SIGNAL/SLOT mechanism of PyQt
                        self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),data2plot)#note PyQt_PyObject
                        self.numItems -=1
                
        def __del__(self):    
            self.exiting = True
            self.wait()

            
class DataPlot(object):
    def __init__(self, xdata,  ydata = None,  name = None):
        self.x = xdata
        if ydata != None:
            self.y = ydata
        else:
            self.y = None
            
        if name:
            self.name = name
        else:
            self.name = 'None'
        
        self.axSet = False
        self.mplAx = None
    
    def setAxis(self,  mplAxInstance):
        self.axSet = True
        self.mplAx = mplAxInstance
    
    def plot(self,  mplAxInstance, scatter = False):
        #if self.axSet:
        self.mplAx = mplAxInstance
        if self.y != None:
            if scatter:
                self.mplAx.scatter(self.x,  self.y,  label = self.name)
            else:
                self.mplAx.plot(self.x,  self.y,  label = self.name)
        else:
            self.mplAx.plot(self.x,  label = self.name)
#    else:
#        errMsg = 'axis must be set before attempting to plot'
#        raise errMsg
        

class Plot_Widget(QtGui.QWidget,  Ui_Form):
    def __init__(self, data2plot=None, parent = None):
        super(Plot_Widget, self).__init__(parent)
        self.setupUi(self)
        
        self.setupVars()
        self.readThread = LoadThread()
        if self.initDataList():
            self.loadOk = True
            self.setupGUI()
        else:
            self.loadOk = False

        QtCore.QObject.connect(self.indexSpinBox, QtCore.SIGNAL("valueChanged (int)"), self.updatePlot)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"), self.updateGUI)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("terminated()"), self.updateGUI)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("finished()"), self.updateGUI)
        
    
    def updatePlotIndex(self):
        self.indexSpinBox.setValue(self.indexHSlider.value())
        self.plotByIndex(self.indexSpinBox.value())
    
    def updatePlot(self, index):
        self.initIndex = index
        QtCore.QTimer.singleShot(500,  self.plotByIndex)
    
    def plotByIndex(self, plotIndex=None):
        if plotIndex == None:
            plotIndex = self.initIndex
        if plotIndex == self.indexSpinBox.value():#this is just to see if the user is still sliding things around before updating plot
            if self.loadOk:
                curAx = self.plotWidget.canvas.ax
                curAx.cla()
                curData = self.dataList[plotIndex]
                curData.plot(curAx)
                self.plotWidget.canvas.format_labels()
                self.plotWidget.canvas.draw()
                self.plotWidget.setFocus()#this is needed so that you can use CTRL+Z to zoom
                self.specNameEdit.setText(self.dirList[plotIndex])
    
    def setupVars(self):
        self.dirList = []
        self.curDir = os.getcwd()
        self.dataList = []
    
    def setupGUI(self):
        self.specNameEdit.clear()
        self.indexHSlider.setMaximum(0)
        self.indexSpinBox.setMaximum(0)
        
    def updateGUI(self,  loadedItem=None):
        if loadedItem != None:
            self.dataList.append(loadedItem)
        
        self.numSpec = len(self.dataList)
        if self.numSpec == 1:
            self.plotByIndex(0)
            self.indexHSlider.setMaximum(self.numSpec)
            self.indexSpinBox.setMaximum(self.numSpec)
        else:
            self.indexHSlider.setMaximum(self.numSpec-1)
            self.indexSpinBox.setMaximum(self.numSpec-1)
        #print self.numSpec
        
        #self.plotByIndex(0)
    
    def readData(self, dir):#dir is directory or data to load
    #add try/except for this....?
        tempFlex = FR(dir)
        tempSpec = tempFlex.data['spectrum']
        data2plot = DataPlot(tempSpec[:, 0],  tempSpec[:, 1])
        self.dataList.append(data2plot)
        return True
    
    def initDataList(self):
        dirList = LF()
        if len(dirList) !=0:
            self.dirList = dirList
            if self.readThread.updateThread(dirList):
                self.readThread.start()
                return True
#              for i in range(self.numSpec):
#                specName = 'test %d'%i
#                x, y = S.rand(2, 25)
#                data2plot = DataPlot(x, y,  name = specName)
#    ##            y = S.rand(25)
#    ##            data2plot = DataPlot(y,  name = specName)
#                self.dataList.append(data2plot)
#            return True

if __name__ == "__main__":
    import sys    
    app = QtGui.QApplication(sys.argv)
    plot = Plot_Widget()
    plot.show()
    sys.exit(app.exec_())     
