#!/usr/bin/env python
from PyQt4 import QtCore,  QtGui
import sys, os

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backend_bases import NavigationToolbar2

from matplotlib.figure import Figure

from Plot_Options_Line2D import Plot_Options_Dialog as POD

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

class DoubleMyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width = 6, height = 5, dpi = 100, sharex = None, sharey = None):
        self.fig = Figure(figsize = (width, height), dpi=dpi, facecolor = '#FFFFFF')
        self.ax = self.fig.add_subplot(211, sharex = sharex, sharey = sharey)
        self.ax2 = self.fig.add_subplot(212, sharex = sharex, sharey = sharey)
        self.axList = [self.ax, self.ax2]
        self.fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)
        self.plotTitle = ''
        self.xtitle="X"#"Drift Time (ms)"
        self.ytitle="Y"#"Intensity"
        self.ax.set_xlabel(self.xtitle, fontsize = 9)
        self.ax.set_ylabel(self.ytitle, fontsize = 9)
        self.grid_status = True
        self.xaxis_style = 'linear'
        self.yaxis_style = 'linear'
        self.format_labels()
        self.ax.hold(True)


        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self,
            QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)



    def format_labels(self, xItalic = False):
        for ax in self.axList:
            ax.set_title(self.plotTitle)
            ax.title.set_fontsize(10)
            xLabel = self.xtitle#self.ax.get_xlabel()
            yLabel = self.ytitle#self.ax.get_ylabel()
            if xItalic:
                ax.set_xlabel(xLabel, fontsize = 9, fontstyle = 'italic')
            else:
                ax.set_xlabel(xLabel, fontsize = 9)
            ax.set_ylabel(yLabel, fontsize = 9)
            labels_x = ax.get_xticklabels()
            labels_y = ax.get_yticklabels()

            for xlabel in labels_x:
                xlabel.set_fontsize(8)
            for ylabel in labels_y:
                ylabel.set_fontsize(8)
                ylabel.set_color('b')
            if ax.get_legend() != None:
                self.ax.legend(borderaxespad = 0.03, axespad=0.25)
                texts = ax.get_legend().get_texts()
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

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width = 10, height = 12, dpi = 100, sharex = None, sharey = None):
        self.fig = Figure(figsize = (width, height), dpi=dpi, facecolor = '#FFFFFF')
        self.ax = self.fig.add_subplot(111, sharex = sharex, sharey = sharey)
        self.fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.94)
        self.xtitle="m/z"
        self.ytitle="Intensity"
        self.plotTitle = None
        self.grid_status = True
        self.xaxis_style = 'linear'
        self.yaxis_style = 'linear'
        self.format_labels()
        self.ax.hold(True)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    def format_labels(self, xItalic = False):
        if self.plotTitle != None:
            self.ax.set_title(self.plotTitle)
            self.ax.title.set_fontsize(10)
        xLabel = self.xtitle#self.ax.get_xlabel()
        yLabel = self.ytitle#self.ax.get_ylabel()
        if xItalic:
            self.ax.set_xlabel(xLabel, fontsize = 9, fontstyle = 'italic')
        else:
            self.ax.set_xlabel(xLabel, fontsize = 9)
        self.ax.set_ylabel(yLabel, fontsize = 9)
        labels_x = self.ax.get_xticklabels()
        labels_y = self.ax.get_yticklabels()

#        yfmt = self.ax.yaxis.get_major_formatter()
#        xfmt = self.ax.xaxis.get_major_formatter()
#        yfmt.set_powerlimits((-3, 2))
#        xfmt.set_powerlimits((-3, 2))
#        yfmt.set_scientific(True)
#        xfmt.set_scientific(True)


        for xlabel in labels_x:
            xlabel.set_fontsize(8)
        for ylabel in labels_y:
            ylabel.set_fontsize(8)
            ylabel.set_color('b')
        if self.ax.get_legend() != None:
            texts = self.ax.get_legend().get_texts()
            for text in texts:
                text.set_fontsize(7)

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
    def __init__(self, parent = None, enableAutoScale = True, enableCSV = False, enableEdit = True, doublePlot = False, layoutDir = 'h'):
        QtGui.QWidget.__init__(self, parent)
        if doublePlot:
            self.canvas = DoubleMyMplCanvas()
        else:
            self.canvas = MyMplCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self.canvas)
