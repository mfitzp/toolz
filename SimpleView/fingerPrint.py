import os, sys, traceback
from PyQt4 import QtGui, QtCore
import numpy as N

import ui_fingerPrint

class Finger_Widget(QtGui.QWidget, ui_fingerPrint.Ui_fingerPlotWidget):
    def __init__(self, parent = None):
        super(Finger_Widget, self).__init__(None)
#        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.ui = self.setupUi(self)
        self.mainAx = self.plotWidget.canvas.ax

        self.__initConnections__()

        print "Finger Widget"

    def __initConnections__(self):
        self.actionAutoScale = QtGui.QAction("AutoScale",  self)#self.MainWindow)
        self.actionAutoScale.setShortcut("Ctrl+A")
        self.plotWidget.addAction(self.actionAutoScale)
        QtCore.QObject.connect(self.actionAutoScale, QtCore.SIGNAL("triggered()"), self.autoscale_plot)

    def autoscale_plot(self):
#        print "Auto Finger"
        self.mainAx.autoscale_view(tight = False, scalex=True, scaley=True)
        self.mainAx.set_ylim(ymin = 0)
        self.plotWidget.canvas.draw()

if __name__ == "__main__":
    #from scipy import rand
    app = QtGui.QApplication(sys.argv)
    finger = Finger_Widget()
    finger.show()
    sys.exit(app.exec_())
