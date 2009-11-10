#!/usr/bin/env python
from PyQt4 import QtCore,  QtGui
import sys, os

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backend_bases import NavigationToolbar2

from matplotlib.figure import Figure

import numpy as N

class EventFilter(QtCore.QObject):

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        if parent != None:
            self.parent = parent

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Enter:
            obj.focusEvent(self.parent)
            #print "got the focus"
        elif event.type() == QtCore.QEvent.Leave:
            obj.lossFocusEvent(self.parent)
            #print "lost the focus"
        return QtCore.QObject.eventFilter(self, obj, event)

class MyMplCanvas(FigureCanvas):
	def __init__(self, parent=None, width = 10, height = 12, dpi = 100, sharex = None, sharey = None):
		self.fig = Figure(figsize = (width, height), dpi=dpi, facecolor = '#FFFFFF')
		self.ax = self.fig.add_subplot(111, sharex = sharex, sharey = sharey)
		self.fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.94)
		self.xtitle="m/z"
		self.ytitle="Intensity"
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
#		self.ax.set_title(self.PlotTitle)
#		self.ax.title.set_fontsize(10)
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
#        self.toolbar.hide()
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


        self.installEventFilter(EventFilter(self))

        ###########SAVING FIGURE TO CLIPBOARD##########
        self.cb = None #will be used for the clipboard
        self.tempPath = getHomeDir()
        self.tempPath = os.path.join(self.tempPath,'tempMPL.png')

    def ZoomToggle(self):
        self.toolbar.zoom()

    def autoscale_plot(self):
        self.toolbar.home()

    def mpl2Clip(self):
        try:
            self.canvas.fig.savefig(self.tempPath)
            tempImg = QtGui.QImage(self.tempPath)
            self.cb = QtGui.QApplication.clipboard()
            self.cb.setImage(tempImg)
        except:
            print 'Error copying figure to clipboard'
            errorMsg = "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
            print errorMsg

    def focusEvent(self, event):
#        self.enableAutoScale()
#        self.enableZoom()
        self.enableClip()
#        self.enableCSV()
        #print "Focus In %s"%self.canvas.plotTitle

    def lossFocusEvent(self, event):
#        self.disableAutoScale()
#        self.disableZoom()
        self.disableClip()
#        self.disableCSV()
        #print "Focus Out %s"%self.canvas.plotTitle

    def enableClip(self):
        self.mpl2ClipAction = QtGui.QAction("Save to Clipboard",  self)
        self.mpl2ClipAction.setShortcut("Ctrl+C")
        self.addAction(self.mpl2ClipAction)
        QtCore.QObject.connect(self.mpl2ClipAction,QtCore.SIGNAL("triggered()"), self.mpl2Clip)

    def disableClip(self):
        QtCore.QObject.disconnect(self.mpl2ClipAction,QtCore.SIGNAL("triggered()"), self.mpl2Clip)
        self.removeAction(self.mpl2ClipAction)


def valid(path):
    if path and os.path.isdir(path):
        return True
    return False

def env(name):
    return os.environ.get( name, '' )

def getHomeDir():
    if sys.platform != 'win32':
        return os.path.expanduser( '~' )

    homeDir = env( 'USERPROFILE' )
    if not valid(homeDir):
        homeDir = env( 'HOME' )
        if not valid(homeDir) :
            homeDir = '%s%s' % (env('HOMEDRIVE'),env('HOMEPATH'))
            if not valid(homeDir) :
                homeDir = env( 'SYSTEMDRIVE' )
                if homeDir and (not homeDir.endswith('\\')) :
                    homeDir += '\\'
                if not valid(homeDir) :
                    homeDir = 'C:\\'
    return homeDir

def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    w = MPL_Widget()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
