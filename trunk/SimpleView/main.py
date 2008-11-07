#!/usr/bin/env python
###################################
'''To Do:

Add update function for file path display--how to keep old dirList after second load?
Print Screen?

Add progress bar to status bar...look at Ashoka's Code




'''
###################################
import os, sys
import time

from PyQt4 import QtCore,  QtGui

import numpy as N
import scipy as S

from matplotlib.lines import Line2D

from FolderParse import Load_FID_Folder as LFid
from FolderParse import Load_mzXML_Folder as LmzXML
from flexReader import brukerFlexDoc as FR
from mzXML_reader import mzXMLDoc as mzXMLR

import ui_main


class Plot_Widget(QtGui.QMainWindow,  ui_main.Ui_MainWindow):
    def __init__(self, parent = None):
        super(Plot_Widget,  self).__init__(parent)
        self.ui = self.setupUi(self)

        self.handleActionA = QtGui.QAction("Cursor A", self)
        self.plotWidget.addAction(self.handleActionA)

        self.handleActionB = QtGui.QAction("Cursor B", self)
        self.plotWidget.addAction(self.handleActionB)

        self.cursorClearAction = QtGui.QAction("Clear Cursors",  self)
        self.plotWidget.addAction(self.cursorClearAction)

        QtCore.QObject.connect(self.handleActionA, QtCore.SIGNAL("triggered()"),self.SelectPointsA)
        QtCore.QObject.connect(self.handleActionB, QtCore.SIGNAL("triggered()"),self.SelectPointsB)
        QtCore.QObject.connect(self.cursorClearAction, QtCore.SIGNAL("triggered()"),self.cursorClear)

        self.setupVars()
        self.setupGUI()
        self.setupPlot()
        self.readThread = LoadThread()

        QtCore.QObject.connect(self.indexSpinBox, QtCore.SIGNAL("valueChanged (int)"), self.updatePlot)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"), self.updateGUI)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("terminated()"), self.updateGUI)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("finished()"), self.updateGUI)
        QtCore.QObject.connect(self.loadDirBtn, QtCore.SIGNAL("clicked()"), self.initDataList)
        QtCore.QObject.connect(self.action_Open,QtCore.SIGNAL("triggered()"),self.initDataList)
        QtCore.QObject.connect(self.specListWidget, QtCore.SIGNAL("itemClicked (QListWidgetItem *)"), self.specListSelect)

    def specListSelect(self, widgetItem):
        selectItems = self.specListWidget.selectedItems()
        #curRow
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
                    curDataName = self.dataList[i]
                    self.dataDict[curDataName].plot(curAx)
                #the following makes it so the change is ignored and the plot does not update
                self.ignoreSignal = True
                self.indexHSlider.setValue(i)
                self.indexSpinBox.setValue(i)
                self.ignoreSignal = False
            else:
                if plotIndex == None:
                    plotIndex = self.initIndex
                if plotIndex == self.indexSpinBox.value():#this is just to see if the user is still sliding things around before updating plot
                    curDataName = self.dataList[plotIndex]
                    self.dataDict[curDataName].plot(curAx)
                    self.specNameEdit.setText(self.dirList[plotIndex])#use dataList to ge the name?
                    #the following makes it so the change is ignored and the plot does not update
                    self.ignoreSignal = True
                    self.specListWidget.setCurrentRow(plotIndex)
                    self.ignoreSignal = False
            if self.plotLegendCB.isChecked():
                curAx.legend(axespad = 0.03, pad=0.25)
            try:
                minX = curAx.get_lines()[0].get_xdata()[0]
                self.addPickers(minX)
            except:
                errorMsg = "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
                print errorMsg
                self.addPickers()
            self.plotWidget.canvas.format_labels()
            self.plotWidget.canvas.draw()
            self.plotWidget.setFocus()#this is needed so that you can use CTRL+Z to zoom


    def setupVars(self):
        self.dirList = []
        self.curDir = os.getcwd()
        self.dataList = []
        self.dataDict = {}
        self.loadOk = False
        self.multiPlotIndex = []
        self.ignoreSignal = False
        self.firstLoad = True

    def setupGUI(self):
        self.specNameEdit.clear()
        self.indexHSlider.setMaximum(0)
        self.indexSpinBox.setMaximum(0)
        self.initContextMenus()

    def updateGUI(self,  loadedItem=None):
        if loadedItem != None:
            if self.dataDict.has_key(loadedItem.name):
                pass
            else:
                self.dataList.append(loadedItem.name)
                self.specListWidget.addItem(loadedItem.name)
            self.dataDict[loadedItem.name] = loadedItem

        self.numSpec = len(self.dataDict)
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
        if not self.firstLoad:
            #reinitialize GUI and spectrumList
            self.setupGUI()
        if self.loadmzXMLCB.isChecked():
            loadLIFT = self.excludeLIFTCB.isChecked()
            dirList = LmzXML(excludeLIFT = loadLIFT)
            if len(dirList) !=0:
                self.dirList = dirList
                self.loadOk = True
                self.firstLoad = False
                if self.readThread.updateThread(dirList,  loadmzXML = True):
                    self.readThread.start()

        else:
            dirList = LFid()
            if len(dirList) !=0:
                self.dirList = dirList
                self.loadOk = True
                self.firstLoad = False
                if self.readThread.updateThread(dirList):
                    self.readThread.start()

        #########  Index Picker  ###############################

    def setupPlot(self):
        self.cAPicker = None
        self.cBPicker = None

        self.cAOn = False#also used for picker
        self.cBOn = False

        self.cursorAInfo=[0, 0, 0, 0]
        self.cursorBInfo=[0, 0, 0, 0]

        self.indexA = 0
        self.indexB = 0

        self.dx = 0
        self.dy = 0

        self.addPickers()

    def addPickers(self, minX = 0):
        #minX is provided so that the plot will scale correctly when a data trace is initiated
        self.selectHandleA,  = self.plotWidget.canvas.ax.plot([minX], [0], 'o',\
                                        ms=8, alpha=.4, color='yellow', visible=False,  label = '_nolegend_')
        self.selectHandleB,  = self.plotWidget.canvas.ax.plot([minX], [0], 's',\
                                        ms=8, alpha=.4, color='green', visible=False,  label = '_nolegend_')

    def initContextMenus(self):
        self.plotWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.plotWidget.connect(self.plotWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.__mplContext__)

    def __mplContext__(self, point):
        '''Create a menu for the mpl widget'''
        ct_menu = QtGui.QMenu("Plot Menu", self.plotWidget)
