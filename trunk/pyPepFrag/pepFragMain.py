# -------------------------------------------------------------------------
#     Copyright (C) 2008-2010 Martin Strohalm <mmass@biographics.cz>

#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#     GNU General Public License for more details.

#     Complete text of GNU GPL can be found in the file LICENSE in the
#     main directory of the program
# -------------------------------------------------------------------------

import numpy as N
import sys
from PyQt4 import QtGui, QtCore
from mpl_pyqt4_widget import MPL_Widget
from FragPlotWidgets import FragPlot

import configParams as config
import mspy


def doFrag(curSeq):
    """Perform peptide fragmentation."""

    # get fragment types
    serTypeDict = {}
    serTypeDict['a'] = 1
    serTypeDict['b'] = 2
    serTypeDict['y'] = 3
    serTypeDict['-NH3'] = 4
    serTypeDict['-H2O'] = 5
    serTypeDict['c'] = 6
    serTypeDict['x'] = 7
    serTypeDict['z'] = 8
    serTypeDict['int'] = 9
    serTypeDict['int-CO'] = 10
    serTypeDict['int-NH3'] = 11
    serTypeDict['int-H2O'] = 12
    serTypeDict['n-ladder'] = 13
    serTypeDict['c-ladder'] = 14

    series = []
    #series.append('a')
    series.append('b')
    series.append('y')
#    series.append('a-H2O')
#    series.append('b-H2O')
    #series.append('y-H2O')
    #series.append('int')
    i = 0
    serTypeDict = {}
    #config.sequence['fragment']['fragments'].append('a')
    config.sequence['fragment']['fragments'].append('b')
    serTypeDict[config.sequence['fragment']['fragments'][-1]] = i
    i+=1
    config.sequence['fragment']['fragments'].append('y')
    serTypeDict[config.sequence['fragment']['fragments'][-1]] = i
    i+=1
#    config.sequence['fragment']['fragments'].append('a-H2O')
#    serTypeDict[config.sequence['fragment']['fragments'][-1]] = i
#    i+=1
#    config.sequence['fragment']['fragments'].append('b-H2O')
#    serTypeDict[config.sequence['fragment']['fragments'][-1]] = i
#    i+=1
    #config.sequence['fragment']['fragments'].append('y-H2O')
    #config.sequence['fragment']['fragments'].append('int')

#    i = 0
#
#    if 'a' in config.sequence['fragment']['fragments']:
#        series.append('a')
#        serTypeDict['a']=i
#        i+=1
#    if 'b' in config.sequence['fragment']['fragments']:
#        series.append('b')
#        serTypeDict['b'] = i
#        i+=1
#    if 'y' in config.sequence['fragment']['fragments']:
#        series.append('y')
#        serTypeDict['y'] = i
#        i+=1
#    for serie in series[:]:
#        if '-NH3' in config.sequence['fragment']['fragments']:
#            series.append(serie+'-NH3')
#            serTypeDict[serie+'-NH3'] = i
#            i+=1
#        if '-H2O' in config.sequence['fragment']['fragments']:
#            series.append(serie+'-H2O')
#            serTypeDict[serie+'-H2O'] = i
#            i+=1
#
#    if 'c' in config.sequence['fragment']['fragments']:
#        series.append('c')
#        serTypeDict['c'] = i
#        i+=1
#    if 'x' in config.sequence['fragment']['fragments']:
#        series.append('x')
#        serTypeDict['x'] = i
#        i+=1
#    if 'z' in config.sequence['fragment']['fragments']:
#        series.append('z')
#        serTypeDict['z'] = i
#        i+=1
#    if 'int' in config.sequence['fragment']['fragments']:
#        series.append('int')
#        serTypeDict['int'] = i
#        i+=1
#        series.append('int-CO')
#        serTypeDict['int-CO'] = i
#        i+=1
#        series.append('int-NH3')
#        serTypeDict['int-NH3'] = i
#        i+=1
#        series.append('int-H2O')
#        serTypeDict['int-H2O'] = i
#        i+=1
#
#    if 'n-ladder' in config.sequence['fragment']['fragments']:
#        series.append('n-ladder')
#        serTypeDict['n-ladder'] = i
#        i+=1
#
#    if 'c-ladder' in config.sequence['fragment']['fragments']:
#        series.append('c-ladder')
#        serTypeDict['c-ladder'] = i
#        i+=1


    # fragment sequence
    fragments = []
    for serie in series:
        fragments += mspy.fragment(curSeq, serie)

    # variate mods
    variants = []
    for fragment in fragments:
        variants += mspy.variateMods(fragment, position=False, maxMods=config.sequence['fragment']['maxMods'])
    fragments = variants

    # get max charge and polarity
    polarity = 1
    if config.sequence['fragment']['maxCharge'] < 0:
        polarity = -1
    maxCharge = abs(config.sequence['fragment']['maxCharge'])+1

    # calculate mz and check limits
    curFrags = []
    for i,fragment in enumerate(fragments):
        for z in range(1, maxCharge):
            if not config.sequence['fragment']['filterFragments'] or not fragment.fragFiltered:
                curFrags.append([
                    serTypeDict[str(fragment.fragmentSerie)],
                    fragment.fragmentSerie,
                    fragment.fragmentIndex,
                    fragment.userRange,
                    fragment.getMZ(z*polarity)[config.sequence['fragment']['massType']],
                    z*polarity,
                    fragment.getFormated(config.sequence['fragment']['listFormat']),
                    None,
                    fragment,
                    [],
                ])

