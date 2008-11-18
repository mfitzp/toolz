#!/usr/bin/env python
###################################
'''To Do:
exclude list/include list with tolerance
'''
###################################
import os, sys
import time

from PyQt4 import QtCore,  QtGui

import numpy as N
import scipy as S
import tables as T

from matplotlib import colors
from matplotlib.widgets import SpanSelector, RectangleSelector
from pylab import cm
cmaps = [cm.jet,  cm.hot,  cm.spectral]

#from LECO_IO import ChromaTOF_Reader as CR
#import SplitNStich as SNS
import PeakFunctions as PF
import supportFunc as SF

import ui_iterate

EXCLUDE = N.arange(30,80)

class Plot_Widget(QtGui.QMainWindow,  ui_iterate.Ui_MainWindow):
    def __init__(self, parent = None):
        super(Plot_Widget,  self).__init__(parent)
        self.ui = self.setupUi(self)

        self.setupVars()
        self.setupGUI()

        QtCore.QObject.connect(self.indexSpinBox, QtCore.SIGNAL("valueChanged (int)"), self.updatePlot)

        self.Zoom = QtGui.QAction("Zoom",  self)
        self.Zoom.setShortcut("Ctrl+Z")
        self.plotWidget.addAction(self.Zoom)
        QtCore.QObject.connect(self.Zoom,QtCore.SIGNAL("triggered()"), self.ZoomToggle)

        self.actionAutoScale = QtGui.QAction("AutoScale",  self)#self.MainWindow)
        self.actionAutoScale.setShortcut("Ctrl+A")
        self.plotWidget.addAction(self.actionAutoScale)
        QtCore.QObject.connect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)

    def setupVars(self):

        self.ref = 'TAi-R1_T.h5'
        self.sam = 'TCiv-R1_T.h5'

        self.numSpec = 25
        self.startIndex = 55000
        self.specIncrement = 200

        self.imageAxis = None

    def setupGUI(self):

        self.plotWidget.canvas.setupSub(1)
        self.plotWidget2.canvas.setupSub(2)

        self.imageAxis = self.plotWidget.canvas.axDict['ax1']
        self.RS = RectangleSelector(self.imageAxis, self.setZScale, minspanx = 2,
                        minspany = 2, drawtype='box',useblit=True)
        self.usrZoom = False
        self.RS.visible = False

        self.plotWidget.canvas.mpl_connect('button_press_event', self.imageClick)

        self.eicAxis = self.plotWidget2.canvas.axDict['ax1']
        self.mzAxis = self.plotWidget2.canvas.axDict['ax2']

        self.indexHSlider.setMinimum(1)
        self.indexSpinBox.setMinimum(1)
        self.indexHSlider.setMaximum(self.numSpec)
        self.indexSpinBox.setMaximum(self.numSpec)

        self.addPickers()

    def addPickers(self, minX = 0):
        #minX is provided so that the plot will scale correctly when a data trace is initiated
        self.selectCursA,  = self.imageAxis.plot([minX], [0], 'o',\
                                        ms=7, alpha=.8, color='yellow', visible=True,  label = '_nolegend_')
        self.xLine = self.imageAxis.axvline(x=0, ls = ':', color = 'y', alpha = 0.6)
        self.yLine = self.imageAxis.axhline(y=0, ls = ':', color = 'y', alpha = 0.6)
#        self.cAPicker = self.plotWidget.canvas.mpl_connect('pick_event', self.imageClick)

    def imageClick(self, event):

#        if event.mouseevent.xdata != None and event.mouseevent.ydata != None:
#            xPnt, yPnt =  int(N.round(event.mouseevent.xdata)), event.mouseevent.ydata
        if event.xdata != None and event.ydata != None:
            self.selectCursA.set_data([event.xdata], [event.ydata])
            xPnt, yPnt =  int(N.round(event.xdata)), int(N.round(event.ydata))
            print xPnt, yPnt
