'''
# -*- coding: utf-8 -*-
# main.py
# Primary interface to the pysotope package
# Copyright (c) 2009, Brian H. Clowers
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of the copyright holders nor the names of any
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

This widget interfaces to the mercury algorithm written by the following:

 * Copyright (c) 2006
 *     Marc Kirchner <marc.kirchner@iwr.uni-heidelberg.de>
 *
 * Based on the emass implementation of Perttu Haimi
 * (see Copyright notice below).
 *
 * This code may be distributed under the terms of the
 * Lesser GNU Public License (LGPL) version 2 or any later version.
 *
 * Based on an algorithm developed by Alan L. Rockwood.
 *
 * Published in
 * Rockwood, A.L. and Haimi, P.: "Efficent calculation of
 * Accurate Masses of Isotopic Peaks",
 * Journal of The American Society for Mass Spectrometry
 * JASMS 03-2263, 2006
 *
 * Copyright (c) 2005 Perttu Haimi and Alan L. Rockwood

 It also uses the python script put together by Christoph Gohlke that contains
 a list of the natural elements.  That script was modified to include some of the newer
 elements by BHC in 2009.

 If I ever meet you in person I'd like to buy a few beers for
 the folks supporting matplotlib, numpy and PyQt4.  While I'm sure that would
 empty my bank account I'd give it a whirl.
'''


"""
/usr/bin/pyuic4 /home/clowers/workspace/pysotope/main.ui  -o /home/clowers/workspace/pysotope/ui_main.py
"""
#Importing built-in python modules and functions
import sys, os
from os import walk,  path

#import base64
import string
import time

from PyQt4 import QtCore, QtGui, QtSvg
from PyQt4.QtGui import QFileDialog,  QApplication

from matplotlib import rc, rcParams, use, interactive
use('Qt4Agg')

import numpy as N
import csv

from matplotlib.backends import backend_qt4, backend_qt4agg
backend_qt4.qApp = QtGui.qApp


#from io import hdfIO
from matplotlib.lines import Line2D
from matplotlib.widgets import SpanSelector

#import GUI scripts
import ui_main
from mpl_custom_widget import MPL_Widget
from mplElemIso import MPL_Widget as mplIso
from pyelements import elemDict
from elemParser import molmass, getAtoms, TableofElementsList
from isotopeCalc import isoCalc
import gaussFunctions as GF
#from xtandem_parser_class import XT_RESULTS
#import dbIO
#from customTable import DBTable
#from rangeDialog import rangeDialog as RD
#from FragmentPlot import FragPlotWidgets
#import queryFunctions as QF

plot_colors = ['#297AA3','#A3293D','#3B9DCE','#293DA3','#5229A3','#8F29A3','#A3297A',
'#7AA329','#3DA329','#29A352','#29A38F','#A38F29','#3B9DCE','#6CB6DA','#CE6C3B','#DA916C',
'#0080FF','#0000FF','#7ABDFF','#8000FF','#FF0080','#FF0000','#FF8000','#FFFF00','#A35229','#80FF00',
'#00FF00','#00FF80','#00FFFF','#3D9EFF','#FF9E3D','#FFBD7A']

markers = ['o', 'd','>', 's', '^',  'p', '<', 'h', 'v']

class periodicTableWidget(QtSvg.QSvgWidget):
    def __init__(self, parent = None):
        super(periodicTableWidget,  self).__init__(parent)
        print "Periodic Table Started"
        self.load('images\periodicTable.svg')
        self.origH = self.renderer().defaultSize().height()
        self.origW = self.renderer().defaultSize().width()
        print "Original Size: ", self.origW, self.origH
        self.xMod = 1
        self.yMod = 1
        self.loadCoords()

    def loadCoords(self):
        fileName = 'periodicTableCoordinates.csv'
        tempCoord = csv.reader(open(fileName, 'r'), delimiter = ',')
        ind = []
        xLo = []
        xHi = []
        yLo = []
        yHi = []
        self.elems = []
        for row in tempCoord:
#            print row
            ind.append(int(row[0]))
            xLo.append(int(row[1]))
            yLo.append(int(row[2]))
            xHi.append(int(row[3]))
            yHi.append(int(row[4]))
            self.elems.append(row[5])

#        self.elems = N.array(elems)
        self.ind = N.array(ind)
        self.xLo = N.array(xLo)
        self.xHi = N.array(xHi)
        self.yLo = N.array(yLo)
        self.yHi = N.array(yHi)
#        print type(self.xLo)
#        print self.xLo.min(), self.xLo.max()

    def mousePressEvent(self, event):
        '''
        The SVG coordinates are reversed in the y dimension so we need to subtract
        '''
#        print event.button(), event.x(), self.origH-event.y()
        xP = N.round(event.x()/self.xMod)#event.x()+
        yP = N.round(self.origH-(event.y()/self.yMod))
#        print xP, yP, event.x(), self.origH-(event.y())
        crit = (xP >= self.xLo) & (xP <= self.xHi) & (yP >= self.yLo) & (yP <= self.yHi)
        Ans = N.where(crit)[0]
        if len(Ans)>0:
            curAtom = self.elems[Ans]
