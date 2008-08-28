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
            self.evalue_cutoff = 0.01
        
        if ppm_cutoff:
            self.ppm_cutoff = ppm_cutoff
        else:
            self.ppm_cutoff = 2  
            
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
            pttrn = re.compile('.*scan=(\d+)\s.*')
            tree = ET.parse(fileName)
            r = tree.getroot()
      
            n = 0
            for c in r.getchildren():
                if c.attrib['label'] != 'no model obtained':
                    description = c.find('group').find('note').text
                    scan = pttrn.match(description).group(1)
                    mhObs  = c.attrib['mh']
                    charge = c.attrib['z']
                    mzObs = (float(mhObs)+(int(charge)-1)*1.00727646688)/int(charge)        
                    for protein in c.findall('protein'):
                        protID = protein.attrib['label']
                        pro_eVal = float(protein.attrib['expect'])
                        #prot_result = XT_protein(protID,  pro_eVal)
                        for peptide in protein.findall('peptide'):
                            for domain in peptide.findall('domain'):
                                pepSeq = domain.attrib['seq']
                                mhTheor = domain.attrib['mh']
                                eValue = float(domain.attrib['expect'])
                                hscore = float(domain.attrib['hyperscore'])
                                nextscore = float(domain.attrib['nextscore'])
                                mzTheor = (float(mhTheor)+(int(charge)-1)*1.00727646688)/int(charge)
                                ppm = 1e6*(mzObs-mzTheor)/mzTheor
                                #print type(eValue)
                                #print type(ppm)
                                if eValue < self.evalue_cutoff and abs(ppm) < self.ppm_cutoff:
                                    ppm_errors.append(float(ppm))
                                    theoMZs.append(mzTheor)
                                    scanID.append(int(scan))
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
    filename = 'VP2P47_C_unf_5xDil_rn1_12Oct07_Raptor_Fst-75-1_FIXED_dta_OUT.xml'
    x = parseXtandemResults(filename)
    t2 = time.clock()


