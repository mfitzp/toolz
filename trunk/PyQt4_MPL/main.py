#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import numpy as N
import scipy as S

from ui_main import Ui_Form

class Plot_Widget(QWidget,  Ui_Form):
    def __init__(self, data2plot=None, parent = None):
        super(Plot_Widget, self).__init__(parent)
        self.setupUi(self)
        
        QObject.connect(self.plotBtn, SIGNAL("clicked()"),self.plotData)
        
        
    def plotData(self):
        x, y = S.rand(2, 30)
        self.plotWidget.canvas.ax.plot(x, y, 'o')
        self.plotWidget.canvas.draw()


if __name__ == "__main__":
    import sys    
    app = QApplication(sys.argv)
    plot = Plot_Widget()#data2plot,  varDict = totaldict)
    plot.show()
    sys.exit(app.exec_())     
