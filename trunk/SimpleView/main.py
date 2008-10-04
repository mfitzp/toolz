#!/usr/bin/env python

import os
import time

from PyQt4 import QtCore,  QtGui

import numpy as N
import scipy as S

from FolderParse import __loadDataFolder__ as LF
from flexReader import brukerFlexDoc as FR



from ui_main import Ui_Form


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
        if self.initDataList():
            self.loadOk = True
            self.setupWidgets()
        else:
            self.loadOk = False

        #QtCore.QObject.connect(self.indexSpinBox, QtCore.SIGNAL("valueChanged (int)"),self.plotByIndex)
        QtCore.QObject.connect(self.indexHSlider,  QtCore.SIGNAL("sliderReleased()"),self.updatePlotIndex)
        #sliderReleased()
    
    def updatePlotIndex(self):
        self.indexSpinBox.setValue(self.indexHSlider.value())
        self.plotByIndex(self.indexSpinBox.value())
    
    def plotByIndex(self, plotIndex):
        #Could QTimer be used?
#        time.sleep(0.5)
#        if plotIndex == self.indexSpinBox.value():#this is just to see if the user is still sliding things around
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
        
    def setupWidgets(self):
        self.indexHSlider.setMaximum(self.numSpec-1)
        self.indexSpinBox.setMaximum(self.numSpec-1)
        self.specNameEdit.clear()
        self.plotByIndex(0)

    def initDataList(self):
        dirList = LF()
        if len(dirList) !=0:
            self.numSpec = len(dirList)
            self.dirList = dirList
            
            #This is where the threading needs to start....
            for dir in self.dirList:
                tempFlex = FR(dir)
                tempSpec = tempFlex.data['spectrum']
                data2plot = DataPlot(tempSpec[:, 0],  tempSpec[:, 1])
                self.dataList.append(data2plot)
            
            return True
#            for i in range(self.numSpec):
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
    plot = Plot_Widget()#data2plot,  varDict = totaldict)
    plot.show()
    sys.exit(app.exec_())     