#    
#The shell running Python 2.5.2 (r252:60911, Feb 21 2008, 13:11:45) [MSC v.1310 32 bit (Intel)] on win32.
#Type "copyright", "credits" or "license" for more information on Python.
#
# object? -> Print details about 'object'
#
#>>> from xml.etree import cElementTree as ET
#>>> tree = ET.parse('C:\SVN\toolz\XTandem_Parsing\xmlFiles\BSATest.xml')
#ValueError: invalid \x escape
#>>> tree = ET.parse('C:\\SVN\\toolz\\XTandem_Parsing\\xmlFiles\\BSATest.xml')
#>>> r = tree.getroot()
#>>> r
#<Element 'bioml' at 023D7740>
#>>> r.getchildren()
#[<Element 'group' at 023D7818>, <Element 'group' at 023D7C68>, <Element 'group' at 027FC080>, <Element 'group' at 027FC488>, <Element 'group' at 027FC908>, <Element 'group' at 027FCD40>, <Element 'group' at 0280B1A0>, <Element 'group' at 0280B5A8>, <Element 'group' at 0280B9E0>, <Element 'group' at 0280BE18>, <Element 'group' at 0281C2A8>, <Element 'group' at 0281C710>, <Element 'group' at 0281CB48>, <Element 'group' at 0281CFB0>, <Element 'group' at 03A8D410>, <Element 'group' at 03A8D908>, <Element 'group' at 03A8DD10>, <Element 'group' at 03A9B140>, <Element 'group' at 03A9B548>, <Element 'group' at 03A9B950>, <Element 'group' at 03A9BDE8>, <Element 'group' at 03AAE2D8>, <Element 'group' at 03AAE740>, <Element 'group' at 03AAEB48>, <Element 'group' at 03AAEF50>, <Element 'group' at 03AC1410>, <Element 'group' at 03AC18A8>, <Element 'group' at 03AC1D10>, <Element 'group' at 03AD2170>, <Element 'group' at 03AD25A8>, <Element 'group' at 03AD29B0>, <Element 'group' at 03AD2DB8>, <Element 'group' at 03AE11E8>, <Element 'group' at 03AE1620>, <Element 'group' at 03AE1A58>, <Element 'group' at 03AE1E90>, <Element 'group' at 03AF12C0>, <Element 'group' at 03AF16C8>, <Element 'group' at 03AF1AD0>, <Element 'group' at 03AF1F50>, <Element 'group' at 03B123F8>, <Element 'group' at 03B12878>, <Element 'group' at 03B12CF8>, <Element 'group' at 03B22188>, <Element 'group' at 03B225C0>, <Element 'group' at 03B22A28>, <Element 'group' at 03B22E90>, <Element 'group' at 03B322F0>, <Element 'group' at 03B32800>, <Element 'group' at 03B32D58>, <Element 'group' at 03B43188>, <Element 'group' at 03B435C0>, <Element 'group' at 03B439C8>, <Element 'group' at 03B43E00>, <Element 'group' at 03B67260>, <Element 'group' at 03B67668>, <Element 'group' at 03B67AA0>, <Element 'group' at 03B67ED8>, <Element 'group' at 03B79308>, <Element 'group' at 03B797A0>, <Element 'group' at 03B79C68>, <Element 'group' at 03B86128>, <Element 'group' at 03B865C0>, <Element 'group' at 03B86950>, <Element 'group' at 03B86CE0>, <Element 'group' at 03B99188>, <Element 'group' at 03B997A0>, <Element 'group' at 03B99BD8>, <Element 'group' at 03B99F80>, <Element 'group' at 03BCB3B0>, <Element 'group' at 03BCB740>, <Element 'group' at 03BCBAD0>, <Element 'group' at 03BDC080>, <Element 'group' at 03BDC2D8>]
#>>> a = r.getchildren()[0]
#>>> a
#<Element 'group' at 023D7818>
#>>> a.items()
#[('rt', 'PT1846.46S'), ('mh', '1250.172724'), ('label', 'ENSBTAP00000022763'), ('maxI', '52000'), ('expect', '4.8e-003'), ('sumI', '5.45'), ('fI', '520'), ('z', '2'), ('type', 'model'), ('id', '1164')]
#>>> a.getchildren()
#[<Element 'protein' at 023D75A8>, <Element 'protein' at 023D7920>, <Element 'group' at 023D7848>, <Element 'group' at 023D77B8>]
#>>> a
#<Element 'group' at 023D7818>
#>>> a.items()
#[('rt', 'PT1846.46S'), ('mh', '1250.172724'), ('label', 'ENSBTAP00000022763'), ('maxI', '52000'), ('expect', '4.8e-003'), ('sumI', '5.45'), ('fI', '520'), ('z', '2'), ('type', 'model'), ('id', '1164')]
#>>> a.keys()
#['rt', 'mh', 'label', 'maxI', 'expect', 'sumI', 'fI', 'z', 'type', 'id']
#>>> a1 = a.getchildren()[0]
#>>> a1
#<Element 'protein' at 023D75A8>
#>>> a1.items9)
#  File "<input>", line 1
#    a1.items9)
#             ^
#SyntaxError: invalid syntax
#>>> a1.items()
#[('uid', '19080'), ('label', 'ENSBTAP00000022763'), ('expect', '-368.6'), ('sumI', '8.31'), ('id', '1164.1')]
#>>> a1.keys()
#['uid', 'label', 'expect', 'sumI', 'id']
#>>> a1.note
#Traceback (most recent call last):
#  File "<input>", line 1, in <module>
#AttributeError: note
#>>> a1.findall('note')
#[<Element 'note' at 023D7890>]
#>>> print a1.findall('note')
#[<Element 'note' at 023D7890>]
#>>> print a1.findall('note')[0]
#<Element 'note' at 023D7890>
#>>> note =  a1.findall('note')[0]
#>>> note
#<Element 'note' at 023D7890>
#>>> note.text
#'ENSBTAP00000022763'
#>>> pep = a1.findall('peptide')
#>>> pep
#[<Element 'peptide' at 023D78D8>]
#>>> pep = a1.findall('peptide')[0]
#>>> pep
#<Element 'peptide' at 023D78D8>
#>>> pep.keys()
#['start', 'end']
#>>> pep.items()
#[('start', '1'), ('end', '607')]
#>>> dom = a1.findall('domain')[0]
#Traceback (most recent call last):
#  File "<input>", line 1, in <module>
#IndexError: list index out of range
#>>> dom = a1.findall('domain')
#>>> dom
#[]
#>>> a
#<Element 'group' at 023D7818>
#>>> a.findall('domain')
#[]
#>>> a1.findall('domain')
#[]
#>>> a
#<Element 'group' at 023D7818>
#>>> a.getchildren()
#[<Element 'protein' at 023D75A8>, <Element 'protein' at 023D7920>, <Element 'group' at 023D7848>, <Element 'group' at 023D77B8>]
#>>> for j in a.getchildren()
#  File "<input>", line 1
#    for j in a.getchildren()
#                           
#^
#SyntaxError: invalid syntax
#>>> for j in a.getchildren():
#... 	print j.items()
#... 
#[('uid', '19080'), ('label', 'ENSBTAP00000022763'), ('expect', '-368.6'), ('sumI', '8.31'), ('id', '1164.1')]
#[('uid', '27695'), ('label', 'sp|ALBU_BOVIN|'), ('expect', '-368.6'), ('sumI', '8.31'), ('id', '1164.2')]
#[('type', 'support'), ('label', 'supporting data')]
#[('type', 'support'), ('label', 'fragment ion mass spectrum')]
#>>> a1.items()
#[('uid', '19080'), ('label', 'ENSBTAP00000022763'), ('expect', '-368.6'), ('sumI', '8.31'), ('id', '1164.1')]
#>>> a1.getchildren()
#[<Element 'note' at 023D7890>, <Element 'file' at 023D7830>, <Element 'peptide' at 023D78D8>]
#>>> pep
#<Element 'peptide' at 023D78D8>
#>>> pep.getchildren()
#[<Element 'domain' at 023D77A0>]
#>>> dom = pep.findall('domain')[0]
#>>> dom
#<Element 'domain' at 023D77A0>
#>>> dom.items()
#[('b_ions', '6'), ('pre', 'IAHR'), ('end', '44'), ('seq', 'FKDLGEEHFK'), ('nextscore', '25.5'), ('mh', '1249.621'), ('y_ions', '8'), ('start', '35'), ('hyperscore', '42.0'), ('b_score', '9.5'), ('expect', '4.8e-003'), ('delta', '0.552'), ('post', 'GLVL'), ('missed_cleavages', '1'), ('id', '1164.1.1'), ('y_score', '11.8')]
#>>> dom.get('b_ions')
#'6'
#>>> 
