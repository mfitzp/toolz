

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

def Load_mzXML_Folder(startDir, excludeLIFT = False,  debug = False):
#        if self.dbStatus:
#    directory= str(QFileDialog.getExistingDirectory())
    #print directory

    if startDir:
        directory = startDir

        t1 = time.clock()
        dirList = []
        i=0
        if excludeLIFT:
            for root, dirs, files in walk(directory):
                #for dir in dirs:
                for file in files:
                    if 'mzXML' in file:
                        #temptime = time.clock()
                        if 'LIFT' not in file:
                            datadir = path.abspath(path.join(root, file))
                            dirList.append(datadir)

                            if debug:
                                i+=1
                                if i == 30:
                                    t2 = time.clock()
                                    for item in dirList:
                                        print item
                                        print ''
                                    print t2-t1,  " sec Total"
                                    return dirList

    #        for item in dirList:
    #            print item
            return dirList, startDir

        else:

            for root, dirs, files in walk(directory):
                #for dir in dirs:
                for file in files:
                    if 'mzXML' in file:
                        #temptime = time.clock()
                        datadir = path.abspath(path.join(root, file))
                        dirList.append(datadir)

                        if debug:
                            i+=1
                            if i == 30:
                                t2 = time.clock()
                                for item in dirList:
                                    print item
                                    print ''
                                print t2-t1,  " sec Total"
                                return dirList

    #        for item in dirList:
    #            print item
            return dirList, startDir
    else:
        dirList=[]
        return dirList, None

def run_main():
    app = QApplication(sys.argv)
    try:
        Load_mzXML_Folder()
        sys.exit(app.exec_())
    except:
        raise
        sys.exit(app.exec_())



if __name__ == "__main__":
    run_main()