#    print serTypeDict
    return curFrags, series
# ----


def pepFrag(seq, X, Y, plotCanvas):

#    w = MPL_Widget(enableAutoScale = False, doublePlot = True, enableEdit = True)
    ax1 = plotCanvas.ax1
    ax2 = plotCanvas.ax2

    pep = seq
    mz = X
    yVals = Y

    sortInd = X.argsort()
    X = X[sortInd]
    Y = Y[sortInd]


    curSeq = mspy.sequence(pep)
    ans, series = doFrag(curSeq)
    fragType = []
    fragMZ = []

    for i, item in enumerate(ans):
        fragType.append(ans[i][0])
        fragMZ.append(ans[i][4])
#        print item

    fragMZ = N.array(fragMZ)
    fragMZ.sort()
    fragType = N.array(fragType)
    fragYVals = N.zeros_like(fragMZ)
    fragYVals+=1#scale to 100

    absTol = 2000#ppm
    ppmErrs = []
    for i,frag in enumerate(fragMZ):
        foundInd = mz.searchsorted(frag)

        if foundInd == 0:
            prevInd = 0
        else:
            prevInd = foundInd-1

        if foundInd >= len(mz):
            foundInd+=-1
            prevInd+=-1


#        print len(mz), foundInd, prevInd
        foundMZ = X[foundInd]
        prevMZ = X[prevInd]
        foundDiff = N.abs(foundMZ-frag)
        prevDiff = N.abs(prevMZ-frag)
        foundDiffOk = foundDiff < (foundMZ*absTol*1E-6)
        prevDiffOk = prevDiff < (prevMZ*absTol*1E-6)

        if foundDiffOk and prevDiffOk:
            if foundDiff < prevDiff:
                ppmErrs.append([frag, foundDiff/frag*1E6])
                fragYVals[i] = Y[foundInd]
            else:
                ppmErrs.append([frag, prevDiff/frag*1E6])
                fragYVals[i] = Y[prevInd]
        elif foundDiffOk:
            ppmErrs.append([frag, foundDiff/frag*1E6])
            fragYVals[i] = Y[foundInd]
        elif prevDiffOk:
            ppmErrs.append([frag, prevDiff/frag*1E6])
            fragYVals[i] = Y[prevInd]

    ax1.vlines(X, 0, Y, colors = 'k', alpha = 0.4)
    for frag in fragType:
        fragInd = N.where(fragType == frag)[0]
        tempFrag = fragMZ[fragInd]
        tempInt = fragYVals[fragInd]
        ax1.vlines(tempFrag, 0, tempInt, colors = COLORS[frag], linestyles = 'solid', alpha = 0.8)#