#            print curAtom
            if elemDict.has_key(curAtom):
                elem = elemDict[curAtom]
                print elem.name, elem.mass
                self.emit(QtCore.SIGNAL("elementSelected(PyQt_PyObject)"),elem)
#                self.load('images\Hydrogen.svg')
#                self.emit
    #        print Ans, self.elems[Ans]

    def resizeEvent(self, event):
        oldSize = event.oldSize()
        newSize = event.size()
        self.xMod = 1.0*newSize.width()/self.origW#changed to float
        self.yMod = 1.0*newSize.height()/self.origH
#        print self.xMod, self.yMod
        pass

class pysotope(QtGui.QMainWindow,  ui_main.Ui_MainWindow):
    def __init__(self, parent = None):
        super(pysotope,  self).__init__(parent)
        #self.ui = ui_main.Ui_MainWindow
        self.ui = self.setupUi(self)
        #self.MainWindow = MainWindow
        #ui_main.Ui_MainWindow.setupUi(self, self.MainWindow)

#        self.__additionalVariables__()
#        self.__additionalConnections__()
#        self.__setMessages__()
#        self.__initContextMenus__()
        self.__initVars__()
        self.startup()

    def __initVars__(self):
        self.openTableList = []
        self.openPlotList = []

    def updateElemData(self, elem):
        '''
            "Name" = elem.name
            ("Symbol", elem.symbol),
            ("Atomic Number", elem.number),
            ("Group", elem.group),
            ("Period", elem.period),
            ("Block", elem.block),
            ("Atomic Weight", elem.mass),
            ("Atomic Radius", elem.atmrad),
            ("Covalent Radius", elem.covrad),
            ("Van der Waals Radius", elem.vdwrad),
            ("Electronegativity", elem.en),
            ("Electron Configuration", elem.eleconfig),
            ("Electron per Shell", ', '.join(
                "%i" % i for i in elem.eleshells)),
            "%-22s : %s"    % ("Oxidation States", elem.oxistates),
            "%-22s : %s"    % ("Isotopes", ', '.join(
                "(%i, %.10g, %.10g)" % (a,b,c*100.0) for a,b,c in \
                                                            elem.isotopes)),
            ("Ionization Potentials", ', '.join(
                "%.10g" % ion for ion in elem.ionenergy)),
            ""])
        return result
        '''
        self.curElem = elem
        self.curElemDict = {}
        self.curElemDict["Name"] = elem.name
        self.curElemDict["Symbol"] = elem.symbol
        self.curElemDict["Atomic Number"] = str(elem.number)
        self.curElemDict["Group"] = str(elem.group)
        self.curElemDict["Period"] = str(elem.period)
        self.curElemDict["Block"] = str(elem.block)
        self.curElemDict["Atomic Mass"] = str(elem.mass)
        self.curElemDict["Atomic Radius"] = str(elem.atmrad)
        self.curElemDict["Covalent Radius"] = str(elem.covrad)
        self.curElemDict["Van der Waals Radius"] = str(elem.vdwrad)
        self.curElemDict["Electronegativity"] = str(elem.en)
        self.curElemDict["Electron Configuration"] = str(elem.eleconfig)
        self.keyList = ["Symbol", "Name", "Atomic Number", "Atomic Mass", "Group",
                        "Period", "Block", "Atomic Radius", "Covalent Radius", "Van der Waals Radius",
                        "Electronegativity", "Electron Configuration"]
        self.elemTableWidget.clear()
        self.elemTableWidget.setRowCount(len(self.keyList)+1)#adding one for isotope plot
#        print self.curElem.isotopes, type(self.curElem.isotopes)

        curIsos = self.curElem.isotopes
        isoX = [curIsos[0][1]-1]#sets first point at 0 so range will be displayed correctly#N.zeros(len(curIsos)+2)
        isoY = [0.0]#N.zeros(len(curIsos)+2)

        for i,iso in enumerate(curIsos):

            print iso[1], iso[2]
            isoX.append(iso[1])
            isoY.append(iso[2])

#        print isoX
#        print isoY
        isoOk = False
        if len(isoX) > 0 and len(isoY) > 0:
            isoX.append(isoX[-1]+1)
            isoY.append(0.0)
            isoOk = True
            isoX = N.array(isoX)
            isoY = N.array(isoY)
            isoY*=100
        n = 0

        self.elemTableWidget.horizontalHeader().hide()
        self.elemTableWidget.verticalHeader().hide()

        for key in self.keyList:
            if self.curElemDict.has_key(key):