#        self.toolbar.hide()
        self.installEventFilter(EventFilter(self))

        if layoutDir == 'v':
            self.toolbar.setOrientation(QtCore.Qt.Vertical)
            self.layout = QtGui.QHBoxLayout()


        elif layoutDir == 'h':
            self.layout = QtGui.QVBoxLayout()
#            self.layout.addWidget(self.canvas)
#            self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

        ##########################

        self.dataLabels = None

        ###########SAVING FIGURE TO CLIPBOARD##########
        self.cb = None #will be used for the clipboard
        self.tempPath = getHomeDir()
        self.tempPath = os.path.join(self.tempPath,'tempMPL.png')

        if enableEdit:
            self.enableEdit()

        self.lineDict = None
        self.addLegend = False


        self.x = None#used for picker
        self.y = None

        #######SAVING FIGURE DATA############################
        if enableCSV:
            self.enableCSV()


        ########### HELPER FUNCTIONS #########################
        self.clearPlotAction = QtGui.QAction("Clear Plot", self)
        self.addAction(self.clearPlotAction)
        QtCore.QObject.connect(self, QtCore.SIGNAL("triggered()"), self.clearPlot)

#    def focusOutEvent(self, event):
#        print "Focus Out"

    def clearPlot(self):
        print "Clear Plot"
        self.canvas.ax.cla()
        self.canvas.format_labels()
        self.canvas.draw()

#    def __initContextMenus__(self):
#        self.clearPlotAction = QtGui.QAction("Clear Plot", self)
#        self.addAction(self.clearPlotAction)
#        QtCore.QObject.connect(self, QtCore.SIGNAL("triggered()"), self.clearPlot)
#
#        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
#        self.connect(self, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.plotTabContext)

#    def plotTabContext(self, point):
#        '''Create a menu for mainTabWidget'''
#        plotCT_menu = QtGui.QMenu("Menu", self)
#        plotCT_menu.addAction(self.Zoom)
#        plotCT_menu.addAction(self.actionAutoScale)
#        plotCT_menu.addSeparator()
#        plotCT_menu.addAction(self.clearPlotAction)
#        plotCT_menu.exec_(self.mapToGlobal(point))

    def focusEvent(self, event):
        self.enableAutoScale()
        self.enableZoom()
        self.enableClip()
#        self.enableCSV()
        #print "Focus In %s"%self.canvas.plotTitle

    def lossFocusEvent(self, event):
        self.disableAutoScale()
        self.disableZoom()
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

    def enableEdit(self):
        self.editAction = QtGui.QAction("Edit Line Properties",  self)
        self.editAction.setShortcut("Ctrl+Alt+E")
        self.addAction(self.editAction)
        QtCore.QObject.connect(self.editAction,QtCore.SIGNAL("triggered()"), self.editPlotProperties)

    def disableEdit(self):
        if self.editAction:
            QtCore.QObject.disconnect(self.editAction,QtCore.SIGNAL("triggered()"), self.editPlotProperties)
            self.removeAction(self.editAction)

    def enableZoom(self):
        self.Zoom = QtGui.QAction("Zoom",  self)
        self.Zoom.setShortcut("Ctrl+Z")
        self.addAction(self.Zoom)
        QtCore.QObject.connect(self.Zoom, QtCore.SIGNAL("triggered()"), self.ZoomToggle)

    def disableZoom(self):
        if self.Zoom != None:
            QtCore.QObject.disconnect(self.Zoom,QtCore.SIGNAL("triggered()"), self.ZoomToggle)
            self.removeAction(self.Zoom)

    def disableAutoScale(self):
        if self.actionAutoScale != None:
            QtCore.QObject.disconnect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)
            self.removeAction(self.actionAutoScale)

    def enableAutoScale(self):
        self.actionAutoScale = QtGui.QAction("AutoScale",  self)#self.MainWindow)
        self.actionAutoScale.setShortcut("Ctrl+A")
        self.addAction(self.actionAutoScale)
        QtCore.QObject.connect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)

    def enableCSV(self):
        self.saveCSVAction = QtGui.QAction("Save to CSV",  self)
        self.saveCSVAction.setShortcut("Ctrl+Alt+S")
        self.addAction(self.saveCSVAction)
        QtCore.QObject.connect(self.saveCSVAction,QtCore.SIGNAL("triggered()"), self.save2CSV)

    def disableCSV(self):
        QtCore.QObject.disconnect(self.saveCSVAction,QtCore.SIGNAL("triggered()"), self.save2CSV)
        self.removeAction(self.saveCSVAction)

    def setLineDict(self):
        self.lineDict = {}
        lineList = self.canvas.ax.get_lines()
        if lineList > 0:
            for line in lineList:
                self.lineDict[line.get_label()]=line

    def editPlotProperties(self):
        print "Edit Enabled"
        self.setLineDict()