#    ax1.legend()#legend is broken in mpl 0.98.5
    i = 1
    ppmErrs = N.array(ppmErrs)
    errs = ppmErrs[:,1]
    errY = N.arange(len(errs))
    errY+=1
    ax2.plot(errs, errY, 'go', alpha = 0.6)

    ax2.axvline(ymax = errY.max(), color = 'k', ls = '--')
    ax2.set_xlim(xmin = N.abs(errs.max())*-1.1, xman = N.abs(errs.max())*1.1)
    ax1.text(0.03, 0.95, seq, fontsize=7,\
            bbox=dict(facecolor='yellow', alpha=0.1),\
            transform=ax1.transAxes, va='top')
    plotCanvas.format_labels()
    plotCanvas.draw()

if __name__ == "__main__":
    import numpy as N
    import pylab as P
    import sys
    from PyQt4 import QtGui, QtCore
    from mpl_pyqt4_widget import MPL_Widget
    import xtandem_parser_class as XTParser

    COLORS = ['#297AA3','#A3293D','#3B9DCE','#293DA3','#5229A3','#8F29A3','#A3297A',
    '#7AA329','#3DA329','#29A352','#29A38F','#A38F29','#3B9DCE','#6CB6DA','#CE6C3B','#DA916C',
    '#0080FF','#0000FF','#7ABDFF','#8000FF','#FF0080','#FF0000','#FF8000','#FFFF00','#A35229','#80FF00',
    '#00FF00','#00FF80','#00FFFF','#3D9EFF','#FF9E3D','#FFBD7A']

    app = QtGui.QApplication(sys.argv)

    XT = XTParser.XT_RESULTS('XTTest.xml')
    selInd = XT.dataDict['pep_eVal'].argsort()
    firstInd = selInd[0]
    secondInd = selInd[1]
    topInd = selInd[30:33]

    for ind in topInd:
        print XT.dataDict['pep_eVal'][ind]
        seq = XT.dataDict['pepID'][ind]
        X = XT.dataDict['xFrags'][ind]
        Y = XT.dataDict['yFrags'][ind]
        pepFrag(seq, X, Y)

#    mz = N.array([360.051, 371.971, 408.168, 475.257, 572.221, 592.733, 595.249, 605.034, 623.413, 635.276, 642.189,
#          643.776, 648.206, 683.262, 690.683, 692.273, 700.84, 716.189, 719.344, 736.303, 749.344, 763.286,
#          778.233, 780.335, 793.199, 798.8, 800.332, 812.339, 820.361, 847.438, 865.363, 866.429, 922.456,
#          927.432, 959.562, 976.43, 993.534, 1092.5, 1124.54, 1140.53, 1166.53, 1171.66, 1190.57, 1268.53,
#          1270.57, 1280.47, 1286.69, 1298.55, 1387.6, 1401.68])
#    yVals = N.array([6, 14, 6, 6, 5, 7, 14, 4, 4, 12, 8, 100, 5, 5, 5, 10, 57, 5, 8, 21, 7, 5, 5, 4, 5, 5, 6, 12, 48, 6,
#                     10, 5, 7, 9, 4, 22, 10, 5, 6, 4, 9, 6, 23, 5, 7, 4, 90, 9, 4, 7])

    sys.exit(app.exec_())

