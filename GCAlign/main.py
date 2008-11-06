#!/usr/bin/env python
###################################
'''To Do:
'''
###################################
import os, sys
import time

from PyQt4 import QtCore,  QtGui

import numpy as N
import scipy as S
import tables as T

from pylab import cm
cmaps = [cm.spectral,  cm.hot,  cm.spectral]

from LECO_IO import ChromaTOF_Reader as CR
import SplitNStich as SNS
import PeakFunctions as PF
import supportFunc as SF


import ui_iterate


class Plot_Widget(QtGui.QMainWindow,  ui_iterate.Ui_MainWindow):
    def __init__(self, parent = None):
        super(Plot_Widget,  self).__init__(parent)
        self.ui = self.setupUi(self)

        self.setupVars()
        self.setupGUI()

        QtCore.QObject.connect(self.indexSpinBox, QtCore.SIGNAL("valueChanged (int)"), self.updatePlot)


    def setupVars(self):

        self.ref = 'TAi-R1_T.h5'
        self.sam = 'TCiv-R1_T.h5'

        self.numSpec = 25
        self.startIndex = 55000
        self.specIncrement = 200

    def setupGUI(self):

        self.plotWidget.canvas.setupSub(4)
        self.plotWidget2.canvas.setupSub(2)

        self.indexHSlider.setMinimum(1)
        self.indexSpinBox.setMinimum(1)
        self.indexHSlider.setMaximum(self.numSpec)
        self.indexSpinBox.setMaximum(self.numSpec)

    def updatePlot(self, index):
        for ax in self.plotWidget.canvas.axDict.itervalues():
            ax.cla()

        for ax in self.plotWidget2.canvas.axDict.itervalues():
            ax.cla()

        refZ, refOK = self.getMZSlice(self.ref, index)
        samZ, samOK = self.getMZSlice(self.sam, index)

        if refOK and samOK:
            rows = refZ.shape[0]
            cols = samZ.shape[1]


            sicR = SF.getBPC(refZ)
            sicS = SF.getBPC(samZ)

            cor2D, maxShift, corVals = SF.corrMatrix(refZ, samZ)

            cor = N.correlate(sicR, sicS, mode = 'same')
            shift = N.round(cor.argmax()-len(sicR)/2)#gets value to shift by
            self.specNameEdit.setText(str(shift))
            print shift

            corVals = SF.crudeNoiseFilter(corVals, 2)
            corIndices = N.where(corVals>0)[0]
            corMax = corVals[corIndices]

            ax1 = self.plotWidget.canvas.axDict['ax1']
            ax1.contour(refZ, alpha = 1,  origin = 'lower',  cmap = cmaps[0], label = 'R')
            ax1.contour(samZ, alpha = 0.5,  origin = 'lower',  cmap = cmaps[1], label = 'S')

            ax2 = self.plotWidget.canvas.axDict['ax2']
            ax2.plot(sicR)
            ax2.plot(sicS)

            ax3 = self.plotWidget.canvas.axDict['ax3']
            ax3.plot(corVals)
            ax3.plot(corIndices, corMax, 'ro')

            ax4 = self.plotWidget.canvas.axDict['ax4']

            nHist = N.histogram(maxShift[corIndices], bins = int(cols*0.5), new=True, weights = N.sqrt(corMax[corMax.argsort()[-len(corIndices):]]))
            nHisty = nHist[0]
            nHistx = nHist[1][:-1]
            ax4.vlines(nHistx,0, nHisty, lw = 2.0)
########################################################################################
            ax1a = self.plotWidget2.canvas.axDict['ax1']
            ax1a.hist(maxShift[corVals.argsort()[-20:]], bins = int(cols*0.5))

            ax2a = self.plotWidget2.canvas.axDict['ax2']
#            ax2a.hist(maxShift[corVals.argsort()[-25:]], bins = int(cols*0.5))
            indicies = corVals.argsort()[-25:]
            nHist2 = N.histogram(maxShift[indicies], bins = int(cols*0.5), new=True, weights = N.sqrt(corVals[indicies]))
            nHisty2 = nHist2[0]
            nHistx2 = nHist2[1][:-1]
            ax2a.vlines(nHistx2,0, nHisty2, lw = 2.0)


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



    def getMZSlice(self, fileName, index):
        f = T.openFile(fileName, 'r')
        mz = f.root.dataCube
        self.maxRows = mz.shape[0]
        if self.startIndex+self.specIncrement*index >= self.maxRows:
            mzSlice = N.zeros(1)
            getState = False
        else:
            mzSlice = SNS.normArray(mz[self.startIndex+self.specIncrement*(index-1):self.startIndex+self.specIncrement*index])
            getState = True

        f.close()

        return mzSlice, getState


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    plot = Plot_Widget()
    plot.show()
    sys.exit(app.exec_())
