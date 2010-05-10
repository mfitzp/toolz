import os, sys, traceback

import numpy as N
import matplotlib.pyplot as P
#from mzXMLReader import mzXMLDoc
from mzDataReader import mzDataDoc
import csv

'''

neutral losses          Glycosidic ions (M+H)+
162.0528                163.06007
324.1056                325.11287
486.1584                487.16567
648.2112                366.13947
810.264
1013.3434
972.3168
1175.3962
1134.3696
1337.449
1296.4224
1499.5018
1458.4752
1661.5546

'''

'''
These lists are used to define which m/z
values are going to be examined.

The names lists are used for the headers of
the resulting csv/summary file.
'''

LOSSLIST = [162.0528,
            324.1056,
            486.1584,
            648.2112,
            810.264,
            1013.3434,
            972.3168,
            1175.3962,
            1134.3696,
            1337.449,
            1296.4224,
            1499.5018,
            1458.4752,
            1661.5546
            ]

LOSSNAMES = []
for loss in LOSSLIST:
    LOSSNAMES.append("[M-%s]+"%loss)
    LOSSNAMES.append("[M-%s]+ Int"%loss)

GLYCOLIST = [163.06007,
             325.11287,
             366.13947,
             487.16567
             ]
GLYCONAMES = []
for glyco in GLYCOLIST:
    GLYCONAMES.append('[M+%s]+'%glyco)
    GLYCONAMES.append('[M+%s]+ Int'%glyco)

MISCHEADERS =[
               'Scan',
               'Frag m/z'
               ]

def flattenX(x):
    """
    Helper Function
    flatten(sequence) -> list

    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, MyVector(8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]"""

    result = []
    for el in x:
        #if isinstance(el, (list, tuple)):
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flattenX(el))
        else:
            result.append(el)
    return result

def filterScan(scan, mzVal, ppmTol, scanInfo, mzArray, intArray):
    filterResult = []
    dataOk = False#boolean to test if data in a window was found
    for i,mzLoss in enumerate(LOSSLIST):#iterate through loss list
        mzWinCenter = mzVal - mzLoss#calculates the middle of window to examine
        mzWinHi = mzWinCenter+mzWinCenter*(ppmTol/1000000.0)#get hi and low windows
        mzWinLo = mzWinCenter-mzWinCenter*(ppmTol/1000000.0)#need to add zero to conver to float
        if mzWinLo>0.0:
            criterion = (mzArray >= mzWinLo) & (mzArray <= mzWinHi)
            winInd = N.where(criterion)[0]
            if len(winInd)>0:
                dataOk = True
                '''
                I'm making an assumption here that
                we want the maximum value....big one I know
                I'm ignoring isotopes. Something fancy could be done later but this
                is quick and dirty.
                '''
                tempMZ = mzArray[winInd]
                tempInt = intArray[winInd]
                if len(tempInt)>1:
                    maxInd = tempInt.argmax()
                    filterResult.append(tempMZ[maxInd])
                    filterResult.append(tempInt[maxInd])
                else:
                    filterResult.append(tempMZ)
                    filterResult.append(tempInt)

                    #print scanInfo['id'], i, mzVal, mzLoss, mzWinCenter, mzWinLo, mzWinHi, winInd, mzArray[winInd]
            else:
                filterResult.append(0)
                filterResult.append(0)
        else:
            filterResult.append(-1)
            filterResult.append(-1)

    for j,mzGain in enumerate(GLYCOLIST):
        mzWinCenter = mzVal + mzGain#calculates the middle of window to examine
        mzWinHi = mzWinCenter+mzWinCenter*(ppmTol/1000000.0)#get hi and low windows
        mzWinLo = mzWinCenter-mzWinCenter*(ppmTol/1000000.0)#need to add zero to conver to float
        if mzWinLo>0.0:
            criterion = (mzArray >= mzWinLo) & (mzArray <= mzWinHi)
            winInd = N.where(criterion)[0]
            if len(winInd)>0:
                dataOk = True
                '''
                Again same big assumption here
                '''
                tempMZ = mzArray[winInd]
                tempInt = intArray[winInd]
                if len(tempInt)>1:
                    maxInd = tempInt.argmax()
                    filterResult.append(tempMZ[maxInd])
                    filterResult.append(tempInt[maxInd])
                else:
                    filterResult.append(tempMZ)
                    filterResult.append(tempInt)
                    #print "\t", scanInfo['id'], j+i, mzVal, mzGain, mzWinCenter, mzWinLo, mzWinHi, winInd, mzArray[winInd]
            else:
                filterResult.append(0)
                filterResult.append(0)
        else:
            filterResult.append(-1)
            filterResult.append(-1)
    return dataOk, filterResult

