# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class MainDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.resize(700, 250)
        self.btn = QPushButton()
        self.btn.setText("Test")
        QObject.connect(self.btn, SIGNAL("clicked()"), self.btnClicked)

        self.txt = QTextEdit()
        self.txt.setReadOnly(True)
        self.lineEdit = QLineEdit()
        self.processList = [["uname", ['--kernel-name']], ["uname", ["--processor"]], ["uname", ['--machine']]]

        layout = QGridLayout(self)
        layout.setSpacing(8)
        layout.addWidget(self.lineEdit, 0, 0)
        layout.addWidget(self.btn, 0, 1)
        layout.addWidget(self.txt, 1, 0)

    def btnClicked(self):
        self.process = QProcess(self)
        #self.process.setProcessChannelMode(QProcess.MergedChannels)
        #self.process.setStandardErrorFile('errLog.txt')
        #self.process.setStandardOutputFile('outLog.txt')
        QObject.connect(self.process, SIGNAL("finished(int)"), self.finished)
        QObject.connect(self.process, SIGNAL("readyReadStandardOutput()"), self.OnProcessOutputReady)
        QObject.connect(self.process, SIGNAL("readyReadStandardError()"), self.OnProcessOutputError)
        QObject.connect(self.process, SIGNAL("error(QProcess::ProcessError)"), self.processError)
        #QObject.connect(self.process, SIGNAL("readyRead()"), self.processRead)

        self.processList = []
        processTxt = str(self.lineEdit.text())
        self.processList.append(processTxt)

        sublist = self.processList[0]
        del self.processList[0]
        print(sublist)
        if len(sublist) > 1:
            self.process.start(sublist)
        elif len(sublist) == 1:
            self.process.start(sublist[0])

    def processRead(self):
        errMsg = self.process.readAllStandardOutput().data()
        print len(errMsg), str(errMsg)
        errMsg = self.process.readAllStandardError().data()
        print len(errMsg), str(errMsg)

    def stopProcess(self):
        if self.process:
            self.disconnect(self.process, SIGNAL('error(QProcess::ProcessError)'), self.processError)
            self.disconnect(self.process, SIGNAL('finished(int)'), self.finished)
            self.disconnect(self.process, SIGNAL("finished(int)"), self.finished)
            self.disconnect(self.process, SIGNAL("readyReadStandardOutput()"), self.OnProcessOutputReady)
            self.disconnect(self.process, SIGNAL("readyReadStandardError()"), self.OnProcessOutputError)

            if self.process.state() != QProcess.NotRunning:
                self.process.terminate()
                if not self.process.waitForFinished(5000):
                    self.process.kill()
            self.process = None

    def processError(self, error):
        if error == QProcess.FailedToStart:
            print "Process failed to start: %s" % self.process.errorString()
        elif error == QProcess.Crashed:
            print "Process crashed with exit code %s." % self.process.exitCode()
        else:
            print "Process failed with error %s." % error

        self.processRead()
        #codec = QTextCodec.codecForName("UTF-8")
        #errMsg = self.process.readAllStandardError()
#        print len(errMsg), errMsg
        #self.txt.setText(self.txt.toPlainText() + codec.toUnicode(self.process.readAllStandardError().data()))

        self.stopProcess()

    def OnProcessOutputError(self):
        print "OutputError"
        codec = QTextCodec.codecForName("UTF-8")
        self.txt.setText(self.txt.toPlainText() + codec.toUnicode(self.process.readAllStandardError().data()))
        #self.processRead()

    def OnProcessOutputReady(self):
        print "StandardOutput"
        codec = QTextCodec.codecForName("UTF-8")
        self.txt.setText(self.txt.toPlainText() + codec.toUnicode(self.process.readAllStandardOutput().data()))
        #self.processRead()

    def finished(self, rv):
        print "Return Code: ",rv
        #self.processRead()

        #errMsg = self.process.readAllStandardOutput().data()
#        encoding = sys.getfilesystemencoding() or 'utf-8'
#        errMsg = str(self.process.readAllStandardOutput()).decode(encoding, 'replace')

        #print len(errMsg), errMsg
        if (len(self.processList) == 0):
            self.process = None
            return
        sublist = self.processList[0]
        del self.processList[0]
        print(sublist)
        self.process.start(sublist[0], sublist[1])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainDialog()
    window.show()
    sys.exit(app.exec_())