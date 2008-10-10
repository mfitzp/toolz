#!/usr/bin/env python

import os
import time

from PyQt4 import QtCore,  QtGui

import numpy as N
import scipy as S

from FolderParse import Load_FID_Folder as LFid
from FolderParse import Load_mzXML_Folder as LmzXML
from flexReader import brukerFlexDoc as FR
from mzXML_reader import mzXMLDoc as mzXMLR

#from ui_main import Ui_Form
import ui_main


class Plot_Widget(QtGui.QMainWindow,  ui_main.Ui_MainWindow):
    def __init__(self, parent = None):
        super(Plot_Widget,  self).__init__(parent)
        self.ui = self.setupUi(self)
        
        self.setupVars()
        self.setupGUI()
        self.readThread = LoadThread()

        QtCore.QObject.connect(self.indexSpinBox, QtCore.SIGNAL("valueChanged (int)"), self.updatePlot)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"), self.updateGUI)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("terminated()"), self.updateGUI)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("finished()"), self.updateGUI)
        QtCore.QObject.connect(self.loadDirBtn, QtCore.SIGNAL("clicked()"), self.initDataList)
        QtCore.QObject.connect(self.specListWidget, QtCore.SIGNAL("itemClicked (QListWidgetItem *)"), self.specListSelect)
        
    
    def specListSelect(self, widgetItem):
        selectItems = self.specListWidget.selectedItems()
        if len(selectItems) > 0:
            self.multiPlotIndex = []#reset indexes to plot
            for item in selectItems:
                self.multiPlotIndex.append(self.specListWidget.indexFromItem(item).row()) 

            self.plotByIndex(multiPlot = True)
            
        
    
    def updatePlotIndex(self):
        self.indexSpinBox.setValue(self.indexHSlider.value())
        self.plotByIndex(self.indexSpinBox.value())
    
    def updatePlot(self, index):
        if self.ignoreSignal:
            return         
        else:
            self.initIndex = index
            QtCore.QTimer.singleShot(500,  self.plotByIndex)
    
    def plotByIndex(self, plotIndex=None,  multiPlot = False):
        if self.loadOk:
            curAx = self.plotWidget.canvas.ax
            curAx.cla()
            if multiPlot:
                for i in self.multiPlotIndex:
                    curData = self.dataList[i]
                    curData.plot(curAx)
                #the following makes it so the change is ignored and the plot does not update
                self.ignoreSignal = True
                self.indexHSlider.setValue(i)
                self.indexSpinBox.setValue(i)
                self.ignoreSignal = False
            else:
                if plotIndex == None:
                    plotIndex = self.initIndex
                if plotIndex == self.indexSpinBox.value():#this is just to see if the user is still sliding things around before updating plot
                    curData = self.dataList[plotIndex]
                    curData.plot(curAx)
                    self.specNameEdit.setText(self.dirList[plotIndex])
                    #the following makes it so the change is ignored and the plot does not update
                    self.ignoreSignal = True
                    self.specListWidget.setCurrentRow(plotIndex)
                    self.ignoreSignal = False
                    
            curAx.legend(axespad = 0.03, pad=0.25)
            self.plotWidget.canvas.format_labels()
            self.plotWidget.canvas.draw()
            self.plotWidget.setFocus()#this is needed so that you can use CTRL+Z to zoom
    
    def setupVars(self):
        self.dirList = []
        self.curDir = os.getcwd()
        self.dataList = []
        self.loadOk = False
        self.multiPlotIndex = []
        self.ignoreSignal = False
    
    def setupGUI(self):
        self.specNameEdit.clear()
        self.indexHSlider.setMaximum(0)
        self.indexSpinBox.setMaximum(0)
        
    def updateGUI(self,  loadedItem=None):
        if loadedItem != None:
            self.dataList.append(loadedItem)
            self.specListWidget.addItem(loadedItem.name)
        
        self.numSpec = len(self.dataList)
        if self.numSpec == 1:
            self.plotByIndex(0)
            self.indexHSlider.setMaximum(self.numSpec)
            self.indexSpinBox.setMaximum(self.numSpec)
        else:
            self.indexHSlider.setMaximum(self.numSpec-1)
            self.indexSpinBox.setMaximum(self.numSpec-1)
    
    def readData(self, dir):#dir is directory or data to load
    #add try/except for this....?
        tempFlex = FR(dir)
        tempSpec = tempFlex.data['spectrum']
        data2plot = DataPlot(tempSpec[:, 0],  tempSpec[:, 1])
        self.dataList.append(data2plot)
        return True
    
    def initDataList(self):
        if self.loadmzXMLCB.isChecked():
            dirList = LmzXML()
            if len(dirList) !=0:
                self.dirList = dirList
                self.loadOk = True
                if self.readThread.updateThread(dirList,  loadmzXML = True):
                    self.readThread.start()
                    
        else:    
            dirList = LFid()
            if len(dirList) !=0:
                self.dirList = dirList
                self.loadOk = True
                if self.readThread.updateThread(dirList):
                    self.readThread.start()
                    

class LoadThread(QtCore.QThread):
        def __init__(self, parent = None):    
            QtCore.QThread.__init__(self, parent)
            
            self.finished = False
            self.ready = False
            self.loadmzXML = False
         
        def updateThread(self, loadList, loadmzXML = False):
            self.loadList = loadList
            self.loadmzXML = loadmzXML
            self.numItems = len(loadList)
            self.ready = True
            return True
        
        def run(self):
            if self.ready:
                if self.loadmzXML:
                    while not self.finished and self.numItems > 0:
                        for item in self.loadList:
                            tempmzXML =  mzXMLR(item)
                            tempSpec = tempmzXML.data['spectrum']
                            if len(tempSpec)>0:
                                data2plot = DataPlot(tempSpec[0],  tempSpec[1],  name = os.path.basename(item))
                                #this following line is key to pass python object via the SIGNAL/SLOT mechanism of PyQt
                                #note PyQt_PyObject
                                self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),data2plot)

                            self.numItems -=1
                else:
                    while not self.finished and self.numItems > 0:
                        for item in self.loadList:
                            tempFlex = FR(item)
                            tempSpec = tempFlex.data['spectrum']
                            data2plot = DataPlot(tempSpec[:, 0],  tempSpec[:, 1])
                            data2plot.setPeakList(tempFlex.data['peaklist'])
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
        self.pkListOk = False
        self.peakList = None
        self.mplAx = None
    
    def setAxis(self,  mplAxInstance):
        self.axSet = True
        self.mplAx = mplAxInstance
    
    def setPeakList(self, peaklist):
        if peaklist != None:
            if len(peaklist)>0:
                self.pkListOk = True
                self.peakList = peaklist
            
    
    def plot(self,  mplAxInstance, scatter = False):
        #if self.axSet:
        self.mplAx = mplAxInstance
        if self.y != None:
            if scatter:
                self.mplAx.scatter(self.x,  self.y,  label = self.name)
            else:
                self.mplAx.plot(self.x,  self.y,  label = self.name)#,  color = 'b')
                if self.pkListOk:
                    self.mplAx.vlines(self.peakList[:, 0], 0, self.peakList[:, 1],  color = 'r')
        else:
            self.mplAx.plot(self.x,  label = self.name)
#    else:
#        errMsg = 'axis must be set before attempting to plot'
#        raise errMsg

if __name__ == "__main__":
    import sys    
    app = QtGui.QApplication(sys.argv)    
    plot = Plot_Widget()
    plot.show()
    sys.exit(app.exec_())     
