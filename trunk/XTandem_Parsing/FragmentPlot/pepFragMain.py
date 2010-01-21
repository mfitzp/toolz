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

import configParams as configP
import mspy

COLORS = ['#297AA3','#A3293D','#3B9DCE','#293DA3','#5229A3','#8F29A3','#A3297A',
'#7AA329','#3DA329','#29A352','#29A38F','#A38F29','#3B9DCE','#6CB6DA','#CE6C3B','#DA916C',
'#0080FF','#0000FF','#7ABDFF','#8000FF','#FF0080','#FF0000','#FF8000','#FFFF00','#A35229','#80FF00',
'#00FF00','#00FF80','#00FFFF','#3D9EFF','#FF9E3D','#FFBD7A']


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
    series.append('a')
    series.append('b')
    series.append('y')
    series.append('a-H2O')
    series.append('b-H2O')
    series.append('y-H2O')
    #series.append('int')
    i = 0
    serTypeDict = {}
    configP.sequence['fragment']['fragments'].append('a')
    serTypeDict[configP.sequence['fragment']['fragments'][-1]] = i
    i+=1
    configP.sequence['fragment']['fragments'].append('b')
    serTypeDict[configP.sequence['fragment']['fragments'][-1]] = i
    i+=1
    configP.sequence['fragment']['fragments'].append('y')
    serTypeDict[configP.sequence['fragment']['fragments'][-1]] = i
    i+=1
    configP.sequence['fragment']['fragments'].append('a-H2O')
    serTypeDict[configP.sequence['fragment']['fragments'][-1]] = i
    i+=1
    configP.sequence['fragment']['fragments'].append('b-H2O')
    serTypeDict[configP.sequence['fragment']['fragments'][-1]] = i
    i+=1
    configP.sequence['fragment']['fragments'].append('y-H2O')
    serTypeDict[configP.sequence['fragment']['fragments'][-1]] = i
    i+=1

#    print serTypeDict
#    configP.sequence['fragment']['fragments'].append('int')

#    i = 0
#
#    if 'a' in configP.sequence['fragment']['fragments']:
#        series.append('a')
#        serTypeDict['a']=i
#        i+=1
#    if 'b' in configP.sequence['fragment']['fragments']:
#        series.append('b')
#        serTypeDict['b'] = i
#        i+=1
#    if 'y' in configP.sequence['fragment']['fragments']:
#        series.append('y')
#        serTypeDict['y'] = i
#        i+=1
#    for serie in series[:]:
#        if '-NH3' in configP.sequence['fragment']['fragments']:
#            series.append(serie+'-NH3')
#            serTypeDict[serie+'-NH3'] = i
#            i+=1
#        if '-H2O' in configP.sequence['fragment']['fragments']:
#            series.append(serie+'-H2O')
#            serTypeDict[serie+'-H2O'] = i
#            i+=1
#
#    if 'c' in configP.sequence['fragment']['fragments']:
#        series.append('c')
#        serTypeDict['c'] = i
#        i+=1
#    if 'x' in configP.sequence['fragment']['fragments']:
#        series.append('x')
#        serTypeDict['x'] = i
#        i+=1
#    if 'z' in configP.sequence['fragment']['fragments']:
#        series.append('z')
#        serTypeDict['z'] = i
#        i+=1
#    if 'int' in configP.sequence['fragment']['fragments']:
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
#    if 'n-ladder' in configP.sequence['fragment']['fragments']:
#        series.append('n-ladder')
#        serTypeDict['n-ladder'] = i
#        i+=1
#
#    if 'c-ladder' in configP.sequence['fragment']['fragments']:
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
        variants += mspy.variateMods(fragment, position=False, maxMods=configP.sequence['fragment']['maxMods'])
    fragments = variants

    # get max charge and polarity
    polarity = 1
    if configP.sequence['fragment']['maxCharge'] < 0:
        polarity = -1
    maxCharge = abs(configP.sequence['fragment']['maxCharge'])+1

    # calculate mz and check limits
    curFrags = []
    for i,fragment in enumerate(fragments):
        for z in range(1, maxCharge):
            if not configP.sequence['fragment']['filterFragments'] or not fragment.fragFiltered:
                curFrags.append([
                    serTypeDict[str(fragment.fragmentSerie)],
                    fragment.fragmentSerie,
                    fragment.fragmentIndex,
                    fragment.userRange,
                    fragment.getMZ(z*polarity)[configP.sequence['fragment']['massType']],
                    z*polarity,
                    fragment.getFormated(configP.sequence['fragment']['listFormat']),
                    None,
                    fragment,
                    [],
                ])

