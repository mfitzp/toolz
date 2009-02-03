import numpy as N
import rpy2.robjects as ro
import rpy2.rinterface as ri

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

        print "EIC Create Time: ", time.clock() - t1

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