#            self.selectCursA.set_data([xPnt], [yPnt])
            self.xLine.set_xdata([xPnt])
            self.yLine.set_ydata([yPnt])
            self.imageAxis.draw_artist(self.selectCursA)
            self.imageAxis.draw_artist(self.xLine)
            self.imageAxis.draw_artist(self.yLine)




            self.plotWidget.canvas.blit(self.imageAxis.bbox)




    def colorScale(self, dataMtx):
        dataMtx = N.ma.masked_where(dataMtx<= 0, dataMtx)
        lev_exp = N.arange(0, N.log10(dataMtx.max())+1)
        #print z.max(), z.min()
        #print lev_exp
        levs = N.power(10, lev_exp)
        return dataMtx, levs
        #cs = P.contourf(z, levs, norm=colors.LogNorm())


    def updatePlot(self, index):
        for ax in self.plotWidget.canvas.axDict.itervalues():
            ax.cla()


        for ax in self.plotWidget2.canvas.axDict.itervalues():
            ax.cla()

        self.addPickers()
        self.refZ, refOK = self.getMZSlice(self.ref, index)
        self.samZ, samOK = self.getMZSlice(self.sam, index)

        if refOK and samOK:
            rows = self.refZ.shape[0]
            cols = self.samZ.shape[1]


            sicR = SF.getBPC(self.refZ)
            sicS = SF.getBPC(self.samZ)

#            cor2D, maxShift, corVals = SF.corrMatrix(self.refZ, self.samZ)
            cor2D, maxShift, corVals = SF.corrMatrix(self.refZ, self.samZ, excludeList = EXCLUDE)

            cor = N.correlate(sicR, sicS, mode = 'same')
            shift = N.round(cor.argmax()-len(sicR)/2)#gets value to shift by
            self.specNameEdit.setText(str(shift))
            print shift

            corVals = SF.crudeNoiseFilter(corVals, 2)
            corIndices = N.where(corVals>0)[0]
            corMax = corVals[corIndices]

            ############colorMap Section
#            self.refZ, cLvlsZ = self.colorScale(self.refZ)
#            self.samZ, cLvlsS = self.colorScale(self.samZ)

            #P.contourf(z, levs, norm=colors.LogNorm())

            ax1 = self.plotWidget.canvas.axDict['ax1']
            self.refIm = ax1.contour(self.refZ, alpha = 1,  aspect = 'auto', origin = 'lower',  cmap = cmaps[0], label = 'R', picker = 5)
            #ax1.contour(self.samZ, alpha = 0.5,  origin = 'lower',  cmap = cmaps[1], label = 'S')
#            ax1.contour(N.log(self.refZ), alpha = 1,  origin = 'lower',  cmap = cmaps[0], label = 'R')
#            ax1.contour(N.log(self.samZ), alpha = 0.5,  origin = 'lower',  cmap = cmaps[1], label = 'S')
#            ax1.imshow(N.log(self.refZ), alpha = 1,  origin = 'lower',  cmap = cmaps[0], label = 'R')
#            ax1.imshow(N.log(self.samZ), alpha = 0.5,  origin = 'lower',  cmap = cmaps[1], label = 'S')
#            ax1.pcolormesh(self.refZ, alpha = 1,  origin = 'lower',  cmap = cmaps[0], label = 'R')
#            ax1.pcolormesh(self.samZ, alpha = 0.5,  origin = 'lower',  cmap = cmaps[1], label = 'S')

#            ax2 = self.plotWidget.canvas.axDict['ax2']
#            ax2.plot(sicR)
#            ax2.plot(sicS)

            ax1a = self.plotWidget2.canvas.axDict['ax1']
            ax2a = self.plotWidget2.canvas.axDict['ax2']
            ax1a.plot(sicR)
            ax1a.plot(sicS)

            #was ax3
#            ax3 = self.plotWidget.canvas.axDict['ax3']
#            ax1a.plot(corVals)
#            ax1a.plot(corIndices, corMax, 'ro')

#            ax4 = self.plotWidget.canvas.axDict['ax4']

            nHist = N.histogram(maxShift[corIndices], bins = int(cols*0.5), new=True, weights = N.sqrt(corMax[corMax.argsort()[-len(corIndices):]]))
            nHisty = nHist[0]
            nHistx = nHist[1][:-1]
            ax2a.vlines(nHistx,0, nHisty, lw = 2.0)