#    print serTypeDict
    return curFrags, series
# ----


def pepFrag(seq, X, Y, plotCanvas, annotation = None):

#    w = MPL_Widget(enableAutoScale = False, doublePlot = True, enableEdit = True)
    ax1 = plotCanvas.ax
    ax2 = plotCanvas.ax2

    pep = seq
    mz = X
    yVals = Y

    sortInd = X.argsort()
    X = X[sortInd]
    Y = Y[sortInd]


    curSeq = mspy.sequence(pep)
    ans, series = doFrag(curSeq)
    fragRange = N.arange(len(series))
    fragType = []
    fragMZ = []

#    print "Series: ", series

#    for val in ans:
#        print val

    for i, item in enumerate(ans):
        fragType.append(ans[i][0])
        fragMZ.append(ans[i][4])
#        print item

    fragMZ = N.array(fragMZ)
    fragType = N.array(fragType)
    fragMZInd = fragMZ.argsort()
    fragMZ = fragMZ[fragMZInd]
    fragType = fragType[fragMZInd]
    fragYVals = N.zeros_like(fragMZ)
    fragYVals+=1#

    absTol = 3000#ppm
    ppmErrs = []
    ppmErrType = []
    for i,frag in enumerate(fragMZ):
        foundInd = X.searchsorted(frag)

        if foundInd == 0:
            prevInd = 0
        else:
            prevInd = foundInd-1

        if foundInd >= len(X):
            foundInd+=-1
            prevInd+=-1

        if foundInd < 0:
            foundInd = 0
        if prevInd < 0:
            prevInd = 0

#        print len(mz), foundInd, prevInd
        foundMZ = X[foundInd]
        prevMZ = X[prevInd]
        foundDiff = foundMZ-frag
        prevDiff = prevMZ-frag
        foundDiffOk = N.abs(foundDiff) < (foundMZ*absTol*1E-6)
        prevDiffOk = N.abs(prevDiff) < (prevMZ*absTol*1E-6)

        if foundDiffOk and prevDiffOk:
            if N.abs(foundDiff) < N.abs(prevDiff):
                ppmErrs.append([frag, foundDiff/frag*1E6])
                ppmErrType.append(fragType[i])
                fragYVals[i] = Y[foundInd]
            else:
                ppmErrs.append([frag, prevDiff/frag*1E6])
                ppmErrType.append(fragType[i])
                fragYVals[i] = Y[prevInd]
        elif foundDiffOk:
            ppmErrs.append([frag, foundDiff/frag*1E6])
            ppmErrType.append(fragType[i])
            fragYVals[i] = Y[foundInd]
        elif prevDiffOk:
            ppmErrs.append([frag, prevDiff/frag*1E6])
            ppmErrType.append(fragType[i])
            fragYVals[i] = Y[prevInd]

    #plot the lines for each spectrum before being matched
    ax1.vlines(X, 0, Y, colors = 'k', alpha = 1.0)#0.6)



    m = 1
    ppmErrType = N.array(ppmErrType)
    ppmErrs = N.array(ppmErrs)
    errs = ppmErrs[:,1]
    errY = N.arange(len(errs))
    errY+=1
#    ax2.plot(errs, errY, 'go', ms = 5, alpha = 0.6)

    tempColors = ['r', 'b', 'g', 'y', 'm', 'b', 'k']
    tempMarkers = ['o','s','d','^', 'h', 'p', 'o', 'd', 's']
    n = 1
    for m,frag in enumerate(fragRange):
        fragInd = N.where(fragType == frag)[0]
        tempFrag = fragMZ[fragInd]

        errInd = N.where(ppmErrType == frag)[0]
        tempErrs = errs[errInd]
        tempErrY = N.arange(n,len(tempErrs)+n)
        n+=len(tempErrs)
        ax2.plot(tempErrs, tempErrY, linestyle = 'None', marker = tempMarkers[frag], color = tempColors[frag], ms = 5, alpha = 0.6)
#        print frag, tempFrag
        tempInt = fragYVals[fragInd]
        ax1.vlines(tempFrag, 0, tempInt, colors = tempColors[frag], linestyles = 'solid', alpha = 0.8)#
#    ax1.legend()#legend is broken in mpl 0.98.5


