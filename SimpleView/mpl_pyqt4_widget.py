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
        ############### Add Actions ################
                
        self.Zoom = QtGui.QAction("Zoom",  self)
        self.Zoom.setShortcut("Ctrl+Z")
        self.addAction(self.Zoom)
        QtCore.QObject.connect(self.Zoom,QtCore.SIGNAL("triggered()"), self.ZoomToggle)
        
        self.actionAutoScale = QtGui.QAction("AutoScale",  self)#self.MainWindow)
        self.actionAutoScale.setShortcut("Ctrl+A")
        self.addAction(self.actionAutoScale)
        QtCore.QObject.connect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)
        ##############################################
        ########### Misc Code #########################        
                
#        self.span = SpanSelector(self.canvas.ax, self.onselect, 'horizontal', 
#                        useblit=True, rectprops=dict(alpha=0.5, facecolor='#C6DEFF') )
#                          
#        self.span.visible = False
#        self.hZoom = False
#    def hZoomToggle(self):
#        if self.hZoom:
#            self.hZoom = False
#            self.span.visible = False
#        else:
#            self.hZoom = True
#            self.span.visible = True
#    
#    def onselect(self, xmin, xmax):
#        #print xmin,  xmax
#        if self.hZoom:
#            self.canvas.ax.set_xlim(xmin,  xmax)
#            self.canvas.ax.autoscale_view(scalex=False)
#            #x values provided, need to get indices for y values
#            self.canvas.draw()
#            
##        if self.zoomWasTrue:
##            #self.hZoomToggle()
##            self.hZoom = True
##            self.span.visible = True
        #########  Index Picker  ###############################
