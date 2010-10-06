#!/usr/bin/env python

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from numpy import *
from scipy.integrate import odeint
import mpl_toolkits.mplot3d as p3
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MyForm(QDialog):
    def __init__(self, parent = None):
        super(MyForm, self).__init__(parent)
        self.setWindowTitle('Lorenz System (matplotlib and PyQt) - yus')
        self.resize(420, 400)
        # widgets
        self.plot = LorenzPlot()
        self.r_label = QLabel(u"<font size=7 color=darkred> \u03C1 =</font>")   #rho symbol
        self.s_label = QLabel(u"<font size=7 color=darkred> \u03C3 = 8.0</font>")   #sigma symbol
        self.b_label = QLabel(u"<font size=7 color=darkred> \u03B2 = 8/3</font>")   #beta symbol
        self.r_intput = QDoubleSpinBox()
        self.r_intput.setDecimals(1)
        self.r_intput.setRange(0.0, 50)
        # layout
        layout = QGridLayout()
        layout.addWidget(self.plot, 0, 0, 10, 10)
        layout.addWidget(self.r_label, 10, 0)
        layout.addWidget(self.s_label, 10, 3)
        layout.addWidget(self.b_label, 10, 6)
        layout.addWidget(self.r_intput, 10, 1)        
        self.setLayout(layout)
        #signal
        self.connect(self.r_intput, SIGNAL("valueChanged(double)"), self.r_adjust)        
        self.r_intput.setValue(27)
        
    def r_adjust(self, r_new):
        self.plot.draw_plot(r = r_new)

class LorenzPlot(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        
        self.fig = Figure() # 5" by 4"
        self.ax = p3.Axes3D(self.fig)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.fig.canvas)
        
            
    def resizeEvent(self, ev):
        #self.fig.set_size_inches(10,8)
        self.ax = p3.Axes3D(self.fig)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.draw_plot()

    def Lorenz(self, w, t, s, r, b):
        x, y, z = w
        return array([s*(y-x), r*x-y-x*z, x*y-b*z])

    def draw_plot(self, s=8.0, r=28.1, b=16/3.0):
        # Parameters
        self.s, self.r, self.b = s, r, b
        
        self.w_0 = array([0., 0.8, 0.])         # initial condition
        self.time = arange(0., 100., 0.01)      # time vector 
        #integrate a system of ordinary differential equations
        self.trajectory = odeint(self.Lorenz, self.w_0, self.time, args=(self.s, self.r, self.b))
        
        self.x = self.trajectory[:, 0]
        self.y = self.trajectory[:, 1]
        self.z = self.trajectory[:, 2]
        
        self.ax = p3.Axes3D(self.fig)
        self.ax.plot3D(self.x, self.y, self.z)
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec_())
