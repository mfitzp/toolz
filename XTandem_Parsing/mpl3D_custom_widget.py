#!/usr/bin/env python
from PyQt4 import QtCore,  QtGui
#from PyQt4.QtGui import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backend_bases import NavigationToolbar2

from matplotlib.figure import Figure

from mpl_toolkits.mplot3d import Axes3D
'''
self.fig = Figure(figsize = (width, height), dpi=dpi, facecolor = '#FFFFFF')
self.ax = Axes3D(self.fig)
self.ax.scatter3D(S.rand(200), S.rand(200), S.rand(200))
'''

from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np



import numpy as N
import scipy as S

def randrange(n, vmin, vmax):
    return (vmax-vmin)*np.random.rand(n) + vmin


class MyMplCanvas(FigureCanvas):
	def __init__(self, parent=None, width = 10, height = 12, dpi = 100, sharex = None, sharey = None):
		self.fig = Figure(figsize = (width, height), dpi=dpi, facecolor = '#FFFFFF')

		self.ax = Axes3D(self.fig)
#		n = 100
#		for c, zl, zh in [('r', -50, -25), ('b', -30, -5)]:
#		    xs = randrange(n, 23, 32)
#		    ys = randrange(n, 0, 100)
#		    zs = randrange(n, zl, zh)
		self.ax.scatter3D(S.rand(200), S.rand(200), S.rand(200))#, c = c,  alpha = 0.8)

		self.ax.set_xlabel('X Label')
		self.ax.set_ylabel('Y Label')
		self.ax.set_zlabel('Z Label')

#		self.ax = self.fig.add_subplot(111, sharex = sharex, sharey = sharey)
#		self.fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)
		self.xtitle="x-Axis"
		self.ytitle="y-Axis"
		self.PlotTitle = "Plot"
		self.grid_status = True
		self.xaxis_style = 'linear'
		self.yaxis_style = 'linear'
		self.format_labels()
		self.ax.hold(True)
		FigureCanvas.__init__(self, self.fig)
		#self.fc = FigureCanvas(self.fig)
		FigureCanvas.setSizePolicy(self,
			QtGui.QSizePolicy.Expanding,
			QtGui.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

	def format_labels(self):
		self.ax.set_title(self.PlotTitle)
		self.ax.title.set_fontsize(10)
		self.ax.set_xlabel(self.xtitle, fontsize = 9)
		self.ax.set_ylabel(self.ytitle, fontsize = 9)
		labels_x = self.ax.get_xticklabels()
		labels_y = self.ax.get_yticklabels()

		for xlabel in labels_x:
			xlabel.set_fontsize(8)
		for ylabel in labels_y:
			ylabel.set_fontsize(8)
			ylabel.set_color('b')

	def sizeHint(self):
		w, h = self.get_width_height()
		return QtCore.QSize(w, h)

	def minimumSizeHint(self):
		return QtCore.QSize(10, 10)

	def sizeHint(self):
		w, h = self.get_width_height()
		return QtCore.QSize(w, h)

	def minimumSizeHint(self):
		return QtCore.QSize(10, 10)


class MyNavigationToolbar(NavigationToolbar) :
	def __init__(self , parent , canvas , direction = 'h' ) :
		#NavigationToolbar.__init__(self,parent,canevas)
		#self.layout = QVBoxLayout( self )

		self.canvas = canvas
		QWidget.__init__( self, parent )

		if direction=='h' :
			self.layout = QHBoxLayout( self )
		else :
			self.layout = QVBoxLayout( self )

		self.layout.setMargin( 2 )
		self.layout.setSpacing( 0 )

		NavigationToolbar2.__init__( self, canvas )
	def set_message( self, s ):
		pass


class MPL_Widget(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MyMplCanvas()
        #self.toolbar = MyNavigationToolbar(self.canvas, self.canvas, direction = 'v')
        self.toolbar = NavigationToolbar(self.canvas, self.canvas)
        #self.toolbar.hide()
        self.hbox = QtGui.QHBoxLayout()
        #self.hbox.addWidget(self.toolbar)
        self.hbox.addWidget(self.canvas)
        self.setLayout(self.hbox)
        ##########################
        self.hZoom = QtGui.QAction("Zoom",  self)
        self.hZoom.setShortcut("Ctrl+Z")
        self.addAction(self.hZoom)
        QtCore.QObject.connect(self.hZoom,QtCore.SIGNAL("triggered()"), self.ZoomToggle)

        self.actionAutoScale = QtGui.QAction("AutoScale",  self)#self.MainWindow)
        self.actionAutoScale.setShortcut("Ctrl+A")
        self.addAction(self.actionAutoScale)
        QtCore.QObject.connect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)

    def ZoomToggle(self):
        self.toolbar.zoom()

    def autoscale_plot(self):
        self.toolbar.home()


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    w = MPL_Widget()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