#    def saveCSVTable(self, tableName = None, saveFileName = None):
#        if tableName is None and saveFileName is None:
#            saveFileName = QtGui.QFileDialog.getSaveFileName(self,\
#                                                     self.SaveDataText,\
#                                                     self.__curDir, 'CSV Text File (*.csv)')
#            if saveFileName:
#                curTbl = str(self.queryTblList.currentItem().text())
#                if len(curTbl)>0:
#                    self.curDB.DUMP_TABLE(curTbl, saveFileName)
#                    self.__curDir = getCurDir(saveFileName)
#        else:
#            self.curDB.DUMP_TABLE(tableName, saveFileName)
#            self.__curDir = getCurDir(saveFileName)



def writeTable(fileName, colList, data2write):
    if fileName != None:
        if len(data2write)>0:
            dumpWriter = csv.writer(open(fileName, 'w'), delimiter = ',', quotechar= "'")
            try:
                dumpWriter.writerow(colList)
                for record in data2write:
                    dumpWriter.writerow(record)
                print "%s written to disk!"%fileName
            except:
                errorMsg = "Sorry: %s:%s"%(sys.exc_type, sys.exc_value)
                msg = errorMsg + '\nSave Error'
                print msg
                #error = QtGui.QMessageBox.warning(self.parent, "CSV Table Save Error!",  msg)





def processScanList(scanList, mzDataInst, ppmTol = 250, fileName = "filterOutput.csv", columnList = None):

    if columnList != None:
        numCols = len(columnList)
    else:
        numCols = len(MISCHEADERS)+len(LOSSLIST)+len(GLYCOLIST)

    data2write = []#This is the array where data will be stored and written
    for scan in scanList:
        scanInfo = mzDataInst.getScanInfo(scan)
        msLevel = scanInfo['level']
        mzVal = scanInfo['mz']
        mzArray = None
        intArray = None
        if msLevel > 1:#screen for msLevels above the parent scan
            ans = mzDataInst.handleSpectrum(scan)
            if len(ans) == 3:#check for correct return numbers
                if ans[0] is True:#check for correct return state
                    mzArray = ans[1]
                    intArray = ans[2]

                    filterAns = filterScan(scan, mzVal, ppmTol, scanInfo, mzArray, intArray)
                    if filterAns[0]:
                        dataRow = []#temporary storage of data
                        dataRow.append(scanInfo['id'])
                        dataRow.append(mzVal)
                        dataRow.append(filterAns[1])
                        data2write.append(flattenX(dataRow))
    if len(data2write)>0:
        COLUMNHEADERS = flattenX([MISCHEADERS, LOSSNAMES, GLYCONAMES])
        writeTable(fileName, COLUMNHEADERS, data2write)


def mainFunc():
    COLUMNHEADERS = flattenX([MISCHEADERS, LOSSNAMES, GLYCONAMES])
    print len(COLUMNHEADERS)
    print COLUMNHEADERS

if __name__ == "__main__":
    #fn = 'RnB10V_2.mzData'
    #fn = '/home/clowers/Desktop/Froehlich/RnB10V_3.mzData'
    mzx = mzDataDoc(fn)
    processScanList(mzx.scanList, mzx, fileName = "/home/clowers/Desktop/RnB10V_3.csv")

#    for i in mzx.getScans(mzx.scanList):
#        print i