#                self.elemTableWidget.takeVerticalHeaderItem(n)
                keyItem = QtGui.QTableWidgetItem(key)
                dictItems = self.curElemDict[key]
                valItem = QtGui.QTableWidgetItem(dictItems)
                if n == 0:
                    fontSize = 35
                    curFont = QtGui.QFont()
                    curFont.setItalic(True)
                    curFont.setBold(True)
                    curFont.setPointSize(35)
                    valItem.setFont(curFont)
                    self.elemTableWidget.setItem(n, 0, valItem)
                    self.elemTableWidget.setRowHeight(0, fontSize+15)
                else:
                    self.elemTableWidget.setItem(n, 0, keyItem)
                    self.elemTableWidget.setItem(n, 1, valItem)
                n+=1

        if isoOk:
            isoPlot = mplIso()
            isoPlot.canvas.ax.vlines(isoX, 0, isoY, 'r')
            isoPlot.canvas.ax.set_ylim(ymin = -5)
            isoPlot.canvas.format_labels()
            isoPlot.canvas.draw()
#            isoPlot.show()
            self.elemTableWidget.setCellWidget(12, 0, isoPlot)
            self.elemTableWidget.setRowHeight(12, 200)
#        print "IsoOk: ", isoOk
        self.elemTableWidget.resizeColumnsToContents()

    def calcFormulaA(self):
        formulaStr = str(self.formulaInputA.text())
        if len(formulaStr)>0:
            mwAns = molmass(formulaStr)
            charge = self.chargeA.value()
            mwAns += self.electronMass*charge
            self.formulaA_MW_LE.setText(str(mwAns))
            self.calcIsotopeA(formulaStr, self.formulaA_CB.isChecked())

    def calcFormulaB(self):
        formulaStr = str(self.formulaInputB.text())
        if len(formulaStr)>0:
            mwAns = molmass(formulaStr)
            charge = self.chargeB.value()
            mwAns += self.electronMass*charge
            self.formulaB_MW_LE.setText(str(mwAns))
            self.calcIsotopeB(formulaStr, self.formulaB_CB.isChecked())

    def calcGaussIsos(self, centroids, abundances, res = 10000):
        if len(centroids) > 0:
            peakListX = []
            peakListY = []
            for i,iso in enumerate(centroids):
                abund = abundances[i]
                pkWidth = iso/res
                tempX = N.arange(iso-(pkWidth*4), iso+(pkWidth*4), 0.001)
                peakListX.append(tempX)
                peakListY.append(GF.getGauss(tempX, iso, pkWidth, amp = abund))
            return True, peakListX, peakListY
        else:
            return False, None, None


    def dumpToCSV(self, fileName, centroids, profile):
        if len(centroids)>0 and len(profile)>0:
            dumpWriter = csv.writer(open(fileName, 'w'), delimiter = ',', quotechar= "'")
            try:

                dumpWriter.writerow(['X', 'Y', 'Centroid X', 'Centroid Y'])
                for i,cent in enumerate(centroids):
                    dumpWriter.writerow[profile[0], profile[1], cent[0], cent[1]]

                for val in profile[:i]:
                    dumpWriter.writerow([val[0], val[i]])
            except:
                print "Write CSV FAILED"

    def plotIsos(self):
        if len(self.isoCentroidsA) > 0:
            self.plotWidget.canvas.ax.vlines(self.isoCentroidsA[0], 0, self.isoCentroidsA[1], 'r', label = '_nolegend_')

        if len(self.isoCentroidsB) > 0:
            self.plotWidget.canvas.ax.vlines(self.isoCentroidsB[0], 0, self.isoCentroidsB[1], 'b', label = '_nolegend_')

        if self.formulaA_CB.isChecked():
            if len(self.isoTracesA)>0:
                for i,trace in enumerate(self.isoTracesA):
                    if i == 0:
                        labelStrA = str(self.formulaInputA.text())+' +'+str(self.chargeA.value())
                        self.plotWidget.canvas.ax.plot(trace[0], trace[1],'b', alpha = 0.5, label = labelStrA)
                    else:
                        self.plotWidget.canvas.ax.plot(trace[0], trace[1],'b', alpha = 0.5)

        if self.formulaB_CB.isChecked():
            if len(self.isoTracesB)>0:
                for i,trace in enumerate(self.isoTracesB):
                    if i == 0:
                        labelStrB = str(self.formulaInputB.text())+' +'+str(self.chargeB.value())
                        self.plotWidget.canvas.ax.plot(trace[0], trace[1],'r', alpha = 0.5, label = labelStrB)
                    else:
                        self.plotWidget.canvas.ax.plot(trace[0], trace[1],'r', alpha = 0.5)
        self.plotWidget.canvas.ax.legend()
        self.plotWidget.canvas.format_labels()
        self.plotWidget.canvas.ax.set_ylim(ymin = -0.01)

