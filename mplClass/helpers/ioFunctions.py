import os, sys, traceback
from formlayout import fedit
import numpy as N
PYQT_OK = True
try:
    from PyQt4.QtGui import QMessageBox
except:
    PYQT_OK = False






class importDialog:
    def __init__(self, fileName, fileType = '.csv', delimiter = ',',
                 skiprows = 0, colRow = 0, transpose = False, parent = None):
        '''
        Class to provide parameters for import a csv file
        '''
        self.fileName = fileName
        self.fileType = fileType
        self.delimiter = delimiter
        self.skiprows = skiprows
        self.columnRow = colRow
        self.transpose = transpose
        self.parent = parent
        
        self.validDelimiterTypes = {}
        #FOR SOME REASON DUMMY VALUE IS NEEDED AS THE FIRST VALUE IS NOT TAKEN        
        self.validDelimiterTypes['DummyVal'] =''
        self.validDelimiterTypes['Comma'] =','
        self.validDelimiterTypes['Space'] = ' '
        self.validDelimiterTypes['Tab'] = '\t'
        commentTxt = '''If the "Column Header Row" or the\n"Rows to Skip" parameter is left\nat 0 then this value will be ignored.'''
        
        self.paramList = []
        self.paramList.append(('Delimiter Definition', self.validDelimiterTypes.keys()))
        self.paramList.append(('Column Header Row', self.columnRow))
        self.paramList.append(('Rows to Skip', self.skiprows))
        #self.paramList.append(('Transpose Data', self.transpose))
        
        self.colHeaders = None
        #icon=None, parent=None, apply=None
        self.importParams = fedit(self.paramList, title = "Define Import Parameters", comment = commentTxt,
                                  parent = self.parent)

    def getResult(self):
        if self.importParams != None:
            loadOk, colHeaders, dataList = self.loadData()
            return loadOk, colHeaders, dataList 
    
    def loadData(self):
        '''
        Load array into numpy arrays based upon the user defined definitions
        '''
        try:
            if self.importParams != None:
                '''
                fedit returns None if user cancels
                '''
                delimiter = self.validDelimiterTypes[self.importParams[0]]
                colRow = self.importParams[1]
                skipRows = self.importParams[2]
                #transpose = self.importParams[3]
                if skipRows != colRow:
                    '''
                    Yeah, yeah, I know this is ugly, but it is late...
                    '''
                    if skipRows == 0 and colRow > 0:
                        skipRows = colRow
                
                self.dataList = N.loadtxt(self.fileName, delimiter = delimiter, skiprows = skipRows, unpack = True)
                if colRow > 0:
                    f = open(self.fileName, 'r')
                    for i in xrange(colRow):
                        colHeaderLine = f.readline()
                    f.close()
                    tempColHeaders = colHeaderLine.splitlines()[0]
                    tempColHeaders = tempColHeaders.split(delimiter)
                    #Add file specific info to arrays
                    coreName = os.path.basename(self.fileName)
                    coreName = coreName.split('.')[0]
                    self.colHeaders = []
                    for col in tempColHeaders:
                        self.colHeaders.append('%s_%s'%(coreName, col))
                else:
                    #self.colHeaders = ['x']
                    coreName = os.path.basename(self.fileName)
                    coreName = coreName.split('.')[0]
                    self.colHeaders = []
                    for i in xrange(len(self.dataList)):
                        self.colHeaders.append('%s_%s'%(coreName,i+1))
                        
                
                return True, self.colHeaders, self.dataList
        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
            errorMsg = "Sorry: %s\n\n:%s\n%s\n\n"%(exceptionType, exceptionValue, exceptionTraceback)
            for val in traceback.format_stack()[:-1]:
                errorMsg +='%s\n'%val
            print errorMsg
            if self.parent != None and PYQT_OK:
                QMessageBox.warning(self.parent, "Load Data Error", errorMsg)

            return False, [], []
                
                
                
