#Adapted by BHC from:
# $Id: ams.averagine.R 124 2006-10-20 10:02:25Z mkirchner $

import numpy as N
from pyelements import elemDict

try:
    import libmercuryInterface as LMI
    libmercuryOk = True
except:
    libmercuryOk = False


def isoCalc(elemList, elemComp, charge = 1):
    '''
    interface to mercury calc to get user defined isotope patterns
    Limiting the maximum isotopes to be considered to 5
    '''
    if len(elemList)== 0 or len(elemComp) == 0:
        return False

    if len(elemList) != len(elemComp):
        return False

    maxIsotopes = 7
    numElements = len(elemList)
    numIsotopes = N.zeros(maxIsotopes, dtype = N.int)

    elemMasses = N.zeros((numElements, maxIsotopes))
    elemAbundances = N.zeros((numElements, maxIsotopes))

    for i,elem in enumerate(elemList):
        if elemDict.has_key(elem):
            tempIsos = elemDict[elem].isotopes
            tempOrder = []
            tempOrder = N.array(tempOrder)
            orderInd = tempOrder.argsort()
#            print orderInd
#            tempIsos = tempIsos[maxOrder]
            maxIso = len(tempIsos)
            if maxIso > maxIsotopes:
                maxIso = maxIsotopes
            numIsotopes[i] = int(maxIso)
            for j in xrange(maxIso):
                #each iso is a tuple that is the (nominal mass, isotope mass, isotope abundance)
                iso = tempIsos[j]
#                print elem, iso[1], iso[2]
                elemMasses[i][j]=iso[1]
                elemAbundances[i][j]=iso[2]

#    print elemList
#    print elemMasses
#    print elemAbundances
#    print numIsotopes

    if libmercuryOk:
        print "Libmercury OK"
        mercAns = LMI.mercury(elemComp, numIsotopes, elemMasses, elemAbundances, charge, 1e-3)
#        mercAns = LMI.mercury(modelComp, numIsotopes, elemMasses, elemAbundances, charge, 1e-3)
        if mercAns[0] == 0:
            return [True, mercAns[1]]
    else:
        return [False, None]



def averagineCalc(avgMass, charge = 1):

    elemList = ['H','C','N','O','S']
    numIsotopes = N.array([2, 2, 2, 3, 5])

    maxDim1 = numIsotopes.max()
    maxDim2 = len(elemList)

    elemMasses = N.array([[1.0078246,    2.0141021,    0,        0,    0],
    [12.0000000,     13.0033554,     0,         0,    0],
    [14.0030732,     15.0001088,     0,         0,    0],
    [15.9949141,     16.9991322,     17.9991616,     0,    0],
    [31.972070,     32.971456,     33.967866,     34,    35.967080]])

    elemAbundances = N.array([[0.99985,    0.00015,    0,        0,    0],
    [0.988930,    0.011070,     0,         0,    0],
    [0.996337,    0.003663,     0,         0,    0],
    [0.997590,    0.000374,    0.002036,     0,    0],
    [0.9502,    0.0075,        0.0421,     0,    0.0002]])

    avgDict = {}
    avgDict['H']=7.7583
    avgDict['C']=4.9384
    avgDict['N']=1.3577
    avgDict['O']=1.4773
    avgDict['S']=0.0417

    avgMassDict = {}#this is the averagine mass dictionary not the average mass!
    avgMassDict['H']=1.00794
    avgMassDict['C']=12.011
    avgMassDict['N']=14.00670
    avgMassDict['O']=15.99940
    avgMassDict['S']=32.06600

    avgMonomerMass = 111.1254

    #n = int(N.round(avgMass/avgMonomerMass))
    n = avgMass/avgMonomerMass

    modelComp = []
    modelComp.append(int(N.round(avgDict['H']*n)))
    modelComp.append(int(N.round(avgDict['C']*n)))
    modelComp.append(int(N.round(avgDict['N']*n)))
    modelComp.append(int(N.round(avgDict['O']*n)))
    modelComp.append(int(N.round(avgDict['S']*n)))

    modelMass = 0.0
    for i,elem in enumerate(elemList):
        modelMass+=avgMassDict[elem]*modelComp[i]

    actualMass = avgMonomerMass*n
    modelDev = actualMass - modelMass

    print "Actual Mass, Deviation: ", actualMass, modelDev

    if libmercuryOk:
        mercAns = LMI.mercury(modelComp, numIsotopes, elemMasses, elemAbundances, charge, 1e-3)
        if mercAns[0] == 0:
            return mercAns


if __name__ == "__main__":
#    numElemList = [6, 33, 99, 1, 4]
#    elemList = ['O', 'Ba', 'H', 'C', 'O']
#    H117C74N20O22S1
    numElemList = [117, 74, 20, 22, 1]
    elemList = ['H', 'Ca', 'N', 'O', 'S']
    ans = isoCalc(elemList, numElemList)
    print ans
    '''
    Libmercury OK
    5 5
    5 5
    [6, 33, 99, 1, 4] <type 'list'>
    [3 5 2 2 3] <type 'numpy.ndarray'> int32
    (5, 5) <type 'numpy.ndarray'> float64
    (5, 5) <type 'numpy.ndarray'> float64
    '''
#    ans = averagineCalc(1672)
#    '''
#    5 5
#    5 5
#    [117, 74, 20, 22, 1] <type 'list'>
#    [2 2 2 3 5] <type 'numpy.ndarray'> int32
#    (5, 5) <type 'numpy.ndarray'> float64
#    (5, 5) <type 'numpy.ndarray'> float64
#    '''
#    print ans

'''
"ams.averagine" <-
function(avgmass)
{
    # Senko et al., 1995
    model.freq <- list(H=7.7583, C=4.9384, N=1.3577, O=1.4773, S=0.0417);
    # avg. atom masses from GPMAW (http://welcome.to/gpmaw)
    elem.avgmass <- list(H=1.00794, C=12.011, N=14.00670, O=15.99940, S=32.06600);
    model.mass.avg <- 111.1254;

    # number of averagine AAs
    n <- avgmass / model.mass.avg;
    # number of atoms
    freq <- round(sapply(model.freq, '*', n));
    # pad with hydrogen
    modelmass <- sum(freq * as.numeric(elem.avgmass));
    deviance.mass <- avgmass - modelmass; # may be negative for round towards larger ints
    deviance.H <- deviance.mass %/% elem.avgmass$H;
    freq["H"] <- freq["H"] + deviance.H;
    # calculate error
    err.mass <- deviance.mass - deviance.H*elem.avgmass$H;

    return(list(model=as.list(freq), masserror=err.mass, hydrogencorrection=deviance.H));
}
'''
