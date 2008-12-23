#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as N
import scipy as S

from fit import *
import ui_Fit_Info

class Fit_Info_Dialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, None)
        self.ui = ui_Fit_Info.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.comboBox.addItems(functions.keys())
        self.ui.comboBox.setCurrentIndex(3)
        self.getFitInfo(self.ui.comboBox.currentText())
        self.make_connections()
        
    def make_connections(self):
        self.connect(self.ui.comboBox,SIGNAL("currentIndexChanged(QString)"), self.getFitInfo)
        
    def getFitInfo(self, fit_name):
        try:
            self.fitInfo = functions.get(str(fit_name))
            n = 0
            for item in self.fitInfo.iteritems():
                m = 0
                for entry in item:
                    #print entry, type(str(entry))
                    newitem = QTableWidgetItem(str(entry))
                    self.ui.tableWidget.setItem(n,  m,  newitem)
                    m+=1
                n+=1
            
            self.ui.tableWidget.resizeColumnsToContents()
        except:
            print "Error Obtaining Fit Info"

if __name__ == "__main__":

    app = QApplication(sys.argv)
    FD = Fit_Info_Dialog()
    FD.show()
    sys.exit(app.exec_())     

        


