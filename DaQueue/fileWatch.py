#!/usr/bin/python

# gridlayout2.py

from os import walk, path
import sys
from PyQt4 import QtGui, QtCore


class GridLayout(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setWindowTitle('grid layout')

        title = QtGui.QLabel('Title')
        author = QtGui.QLabel('Author')
        review = QtGui.QLabel('Review')

        titleEdit = QtGui.QLineEdit()
        authorEdit = QtGui.QLineEdit()
        reviewEdit = QtGui.QTextEdit()

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)

        self.setLayout(grid)
        self.resize(350, 300)

        self.queuedFiles = []
        self.finishedFiles = []
        self.failedFiles = []

        self.watcher = QtCore.QFileSystemWatcher(self)

        self.startDir = '/home/clowers/Desktop/watchDir'
        self.watcher.addPath(self.startDir)
        self.updateDirs(self.startDir, firstRun = True)
        self.updateFiles(self.startDir, firstRun = True)

#        QtCore.QObject.connect(self.watcher,QtCore.SIGNAL("fileChanged(const QString&)"), self.file_changed)
        QtCore.QObject.connect(self.watcher,QtCore.SIGNAL("directoryChanged(const QString&)"), self.dir_changed)

#    def file_changed(self, val):
#        print "File String", str(val)
#        for dir in self.watcher.directories():
#            print '\t',str(dir)

    def dir_changed(self, val):
        print "Dir String", str(val)
        for dir in self.watcher.directories():
            print '\t',str(dir)
        print '\n'

        self.updateDirs(self.startDir)
        self.updateFiles(self.startDir)
#        for f in self.watcher.files():
#            print '\t\t',str(f)

    def updateDirs(self, startDir, firstRun = False, debug = False):
        '''update the watch dir list'''
        if startDir:
            numFiles = 0
            for root, dirs, files in walk(startDir):
                if firstRun:
                    if len(dirs) > 0:
                        for dir in dirs:
                            self.watcher.addPath(dir)
                else:
                    for dir in dirs:
                        if QtCore.QString(dir) not in self.watcher.directories():
                            self.watcher.addPath(dir)


    def updateFiles(self, startDir, firstRun = False, debug = False):
        if startDir:
            numFiles = 0
            for root, dirs, files in walk(startDir):
                for f in files:
                    self.queuedFiles.append(path.abspath(f))




    def __setupDB__(self):
        '''
        Initialize DB
        ''
        '''



def run_main():
    app = QtGui.QApplication(sys.argv)
    qb = GridLayout()
    qb.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_main()
