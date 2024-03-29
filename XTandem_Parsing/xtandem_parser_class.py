import re
import string
import xml.etree.ElementTree#imported for py2exe to work
from xml.etree import cElementTree as ET
import numpy as N
import time


#from xtandem_peptide import XT_peptide, XT_protein

class XT_RESULTS:
    def __init__(self, fileName = None,  parseFile = True,  evalue_cutoff = None,  ppm_cutoff = None):
        t1 = time.clock()
        self.fileName = fileName

        if evalue_cutoff:
            self.evalue_cutoff = evalue_cutoff
        else:
            self.evalue_cutoff = 1

        if ppm_cutoff:
            self.ppm_cutoff = ppm_cutoff
        else:
            self.ppm_cutoff = 10000

#        self.ppm_errors = None
#        self.theoMZs = None
#        self.scanID = None
#        self.pro_eVals = None
#        self.pep_eValues = None
#        self.pepLens = None
#        self.hScores = None
#        self.nextScores = None

        pepID = []
        proID = []
        pepStart = []
        pepStop = []

        ppm_error = []
        theoMZ = []
        scanID = []
        scanIntensity = []
        pro_eVal=[]
        pep_eValue=[]
        hScore = []
        nextScore = []
        pepLen = []
        deltaH = []
        fragXVals = []
        fragYVals = []
        self.dataLen = 0
        self.dataDict = {}
        self.prot_dict = None

        if parseFile:
            pttrn = re.compile('.*id=(\d+)\s.*')
            #pttrn = re.compile('.*scan=(\d+)\s.*')
            tree = ET.parse(fileName)
            r = tree.getroot()
            groups = r.getchildren()

            n = 0
            m = 0
            for group in groups:
                if group.get('type') != 'no model obtained':
                    #print group.get('maxI'), type(group.get('maxI'))
                    maxI = group.get('maxI')
                    if maxI != None:
                        curIntensity = N.float(maxI)
                    else:
                        curIntensity = 0.0
                    for protein in group.findall('protein'):
                        cur_scan  = protein.get('id')
                        cur_protID = protein.attrib['label']
                        cur_pro_eVal = N.float(protein.attrib['expect'])
                        #print '\t',protein.get('maxI')
                        #prot_result = XT_protein(protID,  pro_eVal)
                        for peptide in protein.findall('peptide'):
                            for domain in peptide.findall('domain'):
                                cur_pepSeq = domain.attrib['seq']
                                cur_seqStart = N.int(domain.attrib['start'])
                                cur_seqStop = N.int(domain.attrib['end'])
                                cur_eValue = N.float(domain.attrib['expect'])
                                cur_hscore = N.float(domain.attrib['hyperscore'])
                                cur_nextscore = N.float(domain.attrib['nextscore'])
                                cur_deltaH = cur_hscore - cur_nextscore
                                cur_mzTheor = N.float(domain.get('mh'))
                                cur_ppm = 1e6*(N.float(domain.get('delta')))/cur_mzTheor
                                if cur_eValue < self.evalue_cutoff and abs(cur_ppm) < self.ppm_cutoff:
                                    ppm_error.append(N.float(cur_ppm))
                                    theoMZ.append(cur_mzTheor)
                                    scanID.append(int(cur_scan.split('.')[0]))
                                    pro_eVal.append(cur_pro_eVal)
                                    proID.append(cur_protID)
                                    pep_eValue.append(cur_eValue)
                                    pepID.append(cur_pepSeq)
                                    pepStart.append(cur_seqStart)
                                    pepStop.append(cur_seqStop)
                                    pepLen.append(len(cur_pepSeq))
                                    hScore.append(cur_hscore)
                                    nextScore.append(cur_nextscore)
                                    deltaH.append(cur_deltaH)
                                    scanIntensity.append(curIntensity)
                                    for subGroup in group.getchildren():
                                        if subGroup.get('label') == "fragment ion mass spectrum":
                                            #print "Frag"
                                            fragText, fragInfo = subGroup.getchildren()
                                            fragScan = fragInfo.get('id')
                                            tempStr = str(scanID[-1])
                                            if tempStr == fragScan:
                                                n+=1
                                                for fragElem in fragInfo.getchildren():
                                                    if 'Xdata' in fragElem.tag:
                                                        #print "XData"
                                                        xStr = fragElem[0].text
                                                        strXSplit = xStr.split('\n')
                                                        tempXStr = ''
                                                        for xStr in strXSplit:
                                                            tempXStr+=' '#needed so that sequence joins without decimals
                                                            tempXStr+=xStr
                    #                                    tempXStr.join(strXSplit)#this should work but doesn't
                                                        fragXVals.append(tempXStr)#need to split because there are the return characters
                                                    elif 'Ydata' in fragElem.tag:
                                                        #print 'YData'
                                                        yStr = fragElem[0].text
                                                        #fragYVals.append(N.array(yStr.split('\n')[1].split(), dtype = N.float))#conver to array with dtype set or it will default to string types
                                                        strYSplit = yStr.split('\n')
                                                        tempYStr = ''
                                                        for yStr in strYSplit:
                                                            tempYStr+=' '
                                                            tempYStr+=yStr
                    #                                    tempYStr.join(strYSplit)
                                                        fragYVals.append(tempYStr)#conver to array with dtype set or it will default to string types


            '''
            So I'm not convinced that this is the best way.
            Perhaps a list of individual dictionaries would be more efficient
            But I'm needed this thing to work yesterday!
            '''

            t2 = time.clock()
            print "Initial Read Time (s): ",(t2-t1)
            self.iterLen = len(scanID)
            #                    'index': N.arange(len(pepID)),
            #need to sort the values
            scanOrder = N.array(scanID).argsort()
            #print len(scanOrder), len(fragXVals), len(fragYVals)
            if len(pepID) != 0:
                self.dataDict = {
                    'pepID': N.array(pepID)[scanOrder],
                    'pep_eVal' : N.array(pep_eValue)[scanOrder],
                    'scanID' : N.array(scanID)[scanOrder],
                    'ppm_error':N.array(ppm_error)[scanOrder],
                    'theoMZ':N.array(theoMZ)[scanOrder],
                    'hScore':N.array(hScore)[scanOrder],
                    'nextScore':N.array(nextScore)[scanOrder],
                    'pepLen':N.array(pepLen)[scanOrder],
                    'proID':N.array(proID)[scanOrder],
                    'pro_eVal':N.array(pro_eVal)[scanOrder],
                    'deltaH':N.array(deltaH)[scanOrder],
                    'xFrags':N.array(fragXVals)[scanOrder],
                    'yFrags':N.array(fragYVals)[scanOrder],
                    'scanIntensity':N.array(scanIntensity)[scanOrder],
                    'pepStart':N.array(pepStart)[scanOrder],
                    'pepStop':N.array(pepStop)[scanOrder]
                    }
                self.dataLen = len(pepID)