#        self.plotWidget.canvas.ax.autoscale_view(tight = False, scalex=True, scaley=True)
        self.plotWidget.canvas.draw()

    def calcIsotopeA(self, formula, plotGauss = True):
        '''
        calculates isotope pattern from formula A
        '''
        boolAns, elemList, elemComp = getAtoms(formula)
        print elemList, elemComp
        if boolAns:
            if plotGauss:
                isoAns = isoCalc(elemList, elemComp, charge = self.chargeA.value())
                if isoAns[0]:
                    self.plotWidget.canvas.ax.cla()
                    self.isoCentroidsA = []
                    if not self.formulaB_CB.isChecked():
                        self.isoCentroidsB = []
                        self.isoTracesB = []

                    self.isoCentroidsA.append(isoAns[1][0])
                    self.isoCentroidsA.append(isoAns[1][1])
                    ANS = self.calcGaussIsos(self.isoCentroidsA[0], self.isoCentroidsA[1], self.isoResCalc_SB.value())
                    boolAns, peakListX, peakListY = ANS
                    self.isoTracesA = []
                    if boolAns:
                        for i,peakX in enumerate(peakListX):
                            peakY = peakListY[i]
                            self.isoTracesA.append([peakX, peakY])
                self.plotIsos()
            else:
                print elemList
                print "Element List Wonky"

    def removeIsoA(self):
        if self.isoCentroidsA != None:
            try:
                self.isoCentroidsA.remove()
            except:
                print "IsoPlotA remove failed"

        if len(self.isoTracesA)>0:
            try:
                for peakSet in self.isoTracesA:
                    peakSet.remove()
                self.isoTracesA = []
            except:
                print "PeakSetA remove failed"

    def removeIsoB(self):
        if self.isoCentroidsB != None:
            try:
                self.isoCentroidsB.remove()
            except:
                print "IsoPlotA remove failed"

        if len(self.isoTracesB)>0:
            try:
                for peakSet in self.isoTracesB:
                    peakSet.remove()
                self.isoTracesB = []
            except:
                print "PeakSetB remove failed"

    def calcIsotopeB(self, formula, plotGauss = True):
        '''
        calculates isotope pattern from formula B
        '''
        boolAns, elemList, elemComp = getAtoms(formula)
        print elemList, elemComp
        if boolAns:
            if plotGauss:
                isoAns = isoCalc(elemList, elemComp, charge = self.chargeB.value())
                if isoAns[0]:
                    self.plotWidget.canvas.ax.cla()
                    self.isoCentroidsB = []
                    if not self.formulaA_CB.isChecked():
                        self.isoCentroidsA = []
                        self.isoTracesA = []

                    self.isoCentroidsB.append(isoAns[1][0])
                    self.isoCentroidsB.append(isoAns[1][1])
                    ANS = self.calcGaussIsos(self.isoCentroidsB[0], self.isoCentroidsB[1], self.isoResCalc_SB.value())
                    boolAns, peakListX, peakListY = ANS
                    self.isoTracesB = []
                    if boolAns:
                        for i,peakX in enumerate(peakListX):
                            peakY = peakListY[i]
                            self.isoTracesB.append([peakX, peakY])
                self.plotIsos()
            else:
                print elemList
                print "Element List Wonky"

    def normalize(self, arrayVals):
        if type(arrayVals) is list:
            arrayVals = N.array(arrayVals)

        arrayVals /= arrayVals.max()
        arrayVals != 100
        return arrayVals

    def clearPlot(self):
        self.plotWidget.canvas.ax.cla()
        self.__setupPlot__()
        self.plotWidget.canvas.format_labels()
        self.plotWidget.canvas.draw()
        self.mainTabWidget.setCurrentIndex(1)

    def setupPlotTypes(self):
        self.plotTypes = []
        self.plotTypes.append('Electron Affinities')
        '''
    number -- atomic number
    symbol -- element symbol
    name -- element name in english
    group -- group in the periodic table
    period -- period in the periodic table
    block -- block in the periodic table
    protons -- number of protons
    neutron -- number of neutrons in the most abundant isotope
    electrons -- number of electrons
    mass -- relative atomic mass
    en -- electronegativity (Pauling scale)
    covrad -- Covalent radius (in A)
    atmrad -- Atomic radius (in A)
    vdwrad -- Van der Waals radius (in A)
    tboil -- boiling temperature (in K)
    tmelt -- melting temperature (in K)
    density -- density at 295K (g/cm^3 respectively g/L)
    phase -- 'solid/liquid' or 'gas' at 295K
    acidity -- acidic behaviour
    oxistates -- oxidation states
    eleaffin -- electron affinity (in eV)
    eleshells -- number of electrons per shell
    eleconfig -- ground state electron configuration
    ionenergy -- list of ionization energies (in eV)
    isotopes -- list of isotopes (mass number, rel. atomic mass, fraction)
    maxiso -- index of the most abundant isotope
        '''
        self.plotTypeList.addItems(self.plotTypes)


    def plotEA(self):#plot electronic affinities
        ea = []
        elemList = []
        for elem in TableofElementsList:
            if elemDict.has_key(elem):
                elemList.append(elem)
                ea.append(elemDict[elem].eleaffin)
        self.addPlot(ea, elemList, 'Electron Affinity of the Elements', 'Element #', 'Electron Affinity')


    def addPlot(self, data, dataLabels = None, title = None, xAxisTitle = None, yAxisTitle = None):
        if len(data) != 0:
            subPlot = MPL_Widget()
            subPlot.addPicker()
            if title != None:
                subPlot.setWindowTitle(title)

            ax1 = subPlot.canvas.ax