#    ax2.axvline(ymax = errY.max(), color = 'k', ls = '--')
#    ax2.set_xlim(xmin = N.abs(errs.max())*-1.1, xman = N.abs(errs.max())*1.1)

    errMax = n-len(tempErrs)+1
    ax2.axvline(ymax = errMax, color = 'k', ls = '--')
    ax2.set_xlim(xmin = N.abs(errs).max()*-1.1, xman = N.abs(errs).max()*1.1)
    ax2.set_ylim(ymin = 0, yman = errMax)


    if annotation != None:
        textTag = seq+annotation
    else:
        textTag = seq

    ax1.text(0.03, 0.95, textTag, fontsize=10,\
            bbox=dict(facecolor='yellow', alpha=0.1),\
            transform=ax1.transAxes, va='top')


    matchedInd = N.where(fragYVals>1)[0]
    labelPeaks(fragMZ[matchedInd], fragYVals[matchedInd], ax1, yCutoff = 10)

    plotCanvas.format_labels()
    plotCanvas.draw()


def labelPeaks(xVals, yVals, mplAxis, yCutoff = 1):
    if len(xVals)>0:
        yMax = yVals.max()
        yIncrement = yMax*0.01
        mplAxis.set_ylim(ymax = yMax*1.1)
        for i, xVal in enumerate(xVals):
            if yVals[i]>yCutoff:
                showText = '%.2f'%(xVal)
                mplAxis.text(xVal,yVals[i]+yIncrement, showText, fontsize=7, rotation = 90)


def mainA():
    import numpy as N
    import pylab as P
    import sys
    from PyQt4 import QtGui, QtCore
    from mpl_pyqt4_widget import MPL_Widget
    import xtandem_parser_class as XTParser

    app = QtGui.QApplication(sys.argv)

    XT = XTParser.XT_RESULTS('../XTTest.xml')
    selInd = XT.dataDict['pep_eVal'].argsort()
    firstInd = selInd[0]
    secondInd = selInd[1]
    topInd = selInd[30:33]

    w = MPL_Widget(enableAutoScale = False, doublePlot = True, enableEdit = True)

    ind = 53
#    for ind in topInd:
#        print XT.dataDict['pep_eVal'][ind]
    seq = XT.dataDict['pepID'][ind]
    X = XT.dataDict['xFrags'][ind]
    Y = XT.dataDict['yFrags'][ind]
    X = X.split()
    Y = Y.split()
#        print type(X), type(Y)
    X = N.array(X, dtype = N.float)#conver to array with dtype set or it will default to string types
    Y = N.array(Y, dtype = N.float)
#    print type(X), type(Y)
    pepFrag(seq, X, Y, w.canvas)
    w.show()
    sys.exit(app.exec_())


def mainB():
    import numpy as N
    import pylab as P
    import scipy as S
    import sys
    from PyQt4 import QtGui, QtCore
    from mpl_pyqt4_widget import MPL_Widget
    app = QtGui.QApplication(sys.argv)
    w = MPL_Widget(enableAutoScale = False, doublePlot = True, enableEdit = True)
    #seq = 'ANTHRACISAMES'
    seq = 'ANTHRACISSTERNE'
    #X = P.load('amesPredicted.csv', delimiter = ',')
    X = P.load('sternePredicted.csv', delimiter = ',')
    Y = S.rand(len(X))
    Y*=10
    randInt = []
    for i in xrange(int(0.25*len(X))):
        ind = N.random.random_integers(len(Y)-1)
        Y[ind] = N.random.random_integers(10)*10

    Y/=Y.max()
    Y*=100
#    X = N.array(X, dtype = N.float)#conver to array with dtype set or it will default to string types
#    Y = N.array(Y, dtype = N.float)
#    print type(X), type(Y)
    pepFrag(seq, X, Y, w.canvas)
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    mainB()


#    mz = N.array([360.051, 371.971, 408.168, 475.257, 572.221, 592.733, 595.249, 605.034, 623.413, 635.276, 642.189,
#          643.776, 648.206, 683.262, 690.683, 692.273, 700.84, 716.189, 719.344, 736.303, 749.344, 763.286,
#          778.233, 780.335, 793.199, 798.8, 800.332, 812.339, 820.361, 847.438, 865.363, 866.429, 922.456,
#          927.432, 959.562, 976.43, 993.534, 1092.5, 1124.54, 1140.53, 1166.53, 1171.66, 1190.57, 1268.53,
#          1270.57, 1280.47, 1286.69, 1298.55, 1387.6, 1401.68])
#    yVals = N.array([6, 14, 6, 6, 5, 7, 14, 4, 4, 12, 8, 100, 5, 5, 5, 10, 57, 5, 8, 21, 7, 5, 5, 4, 5, 5, 6, 12, 48, 6,
#                     10, 5, 7, 9, 4, 22, 10, 5, 6, 4, 9, 6, 23, 5, 7, 4, 90, 9, 4, 7])