#                print n, m, self.dataLen, len(self.dataDict['xFrags'])
#                print self.dataDict['xFrags'][53]
            else:
                self.dataDict = False


    def setArrays(self, arrayDict):
        '''
        Used to set arrays when loading from the database
        '''
        if arrayDict:
            self.dataDict = arrayDict
            self.dataLen = len(self.dataDict[self.dataDict.keys()[0]])
#            self.pepIDs = arrayDict.get('pepIDs')
#            self.pep_eValues= arrayDict.get('pep_eValues')
#            self.scanID = arrayDict.get('scanID')
#            self.ppm_errors = arrayDict.get('ppm_errors')
#            self.theoMZs = arrayDict.get('theoMZs')
#            self.hScores = arrayDict.get('hScores')
#            self.nextScores = arrayDict.get('nextScores')
#            self.pepLens= arrayDict.get('pepLens')
#            self.proIDs = arrayDict.get('proIDs')
#            self.pro_eVals = arrayDict.get('pro_eVals')

    def setFN(self, fileName):
        if fileName:
            self.fileName = fileName

    def getProtDict(self,  XT_peplist):
        '''Accepts a list of peptides parsed from an X-Tandem xml file'''
        temp_dict = {}
        for pep in XT_peplist:
            if temp_dict.has_key(pep.protID):
                temp_dict[pep.protID].append(pep)
            else:
                temp_dict[pep.protID] = [pep]

        return temp_dict





if __name__ == '__main__':
    import numpy as N
    import time
    t1 = time.clock()
    #the returned list contains tuples with  6 items, ppm, scan#, protein e-value, protein, peptide e-value, and peptide sequence
    filename = 'R19.xml'
    #filename = 'C01.xml'
    x = XT_RESULTS(filename)
    t2 = time.clock()


#def getPepInfo(xmlTree):
#    for group in a:
#        for protein in group.findall('protein'):
#            for peptide in protein.findall('peptide'):
#                for domain in peptide.findall('domain'):
#                    print domain.get('seq'), protein.get('id')