def openFig(fileName, figure, canvas, axes):
    print "OpenFig"
    
    title, xmin, xmax, xlabel, xscale, ymin, ymax, ylabel, yscale = general
    setFigProperties(axes, title, xmin, xmax, xlabel, xscale, ymin, ymax, ylabel, yscale)

    
    if has_curve:
        # Set / Curves
        for index, curve in enumerate(curves):
            line = linedict[curvelabels[index]]
            label, linestyle, linewidth, color, alpha,\
                marker, markersize, markerfacecolor, markeredgecolor = curve
                
            setLineProperties(line, label, linestyle, linewidth, color,\
                              alpha, marker, markersize, markerfacecolor,\
                              markeredgecolor)
    if has_collection:
        for index, collect in enumerate(collections):
            col = colDict[colLabels[index]]
            label, linestyle, linewidth, color, alpha = collect
            # collect
            setVLineProperties(col, label, linestyle, linewidth, str(color), alpha)
    
    # Redraw
    canvas.draw()


def saveFig(fileName, figure, canvas, axes):
    print "SaveFig"
    """Edit matplotlib figure options"""
    axes = axes
    sep = (None, None) # separator
    
    has_curve = len(axes.get_lines())>0
    has_collection = len(axes.collections)>0
    
    # Get / General
    xmin, xmax = axes.get_xlim()
    ymin, ymax = axes.get_ylim()
    general = [('Title', axes.get_title()),
               sep,
               (None, "<b>X-Axis</b>"),
               ('Min', xmin), ('Max', xmax),
               ('Label', axes.get_xlabel()),
               ('Scale', [axes.get_xscale(), 'linear', 'log']),
               sep,
               (None, "<b>Y-Axis</b>"),
               ('Min', ymin), ('Max', ymax),
               ('Label', axes.get_ylabel()),
               ('Scale', [axes.get_yscale(), 'linear', 'log'])
               ]

    if has_curve:
        # Get / Curves
        linedict = {}
        for line in axes.get_lines():
            label = line.get_label()
            if label == '_nolegend_':
                continue
            linedict[label] = line
        curves = []
        linestyles = LINESTYLES.items()
        markers = MARKERS.items()
        curvelabels = sorted(linedict.keys())
        for label in curvelabels:
            line = linedict[label]
            curvedata = [
                         ('Label', label),
                         sep,
                         (None, '<b>Line</b>'),
                         ('Style', [line.get_linestyle()] + linestyles),
                         ('Width', line.get_linewidth()),
                         ('Color', getMPLColor(line.get_color())),
                         ('Alpha', line.get_alpha()),
                         sep,
                         (None, '<b>Marker</b>'),
                         ('Style', [line.get_marker()] + markers),
                         ('Size', line.get_markersize()),
                         ('Facecolor', getMPLColor(line.get_markerfacecolor())),
                         ('Edgecolor', getMPLColor(line.get_markeredgecolor()))
                         ]
            curves.append([curvedata, label, ""])
        
    if has_collection:
        colDict = {}
        for col in axes.collections:
            label = col.get_label()
            if label == '_nolegend_':
                continue
            colDict[label] = col
        collections = []
        linestyles = LINESTYLES.items()
        colLabels = sorted(colDict.keys())
        for label in colLabels:
            col = colDict[label]
            colData = [
                       ('Label', label),
                       sep,
                       (None, '<b>Line</b>'),
                       #('Style', [col.get_linestyle()] + linestyles),#Ignoring as this is returning None
                       ('Style', ['Solid'] + linestyles),
                       ('Width', col.get_linewidth()[0]),#because it returns a tuple
                       ('Color', getMPLColor(col.get_color()[0].tolist())),
                       ('Alpha', col.get_alpha())                       
                       ]
            collections.append([colData, label, ""])
        
    datalist = [(general, "Axes", "")]    
    if has_curve:
        datalist.append((curves, "Curves", ""))
    if has_collection:
        datalist.append((collections, "Lines", ""))        

    return general, curves, collections             
        


if __name__ == "__main__":
    from PyQt4 import QtGui
    #app = QtGui.QApplication(sys.argv)
    importDialog('test.csv')
    sys.exit()