#        self.indexA = 0
#        self.indexB = 0
#        self.selectHandleA,  = self.ui.mpl_widget.canvas.ax.plot([0], [0], 'o',\
#                                        ms=8, alpha=.4, color='yellow', visible=False,  label = 'Cursor A')
#        self.selectHandleB,  = self.ui.mpl_widget.canvas.ax.plot([0], [0], 's',\
#                                        ms=8, alpha=.4, color='green', visible=False,  label = 'Cursor B')
#
#        self.ui.handleActionA = QAction("Cursor A", self)
#        self.ui.mpl_widget.addAction(self.ui.handleActionA)
#        
#        self.ui.handleActionB = QAction("Cursor B", self)
#        self.ui.mpl_widget.addAction(self.ui.handleActionB)
#        
#        self.ui.cursorClear = QAction("Clear Cursors",  self)
#        self.ui.mpl_widget.addAction(self.ui.cursorClear)
#
#        self.connect(self.ui.handleActionA,SIGNAL("triggered()"),
#                     self.SelectPointsA)
#        self.connect(self.ui.handleActionB,SIGNAL("triggered()"),
#                     self.SelectPointsB)
#        self.connect(self.ui.cursorClear,SIGNAL("triggered()"),
#                     self.cursorClear)                     
#   def cursorClear(self):
#        if self._cidPlotA:
#            self.selectHandleA.set_visible(False)
#            self.ui.mpl_widget.canvas.mpl_disconnect(self._cidPlotA)
#            self._cidPlotA = None
#            self.mplPickPointsA = False
#            self.ui.lineEdit_R.setText('')
#        
#        if self._cidPlotB:
#            self.selectHandleB.set_visible(False)
#            self.ui.mpl_widget.canvas.mpl_disconnect(self._cidPlotB)
#            self._cidPlotB = None
#            self.mplPickPointsB = False
#            self.ui.lineEdit_L.setText('')
#        
#        #print "cidA ", self._cidPlotA
#        #print "cidB ", self._cidPlotB
#        self.ui.mpl_widget.canvas.draw()
#        
#    def cursorStats(self):
#        if self._cidPlotA and self._cidPlotB:
#            self.dx = self.cursorAInfo[1]-self.cursorBInfo[1]
#            self.dy = self.cursorAInfo[2]-self.cursorBInfo[2]
#            cursorAText = 'point: %i\tx: %f\ty: %f\tdx: %f\t%s' % (self.cursorAInfo[0], self.cursorAInfo[1], self.cursorAInfo[2], self.dx, self.cursorAInfo[3])
#            cursorBText = 'point: %i\tx: %f\ty: %f\tdy: %f\t%s' % (self.cursorBInfo[0], self.cursorBInfo[1], self.cursorBInfo[2],  self.dy,  self.cursorBInfo[3])
#            self.ui.lineEdit_R.setText(cursorAText)
#            self.ui.lineEdit_L.setText(cursorBText)
#            return True
#        if self._cidPlotA:
#            cursorAText = 'point: %i\tx: %f\ty: %f\t%s' % (self.cursorAInfo[0], self.cursorAInfo[1], self.cursorAInfo[2], self.cursorAInfo[3])
#            self.ui.lineEdit_R.setText(cursorAText)
#        if self._cidPlotB:
#            cursorBText = 'point: %i\tx: %f\ty: %f\t%s' % (self.cursorBInfo[0], self.cursorBInfo[1], self.cursorBInfo[2],  self.cursorBInfo[3])
#            self.ui.lineEdit_L.setText(cursorBText)
#            
#    def SelectPointsA(self):
#        """
#        This method will be called from the plot context menu for 
#        selecting points
#        """
#        #ico1 = QtGui.QIcon("graphics/tick2.png")
#        #ico2 = QtGui.QIcon("")
#        if self._cidPlotB:
#            self.ui.mpl_widget.canvas.mpl_disconnect(self._cidPlotB)
#            self.mplPickPointsB = False         
#        if not self.mplPickPointsA:
#            self._cidPlotA = self.ui.mpl_widget.canvas.mpl_connect('pick_event', self.OnPickA)
#        else:
#            self.ui.mpl_widget.canvas.draw()
#        
#
#    def SelectPointsB(self):
#        if self._cidPlotA != None:
#            self.ui.mpl_widget.canvas.mpl_disconnect(self._cidPlotA)
#            self.mplPickPointsA = False
#        if not self.mplPickPointsB:
#            self._cidPlotB = self.ui.mpl_widget.canvas.mpl_connect('pick_event', self.OnPickB)
#        else:
#            self.ui.mpl_widget.canvas.draw()
#        
#    def OnPickA(self, event):
#        """
#        This is the pick_event handler for matplotlib
#        This is the pick_event handler for matplotlib
#        This method will get the coordinates of the mouse pointer and
#        finds the closest point and retrieves the corresponding peptide sequence.
#        Also draws a yellow circle around the point.--from Ashoka 5/29/08
#        """
#        if not isinstance(event.artist, Line2D): 
#            return True
#         
#        line = event.artist
#        xc = event.mouseevent.xdata
#        yc = event.mouseevent.ydata
#        xdata = line.get_xdata()
#        ydata = line.get_ydata()
#        maxd = 0.05
#        if xc and yc:
#            distances = N.hypot(xdata-xc, ydata-yc)
#        else:
#            distances = N.hypot(xdata, ydata)
#        
#        self.indexA = distances.argmin()
#        self.selectHandleA.set_visible(True)
#        self.selectHandleA.set_data([xdata[self.indexA]], [ydata[self.indexA]])
#        self.cursorAInfo[0]=self.indexA
#        self.cursorAInfo[1]=xdata[self.indexA]
#        self.cursorAInfo[2]=ydata[self.indexA]
#        self.cursorAInfo[3]=line.get_label()
#        self.cursorStats()
#        
#        self.ui.mpl_widget.canvas.draw()
#        print "Pick A"
#
#    def OnPickB(self, event):
#            if not isinstance(event.artist, Line2D): 
#                return True
#             
#            line = event.artist
#            xc = event.mouseevent.xdata
#            yc = event.mouseevent.ydata
#            xdata = line.get_xdata()
#            ydata = line.get_ydata()
#            maxd = 0.05
#            if xc and yc:
#                distances = N.hypot(xdata-xc, ydata-yc)
#            else:
#                distances = N.hypot(xdata, ydata)#event.mouseevent.xdata, ydata-event.mouseevent.ydata)
#        
#            self.indexB = distances.argmin()
#            self.selectHandleB.set_visible(True)
#            self.selectHandleB.set_data([xdata[self.indexB]], [ydata[self.indexB]])
#            self.cursorBInfo[0]=self.indexB
#            self.cursorBInfo[1]=xdata[self.indexB]
#            self.cursorBInfo[2]=ydata[self.indexB]
#            self.cursorBInfo[3]=line.get_label()
#            self.cursorStats()
#        
#            self.ui.mpl_widget.canvas.draw()
        ###############################



    def ZoomToggle(self):
        #print "Zoom",  self.test
        #self.test+=1
        self.toolbar.zoom()
        
    def autoscale_plot(self):
        #print "AutoScale",  self.test
        #self.test+=1
        self.toolbar.home()
        

def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    w = MPL_Widget()
    w.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
