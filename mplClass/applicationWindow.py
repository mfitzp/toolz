"""
    Copyright (c) 2010 Jose Roquette <josertt@gmail.com>
    
    This file is part of plotalot.

    plotalot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    plotalot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with plotalot.  If not, see <http://www.gnu.org/licenses/>.
    
    
    TODO:   Set vlines color is not working correctly
            Circle collection is not editible
            vlines not handled by xml load function
            Add case for multiple axes....
            Handle Legend
            mplAx3D would also be cool
            scatter vs. mplAx3D vs. line2D
            Error bars
            bar plots for histograms
            on xml load?
                x and y labels #Font size is not loading
            Scripting addition
            Add dataDict functionality for application of scripts
            
"""

from PyQt4 import QtGui, QtCore
import csv
import sys
import os
import numpy as N

from mplPyQt4Class import MPL_WIDGET
#from dataDict import dataSet
from helpers.ioFunctions import importDialog
from helpers.figureOptions import figure_edit, setVLines, editTexts
from helpers.customListWidget import DictTreeWidget

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from mplXML import xml2fig, fig2xml
#~ from edit_dialogs import LegendDialog, ColorsLinesDialog, TitleLabelsDialog, \
                         #~ ChooseSignalsPlot
#~ from definitions_utils import symbols, colors
#~ 
#~ 

DEBUG = False

class PLOT_WIDGET(MPL_WIDGET):
    def __init__(self, parent = None, enableAutoScale = False, parentCallBack = None):
        MPL_WIDGET.__init__(self, parent, enableAutoScale)
        self.setAcceptDrops(True)
        self.curMimeData = None
        self.callback = parentCallBack
        self.resetEventHandler()
        self.clickCount = 0

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        '''
        This appears to work on Ubuntu, other OSes?
        problem with path separators?
        '''
        fileStr = str(event.mimeData().text())
        fileStr = fileStr.split("file://")[1]
        fileStr = fileStr.split("\r\n")[0]
        if os.path.isfile(fileStr):
            if self.callback != None:
                self.callback(fileStr)

    def onclick(self, event):
        #THIS IS BEING CALLED TWICE...WHY??????????
        if self.clickCount == 0:
            self.clickCount = 1
            return
        if event.xdata != None and event.button == 3:#right click button
            print "OK"
            self.canvas.ax.text(event.xdata, event.ydata, '%f, %f'%(event.xdata, event.ydata), fontsize = 5)
            #print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(event.button, event.x, event.y, event.xdata, event.ydata)
            self.canvas.draw()
            self.clickCount = 0

    def resetEventHandler(self):
        self.cid = self.canvas.mpl_connect('button_release_event', self.onclick)


