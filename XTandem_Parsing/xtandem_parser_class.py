import re
from xml.etree import cElementTree as ET
import numpy as N
import time

#try:
#    import psyco
#    psyco.full()
#except:
#    print "No psyco..."
    
from xtandem_peptide import XT_peptide, XT_protein

class XT_RESULTS:
    def __init__(self, fileName,  parseFile = True,  evalue_cutoff = None,  ppm_cutoff = None):
        t1 = time.clock()   
        self.fileName = fileName
        
        if evalue_cutoff:
            self.evalue_cutoff = evalue_cutoff
        else:
            self.evalue_cutoff = 1
        
        if ppm_cutoff:
            self.ppm_cutoff = ppm_cutoff
        else:
            self.ppm_cutoff = .10000  
            
#        self.ppm_errors = None
#        self.theoMZs = None
#        self.scanID = None
#        self.pro_eVals = None
#        self.pep_eValues = None
#        self.pepLengths = None
#        self.hScores = None
#        self.nextScores = None
        
        pepIDs = []
        proIDs = []
        
        ppm_errors = []
        theoMZs = []
        scanID = []
        pro_eVals=[]
        pep_eValues=[]
        hScores = []
        nextScores = []
        pepLengths = []
        
        self.prot_dict = None
        
        if parseFile:
            pttrn = re.compile('.*id=(\d+)\s.*')        
            #pttrn = re.compile('.*scan=(\d+)\s.*')
            tree = ET.parse(fileName)
            r = tree.getroot()
            groups = r.getchildren()
      
            n = 0
            for group in groups:
                if group.get('type') != 'no model obtained':       
                    for protein in group.findall('protein'):
                        scan  = protein.get('id')
                        protID = protein.attrib['label']
                        pro_eVal = float(protein.attrib['expect'])
                        #prot_result = XT_protein(protID,  pro_eVal)
                        for peptide in protein.findall('peptide'):
                            for domain in peptide.findall('domain'):
                                pepSeq = domain.attrib['seq']
                                eValue = float(domain.attrib['expect'])
                                hscore = float(domain.attrib['hyperscore'])
                                nextscore = float(domain.attrib['nextscore'])
                                mzTheor = float(domain.get('mh'))
                                ppm = 1e6*(float(domain.get('delta')))/mzTheor
                                if eValue < self.evalue_cutoff and abs(ppm) < self.ppm_cutoff:
                                    ppm_errors.append(float(ppm))
                                    theoMZs.append(mzTheor)
                                    scanID.append(int(scan.split('.')[0]))
                                    pro_eVals.append(pro_eVal)
                                    proIDs.append(protID)
                                    pep_eValues.append(eValue)
                                    pepIDs.append(pepSeq)
                                    pepLengths.append(len(pepSeq))
                                    hScores.append(hscore)
                                    nextScores.append(nextscore)
            
            t2 = time.clock()
            print "Initial Read Time (s): ",(t2-t1) 
            self.iterLen = len(scanID)
            if len(pepIDs) != 0:
                self.dataDict = {
                    'pepIDs': pepIDs, 
                    'pep_eValues' : N.array(pep_eValues), 
                    'scanID' : N.array(scanID), 
                    'ppm_errors':N.array(ppm_errors),
                    'theoMZs':N.array(theoMZs), 
                    'hScores':N.array(hScores),
                    'nextScores':N.array(nextScores),
                    'pepLengths':N.array(pepLengths), 
                    'proIDs':proIDs, 
                    'pro_eVals':N.array(pro_eVals)
                    }
            else:
                self.dataDict = False
            
    
    def setArrays(self, arrayDict):
        '''Need to be in the following order:
        [
        pepIDs = []
        pep_eValues= []
        scanID = []
        ppm_errors = []
        theoMZs = []
        hScores = []
        nextScores = []
        pepLengths= []
        proIDs = []
        pro_eVals
        ]
        '''
        if arrayDict:
            self.dataDict = arrayDict
#            self.pepIDs = arrayDict.get('pepIDs')
#            self.pep_eValues= arrayDict.get('pep_eValues')
#            self.scanID = arrayDict.get('scanID')
#            self.ppm_errors = arrayDict.get('ppm_errors')
#            self.theoMZs = arrayDict.get('theoMZs')
#            self.hScores = arrayDict.get('hScores')
#            self.nextScores = arrayDict.get('nextScores')
#            self.pepLengths= arrayDict.get('pepLengths')
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
    filename = 'C:\\SVN\\toolz\\XTandem_Parsing\\xmlFiles\\BSATest.xml'
    x = XT_RESULTS(filename)
    t2 = time.clock()


#def getPepInfo(xmlTree):
#    for group in a:
#        for protein in group.findall('protein'):
#            for peptide in protein.findall('peptide'):
#                for domain in peptide.findall('domain'):
#                    print domain.get('seq'), protein.get('id')