###############Original mMass Code#########################
#    def doDigestion(self):
#        """Perform protein digest."""
#
#        # digest sequence
#        peptides = mspy.digest(self.currentSequence, configP.sequence['digest']['enzyme'], miscleavage=configP.sequence['digest']['miscl'], allowMods=configP.sequence['digest']['allowMods'], strict=False)
#
#        # do not cleave if modified
#        enzyme=configP.sequence['digest']['enzyme']
#        if configP.sequence['digest']['allowMods']:
#            enzyme = None
#
#        # get variations for each peptide
#        variants = []
#        for peptide in peptides:
#            variants += mspy.variateMods(peptide, position=False, maxMods=configP.sequence['digest']['maxMods'], enzyme=enzyme)
#        peptides = variants
#
#        # get max charge and polarity
#        polarity = 1
#        if configP.sequence['digest']['maxCharge'] < 0:
#            polarity = -1
#        maxCharge = abs(configP.sequence['digest']['maxCharge'])+1
#
#        # calculate mz and check limits
#        self.currentDigest = []
#        for peptide in peptides:
#            for z in range(1, maxCharge):
#                mz = peptide.getMZ(z*polarity)[configP.sequence['digest']['massType']]
#                if mz >= configP.sequence['digest']['lowMass'] and mz <= configP.sequence['digest']['highMass']:
#                    self.currentDigest.append([
#                        peptide.userRange,
#                        peptide.miscleavages,
#                        mz,
#                        z*polarity,
#                        peptide.getFormated(configP.sequence['digest']['listFormat']),
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
#        if 'a' in configP.sequence['fragment']['fragments']:
#            series.append('a')
#        if 'b' in configP.sequence['fragment']['fragments']:
#            series.append('b')
#        if 'y' in configP.sequence['fragment']['fragments']:
#            series.append('y')
#
#        for serie in series[:]:
#            if '-NH3' in configP.sequence['fragment']['fragments']:
#                series.append(serie+'-NH3')
#            if '-H2O' in configP.sequence['fragment']['fragments']:
#                series.append(serie+'-H2O')
#
#        if 'c' in configP.sequence['fragment']['fragments']:
#            series.append('c')
#        if 'x' in configP.sequence['fragment']['fragments']:
#            series.append('x')
#        if 'z' in configP.sequence['fragment']['fragments']:
#            series.append('z')
#        if 'int' in configP.sequence['fragment']['fragments']:
#            series.append('int')
#            series.append('int-CO')
#            series.append('int-NH3')
#            series.append('int-H2O')
#        if 'n-ladder' in configP.sequence['fragment']['fragments']:
#            series.append('n-ladder')
#        if 'c-ladder' in configP.sequence['fragment']['fragments']:
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
#            variants += mspy.variateMods(fragment, position=False, maxMods=configP.sequence['fragment']['maxMods'])
#        fragments = variants
#
#        # get max charge and polarity
#        polarity = 1
#        if configP.sequence['fragment']['maxCharge'] < 0:
#            polarity = -1
#        maxCharge = abs(configP.sequence['fragment']['maxCharge'])+1
#
#        # calculate mz and check limits
#        self.currentFragments = []
#        for fragment in fragments:
#            for z in range(1, maxCharge):
#                if not configP.sequence['fragment']['filterFragments'] or not fragment.fragFiltered:
#                    self.currentFragments.append([
#                        fragment.fragmentSerie,
#                        fragment.fragmentIndex,
#                        fragment.userRange,
#                        fragment.getMZ(z*polarity)[configP.sequence['fragment']['massType']],
#                        z*polarity,
#                        fragment.getFormated(configP.sequence['fragment']['listFormat']),
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
#        if configP.sequence['search']['maxCharge'] < 0:
#            polarity = -1
#        maxCharge = abs(configP.sequence['search']['maxCharge'])+1
#
#        # search sequence
#        self.currentSearch = []
#        for z in range(1, maxCharge):
#            charge = z*polarity
#            peptides = mspy.searchSequence(self.currentSequence, configP.sequence['search']['mass'], charge, tolerance=configP.sequence['search']['tolerance'], enzyme=configP.sequence['search']['enzyme'], tolUnits=configP.sequence['search']['units'], massType=configP.sequence['search']['massType'], maxMods=configP.sequence['search']['maxMods'])
#            for peptide in peptides:
#                mz = peptide.getMZ(charge)[configP.sequence['search']['massType']]
#                self.currentSearch.append([
#                    peptide.userRange,
#                    mz,
#                    charge,
#                    peptide.getFormated(configP.sequence['search']['listFormat']),
#                    mspy.delta(mz, configP.sequence['search']['mass'], configP.sequence['search']['units']),
#                    peptide,
#                ])