#            plotTitle = 'EIC from %.2f to %.2f'%(mzLo, mzHi)
#            ax1.set_title(plotTitle)
#            ax1.title.set_fontsize(10)
            if xAxisTitle != None:
                subPlot.canvas.xtitle = xAxisTitle
            if yAxisTitle != None:
                subPlot.canvas.ytitle = yAxisTitle
            if dataLabels != None:
                subPlot.dataLabels = dataLabels
                ax1.plot(data, '-or', alpha = 0.6, picker = 5)
            else:
                ax1.plot(data, '-or', alpha = 0.6)


            subPlot.canvas.format_labels()
            subPlot.show()
            self.openPlotList.append(subPlot)


    def startup(self, dbName = None, startDB = True):

        self.setupPlotTypes()
        self.electronMass = 0.00054858
        self.isoTracesA = []
        self.isoTracesB = []
        self.isoCentroidsA = []
        self.isoCentroidsB = []
#        self.plotWidget.removePicker()

        self.svgWidget = periodicTableWidget()#QtSvg.QSvgWidget('periodicTable.svg')
        self.svgHLayout = QtGui.QHBoxLayout(self.periodTab)
        self.svgHLayout.addWidget(self.svgWidget)
        self.svgHLayout.addWidget(self.elemTableWidget)
        QtCore.QObject.connect(self.svgWidget, QtCore.SIGNAL("elementSelected(PyQt_PyObject)"), self.updateElemData)
        self.updateElemData(elemDict['H'])
        QtCore.QObject.connect(self.calcFormulaA_Btn, QtCore.SIGNAL("clicked()"), self.calcFormulaA)
        QtCore.QObject.connect(self.calcFormulaB_Btn, QtCore.SIGNAL("clicked()"), self.calcFormulaB)
#        QtCore.QObject.connect(self.clearPlotBtn, QtCore.SIGNAL("clicked()"), self.clearPlot)
        QtCore.QObject.connect(self.actionTools, QtCore.SIGNAL("triggered()"),self.__testFunc__)\
#        actionSave_Isotope_Profile_A_to_CSV


    def __testFunc__(self):
        self.plotEA()

#        if RD(self.loVal, self.hiVal, parent = self).exec_():
#            print self.loVal, self.hiVal
#            print "Ok"
#        else:
#            print self.loVal, self.hiVal
#            print "Cancel"

#        print self.curDB.LIST_COLUMNS(self.curDB.LIST_TABLES()[0])
#        print type(self.curDB.LIST_TABLES()[0]), self.curDB.LIST_TABLES()

    def closeOpenWindows(self):
        if len(self.openTableList)>0:
            for table in self.openTableList:
                try:
                    print "Closing %s"%str(table.windowTitle())
                    table.close()
                except:
                    pass
        if len(self.openPlotList)>0:
            for plot in self.openPlotList:
                try:
                    plot.close()
                except:
                    pass



    def __saveDataFile__(self):
        return QtGui.QMessageBox.information(self,'', "This feature is not implemented yet.  Use a database outside of memory")
