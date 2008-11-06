#!/usr/bin/env python
from PyQt4 import QtCore,  QtGui
#from PyQt4.QtGui import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
#from matplotlib.backend_bases import NavigationToolbar2

from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector

import numpy as N


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width = 5, height = 5, dpi = 100, sharex = None, sharey = None):
        self.fig = Figure(figsize = (width, height), dpi=dpi, facecolor = '#FFFFFF')
        self.axDict = {}
        self.figInit = False

        self.sharey = sharey
        self.sharey = sharey

#        self.ax1.hold(True)


        FigureCanvas.__init__(self, self.fig)
        #self.fc = FigureCanvas(self.fig)
        FigureCanvas.setSizePolicy(self,
            QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def setupSub(self, numSubRows, numSubCols = 1):
        for m in range(1,numSubRows+1):
            for n in range(1,numSubCols+1):
                axName = 'ax%s'%m
                axLoc = 100*numSubRows+10*n+m
                #print axLoc
                self.axDict[axName] = self.fig.add_subplot(axLoc)#, sharex = self.sharex, sharey = self.sharey)

        self.figInit = True

        self.fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)
        self.xtitle=""
        self.ytitle=""
        #self.PlotTitle = "Plot"
        self.grid_status = True
        self.xaxis_style = 'linear'
        self.yaxis_style = 'linear'
        self.format_labels()



    def format_labels(self):
        if self.figInit:
            for ax in self.axDict.itervalues():
                ax.title.set_fontsize(10)
                ax.set_xlabel(self.xtitle, fontsize = 9)
                ax.set_ylabel(self.ytitle, fontsize = 9)
                labels_x = ax.get_xticklabels()
                labels_y = ax.get_yticklabels()

                for xlabel in labels_x:
                    xlabel.set_fontsize(8)
                for ylabel in labels_y:
                    ylabel.set_fontsize(8)
                    ylabel.set_color('b')
                if ax.get_legend() != None:
                    texts = ax.get_legend().get_texts()
                    for text in texts:
                        text.set_fontsize(8)
        else:
            print "please initiate the number of subplots. Call *.canvas.setupSub(numofSubs)"

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
        #NavigationToolbar.__init__(self,parent,canvas)
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
#        ############### Add Actions ################
#
#        self.Zoom = QtGui.QAction("Zoom",  self)
#        self.Zoom.setShortcut("Ctrl+Z")
#        self.addAction(self.Zoom)
#        QtCore.QObject.connect(self.Zoom,QtCore.SIGNAL("triggered()"), self.ZoomToggle)
#
#        self.actionAutoScale = QtGui.QAction("AutoScale",  self)#self.MainWindow)
#        self.actionAutoScale.setShortcut("Ctrl+A")
#        self.addAction(self.actionAutoScale)
#        QtCore.QObject.connect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)
#        ##############################################
#
#        self.span = SpanSelector(self.canvas.ax, self.onselect, 'horizontal', minspan =0.01,
#                                 useblit=True, rectprops=dict(alpha=0.5, facecolor='#C6DEFF') )
#        self.hZoom = False
#        self.span.visible = False
#
#        self.localYMax = 0
#        self.canvas.mpl_connect('button_press_event', self.onclick)
#
#        ########### Misc Code #########################
#
#
#    def ZoomToggle(self):
#        #self.toolbar.zoom() #this implements the classic zoom
#        if self.hZoom:
#            self.hZoom = False
#            self.span.visible = False
#        else:
#            self.hZoom = True
#            self.span.visible = True
#
#    def autoscale_plot(self):
#        #self.toolbar.home() #implements the classic return to home
#        self.canvas.ax.autoscale_view(tight = False, scalex=True, scaley=True)
#        self.canvas.draw()
#
#    def onclick(self, event):
#        #sets up the maximum Y level to be displayed after the zoom.
#        #if not set then it maxes to the largest point in the data
#        #not necessarily the local max
#        self.localYMax = int(event.ydata)
#
#    def onselect(self, xmin, xmax):
#        #print xmin,  xmax
#        if self.hZoom:
#            self.canvas.ax.set_ylim(ymax = self.localYMax)
#            self.canvas.ax.set_xlim(xmin,  xmax)

def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    w = MPL_Widget()
    x = N.arange(0, 20)
    y = N.sin(x)
    w.canvas.ax.plot(x, y)
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