########################################################################################
#            ax1a = self.plotWidget2.canvas.axDict['ax1']
#            ax1a.hist(maxShift[corVals.argsort()[-20:]], bins = int(cols*0.5))
#
#            ax2a = self.plotWidget2.canvas.axDict['ax2']
##            ax2a.hist(maxShift[corVals.argsort()[-25:]], bins = int(cols*0.5))
#            indicies = corVals.argsort()[-25:]
#            nHist2 = N.histogram(maxShift[indicies], bins = int(cols*0.5), new=True, weights = N.sqrt(corVals[indicies]))
#            nHisty2 = nHist2[0]
#            nHistx2 = nHist2[1][:-1]
#            ax2a.vlines(nHistx2,0, nHisty2, lw = 2.0)


        else:
            print "Requested rows exceed data size!"
            print "Requested end row: %s", self.startIndex+self.specIncrement*index
            print "Available: %s", self.maxRows


        self.plotWidget.canvas.format_labels()
        self.plotWidget.canvas.draw()
        self.plotWidget.setFocus()#this is needed so that you can use CTRL+Z to zoom

        self.plotWidget2.canvas.format_labels()
        self.plotWidget2.canvas.draw()
        self.plotWidget2.setFocus()


###########################

    def autoscale_plot(self):
        #self.toolbar.home() #implements the classic return to home
#        self.imageAxis.cla()
#        self.imageAxis.contour(self.refZ, alpha = 1,  origin = 'lower',  cmap = cmaps[0], label = 'R')
#        self.plotWidget.canvas.format_labels()
#        self.plotWidget.canvas.draw()
        self.imageAxis.autoscale_view(tight = False, scalex=True, scaley=True)
        self.plotWidget.canvas.draw()

    def setZScale(self, event1, event2):
        if self.usrZoom:
            'event1 and event2 are the press and release events'
            dataCoord = [[int(N.round(event1.xdata)), int(N.round(event1.ydata))],[int(N.round(event2.xdata)), int(N.round(event2.ydata))]]
            dataCoord = N.array(dataCoord)
            xLim = dataCoord[:,0]
            yLim = dataCoord[:,1]
            xLim.sort()
            yLim.sort()
    #        print xLim
    #        print yLim
            self.imageAxis.set_xlim(xLim[0],xLim[1])
            self.imageAxis.set_ylim(yLim[0],yLim[1])
            localRef = self.refZ[xLim[0]:xLim[1],yLim[0]:yLim[1]]
#            self.imageAxis.cla()
#            self.imageAxis.contour(localRef, alpha = 1,  origin = 'lower',  cmap = cmaps[0], label = 'R')
#            self.plotWidget.canvas.format_labels()
#            self.plotWidget.canvas.draw()
#            self.refIm.autoscale()
            self.refIm.norm.autoscale(localRef)
            self.plotWidget.canvas.draw()
            #print self.refIm
            #print "(%3.2f, %3.2f) --> (%3.2f, %3.2f)"%(x1,y1,x2,y2)
            #print " The button you used were: ",event1.button, event2.button

    def ZoomToggle(self):
        #self.toolbar.zoom() #this implements the classic zoom
        if self.usrZoom:
            self.usrZoom = False
            self.RS.visible = False
        else:
            self.usrZoom = True
            self.RS.visible = True



    def getMZSlice(self, fileName, index):
        f = T.openFile(fileName, 'r')
        mz = f.root.dataCube
        self.maxRows = mz.shape[0]
        if self.startIndex+self.specIncrement*index >= self.maxRows:
            mzSlice = N.zeros(1)
            getState = False
        else:
            mzSlice = SF.normArray(mz[self.startIndex+self.specIncrement*(index-1):self.startIndex+self.specIncrement*index])
            getState = True

        f.close()

        return mzSlice, getState


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    plot = Plot_Widget()
    plot.show()
    sys.exit(app.exec_())