#        saveFileName = QtGui.QFileDialog.getSaveFileName(self,\
#                                                             self.SaveDataText,\
#                                                             self.__curDir, 'HDF5 File (*.h5);;SQLite Database (*.db)')
#        if saveFileName:
#            if self.curFile:
#                #print "File name is: %s" % (str(self.curFileName))
#                fileType= str(saveFileName).split('.')[-1]
#                if fileType=='h5':
#                    print self.curFile, type(self.curFile)
##                    dbIO.save_XT_HDF5(str(saveFileName),  self.curFile)
#                elif fileType == 'db':
#                    sqldb = dbIO.XT_DB(str(saveFileName), "testTables")#NEED TO FIX THE NAME
#                    sqldb.INSERT_XT_VALUES(sqldb.curTblName, self.curFile)
#                    sqldb.close()
#            else:
#                return QtGui.QMessageBox.information(self,'', "A X!Tandem File must be loaded first before saving")


    def getFNCore(self, filename):
        '''This function parses the filename to get a simple name for the table to be entered into memory and the database'''
        self.sysType = os.sys.platform
        if self.sysType == 'win32':
            fs = filename.split('/')[-1]#fs = file split
            fileCore = fs.split('.')[0]
        else:
            fs = filename.split('/')[-1]#fs = file split
            fileCore = fs.split('.')[0]
        return fileCore



    def getPlotColor(self):
        color = plot_colors[self.plot_num]
        if self.plot_num is len(plot_colors)-1:
            self.plot_num = 0
        else:
            self.plot_num+=1
        return color

    def getPlotMarker(self):
        marker = markers[self.marker_index]
        if self.marker_index is len(markers)-1:
            self.marker_index = 0
        else:
            self.marker_index+=1
        return marker


    def __initContextMenus__(self):
        self.plotWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.plotWidget.connect(self.plotWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.plotTabContext)



    def plotTabContext(self, point):
        '''Create a menu for mainTabWidget'''
        plotCT_menu = QtGui.QMenu("Menu", self.plotWidget)
        plotCT_menu.addAction(self.plotWidget.ZoomToggle)
        plotCT_menu.addAction(self.plotWidget.actionAutoScale)
        #plotCT_menu.addAction(self.actionToggleDraw)
        plotCT_menu.exec_(self.plotWidget.mapToGlobal(point))





    def saveCSVTable(self, tableName = None, saveFileName = None):
        if tableName is None and saveFileName is None:
            saveFileName = QtGui.QFileDialog.getSaveFileName(self,\
                                                     self.SaveDataText,\
                                                     self.__curDir, 'CSV Text File (*.csv)')
            if saveFileName:
                curTbl = str(self.queryTblList.currentItem().text())
                if len(curTbl)>0:
                    self.curDB.DUMP_TABLE(curTbl, saveFileName)
                    self.__curDir = getCurDir(saveFileName)
        else:
            self.curDB.DUMP_TABLE(tableName, saveFileName)
            self.__curDir = getCurDir(saveFileName)


    def getFragSpectrum(self):
        curCol = self.elemTableWidget.currentColumn()
        if self.elemTableWidget.currentItem() == None:
            return False
            #print "Current index: ",  self.elemTableWidget.currentRow(), curCol
        else:
            try:
                curItem = self.elemTableWidget.item(1, 1)
                indexVal = int(curItem.text())
                #indexVal +=-1#this is because we are counting from zero, but the index table counts from 1
                curSeq = self.activeData['pepID'][indexVal]
                xData = self.activeData['xFrags'][indexVal]#this is text and needs to be converted
                yData = self.activeData['yFrags'][indexVal]
                tableText = str(self.elemTableWidget.item(0, 1).text())
                eValText = str(self.activeData['pep_eVal'][indexVal])
                theoMZText = '%.2f'%self.activeData['theoMZ'][indexVal]
                ppmText = '%d'%self.activeData['ppm_error'][indexVal]
                fragTitle = tableText+', '+'Index: '+str(indexVal)+', '+curSeq
                textTag='\n'
                textTag+='e-Val: '
                textTag+= eValText
                textTag+='\n'
                textTag+='m/z: '
                textTag+=theoMZText
                textTag+='\n'
                textTag+='ppm error: '
                textTag+=ppmText

                tempXList = xData.split()
                tempYList = yData.split()
#                print type(tempXList), type(tempYList)
#                print tempXList
                xData = N.array(tempXList, dtype = N.float)#conver to array with dtype set or it will default to string types
                yData = N.array(tempYList, dtype = N.float)
                curFragPlot = FragPlotWidgets.FragPlot(curSeq, xData, yData, title = fragTitle, annotation = textTag)
                curFragPlot.show()
                self.openPlotList.append(curFragPlot)
#                print indexVal
#                print curSeq
#                print xData
#                print yData

