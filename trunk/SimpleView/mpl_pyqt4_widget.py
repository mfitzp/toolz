#!/usr/bin/env python

import os
import sys

from PyQt4 import QtCore,  QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
#from matplotlib.backend_bases import NavigationToolbar2

from matplotlib.figure import Figure

from matplotlib.widgets import SpanSelector
#from matplotlib.pyplot import savefig
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

        ###############ZOOM CONTROLS ################

        self.Zoom = QtGui.QAction("Zoom",  self)
        self.Zoom.setShortcut("Ctrl+Z")
        self.addAction(self.Zoom)
        QtCore.QObject.connect(self.Zoom,QtCore.SIGNAL("triggered()"), self.ZoomToggle)

        #This funciton has been disabled because of the special autoscaling requried for SimpleView
#        self.actionAutoScale = QtGui.QAction("AutoScale",  self)#self.MainWindow)
#        self.actionAutoScale.setShortcut("Ctrl+A")
#        self.addAction(self.actionAutoScale)
#        QtCore.QObject.connect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)

        self.span = SpanSelector(self.canvas.ax, self.onselect, 'horizontal', minspan =0.01,
                                 useblit=True, rectprops=dict(alpha=0.5, facecolor='#C6DEFF') )
        self.hZoom = False
        self.span.visible = False

        self.localYMax = 0
        self.canvas.mpl_connect('button_press_event', self.onclick)

        ###########SAVING FIGURE TO CLIPBOARD##########
        self.cb = None #will be used for the clipboard
        self.tempPath = getHomeDir()
        self.tempPath = os.path.join(self.tempPath,'tempMPL.png')

        self.mpl2ClipAction = QtGui.QAction("Save to Clipboard",  self)
        self.mpl2ClipAction.setShortcut("Ctrl+C")
        self.addAction(self.mpl2ClipAction)
        QtCore.QObject.connect(self.mpl2ClipAction,QtCore.SIGNAL("triggered()"), self.mpl2Clip)


        #######SAVING FIGURE DATA############################
#        self.saveCSVAction = QtGui.QAction("Save to CSV",  self)
#        self.saveCSVAction.setShortcut("Ctrl+Alt+S")
#        self.addAction(self.saveCSVAction)
#        QtCore.QObject.connect(self.saveCSVAction,QtCore.SIGNAL("triggered()"), self.save2CSV)

        ########### HELPER FUNCTIONS #########################

    def ZoomToggle(self):
        #self.toolbar.zoom() #this implements the classic zoom
        if self.hZoom:
            self.hZoom = False
            self.span.visible = False
        else:
            self.hZoom = True
            self.span.visible = True

    def autoscale_plot(self):
        #self.toolbar.home() #implements the classic return to home
        self.canvas.ax.autoscale_view(tight = False, scalex=True, scaley=True)
        self.canvas.draw()

    def onclick(self, event):
        #sets up the maximum Y level to be displayed after the zoom.
        #if not set then it maxes to the largest point in the data
        #not necessarily the local max
        if event.ydata != None:
            self.localYMax = int(event.ydata)

    def onselect(self, xmin, xmax):
        #print xmin,  xmax
        if self.hZoom:
            self.canvas.ax.set_ylim(ymax = self.localYMax)
            self.canvas.ax.set_xlim(xmin,  xmax)


    def save2CSV(self):
        path = self.SFDialog()
        if path != None:
            try:
                lines = self.canvas.ax.get_lines()
                data2write = []
                for line in lines:
                    data2write.append(line.get_data()[0])
                    data2write.append(line.get_data()[1])
                print data2write
                data2write = N.array(data2write)
                data2write.dtype = N.float32
                N.savetxt(str(path), N.transpose(data2write), delimiter = ',', fmt='%.4f')
            except:
                try:
                    #this is for the case where the data may not be in float format?
                    N.savetxt(str(path), N.transpose(data2write), delimiter = ',')
                except:
                    print 'Error saving figure data'
                    errorMsg = "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
                    print errorMsg


    def SFDialog(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                                         "Select File to Save",
                                         "",
                                         "csv Files (*.csv)")
        if not fileName.isEmpty():
            print fileName
            return fileName
        else:
            return None


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
#        savefig(fname, dpi=None, facecolor='w', edgecolor='w',
#        orientation='portrait', papertype=None, format=None,
#        transparent=False):

####USED TO GET THE USERS HOME DIRECTORY FOR USE OF A TEMP FILE

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
    x = N.arange(0, 20)
    y = N.sin(x)
    y2 = N.cos(x)
    w.canvas.ax.plot(x, y)
    w.canvas.ax.plot(x, y2)
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