class ApplicationWindow(QtGui.QMainWindow):
    """
    This is the main application window
    """

    def __init__(self, fileName = None):
        self.initOK=False#record keeping for first load
        self.mainWindow()
        self.fileName = fileName
        if os.path.isfile(self.fileName):
            self.filePlot()
        self.setVars()
        
    def mainWindow(self):
        """
        Define the widgets of the main window
        """
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Data Plot")

        # Create the menus
        self.file_menu = QtGui.QMenu('&File', self)
        #~ self.file_menu.addAction('&Plot', self.filePlot,
                                 #~ QtCore.Qt.CTRL + QtCore.Qt.Key_P)
        self.file_menu.addAction('Open &CSV', self.getCSVFileName,
                                 QtCore.Qt.CTRL + QtCore.Qt.SHIFT +QtCore.Qt.Key_O)
        self.file_menu.addAction('&Open Session', self.openSession,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_O)
        self.file_menu.addAction('&Save Session', self.savePlot,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)
        
        
        self.edit_menu = QtGui.QMenu('&Edit', self)
        self.edit_menu.addAction('&Figure Options', self.editFigure,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_F)
        self.edit_menu.addAction('&Text Options', self.editText,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_T)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction('&Plot Loaded Data', self.plotLoadedData,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_P)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction('Toggle &Vertical Lines', self.toggleVLines,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_V)
        self.edit_menu.addSeparator()
        self.edit_menu.addSeparator()
        self.edit_menu.addAction('Clear Figure', self.clearFigure, QtCore.Qt.CTRL + QtCore.Qt.Key_Escape)        
        #~ self.edit_menu.addAction('&Legend', self.editLegend,
                                 #~ QtCore.Qt.CTRL + QtCore.Qt.Key_L)
        #~ self.edit_menu.addAction('Line colors and &style', self.editLineColorsStyle,
                                 #~ QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        #~ self.edit_menu.addAction('&Choose signals to plot', self.editChooseSignalsPlot,
                                 #~ QtCore.Qt.CTRL + QtCore.Qt.Key_C)
        self.menuBar().addMenu(self.edit_menu)
        self.edit_menu.setEnabled(False)

        self.help_menu = QtGui.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)
        #~ self.help_menu.addAction('&Open Embedded Terminal', self.openShell)

        self.statusBar().showMessage("Ready", 2000)
    
    
    def plotLoadedData(self):
        if len(self.dataDict)>0:
             dialogWindow = DictTreeWidget(self.dataDict, returnCall = self.dialogReturnCall, parent = self)
             #NOT SURE IF THE DIALOGWINDOWS CONTAINER IS NEEDED
             #self.dialogWindows['dataSelect'] = dialogWindow
             dialogWindow.show()
    
    def dialogReturnCall(self, customObj):
        print type(customObj)
        print customObj
    
    def clearFigure(self):
        if self.initOK:
            self.mplAx.clear()
            self.canvas.format_labels()
            self.canvas.draw()
    
    def dragNdropCall(self, input):
        if ".csv" in input:
            self.loadCSV(input)
            self.statusBar().showMessage("File: %s loaded"%input, 5000)
        elif ".gz" in input:
            print input
            self.processMPLXML(input)
            self.statusBar().showMessage("File: %s loaded"%input, 5000)
            
    def processMPLXML(self, fileName):
        print "processMPLXML", fileName
        nf = xml2fig.XMLFigure(fileName, standAlone = False)
        xmlAxes = nf.axlist
        #Need to update mplPyQt4Class to handle multiple axes....
        self.mplAx.cla()
        for xmlAx in xmlAxes:
            nf._update_axes(xmlAx, self.mplAx)
            nf._add_texts(xmlAx, self.mplAx)
            nf._add_collecions(xmlAx, self.mplAx)#need to add return vals
            nf._add_lines(xmlAx, self.mplAx)#need to add return vals        
        
        self.canvas.xtitle = self.mplAx.get_xlabel()
        self.canvas.ytitle = self.mplAx.get_ylabel()
        #Need to add a way to get acutal data into dataDict
        self.canvas.format_labels()
        self.canvas.draw()
        self.edit_menu.setEnabled(True)
        
        
    def setVars(self):
        '''
        Set mainwindow variables
        '''
        self.curDir = os.getcwd()
        self.dataDict = {}#dataSet()
        self.xValues = None
        self.yValues = []
        self.firstPlot = True
        self.vlinesBool = False
        
        if self.firstPlot:
            self.resize(700, 500)
            self.plotWidget = PLOT_WIDGET(self, enableAutoScale = True, parentCallBack = self.dragNdropCall)
            self.canvas = self.plotWidget.canvas
            self.mplAx = self.plotWidget.canvas.ax
            self.firstPlot = False
            
            self.plotWidget.setFocus()
            self.setCentralWidget(self.plotWidget)
            self.fileName = ""
        
        
        self.dialogWindows = {}#container to hold references to open dialogs
        
        self.initOK = True
    
    def toggleVLines(self):
        if self.vlinesBool:
            self.vlinesBool = False
        else:
            self.vlinesBool = True
            
        setVLines(self.canvas, self.mplAx, self.vlinesBool)
    
    def openSession(self):
        '''
        Open a previously saved plot using y-serial that is compressed in a gzip file
        '''
        print "Open Session"

    def __setDir__(self, fileName):
        if os.path.isfile(fileName):
            self.curDir = os.path.dirname(fileName)
        else:
            self.curDir = os.getcwd()
    
    def getCSVFileName(self):
        '''
        Open a csv file
        '''
        self.fileName = str(QtGui.QFileDialog.getOpenFileName(None, "Open Data File (csv)", self.curDir, "*.csv"))
        if self.fileName != None:
            if os.path.isfile(self.fileName):
                self.__setDir__(self.fileName)
                self.loadCSV(self.fileName)
    
    def loadCSV(self, fileName):
        loadDialog = importDialog(fileName, parent = self)
        boolLoad, colHeaders, dataList = loadDialog.getResult()
        if boolLoad:
            self.populateData(colHeaders, dataList)
            self.plotData(colHeaders)
            
    def populateData(self, colHeaders, dataList):
        self.colHeaders = colHeaders
        for i,dataKey in enumerate(self.colHeaders):
            self.dataDict[dataKey] = dataList[i]
                    
    
    def savePlot(self):
        '''
        Save existing axis as a gzipped serialized xml object for future use....
        '''
        self.fileName = str(QtGui.QFileDialog.getSaveFileName(None, "Save Figure:", self.curDir, "*.xml.gz"))
        if self.fileName:
            if self.fileName.split('.xml.')[-1] != 'gz':
                dirName = os.path.dirname(self.fileName)
                base = os.path.basename(self.fileName)
                base = base.split('.')[0]
                base += '.xml.gz'
                self.fileName = os.path.join(dirName, base)
            self.__setDir__(self.fileName)
            xmlFig = fig2xml.Figure2XML(self.canvas.fig)
            xmlStr = xmlFig.saveXML(self.fileName)        

    def fileQuit(self):
        """Quit the program"""
        self.close()
        
    def plotData(self, dataLabels):
        """
        plot the data using matplotlib 
        """
        self.mplAx.cla()
            
        #~ for i in range(0, len(self.yValues)):
            #~ self.mplAx.plot(self.xValues, self.yValues[i])#, linewidth=self.list_line_width[i])
            
        xVals = self.dataDict[dataLabels[0]]
        yVals = []

        for j in xrange(1, len(dataLabels)):
            yVals.append(self.dataDict[dataLabels[j]])
        
        for i in xrange(len(yVals)):
            self.mplAx.plot(xVals, yVals[i])
        
        self.plotWidget.canvas.format_labels()                       
        
        # Now is possible to use the edit menu
        self.edit_menu.setEnabled(True)
        
        if not self.firstPlot:
            self.plotWidget.canvas.draw()     
        
    def editFigure(self):
        #FIX ME
        #THIS CAN RETURN NONE IF NO LINES ARE PRESENT
        general, curves, collections = figure_edit(self.canvas, self.mplAx)
        #print collections
        #~ print general, curves
        #~ ###
        #~ saveDB = y_serial.Main(os.path.join(os.getcwd(),'plot.sqlite'))
        #~ saveDB.insert(general, "#plan agent007 #london", 'generalParams')
        #~ saveDB.insert(curves, "#plan agent007 #london", 'curves')
        #~ saveDB.insert(self.xValues, "#plan agent007 #london", 'rawData')
        #~ ###
    
    def editText(self):
        '''
        Need to account for case with multiple axes
        '''
        editTexts(self.canvas, self.mplAx)
    
    def editTitleLabels(self):
        """
        Calls the dialog to edit the titles and axes labels
        """
        labels_dialog = TitleLabelsDialog(self.title, self.x_label, self.y_label)
        
        new_title, new_xlabel, new_ylabel = labels_dialog.run()
        
        if new_title != None:
            self.title = new_title
            self.x_label = new_xlabel
            self.y_label = new_ylabel
            self.ax.set_xlabel(self.x_label)
            self.ax.set_ylabel(self.y_label)
            self.ax.set_title(self.title)
            self.canvas.draw()
        
    def editLegend(self):
        """
        Call the dialog that allows to edit the legend for the various signals
        """
        legend_dialog = LegendDialog(self.location_code, self.legend_names)
        
        new_location_code, new_legend_names = legend_dialog.run()
        
        if new_location_code != self.location_code and new_location_code != -1:
            self.location_code = new_location_code

        if new_location_code != -1:
            self.legend_names = new_legend_names
            # Determine which signals to put in legend
            curr_legend_names = []
            for i in range(0, len(self.list_signal_is_to_plot)):
                if self.list_signal_is_to_plot[i]:
                    curr_legend_names.append(self.legend_names[i])
            self.ax.legend(curr_legend_names, self.location_code)
            self.canvas.draw()
    
    
    def editLineColorsStyle(self):
        """
        Change the color and line styles for the signals
        """
        colors_style_dialog = ColorsLinesDialog(self.list_colors_plot, self.list_symbols_plot, self.list_line_width)
        new_list_colors_plot, new_list_symbols_plot, new_list_line_width = colors_style_dialog.run()
        
        if new_list_colors_plot != None:
            self.list_colors_plot = new_list_colors_plot
            self.list_symbols_plot = new_list_symbols_plot
            self.list_line_width = new_list_line_width
            self._reDrawPlot()
            
            
    def editChooseSignalsPlot(self):
        """
        Choose the signals that are going to be in the plot
        """
        choose_signals_to_plot = ChooseSignalsPlot(self.list_signal_is_to_plot)
        new_signals_to_plot = choose_signals_to_plot.run()
        
        if new_signals_to_plot != None:
            self.list_signal_is_to_plot = new_signals_to_plot
            self._reDrawPlot()
        

    def about(self):
        """Program about"""
        msg =  'Front-End in PyQt4 for Matplotlib -- 0.2 Alpha Version\n'
        msg += 'Based upon plotalot originally by Jose Roquette <josertt@gmail.com>. '
        msg += 'Modified by Brian Clowers <bhclowers@gmail.com> to include formlayout'
        msg += 'dialogs similar to PyDee aka Spyder.  Additional improvements include'
        msg += 'drag-N-drop for csv files and compressed xml.gz files.'
        QtGui.QMessageBox.about(self, "About plotalot", msg)


# Utils
def which(program):
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None



def embed_ipython(w):
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed(user_ns = dict(w = w))
    ipshell()


if __name__ == "__main__":
    qApp = QtGui.QApplication(sys.argv)
    
    #~ # Determine if we can use Latex or not for text
    #~ if which('dvipng') != None:
        #~ #rc('text', usetex=True)
        #~ #rc('font', family='serif')
        #~ rc('axes', labelsize=10)
        #~ rc('font', size=10)
        #~ rc('legend', fontsize=10)
        #~ rc('xtick', labelsize=8)
        #~ rc('ytick', labelsize=8) 
        #~ rc('text', usetex=True)
    #~ else:
        #~ QtGui.QMessageBox.warning(None, "TeX support disabled", "Missing dvipng")

    if len(sys.argv) < 2:
        fileName = ""
    elif len(sys.argv) == 2:
        fileName = sys.argv[1]
    else:
        QtGui.QMessageBox.critical(None, "Missing File", "The file to parse was not provided.")
        exit(-1)
    aw = ApplicationWindow(fileName)
    aw.setWindowTitle("plotalot")
    aw.show()
    if DEBUG:
        embed_ipython(aw)
    sys.exit(qApp.exec_())
