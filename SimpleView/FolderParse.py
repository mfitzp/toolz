

from os import walk,  path
import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog,  QApplication

import flexReader as FR

import time

#try:
#    import psyco
#    psyco.full()
#except:
#    print "Pysco not installed, try easy_install psyco at your command prompt"

def __loadDataFolder__(debug = False):
#        if self.dbStatus:
    directory= str(QFileDialog.getExistingDirectory())
    #print directory

    if directory:
        numFiles = 0
        for root, dirs, files in walk(directory):
            for dir in dirs:
                if '1SRef' in dir:
                    numFiles+=1
        print numFiles
        
        t1 = time.clock()
        dirList = []
        i=0
        for root, dirs, files in walk(directory):
            for dir in dirs:
                if '1SRef' in dir:
                    temptime = time.clock()

                    root1 = root
                    dir1 = dir
                    file1 = "fid"
                    datadir = path.abspath(path.join(root1,  dir1,  file1))
                    #dirList.append(datadir)
                    if 'LIFT' not in datadir:
                        dirList.append(datadir)

#                    
#                    tempFlex = FR.brukerFlexDoc(datadir)
#                    tempFlex.encodeSpec()
#                    temptime2 = time.clock()
#                    print temptime2-temptime
                    if debug:
                        i+=1
                        if i == 30:
                            t2 = time.clock()
                            for item in dirList:
                                print item
                                print ''
                            print t2-t1,  " sec Total"
                            return dirList
    
        for item in dirList:
            print item
        
        print len(dirList)
        return dirList
