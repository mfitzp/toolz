#!/usr/bin/env python

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import ui_rangeDialog

class rangeDialog(QDialog, ui_rangeDialog.Ui_fieldDialog):
    def __init__(self, loVal, hiVal, parent = None):
        super(rangeDialog, self).__init__(parent)
        self.setupUi(self)

        self.parent = None
        if parent != None:
            self.parent = parent

        self.loVal = loVal
        self.hiVal = hiVal

        self.loValOk = False
        self.hiValOk = False

        self.connect(self.loVal_LE, SIGNAL("editingFinished()"), self.setMin)
        self.connect(self.hiVal_LE, SIGNAL("editingFinished()"), self.setMax)

        self.buttonBox.setEnabled(False)

#    def accept(self):
#        self.emit(SIGNAL("hiVal(double)"), self.hiVal)
#        self.emit(SIGNAL("loVal(double)"), self.loVal)
#        self.close()
#

    def checkVals(self):
        if self.loVal != None and self.hiVal != None:
            if self.loVal < self.hiVal:
                self.loValOk = True
                self.hiValOk = True
                self.buttonBox.setEnabled(True)
                self.parent.loVal = self.loVal
                self.parent.hiVal = self.hiVal
#                print "Vals Ok"
            else:
                self.buttonBox.setEnabled(False)
#                print "Vals not Ok"

    def setMin(self, val=None):
        if val is None:
            val = self.loVal_LE.text()
        try:
            val = float(str(val))
            self.loVal = val
            self.checkVals()
        except:
            pass
#            msg = "Must Enter a Number for the Minimum Value"
#            return QMessageBox.information(self, "Property Error", msg)
#            self.loVal_LE.setFocus()


    def setMax(self, val=None):
        if val is None:
            val = self.hiVal_LE.text()
        try:
            val = float(str(val))
            self.hiVal = val
            self.checkVals()
        except:
            pass
#            msg = "Must Enter a Number for the Maximum Value"
#            return QMessageBox.information(self, "Property Error", msg)
#            self.hiVal_LE.setFocus()


if __name__ == "__main__":
    dialog = QApplication(sys.argv)
    loVal = 0.0
    hiVal = 0.0
    if rangeDialog(loVal, hiVal).exec_():
        print "OK"
        print loVal, hiVal
    else:
        print "Cancel"