###############Original mMass Code#########################
#    def doDigestion(self):
#        """Perform protein digest."""
#
#        # digest sequence
#        peptides = mspy.digest(self.currentSequence, config.sequence['digest']['enzyme'], miscleavage=config.sequence['digest']['miscl'], allowMods=config.sequence['digest']['allowMods'], strict=False)
#
#        # do not cleave if modified
#        enzyme=config.sequence['digest']['enzyme']
#        if config.sequence['digest']['allowMods']:
#            enzyme = None
#
#        # get variations for each peptide
#        variants = []
#        for peptide in peptides:
#            variants += mspy.variateMods(peptide, position=False, maxMods=config.sequence['digest']['maxMods'], enzyme=enzyme)
#        peptides = variants
#
#        # get max charge and polarity
#        polarity = 1
#        if config.sequence['digest']['maxCharge'] < 0:
#            polarity = -1
#        maxCharge = abs(config.sequence['digest']['maxCharge'])+1
#
#        # calculate mz and check limits
#        self.currentDigest = []
#        for peptide in peptides:
#            for z in range(1, maxCharge):
#                mz = peptide.getMZ(z*polarity)[config.sequence['digest']['massType']]
#                if mz >= config.sequence['digest']['lowMass'] and mz <= config.sequence['digest']['highMass']:
#                    self.currentDigest.append([
#                        peptide.userRange,
#                        peptide.miscleavages,
#                        mz,
#                        z*polarity,
#                        peptide.getFormated(config.sequence['digest']['listFormat']),
#                        None,
#                        peptide,
#                        [],
#                    ])
#    # ----
#
#
#    def doFragmentation(self):
#        """Perform peptide fragmentation."""
#
#        # get fragment types
#        series = []
#
#        if 'a' in config.sequence['fragment']['fragments']:
#            series.append('a')
#        if 'b' in config.sequence['fragment']['fragments']:
#            series.append('b')
#        if 'y' in config.sequence['fragment']['fragments']:
#            series.append('y')
#
#        for serie in series[:]:
#            if '-NH3' in config.sequence['fragment']['fragments']:
#                series.append(serie+'-NH3')
#            if '-H2O' in config.sequence['fragment']['fragments']:
#                series.append(serie+'-H2O')
#
#        if 'c' in config.sequence['fragment']['fragments']:
#            series.append('c')
#        if 'x' in config.sequence['fragment']['fragments']:
#            series.append('x')
#        if 'z' in config.sequence['fragment']['fragments']:
#            series.append('z')
#        if 'int' in config.sequence['fragment']['fragments']:
#            series.append('int')
#            series.append('int-CO')
#            series.append('int-NH3')
#            series.append('int-H2O')
#        if 'n-ladder' in config.sequence['fragment']['fragments']:
#            series.append('n-ladder')
#        if 'c-ladder' in config.sequence['fragment']['fragments']:
#            series.append('c-ladder')
#
#        # fragment sequence
#        fragments = []
#        for serie in series:
#            fragments += mspy.fragment(self.currentSequence, serie)
#
#        # variate mods
#        variants = []
#        for fragment in fragments:
#            variants += mspy.variateMods(fragment, position=False, maxMods=config.sequence['fragment']['maxMods'])
#        fragments = variants
#
#        # get max charge and polarity
#        polarity = 1
#        if config.sequence['fragment']['maxCharge'] < 0:
#            polarity = -1
#        maxCharge = abs(config.sequence['fragment']['maxCharge'])+1
#
#        # calculate mz and check limits
#        self.currentFragments = []
#        for fragment in fragments:
#            for z in range(1, maxCharge):
#                if not config.sequence['fragment']['filterFragments'] or not fragment.fragFiltered:
#                    self.currentFragments.append([
#                        fragment.fragmentSerie,
#                        fragment.fragmentIndex,
#                        fragment.userRange,
#                        fragment.getMZ(z*polarity)[config.sequence['fragment']['massType']],
#                        z*polarity,
#                        fragment.getFormated(config.sequence['fragment']['listFormat']),
#                        None,
#                        fragment,
#                        [],
#                    ])
#    # ----
#
#
#    def doSearch(self):
#        """Perform mass search."""
#
#        # get max charge and polarity
#        polarity = 1
#        if config.sequence['search']['maxCharge'] < 0:
#            polarity = -1
#        maxCharge = abs(config.sequence['search']['maxCharge'])+1
#
#        # search sequence
#        self.currentSearch = []
#        for z in range(1, maxCharge):
#            charge = z*polarity
#            peptides = mspy.searchSequence(self.currentSequence, config.sequence['search']['mass'], charge, tolerance=config.sequence['search']['tolerance'], enzyme=config.sequence['search']['enzyme'], tolUnits=config.sequence['search']['units'], massType=config.sequence['search']['massType'], maxMods=config.sequence['search']['maxMods'])
#            for peptide in peptides:
#                mz = peptide.getMZ(charge)[config.sequence['search']['massType']]
#                self.currentSearch.append([
#                    peptide.userRange,
#                    mz,
#                    charge,
#                    peptide.getFormated(config.sequence['search']['listFormat']),
#                    mspy.delta(mz, config.sequence['search']['mass'], config.sequence['search']['units']),
#                    peptide,
#                ])