#        ct_menu.addAction(self.ui.actionZoom)
#        ct_menu.addAction(self.ui.actionAutoScale)
#        ct_menu.addSeparator()
#        ct_menu.addAction(self.ui.actionPlotOptions)
#        ct_menu.addSeparator()
#        ct_menu.addAction(self.ui.actionClear)
#        ct_menu.addSeparator()
        ct_menu.addAction(self.handleActionA)
        ct_menu.addAction(self.handleActionB)
        ct_menu.addAction(self.cursorClearAction)
#        ct_menu.addSeparator()
        ct_menu.exec_(self.plotWidget.mapToGlobal(point))

    def cursorClear(self):
        if self.cAOn:# and self.cAPicker:
            self.selectHandleA.set_visible(False)
            self.plotWidget.canvas.mpl_disconnect(self.cAPicker)
            self.cAOn = False
            self.cAPicker = None
            self.cALabelLE.setText('')
            self.cAIndexLE.setText('')
            self.cA_XLE.setText('')
            self.cA_YLE.setText('')

        if self.cBOn:# and self.cBPicker:
            self.selectHandleB.set_visible(False)
            self.plotWidget.canvas.mpl_disconnect(self.cBPicker)
            self.cBOn = False
            self.cBPicker = None
            self.cBLabelLE.setText('')
            self.cBIndexLE.setText('')
            self.cB_XLE.setText('')
            self.cB_YLE.setText('')

        self.dxLE.setText('')
        self.dyLE.setText('')

        try:#this is so that the cursor label gets removed
            self.cursAText.remove()
            self.cursBText.remove()
        except:
            pass

        self.plotWidget.canvas.draw()


    def cursorStats(self):
        if self.cAOn:
            self.cALabelLE.setText(self.cursorAInfo[3])
            self.cAIndexLE.setText(str(self.cursorAInfo[0]))
            self.cA_XLE.setText('%.4f'%self.cursorAInfo[1])
            self.cA_YLE.setText('%.4f'%self.cursorAInfo[2])

        if self.cBOn:
            self.cBLabelLE.setText(self.cursorBInfo[3])
            self.cBIndexLE.setText(str(self.cursorBInfo[0]))
            self.cB_XLE.setText('%.4f'%self.cursorBInfo[1])
            self.cB_YLE.setText('%.4f'%self.cursorBInfo[2])

        if self.cAOn and self.cBOn:
            self.dx = self.cursorAInfo[1]-self.cursorBInfo[1]
            self.dy = self.cursorAInfo[2]-self.cursorBInfo[2]
            self.dxLE.setText('%.4f'%self.dx)
            self.dyLE.setText('%.4f'%self.dy)
            #return True

    def SelectPointsA(self):
        """
        This method will be called from the plot context menu for
        selecting points
        """
        self.plotWidget.canvas.mpl_disconnect(self.cBPicker)
        self.cBPicker = None
        if self.cAPicker ==None:
            self.cAPicker = self.plotWidget.canvas.mpl_connect('pick_event', self.OnPickA)
            self.cAOn = True


    def SelectPointsB(self):

        self.plotWidget.canvas.mpl_disconnect(self.cAPicker)
        self.cAPicker = None
        if self.cBPicker == None:
            self.cBPicker = self.plotWidget.canvas.mpl_connect('pick_event', self.OnPickB)
            self.cBOn = True

    def OnPickA(self, event):
        """
        This is the pick_event handler for matplotlib
        This is the pick_event handler for matplotlib
        This method will get the coordinates of the mouse pointer and
        finds the closest point and retrieves the corresponding peptide sequence.
        Also draws a yellow circle around the point.--from Ashoka 5/29/08
        """

        #print "Pick A"
        if not isinstance(event.artist, Line2D):
            return True

        try:#this is so that the cursor label gets removed
            self.cursAText.remove()
        except:
            pass

        line = event.artist
        self.indexA = event.ind[0]
        xdata = line.get_xdata()
        ydata = line.get_ydata()

        self.selectHandleA.set_data([xdata[self.indexA]], [ydata[self.indexA]])
        self.selectHandleA.set_visible(True)

        self.cursAText = self.plotWidget.canvas.ax.text(xdata[self.indexA], ydata[self.indexA], '%.4f'%xdata[self.indexA],  fontsize=9, rotation = 45)

        self.cursorAInfo[0]=self.indexA
        self.cursorAInfo[1]=xdata[self.indexA]
        self.cursorAInfo[2]=ydata[self.indexA]
        self.cursorAInfo[3]=line.get_label()
        self.cursorStats()

        self.plotWidget.canvas.draw()

        #print self.cursorAInfo

    def OnPickB(self, event):
        #print "Pick B"
        if not isinstance(event.artist, Line2D):
            return True

        try:#this is so that the cursor label gets removed
            self.cursBText.remove()
        except:
            pass

        line = event.artist
        self.indexB = event.ind[0]
        xdata = line.get_xdata()
        ydata = line.get_ydata()

        self.selectHandleB.set_data([xdata[self.indexB]], [ydata[self.indexB]])
        self.selectHandleB.set_visible(True)

        self.cursAText = self.plotWidget.canvas.ax.text(xdata[self.indexB], ydata[self.indexB], '%.4f'%xdata[self.indexB],  fontsize=9, rotation = 45)

        self.cursorBInfo[0]=self.indexB
        self.cursorBInfo[1]=xdata[self.indexB]
        self.cursorBInfo[2]=ydata[self.indexB]
        self.cursorBInfo[3]=line.get_label()
        self.cursorStats()

        self.plotWidget.canvas.draw()

        #print self.cursorAInfo

        ###############################


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
                                data2plot.setPeakList(tempmzXML.data['peaklist'])
                                #this following line is key to pass python object via the SIGNAL/SLOT mechanism of PyQt
                                #note PyQt_PyObject
                                self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),data2plot)

                            self.numItems -=1
                else:
                    while not self.finished and self.numItems > 0:
                        for item in self.loadList:
                            tempFlex = FR(item)
                            tempSpec = tempFlex.data['spectrum']
                            data2plot = DataPlot(tempSpec[:, 0],  tempSpec[:, 1], name = item.split(os.path.sep)[-4])#the -4 index is to handle the Bruker File Structure
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
                self.mplAx.plot(self.x,  self.y,  label = self.name,  picker = 5)#,  color = 'b')
                if self.pkListOk:
                    try:
                        if type(self.peakList[0]) == N.ndarray:
                            self.mplAx.vlines(self.peakList[:, 0], 0, self.peakList[:, 1]*1.1,  color = 'r',  label = '_nolegend_')
                        elif type(self.peakList[0]) == N.float64:
                            #this is the case where there is only one value in the peaklist
                            self.mplAx.vlines(self.peakList[[0]], 0, self.peakList[[1]]*1.2,  color = 'r',  label = '_nolegend_')
                        else:
                            print 'Type of First peakList element', type(self.peakList[0])
                            print "Error plotting peak list"

                    except:
                        print "Error plotting peak list"
                        errorMsg = "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
                        print errorMsg



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
