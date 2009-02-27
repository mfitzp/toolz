import numpy as N
import scipy.stats as stats


def fpCompare(fpStatDict, peakCompDict, alpha=0.05):
    sgmadivmu = 0.0001
    foundList, compList = fpextract(fpStatDict, peakCompDict, alpha, sgmadivmu)
    print len(foundList)
    print foundList
    print len(compList)
    print compList
#    numPeaks = fpStatDict['numMembers'][0]
#    cmpVec = N.zeros_like(foundList)
#    cmpVec +=1
#    indx = N.where(foundList>0)[0]
#    cmpVec[indx] = 0
#    probFp = fpStatDict['freq']*(1-alpha)
#    fpCmpProb = self.fpCompSig(cmpVec, probFp)
#    return fpCmpProg

def fpCompSig(cmpVec, probFp):
    probAll = N.prod(1-probFp)
    numOnes = cmpVec.sum()
    pctDrop = numOnes/len(cmpVec)
    probs = 0
    if pctdrop > 0.8:#is this a static value?
       probs = 0
    elif pctdrop == 0:
       probs = 1
    else:
       missing = N.where(cmpVec == 1)[0]#find(zero1vec == 1);
#           lenM = len(missing)
       observed = N.where(cmpVec == 0)[0]#find(zero1vec==0);
       prob1 = N.prod(1-pvals[missing])
       prob2 = prod(pvals[observed])
       probs = 1-prob2*(1-prob1)

    return probs


def fpextract(fpStatDict, peakCompDict, alpha, sgmadivmu, minTolppm = 50):

    '''
    Variables needed:
    number of spectra for each dictionary
    df1 = numMembers - 1
    df2 = numMembers - 1
    dfe = df1+df2

    '''
    alpha = alpha/2
    fpPeakLoc = fpStatDict['aveLoc']
    fpStdLoc = fpStatDict['stdLoc']
    cmpPeakLoc = peakCompDict['aveLoc']
    cmpPeakInt = peakCompDict['aveInt']
    tol = 3*(1+(fpPeakLoc*sgmadivmu)**2)#not sure why this is the case need to find out
    #need to make an instance of peakCompDict that is for one spectrum
    degF1 = fpStatDict['numMembers'][0]-1 #indexing first value as this is a list with the same values
    degF2 = (N.round(peakCompDict['numMembers']*peakCompDict['prob']))-1 #indexing first value as this is a list with the same values
    degF = degF1+degF2
    foundList = N.zeros_like(fpPeakLoc)
    foundIntList = N.zeros_like(fpPeakLoc)
    compList = N.zeros_like(cmpPeakLoc)
    for i,mz in enumerate(fpPeakLoc):
        absDiff = N.abs(mz-cmpPeakLoc)#need to make arrays the same length
        pool = N.max([minTolppm*mz, fpStdLoc[i]])
        tstat = absDiff/pool
        closest = N.argmin(absDiff)
        sigLvl = 1 - stats.t.cdf(tstat[closest], degF[closest])#this is 1-alpha

        if sigLvl > alpha:
            rempt = 0
        elif absDiff[closest]<tol[i]:
            rempt = 0
        else:
            rempt = 1

        if rempt == 0:
            foundList[i]= cmpPeakLoc[closest]
            foundIntList[i] = cmpPeakInt[closest]
            compList[closest] = 1

    return foundList, compList



if __name__ == "__main__":
    import pylab as P

    ms = P.load('cp033191.txt',delimiter='\t', skiprows=1)
    P.plot(ms[:,0], ms[:,1], 'r')


    unkColumns = P.load('Unknown_FP.csv',delimiter=',', skiprows=1)
    orgAColumns = P.load('OrganismA_FP.csv',delimiter=',', skiprows=1)
    '''
    locn     slocn    ht    sht    prob     Ntot
    0        1        2     3      4        5
    '''
    unkStatDict = {}
    unkStatDict['aveLoc'] = unkColumns[:,0]
    unkStatDict['stdLoc'] = unkColumns[:,1]
    unkStatDict['aveInt'] = unkColumns[:,2]
    unkStatDict['stdInt'] = unkColumns[:,3]
    unkStatDict['prob'] = unkColumns[:,4]
    unkStatDict['numMembers'] = unkColumns[:,5]

    orgAStatDict = {}
    orgAStatDict['aveLoc'] = orgAColumns[:,0]
    orgAStatDict['stdLoc'] = orgAColumns[:,1]
    orgAStatDict['aveInt'] = orgAColumns[:,2]
    orgAStatDict['stdInt'] = orgAColumns[:,3]
    orgAStatDict['prob'] = orgAColumns[:,4]
    orgAStatDict['numMembers'] = orgAColumns[:,5]

    fpCompare(orgAStatDict, unkStatDict)

    P.vlines(unkStatDict['aveLoc'],0,unkStatDict['aveInt'], 'b', alpha = 0.7)
    P.vlines(orgAStatDict['aveLoc'],0,orgAStatDict['aveInt'], 'g', linestyle = '--',alpha = 0.7)

    P.show()