#                curType = self.infoMap[str(curItem.text())]
#                curVal = self.curSelectInfo[str(curItem.text())]
#                curTbl = self.curTbl
            except:
                raise

    def showTable(self):
        curItem = self.queryTblList.currentItem()
        if curItem != None:
            curTbl = str(curItem.text())
            if self.dbStatus:
                ok, result, colNames = self.curDB.GET_TABLE(curTbl)
                if ok:
                    self.openTableList.append(DBTable(result, enableSort = True, title = curTbl, colHeaderList = colNames))
                    self.curDBTable = self.openTableList[-1]#append adds to the end of the list so adding the most recent addition

    def __setMessages__(self):
        '''This function is obvious'''
        self.ClearTableText = "Are you sure you want to erase\nthe entire table content?"
        self.ClearAllDataText = "Are you sure you want to erase\nthe entire data set?"
        self.NotEditableText = "Sorry, this data format is not table-editable."
        self.OpenScriptText = "Choose a python script to launch:"
        self.SaveDataText = "Choose a name for the data file to save:"
        self.ScratchSavePrompt = "Choose file name to save the scratch pad:"
        self.OpenDataText = "Choose a data file to open:"
        self.ResetAllDataText = "This operation will reset all your data.\nWould you like to continue?"
        self.EmptyArrayText = "There is no data in the array selected.  Perhaps the search criteria are too stringent.  Check ppm and e-Value cutoff values.\n"

    def __additionalVariables__(self):
        '''Extra variables that are utilized by other functions'''
        self.__curDir = getHomeDir()
        self.firstLoad = True

    def __additionalConnections__(self):
        '''elemTableWidget context menu actions'''
        self.selectDBFieldAction = QtGui.QAction("Select Table By Field", self)
        self.elemTableWidget.addAction(self.selectDBFieldAction)
        QtCore.QObject.connect(self.selectDBFieldAction,QtCore.SIGNAL("triggered()"), self.selectDBField)

        self.saveDBFieldAction = QtGui.QAction("Save New Table By Field", self)
        self.elemTableWidget.addAction(self.saveDBFieldAction)
        QtCore.QObject.connect(self.saveDBFieldAction,QtCore.SIGNAL("triggered()"), self.saveQueryTable)

        '''Database View, Add, Remove Tools'''
        self.removeTableAction = QtGui.QAction("Remove Table from Database", self)
        self.queryTblList.addAction(self.removeTableAction)
        QtCore.QObject.connect(self.removeTableAction, QtCore.SIGNAL("triggered()"), self.removeTable)

        self.dumpTableAction = QtGui.QAction("Save Table to CSV", self)
        self.queryTblList.addAction(self.dumpTableAction)
        QtCore.QObject.connect(self.dumpTableAction, QtCore.SIGNAL("triggered()"), self.saveCSVTable)

        self.showTableAction = QtGui.QAction("Show Table", self)
        self.queryTblList.addAction(self.showTableAction)
        QtCore.QObject.connect(self.showTableAction, QtCore.SIGNAL("triggered()"), self.showTable)

        QtCore.QObject.connect(self.actionSave_All_Tables, QtCore.SIGNAL("triggered()"), self.dumpAllCSVTables)
        QtCore.QObject.connect(self.actionCopy_Current_Database, QtCore.SIGNAL("triggered()"), self.copyCurrentDatabase)

        '''Fragment Display Tools'''
        self.getFragAction = QtGui.QAction("Display Fragment Spectrum", self)
        self.queryTblList.addAction(self.getFragAction)
        QtCore.QObject.connect(self.getFragAction, QtCore.SIGNAL("triggered()"), self.getFragSpectrum)

        '''Plot GUI Interaction slots'''
        QtCore.QObject.connect(self.db_TableList, QtCore.SIGNAL("itemPressed (QListWidgetItem *)"), self.setColLists)
        QtCore.QObject.connect(self.updatePlotBtn, QtCore.SIGNAL("clicked()"), self.updatePlot)
        QtCore.QObject.connect(self.clearPlotBtn, QtCore.SIGNAL("clicked()"), self.clearPlot)

        '''Query GUI slots'''
        QtCore.QObject.connect(self.queryTblList, QtCore.SIGNAL("itemPressed (QListWidgetItem *)"), self.setQueryLists)
        QtCore.QObject.connect(self.dbExecuteQuery,QtCore.SIGNAL("clicked()"),self.executeSQLQuery)
        QtCore.QObject.connect(self.viewQueryBtn,QtCore.SIGNAL("clicked()"),self.viewQueryResults)
        QtCore.QObject.connect(self.dumpDBBtn,QtCore.SIGNAL("clicked()"),self.dumpCurDB)

        self.queryByTypeAction=QtGui.QAction("Query By Type Value",  self)
        self.queryFieldList.addAction(self.queryByTypeAction)
        QtCore.QObject.connect(self.queryByTypeAction,QtCore.SIGNAL("triggered()"), self.queryByType)

        '''Peptide and Protein Query slots'''
        self.uniqePeptidesAction = QtGui.QAction("Get Unique Peptides", self)
        self.queryTblList.addAction(self.uniqePeptidesAction)
        QtCore.QObject.connect(self.uniqePeptidesAction, QtCore.SIGNAL("triggered()"), self.UNIQUE_PEPTIDES)

        self.uniqeProteinsAction = QtGui.QAction("Get Unique Proteins", self)
        self.queryTblList.addAction(self.uniqeProteinsAction)
        QtCore.QObject.connect(self.uniqeProteinsAction, QtCore.SIGNAL("triggered()"), self.UNIQUE_PROTEINS)

        self.uniqePepByProtAction = QtGui.QAction("Get Unique Peptides by Protein", self)
        self.queryTblList.addAction(self.uniqePepByProtAction)
        QtCore.QObject.connect(self.uniqePepByProtAction, QtCore.SIGNAL("triggered()"), self.GROUP_UNIQUE_PEPTIDES_BY_PROTEIN)

        self.uniqeMultiPepAction = QtGui.QAction("Group Unique Peptides Across Tables", self)
        self.queryTblList.addAction(self.uniqeMultiPepAction)
        QtCore.QObject.connect(self.uniqeMultiPepAction, QtCore.SIGNAL("triggered()"), self.MULTI_UNIQUE_PEPTIDE_GROUP)


        '''Database Connection slots'''
        QtCore.QObject.connect(self.openDBButton, QtCore.SIGNAL("clicked()"), self.setDBConnection)
        QtCore.QObject.connect(self.useMemDB_CB, QtCore.SIGNAL("stateChanged (int)"), self.setMemDB)

        QtCore.QObject.connect(self.dbCommitQuery, QtCore.SIGNAL("clicked()"), self.commitFullQuery)


        '''File menu actions slots'''
        QtCore.QObject.connect(self.action_Open,QtCore.SIGNAL("triggered()"),self.__readDataFile__)
        QtCore.QObject.connect(self.actionLoad_Folder,QtCore.SIGNAL("triggered()"),self.__loadDataFolder__)
        QtCore.QObject.connect(self.action_Save,QtCore.SIGNAL("triggered()"),self.__saveDataFile__)
        QtCore.QObject.connect(self.actionFileOpen,QtCore.SIGNAL("triggered()"),self.__readDataFile__)
        QtCore.QObject.connect(self.actionAbout,QtCore.SIGNAL("triggered()"),self.__showAbout__)

        QtCore.QObject.connect(self.actionHints,QtCore.SIGNAL("triggered()"),self.__showHints__)
        QtCore.QObject.connect(self.action_Exit,QtCore.SIGNAL("triggered()"),self.__exitProgram__)

