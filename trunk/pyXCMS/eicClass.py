import sys, traceback

import numpy as N
import rpy2.robjects as ro
import rpy2.rinterface as ri
import tables as T
import numpy as N

import time

class EIC:
    def __init__(self, eicRInstance = None,
                 names = None,#should be a list of names
                 mzLo = None,
                 mzHi = None,
                 xData = None,#this should be list numpy arrays
                 yData = None):
        '''
        groupnames   signature(object = "xcmsEIC"): get groupnames slot
        mzrange      signature(object = "xcmsEIC"): get mzrange slot
        plot         signature(x = "xcmsEIC"): plot the extracted ion chromatograms
        rtrange      signature(object = "xcmsEIC"): get rtrange slot
        sampnames    signature(object = "xcmsEIC"): get sample names
        '''
#        self.names = []
#        self.mzLo = mzLo
#        self.mzHi = mzHi
        self.eicTraces = []
        self.numEICs = 0
        self.filePath = None
#        self.eicGroups = {}
        t1 = time.clock()

        if eicRInstance != None:
            self.eicRInstance = eicRInstance
            self.mzRanges = N.asarray(ro.r.mzrange(self.eicRInstance))
            self.rtRanges = N.asarray(ro.r.rtrange(self.eicRInstance))
            self.groupNames = ro.r.groupnames(self.eicRInstance)
            self.names = ro.r.sampnames(self.eicRInstance)
            self.eics = self.eicRInstance.eic
            for i,group in enumerate(self.groupNames):
                curMZRange = self.mzRanges[i]
                curRT = self.rtRanges[i]
                metaDict = {'mzlo': curMZRange[0],'mzhi': curMZRange[1],
                            'rtlo': curRT[0],'rthi':curRT[1]}
                dataDict = {}
                for j,name in enumerate(self.names):
                    curEic = self.eics[j]
                    curEic = N.asarray(curEic[i])
                    dataDict[name] =  {'xdata':curEic[:,0],\
                                       'ydata':curEic[:,1]}
                curGroupDict = {}
                curGroupDict[group] = [metaDict, dataDict]
                self.eicTraces.append(curGroupDict)
            self.numEICs = len(self.eicTraces)
            print "EIC Create Time: ", time.clock() - t1

    def save2HDF5(self, fileName):
        try:
            hdf = T.openFile(fileName, mode = "w", title = 'XCMS EIC Data File')
            filters = T.Filters(complevel=5, complib='zlib')
            atom = T.FloatAtom()
            for peakGroup in self.eicTraces:#self.eicTraces is a list
                gName = peakGroup.keys()[0]
                pGroup = hdf.createGroup("/", '%s'%gName, '%s Group'%gName)
                gList = peakGroup.values()[0]
                gMetaDict = gList[0]
                gDataDict = gList[1]
                pGroup._f_setAttr('mzlo',gMetaDict['mzlo'])
                pGroup._f_setAttr('mzhi',gMetaDict['mzhi'])
                pGroup._f_setAttr('rtlo',gMetaDict['rtlo'])
                pGroup._f_setAttr('rthi',gMetaDict['rthi'])
                for dataKey in gDataDict.iterkeys():
                    xData = gDataDict[dataKey]['xdata']
                    yData = gDataDict[dataKey]['ydata']
                    d2Write = N.column_stack((xData,yData))
                    shape = d2Write.shape
                    ca = hdf.createCArray(pGroup, dataKey, atom, shape,  filters = filters)
                    ca[0:shape[0]] = d2Write
                    #ca.flush()

            hdf.close()
        except:
            hdf.close()
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
#                    print 'Error saving figure data'
            errorMsg = "Sorry XCMS Data Not Saved: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
            print errorMsg

    def loadHDF5(self, fileName):
        try:
            eicTraces = []
            mzList = []
            hdf = T.openFile(fileName, mode = "r")
            rt = hdf.root
            groups = rt._v_groups
            for gKey in groups.iterkeys():#self.eicTraces is a list
    #            gName = groups[peakGrouppeakGroup.keys()[0]
                pGroup = groups[gKey]
                mzlo = pGroup._v_attrs.mzlo
                mzhi = pGroup._v_attrs.mzhi
                rtlo = pGroup._v_attrs.rtlo
                rthi = pGroup._v_attrs.rthi
                mzList.append(mzlo)#this is needed to sort the list appropriately
                metaDict = {'mzlo': mzlo,'mzhi': mzhi,'rtlo': rtlo,'rthi':rthi}
                eicDict = pGroup._v_children
                dataDict = {}
                for dkey in eicDict.iterkeys():
                    numData = eicDict[dkey].read()
                    dataDict[dkey] = {'xdata':numData[:,0],\
                                      'ydata':numData[:,1]}
                curGroupDict = {}
                curGroupDict[gKey] = [metaDict, dataDict]
                eicTraces.append(curGroupDict)
            mzList = N.array(mzList)
            mzOrder = mzList.argsort()
            for o in mzOrder:
                self.eicTraces.append(eicTraces[o])
    #        self.eicTraces = self.eicTraces[mzOrder]
            self.numEICs = len(groups)
            hdf.close()
        except:
            hdf.close()
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
#                    print 'Error saving figure data'
            errorMsg = "Sorry XCMS Data Not Loaded: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
            print errorMsg

    def appendEIC(self, eicRInstance):
        t1 = time.clock()
        if eicRInstance != None:
            mzRanges = N.asarray(ro.r.mzrange(eicRInstance))[0]
            rtRanges = N.asarray(ro.r.rtrange(eicRInstance))[0]
            group = "UserEIC_%.2f"%mzRanges[0]
            names = ro.r.sampnames(eicRInstance)
            eics = eicRInstance.eic
            metaDict = {'mzlo': mzRanges[0],'mzhi': mzRanges[1],
                        'rtlo': rtRanges[0],'rthi': rtRanges[1]}
            dataDict = {}
            for j,name in enumerate(names):
                curEic = eics[j]
                curEic = N.asarray(curEic[0])
                dataDict[name] =  {'xdata':curEic[:,0],\
                                   'ydata':curEic[:,1]}
            curGroupDict = {}
            curGroupDict[group] = [metaDict, dataDict]
            self.eicTraces.append(curGroupDict)
