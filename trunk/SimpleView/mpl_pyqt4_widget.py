#!/usr/bin/env python
from PyQt4 import QtCore,  QtGui
#from PyQt4.QtGui import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
#from matplotlib.backend_bases import NavigationToolbar2

from matplotlib.figure import Figure

import numpy as N


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width = 5, height = 5, dpi = 100, sharex = None, sharey = None):
        self.fig = Figure(figsize = (width, height), dpi=dpi, facecolor = '#FFFFFF')
        self.ax = self.fig.add_subplot(111, sharex = sharex, sharey = sharey)
        self.fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)
        self.xtitle="m/z"
        self.ytitle="Intensity"
        #self.PlotTitle = "Plot"
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
        #self.ax.set_title(self.PlotTitle)
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
        if self.ax.get_legend() != None:
            texts = self.ax.get_legend().get_texts()
            for text in texts:
                text.set_fontsize(8)
        
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
        self.toolbar = NavigationToolbar(self.canvas, self.canvas)
        #self.toolbar.hide()
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.canvas)
        self.vbox.addWidget(self.toolbar)
        self.setLayout(self.vbox)
        ##########################
        self.hZoom = QtGui.QAction("Zoom",  self)
        self.hZoom.setShortcut("Ctrl+Z")
        self.addAction(self.hZoom)
        QtCore.QObject.connect(self.hZoom,QtCore.SIGNAL("triggered()"), self.ZoomToggle)
        
        self.actionAutoScale = QtGui.QAction("AutoScale",  self)#self.MainWindow)
        self.actionAutoScale.setShortcut("Ctrl+A")
        self.addAction(self.actionAutoScale)
        QtCore.QObject.connect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)
        
        self.test = 0 

    def ZoomToggle(self):
        #print "Zoom",  self.test
        self.test+=1
        self.toolbar.zoom()
        
    def autoscale_plot(self):
        #print "AutoScale",  self.test
        self.test+=1
        self.toolbar.home()
        

def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    w = MPL_Widget()
    w.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