#        QtCore.QObject.connect(self.actionTools, QtCore.SIGNAL("triggered()"),self.__testFunc__)
        #QtCore.QObject.connect(self.MainWindow,QtCore.SIGNAL("close()"),self.__exitProgram__)


        QtCore.QMetaObject.connectSlotsByName(self)#MainWindow)

###########################################################

    def closeEvent(self,  event = None):
        self.closeOpenWindows()
        pass
#        if self.okToExit():
#            self.closeOpenWindows()
#            pass
#        else:
#            event.ignore()
#
#    def resetData(self, dbName = None):
##        self.plotWidget.canvas.ax.cla()
#        if dbName != None:
#            self.startup(dbName = dbName)
#        else:
#            self.startup()
#
#    def __exitProgram__(self):
#        self.close()
#
#    def okToExit(self):
#        #add a question to save memory database to file
#        if self.dbStatus:
#            reply = QtGui.QMessageBox.question(self, "Save Changes & Exit?", "Commit changes to database and exit? Press discard to exit without saving.",\
#                                               QtGui.QMessageBox.Yes|QtGui.QMessageBox.Discard|QtGui.QMessageBox.Cancel)
#            if reply == QtGui.QMessageBox.Yes:
#                if self.dbStatus:
#                    if self.curDB.dbName == ':memory:':
#                        self.copyCurrentDatabase()
#                    self.curDB.cnx.commit()
#                    self.curDB.close()
#                return True
#
#            elif reply == QtGui.QMessageBox.Discard:
#                if self.dbStatus:
#                    self.curDB.close()
#                return True
#
#            elif reply == QtGui.QMessageBox.Cancel:
#                return False
#        else:
#            return False

    def __askConfirm__(self,title,message):
        clickedButton = QtGui.QMessageBox.question(self,\
                                                   title,message,\
                                                   QtGui.QMessageBox.Yes,QtGui.QMessageBox.Cancel)
        if clickedButton == QtGui.QMessageBox.Yes: return True
        return False

    def __showHints__(self):
        return QtGui.QMessageBox.information(self,
                                             ("Hints and known Issues"),
                                             ("<p>1.  Ctrl+Z -- Zoom </p>",
                                              "<p>2.  Ctrl+A -- Autoscale </p>",
                                              "<p>3.  Ctrl+Z -- Copys a png to the clipboard </p>",
                                              "<p>4.  Ctrl+E -- Edit Properties of Graph </p>"


                                              ))

    def __showAbout__(self):
        return QtGui.QMessageBox.information(self,
                                            ("Pysotope v0.8, November, 2009"),
                                            ("<p><b>Pysotope</b> was written in Python by Brian H. Clowers (bhclowers@gmail.com).</p>"
        "<p>Please keep in mind that the entire effort is very much a"
        " work in progress and that Brian won't quit his day job for programming."
        " The original purpose of Pysotope was to provide a user-friendly, open-source tool"
        " for calculating isotope patterns and exploring the periodic table of the elemtns."
        " Please feel free to update Pysotope (preferably with documentation) and please share your contributions"
        " with the rest of the community.</p>"))


def run_main():
    import sys
    app = QtGui.QApplication(sys.argv)
    #MainWindow = QtGui.QMainWindow()
    ui = pysotope()
    ui.show()
    #ui = XTViewer(MainWindow)
    #MainWindow.show()
    sys.exit(app.exec_())


def getCurDir(dirString):
    tempStr = str(dirString)#incase it is a QString
    if os.path.isfile(tempStr):
        return os.path.dirname(tempStr)
    else:
        return os.getcwd()

def valid(path):
    if path and os.path.isdir(path):
        return True
    return False

def env(name):
    return os.environ.get( name, '' )

def getHomeDir():
    if sys.platform != 'win32':
        return os.path.expanduser( '~' )

    homeDir = env( 'USERPROFILE' )
    if not valid(homeDir):
        homeDir = env( 'HOME' )
        if not valid(homeDir) :
            homeDir = '%s%s' % (env('HOMEDRIVE'),env('HOMEPATH'))
            if not valid(homeDir) :
                homeDir = env( 'SYSTEMDRIVE' )
                if homeDir and (not homeDir.endswith('\\')) :
                    homeDir += '\\'
                if not valid(homeDir) :
                    homeDir = 'C:\\'
    return homeDir


if __name__ == "__main__":
    run_main()
