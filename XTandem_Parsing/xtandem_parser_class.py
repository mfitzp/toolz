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

class XT_xml:
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
            
        self.ppm_errors = None
        self.theoMZs = None
        self.scanID = None
        self.pro_eVals = None
        self.pep_eValues = None
        self.pepLengths = None
        self.hScores = None
        self.nextScores = None
        
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
    
    
    
        

def onpick(event):
    #print "picked"
    #if isinstance(event.artist, Line2D):
    try:
        #self.fragHandle.remove()
        textHandle.remove()
    except:
        pass
    ind = event.ind[0]
    #print ind,  type(event.artist)
    handleA.set_data(N.take(x, [ind]), N.take(y, [ind]))
    handleA.set_visible(True)
    showText = '%s'%(pepseqlist[ind])
    textHandle = ax.text(0.03, 0.95, showText, fontsize=7,\
                                        bbox=dict(facecolor='yellow', alpha=0.1),\
                                        transform=ax.transAxes, va='top')
    fig.canvas.draw()


if __name__ == '__main__':
    from pylab import *
    import numpy as N
    import time
    t1 = time.clock()    
    #the returned list contains tuples with  6 items, ppm, scan#, protein e-value, protein, peptide e-value, and peptide sequence
    filename = 'VP2P47_C_unf_5xDil_rn1_12Oct07_Raptor_Fst-75-1_FIXED_dta_OUT.xml'
    x = parseXtandemResults(filename)
    t2 = time.clock()
    print t2-t1, 'sec'
    ans = x.get('VP2P47_C_unf_5xDil_rn1_12Oct07_Raptor_Fst-75-1_FIXED_dta_OUT.xml')
#    print len(ans)
#    print type(ans[0]), len(ans[0])
#    print type(ans[1]), len(ans[1])
    n=0
    pep_eVal = []
    ppmlist =[]
    peplenlist=[]
    deltascore = []
    pepseqlist = []
    for item in ans[0]:
        pep_eVal.append(item.pep_eVal)
        ppmlist.append(item.ppm)
        peplenlist.append(len(item.pep_seq)**1.5)
        pepseqlist.append(item.pep_seq)
        deltascore.append((item.hscore - item.nextscore))
    pep_eVal = N.array(pep_eVal)
    ppmlist = N.array(ppmlist)
    peplenlist = N.array(peplenlist)
    deltascore = N.array(deltascore)
    fig = figure()
    ax = fig.add_subplot(111)
    handleA,  = ax.plot([0], [0], 'o',\
                    ms=8, alpha=.5, color='yellow', visible=True,  label = 'Cursor A')
    x = pep_eVal
    y = deltascore
    ax.scatter(x, y,  s = peplenlist,  alpha = 0.3,  picker = 5)
    #ax.scatter(ppmlist, deltascore,  s = peplenlist,  alpha = 0.4,  picker = 5)
    ax.set_xscale('log')
    xmin = N.min(pep_eVal)/10
    xmax = N.max(pep_eVal)*10
    ax.set_xlim(xmin, xmax)
    fig.canvas.mpl_connect('pick_event', onpick)
    show()
    #for item in ans[1].iteritems():
        #if n < 20:
            #if len(item[1]) >= 3:
                #for pep in item[1]:
                    #print pep.pep_seq,  pep.protID,  pep.scan
            #n+=1
        #n+=1
    
#    n = 0
#    for pep in ans:
#        #print pep.pep_seq
#        if str(pep.pep_seq) == 'NDEVSSLDAFLDLIR':
#            print n, pep.pep_seq, pep.ppm, pep.pep_eVal,  pep.scan
#            n+=1
        #print pep.pep_seq,  pep.scan
    

