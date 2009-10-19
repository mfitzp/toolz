from os import walk,  path
import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog,  QApplication

import time

#try:
#    import psyco
#    psyco.full()
#except:
#    print "Pysco not installed, try easy_install psyco at your command prompt"

def getBrukerFiles(directory = None, getAgilent = False, DEBUG = False):
    '''
    Parses Autoflex II Generated data file structure to provide
    a list of files to be converted to mzXML by CompassXport
    '''
    if directory == None:
        directory= str(QFileDialog.getExistingDirectory())

    if getAgilent:
        if directory:
            numFiles = 0
            for root, dirs, files in walk(directory):
                for dir in dirs:
                    if '.D' in dir:
                        numFiles+=1
            #print numFiles

            t1 = time.clock()
            dirList = []
            i=0
            for root, dirs, files in walk(directory):
                for dir in dirs:
                    if '.D' in dir:
                        temptime = time.clock()
                        i+=1
                        root1 = root
                        dir1 = dir
                        file1 = "Analysis.yep"
                        datadir = path.abspath(path.join(root1,  dir1,  file1))

                        splitDir = datadir.split(path.sep)
                        '''
                        Example path:
                        C:\\Wahl_Protein_ID\\Data\\EMSL_Agilent_IT\\100709\BNW602391001.D\Analysis.yep
                        '''
                        tempFN = splitDir[-2].replace('.D', '.mzXML')
                        #coreFN = tempFN[-2]#tempFN.split('_')[-1]
                        fn = tempFN#splitDir[-2]+'_'+coreFN+'.'+splitDir[-3]

                        dirList.append((datadir, fn))

    else:
        if directory:
            numFiles = 0
            for root, dirs, files in walk(directory):
                for dir in dirs:
                    if '1SRef' or '1SLin' in dir:
                        numFiles+=1
            #print numFiles

            t1 = time.clock()
            dirList = []
            i=0
            for root, dirs, files in walk(directory):
                for dir in dirs:
                    if '1SRef' in dir:
                        temptime = time.clock()
                        i+=1
                        root1 = root
                        dir1 = dir
                        file1 = "fid"
                        datadir = path.abspath(path.join(root1,  dir1,  file1))

                        splitDir = datadir.split(path.sep)
                        '''
                        Example path:
                        C:\\Sandbox\\Heme\\Heme_S1\\0_A2\\1\\1SRef\\fid
                        '''
                        if 'LIFT' not in datadir:
                            tempFN = splitDir[-4]
                            coreFN = tempFN.split('_')[-1]
                            fn = splitDir[-5]+'_'+coreFN+'_'+splitDir[-3]
                        else:
                            tempFN = splitDir[-5]
                            coreFN = tempFN[-2:]#tempFN.split('_')[-1]
                            fn = splitDir[-6]+'_'+coreFN+'.'+splitDir[-3]

                        dirList.append((datadir, fn))
                    elif '1SLin' in dir:
                        i+=1
                        root1 = root
                        dir1 = dir
                        file1 = "fid"
                        datadir = path.abspath(path.join(root1,  dir1,  file1))

                        splitDir = datadir.split(path.sep)
                        fn = splitDir[-4]

                        dirList.append((datadir, fn))
    if DEBUG:
        for item in dirList:
            print item
    return dirList



def getSubFolders(directory):
    subFolders = []
    for root, dirs, files in walk(directory):
        for dir in dirs:
            if '1SRef' in dir:
                root1 = root
                dir1 = dir
                file1 = 'fid'
                datadir = path.abspath(path.join(root1,  dir1,  file1))
                subFolders.append(datadir)
                #print '\t'+datadir
    return subFolders

def run_main():
    app = QApplication(sys.argv)
    try:
        #dir = 'C:\\Sandbox\\Peptide_ID_spectra'
        dir ='C:\\Wahl_Protein_ID\\Data\\EMSL_Agilent_IT\\100709'
        #dir = 'C:\\Sandbox\\Heme\\Heme_S1'
        getBrukerFiles(dir, getAgilent = True, DEBUG = True)
        sys.exit(app.exec_())
    except:
        raise
        sys.exit(app.exec_())



if __name__ == "__main__":
    run_main()
