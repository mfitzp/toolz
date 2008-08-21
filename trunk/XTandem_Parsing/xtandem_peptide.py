

import PyQt4.QtCore as Core
import PyQt4.QtGui as GUI


class XT_peptide(object):
#ppm, scan#, protein e-value, protein, peptide e-value, and peptide sequence
    def __init__(self, ppm, theomass, scan, prot_eVal,  protID,  pep_eVal, pep_seq, hscore = None, nextscore = None):
        self.ppm = ppm
        self.theomass = theomass
        self.scan = scan
        self.prot_eVal = prot_eVal
        self.protID = protID
        self.pep_eVal = pep_eVal
        self.pep_seq = pep_seq
        if hscore:
            self.hscore = hscore
        if nextscore:
            self.nextscore = nextscore
    

class XT_protein(object):
    def __init__(self, protID,  prot_eVal):
        self.protID = protID
        self.prot_eVal = prot_eVal
        self.peplist = []
    
    def addXTpep(self, XT_peptide):
        self.peplist.append(XT_peptide)