#        if len(self.lineDict) > 0:
        curAx = self.canvas.ax
        if POD(self.lineDict, curAx = curAx, parent = self).exec_():
            if self.addLegend:
                curAx.legend(borderaxespad = 0.03, axespad=0.25)
            self.canvas.format_labels()
            self.canvas.draw()
        else:
            print "Cancel"


    def ZoomToggle(self):
        self.toolbar.zoom() #this implements the classic zoom
#        if self.hZoom:
#            self.hZoom = False
#            self.span.visible = False
#        else:
#            self.hZoom = True
#            self.span.visible = True

    def autoscale_plot(self):
        self.toolbar.home() #implements the classic return to home
#        self.canvas.ax.autoscale_view(tight = False, scalex=True, scaley=True)
#        self.canvas.draw()
#        self.emit(QtCore.SIGNAL("autoScaleAxis(bool)"),True)

#    def onclick(self, event):
#        #sets up the maximum Y level to be displayed after the zoom.
#        #if not set then it maxes to the largest point in the data
#        #not necessarily the local max
#        if event.ydata != None:
#            self.localYMax = int(event.ydata)
#
#    def onselect(self, xmin, xmax):
#        #print xmin,  xmax
#        if self.hZoom:
#            self.canvas.ax.set_ylim(ymax = self.localYMax)
#            self.canvas.ax.set_xlim(xmin, xmax)
#            self.canvas.draw()


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

    def removePicker(self):
        try:
            self.handleA.remove()
        except:
            print ""

    def setData(self, x, y):
        if x != None:
            self.x = x
        if y != None:
            self.y = y

    def addPicker(self):
        '''Sets up the plot variables used for interaction'''
        self.handleA,  = self.canvas.ax.plot([0], [0], 'o',\
                                        ms=8, alpha=.5, color='yellow', visible=True,  label = '_nolegend_')
        self.is_hZoom = False
        self.canvas.mpl_connect('pick_event', self.OnPickPlot)

    def OnPickPlot(self, event):
        self.pickIndex = event.ind[0]
        try:
            self.textHandle.remove()
        except:
            pass
        self.curText = event.artist.get_label()
        if self.x != None and self.y != None:
            #I'd rather do the following ALWAYS but it seems difficult to do in terms of keeping track of which arrays were plotted when multiple plots are present
            paramVal = N.take(self.y, [self.pickIndex])
            self.handleA.set_data(N.take(self.x, [self.pickIndex]), [paramVal])

        else:
            paramVal = event.mouseevent.ydata
            self.handleA.set_data([event.mouseevent.xdata], [paramVal])


        showText = '%s: %s'%(self.dataLabels[self.pickIndex],paramVal[0])
#        showText = '%s: %s'%self.dataLabels[self.pickIndex]
        self.textHandle = self.canvas.ax.text(0.03, 0.95, showText, fontsize=9,\
                                        bbox=dict(facecolor='yellow', alpha=0.1),\
                                        transform=self.canvas.ax.transAxes, va='top')
        self.handleA.set_visible(True)
        self.canvas.draw()

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
    w = MPL_Widget(enableAutoScale = False, doublePlot = False, enableEdit = True)
    x = N.arange(0, 20, 0.1)
    y = N.sin(x)*1E8
    y2 = N.cos(x)
    w.canvas.ax.plot(x, y)
#    w.canvas.ax.plot(x, y2)
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
