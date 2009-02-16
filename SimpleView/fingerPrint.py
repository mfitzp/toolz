import os, sys, traceback
from PyQt4 import QtGui, QtCore
import numpy as N

from matplotlib.patches import Rectangle as Rect
import supportFunc as SF
import ui_fingerPrint
from dbscan import dbscan

COLORS = ['#297AA3','#A3293D','#3B9DCE','#293DA3','#5229A3','#8F29A3','#A3297A',
'#7AA329','#3DA329','#29A352','#29A38F','#A38F29','#3B9DCE','#6CB6DA','#CE6C3B','#DA916C',
'#0080FF','#0000FF','#7ABDFF','#8000FF','#FF0080','#FF0000','#FF8000','#FFFF00','#A35229','#80FF00',
'#00FF00','#00FF80','#00FFFF','#3D9EFF','#FF9E3D','#FFBD7A']

class Finger_Widget(QtGui.QWidget, ui_fingerPrint.Ui_fingerPlotWidget):
    def __init__(self, dataDict = None, parent = None):
        super(Finger_Widget, self).__init__(None)
#        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.ui = self.setupUi(self)
        self.mainAx = self.plotWidget.canvas.ax
        self.dataDict = {}
        self.dataDictOK = False
        self.setupVars()

        if dataDict != None:
            self.dataDict = dataDict
            self.dataDictOK = True
            self.setupPlot()

        self.__initConnections__()

    def __initConnections__(self):
        self.actionAutoScale = QtGui.QAction("AutoScale",  self)#self.MainWindow)
        self.actionAutoScale.setShortcut("Ctrl+A")
        self.plotWidget.addAction(self.actionAutoScale)
        QtCore.QObject.connect(self.actionAutoScale, QtCore.SIGNAL("triggered()"), self.autoscale_plot)

    def updateDataDict(self, dataDict):
        for item in dataDict.iteritems():
            self.dataDict[item[0]]=item[1]
        self.dataDictOK = True

    def setupVars(self):
        self.plotColor = None
        self.plotColorIndex = 0
        self.compositePeakList = []
        self.peakStatDict = {'aveLoc':[],
                             'stdLoc':[],
                             'aveInt':[],
                             'stdInt':[],
                             'numMembers':[],
                             'prob':[]
                             }
        self.xLoc = None
        self.yLoc = None

    def _updatePlotColor_(self):
        if self.plotColorIndex%len(COLORS) == 0:
            self.plotColorIndex = 0
            self.plotColor = COLORS[self.plotColorIndex]
            self.plotColorIndex +=1
        else:
            self.plotColor = COLORS[self.plotColorIndex]
            self.plotColorIndex +=1

    def setupPlot(self):
        if self.dataDictOK:
            for curData in self.dataDict.itervalues():
        #            curData = self.dataDict[childName]
                self._updatePlotColor_()
                curData.plot(self.mainAx, pColor = self.plotColor)
#                pkList = curData.peakList
#                self.mainAx.scatter(pkList[:,0], pkList[:,1]*0, color = self.plotColor)

    def getFPPeakList(self):
        if self.dataDictOK:
#            self.mainAx.cla()
            self.xLoc = N.zeros(1)
            self.yLoc = N.zeros(1)
            for curData in self.dataDict.itervalues():
                pkList = curData.peakList
                self.xLoc = N.append(self.xLoc, pkList[:,0])
                self.yLoc = N.append(self.yLoc, pkList[:,1])
#                self.mainAx.scatter(pkList[:,0],pkList[:,1]*0, color = self.plotColor)
            sortInd = self.xLoc.argsort()
            self.xLoc = self.xLoc[sortInd]
            self.yLoc = self.yLoc[sortInd]
#            self.mainAx.plot(self.xLoc, self.yLoc, '--r')
            groups, gNum = groupOneD(self.xLoc, 500)
            for g in xrange(gNum):
                self._updatePlotColor_()
                subInd = N.where(groups == g)[0]
                curXMean = self.xLoc[subInd].mean()
                curXStd = self.xLoc[subInd].std()
                curYMean = self.yLoc[subInd].mean()
                curYStd = self.yLoc[subInd].std()

                self.peakStatDict['aveLoc'].append(curXMean)
                self.peakStatDict['stdLoc'].append(curXStd)
                self.peakStatDict['aveInt'].append(curYMean)
                self.peakStatDict['stdInt'].append(curYStd)
                self.peakStatDict['numMembers'].append(len(subInd))
#                self.peakStatDict['prob'].append()
                if len(subInd)>=2:
                    self.mainAx.plot(self.xLoc[subInd], self.yLoc[subInd], ms = 4, marker = 'o', alpha = 0.5, color = self.plotColor)
                    #Rect((x,y),width, height)
                    tempRect = Rect((curXMean-curXStd,0),curXStd*2,curYMean+curYStd, alpha = 0.5, facecolor = self.plotColor)
                    self.mainAx.add_patch(tempRect)


            self.setupTable()

    def setupTable(self):
        tableHeaders = ['aveLoc','stdLoc', 'aveInt', 'stdInt', 'numMembers']
        for key in tableHeaders:
            self.peakStatDict[key] = N.array(self.peakStatDict[key])

        tableData = self.peakStatDict['aveLoc']
        for key in tableHeaders[1:]:
            tableData = N.column_stack((tableData,self.peakStatDict[key]))

        self.peakTable.addData(tableData)
        self.peakTable.setSortingEnabled(True)
        self.peakTable.setHorizontalHeaderLabels(tableHeaders)

    def autoscale_plot(self):
#        print "Auto Finger"
        self.mainAx.autoscale_view(tight = False, scalex=True, scaley=True)
        self.mainAx.set_ylim(ymin = 0)
        self.plotWidget.canvas.draw()


def groupOneD(oneDVec, tol):
    '''
    oneDVec is already sorted
    tol is in ppm
    '''
    diffArray = N.diff(oneDVec)
    groups = N.zeros_like(diffArray)
    gNum = 0
    for i,diffVal in enumerate(diffArray):
        ppmDiff = (diffVal/oneDVec[i+1])*1000000
        if ppmDiff <= tol:
            groups[i] = gNum
        else:
            groups[i] = gNum
            gNum+=1
    return groups, gNum



#    for


if __name__ == "__main__":
    #from scipy import rand
    app = QtGui.QApplication(sys.argv)
    finger = Finger_Widget()
    finger.show()
    tempRect = Rect((1,1),3,5, alpha = 0.4)
    finger.mainAx.add_patch(tempRect)
    sys.exit(app.exec_())
