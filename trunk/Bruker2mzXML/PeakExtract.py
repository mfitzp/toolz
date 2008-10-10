
import os
import os.path
import xml.etree.ElementTree
import xml.etree.cElementTree as ET
import sys

#from PyQt4.QtGui import QFileDialog,  QApplication
import numpy as N


#try:
#    import psyco
#    psyco.full()
#except:
#    print "Pysco not installed, try easy_install psyco at your command prompt"


#def open_file():
#    filename = str(QFileDialog.getOpenFileName())
#    if filename:
#        print "Opened: ", filename
#        return filename

class brukerPeakList:
    """ Load and parse spectrum data from Bruker Daltonics Flex series. """
    # ----
    def __init__(self,  path):
        self.data = {
                    'peaklist':None,
                    'basePeak':None, 
                    'basePeakInt':None
                    }
        self.filename = path
        self.ns = None #namespace
        self.getDocument(self.filename)
    # ----
    def saveCSV(self,  path):
        spectrum = self.data.get('peaklist')
        if spectrum != None:
            path+='.csv'
            #t1 = T.clock()
            N.savetxt(path, spectrum, delimiter = ',', fmt='%.4f')
            #t2 = T.clock()
            #print t2-t1
            
    def getDocument(self, path):
        """ Load and process data. """

        self.handlePeaklist(path)

    def handlePeaklist(self, path):
        """ Search for peaklist XML file and get peaklist data. """

        # get peaklist file
        dirname = os.path.dirname(path)
        if os.path.exists(dirname+'/pdata/1/peaklist.xml'):
            path = dirname+'/pdata/1/peaklist.xml'
        else:
            return False

        # parse XML
        try:
            document = ET.parse(path).getroot()
            self.ns = document.tag
            #print self.ns
            #document = xml.dom.minidom.parse(path)
        except:
            return False

        # get peaklist
        peaklist = []
        #peaks = document.getElementsByTagName('pk')
        peaks = document.findall('pk')#self.ns+
        if peaks:
            for peak in peaks:

                # get mass
                massNode = peak.find('mass')
                mass = massNode.text

                # get intensity
                intensNode = peak.find('absi')
                intens = intensNode.text

                # check mass and intensity
                try:
                    mass = float(mass)
                    intens = float(intens)
                except ValueError:
                    return False

                # add peak to peaklist
                peaklist.append([mass, intens])

        peaklist = N.array(peaklist)
        #intenseArray = peaklist[:,1]
        #print intenseArray.argmax()
        if len(peaklist) > 0:
            bploc = peaklist[:,1].argmax()
            self.data['basePeak'] = float(peaklist[bploc][0])
            self.data['basePeakInt'] = float(peaklist[bploc][1])
            self.data['peaklist'] = peaklist
        #print peaklist

        return True
    # ----


#    # ----
#if __name__ == "__main__":
#    
#    import pylab as P
#    import sys
#    app = QApplication(sys.argv)
#    fn = open_file()
#    import time as T
#    
#    if fn:
#        flex = brukerPeakList(fn)
#        spectrum = flex.data.get('peaklist')
#        if spectrum != None:
#            t1 = T.clock()
#            N.savetxt("C:\myfile.csv", spectrum, delimiter = ',', fmt='%.4f')
#            t2 = T.clock()
#            print t2-t1
#            fig = P.figure()
#            ax = fig.add_subplot(111)
#            ax.plot(spectrum[:, 0],  spectrum[:, 1])
#    
#            P.show()
#        else:
#            print "No peaks found"
#    sys.exit(app.exec_())