#            print self.numEICs
            self.numEICs = len(self.eicTraces)
#            print self.numEICs
#            print "EIC Append Time: ", time.clock() - t1



#        data = self.mzRanges
#        shape = data.shape
#        ca = hdf.createCArray(metaGroup, 'mzRanges', atom, shape, filters = filters)
#        ca[0:shape[0]] = data
#        ca.flush()
#        print "mzRanges written"
#
#        data = self.rtRanges
#        shape = data.shape
#        ca = hdf.createCArray(metaGroup, 'rtRanges', atom, shape, filters = filters)
#        ca[0:shape[0]] = data
#        ca.flush()
#        print "rtRanges written"


#        data = self.rtRanges
#        shape = data.shape
#        ca = hdf.createCArray(metaGroup, 'rtRanges', atom, shape, filters = filters)
#        ca[0:shape[0]] = data
#        ca.flush()
#        print "rtRanges written"

#        varGroup = hdf.createGroup("/", 'EICs', 'EIC Arrays')
#        if self.numEICs != 0:

#            for i,gName in enumerate(self.groupNames):
#                tempDict =
#                self.eicGroups[gName] =
#
#            self.mzLo = mzrange[0]
#            self.mzHi = mzrange[1]
#            eicData= self.eicRInstance.eic
#            if len(eicData) != 0:
#                for i,eic in enumerate(eicData):
#                    eic = N.asarray(eic[0])
#                    self.eicTraces[self.names[i]]= {'xdata':N.asarray(eic[:,0]),\
#                                                   'ydata':N.asarray(eic[:,1])}



    def getEIC(self):
        if len(self.eicTraces)>0:
            return self.eicTraces



#def getEICfromGroup(eicGroup, groupTable, m):
#    'mzmed    mzmin    mzmax    rtmed    rtmin    rtmax npeaks KO WT'
#    clf()
#    meta = groupTable[m]
#    mzlo = meta[1]
#    mzhi = meta[2]
#    print mzlo, mzhi
#    for eic in eicGroup:
#        e = eic[m]
#        e = N.asarray(e)
#        plot(e[:,0], e[:,1])
#    titleStr = 'EIC %.2f - %.2f'%(mzlo, mzhi)
#    title(titleStr)

#    def plotXCMS(getEICInstance):
#    clf()
#    sampNames = r.sampnames(getEICInstance)
#    mzrange = r.mzrange(getEICInstance)
#    #print mzrange, len(mzrange)
#    eicData = getEICInstance.eic
#    for i, eic in enumerate(eicData):
#        eic = N.asarray(eic[0])
#        plot(eic[:,0], eic[:,1], label = sampNames[i])
#    legend()
#    title('EIC from %.2f to %.2f m/z'%(mzrange[1], mzrange[3]))
#    xlabel('Time (s)')
#    ylabel('Arbitrary Intensity')