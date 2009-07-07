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

def getBrukerFiles(directory = None):
    if directory == None:
        directory= str(QFileDialog.getExistingDirectory())


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
                    if 'LIFT' not in datadir:
                        fn = splitDir[-4]
                    else:
                        fn = splitDir[-5]+'.'+splitDir[-3]

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
        getBrukerFiles()
        sys.exit(app.exec_())
    except:
        raise
        sys.exit(app.exec_())



if __name__ == "__main__":
    run_main()
