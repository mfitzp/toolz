#!/usr/bin/env python

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from matplotlib.lines import Line2D

import ui_Plot_Options

line_styles = dict(Solid = '-',\
                    Dashed = '--', \
                    DashDot = '-.',\
                    Dotted = ':',\
                    Steps = 'steps', \
                    none = 'None')

marker_styles = dict(none = 'None',\
                    circles = 'o',\
                    triangle_up = '^',\
                    triangle_down  = 'v',\
                    triangle_left  = '<',\
                    triangle_right  = '>',\
                    square  = 's',\
                    plus  = '+',\
                    cross  = 'x',\
                    diamond  = 'D',\
                    thin_diamond  = 'd',\
                    tripod_down  = '1',\
                    tripod_up  = '2',\
                    tripod_left  = '3',\
                    tripod_right  = '4',\
                    hexagon  = 'h',\
                    rotated_hexagon  = 'H',\
                    pentagon  = 'p',\
                    vertical_line  = '|',\
                    horizontal_line  = '_',\
                    dots = '.')

lineColorDict = {'b':'#0000ff', 'g':'#00ff00','r':'#ff0000','c':'#ff00ff','m':'#ff00ff','y':'#ffff00','k':'#000000','w':'#ffffff'}


class Plot_Options_Dialog(QDialog, ui_Plot_Options.Ui_Plot_Options_Dialog):
    def __init__(self, activeTraces = None, curAx = None, parent = None):
        super(Plot_Options_Dialog, self).__init__(parent)
        self.setupUi(self)

        self.parent = None
        self.curAx = curAx
        if parent != None:
            self.parent = parent

        self.plotTitle = "Plot Title"
        self.plotTitle = self.curAx.get_title()
        self.xmin = 0.0
        self.xmax = 10.0
        self.xmin, self.xmax = self.curAx.get_xlim()
        self.xtitle = "X-Axis"
        self.xtitle = self.curAx.get_xlabel()

        self.ymin = 0.0
        self.ymax = 20.0
        self.ymin, self.ymax = self.curAx.get_ylim()
        self.ytitle = "Y-Axis"
        self.ytitle = self.curAx.get_ylabel()

        self.activeplots = activeTraces


        self.connect(self.plottitle_lineEdit, SIGNAL("textEdited(QString)"), self.setPlotTitle)

        self.connect(self.xmin_lineEdit, SIGNAL("editingFinished()"), self.setXMin)
        self.connect(self.xmax_lineEdit, SIGNAL("editingFinished()"), self.setXMax)
        self.connect(self.xlabel_lineEdit, SIGNAL("textEdited(QString)"), self.setXLabel)

        self.connect(self.ymin_lineEdit, SIGNAL("editingFinished()"), self.setYMin)
        self.connect(self.ymax_lineEdit, SIGNAL("editingFinished()"), self.setYMax)
        self.connect(self.ylabel_lineEdit, SIGNAL("textEdited(QString)"), self.setYLabel)

        self.connect(self.activePlotListWidget, SIGNAL("itemClicked(QListWidgetItem *)"), self.getPlotItem)
        self.connect(self.mstyle_comboBox, SIGNAL("currentIndexChanged(QString)"), self.setMStyle)
        self.connect(self.ms_spinBox, SIGNAL("valueChanged(double)"), self.setMSize)
        self.connect(self.lstyle_comboBox, SIGNAL("currentIndexChanged(QString)"), self.setLStyle)
        self.connect(self.lw_spinBox, SIGNAL("valueChanged(double)"), self.setLWidth)
        self.connect(self.lineColorBtn, SIGNAL("colorChanged(QColor)"), self.setLColor)
        self.connect(self.markerColorBtn, SIGNAL("colorChanged(QColor)"), self.setMColor)

        self.connect(self.logx_cb, SIGNAL("stateChanged(int)"), self.setLogX)
        self.connect(self.logy_cb, SIGNAL("stateChanged(int)"), self.setLogY)
        self.connect(self.toggleGrid_btn, SIGNAL("clicked()"), self.setGrid)

        self.populate_dialog()

    def setLogX(self, cbState):
        if cbState == 2:
            self.curAx.set_xscale('log')
        elif cbState == 0:
            self.curAx.set_xscale('linear')

    def setLogY(self, cbState):
        if cbState == 2:
            self.curAx.set_yscale('log')
        elif cbState == 0:
            self.curAx.set_yscale('linear')

    def setGrid(self):
        self.curAx.grid()

    def setPlotTitle(self, label):
        label = str(label)#convert from QString
        self.plotTitle = label
        self.curAx.set_title(label)

    def setXLabel(self, label):
        label = str(label)#convert from QString
        try:
            self.parent.plotWidget.canvas.xtitle = label
        except:
            self.parent.canvas.xtitle = label
        self.xtitle = label
        self.curAx.set_xlabel(label)

    def setYLabel(self, label):
        label = str(label)#convert from QString
        try:
            self.parent.plotWidget.canvas.ytitle = label
        except:
            self.parent.canvas.ytitle = label
        self.ytitle = label
        self.curAx.set_ylabel(label)

    def setXMin(self, val=None):
        if val is None:
            val = self.xmin_lineEdit.text()
        try:
            val = float(str(val))
            self.curAx.set_xlim(xmin=val)
            self.xmin = val
        except:
            msg = "Must Enter a Number for the Minimum Value"
            return QMessageBox.information(self, "Property Error", msg)
            self.curAx.set_xlim(xmin=self.xmin)
#            self.xmin_lineEdit.setText(str(self.xmin))

    def setXMax(self, val=None):
        if val is None:
            val = self.xmax_lineEdit.text()
        try:
            val = float(str(val))
            self.curAx.set_xlim(xmax=val)
            self.xmax = val
        except:
            msg = "Must Enter a Number for the Maximum Value"
            return QMessageBox.information(self, "Property Error", msg)
            self.curAx.set_xlim(xmax=self.xmax)

    def setYMin(self, val = None):
        if val is None:
            val = self.ymin_lineEdit.text()
        try:
            val = float(str(val))
            self.curAx.set_ylim(ymin=val)
            self.ymin = val
        except:
            msg = "Must Enter a Number for the Minimum Value"
            return QMessageBox.information(self, "Property Error", msg)
            self.curAx.set_ylim(ymin=self.ymin)

    def setYMax(self, val = None):
        if val is None:
            val = self.ymax_lineEdit.text()
        try:
            val = float(str(val))
            self.curAx.set_ylim(ymax=val)
            self.ymax = val
        except:
            msg = "Must Enter a Number for the Maximum Value"
            return QMessageBox.information(self, "Property Error", msg)
            self.curAx.set_ylim(ymax=self.ymax)

    def setMSize(self, value):
        #print "Set Marker Size"
        if self.activePlotListWidget.currentItem():
            activeLine = self.getPlotItem(self.activePlotListWidget.currentItem())
            activeLine.set_markersize(value)
            self.setupLineOptions(activeLine)

    def setMStyle(self, value):
        #print "Set Marker Style"
        if self.activePlotListWidget.currentItem():
            activeLine = self.getPlotItem(self.activePlotListWidget.currentItem())
            activeLine.set_marker(marker_styles.get(str(value)))#need to set value to str as it is QString
            self.setupLineOptions(activeLine)

    def setMColor(self, QColor):
        if self.activePlotListWidget.currentItem():
            activeLine = self.getPlotItem(self.activePlotListWidget.currentItem())
            #print str(QColor.name())
            activeLine.set_markerfacecolor(str(QColor.name()))#need to set value to str as it is QString
            self.setupLineOptions(activeLine)

    def setLWidth(self, value):
        #print "Set L Width"
        if self.activePlotListWidget.currentItem():
            activeLine = self.getPlotItem(self.activePlotListWidget.currentItem())
            activeLine.set_linewidth(value)
            self.setupLineOptions(activeLine)

    def setLStyle(self, value):
        #print "Set Line Style"
        if self.activePlotListWidget.currentItem():
            activeLine = self.getPlotItem(self.activePlotListWidget.currentItem())
            activeLine.set_linestyle(line_styles.get(str(value)))#need to set value to str as it is QString
            self.setupLineOptions(activeLine)

    def setLColor(self, QColor):
        if self.activePlotListWidget.currentItem():
            activeLine = self.getPlotItem(self.activePlotListWidget.currentItem())
            #print str(QColor.name())
            activeLine.set_color(str(QColor.name()))#need to set value to str as it is QString
            self.setupLineOptions(activeLine)

    def getPlotItem(self, item):
        linePlotItem = self.activeplots.get(str(item.text()))
        self.setupLineOptions(linePlotItem)
        return linePlotItem

    def getKey(self, dict, value):
        for key, val in dict.items():
            if val == value:
                return key

    def setupLineOptions(self, lineInstance):

        match_index = self.mstyle_comboBox.findText(self.getKey(marker_styles, lineInstance.get_marker()))
        self.mstyle_comboBox.setCurrentIndex(match_index)

        ls = lineInstance.get_linestyle()
        key = self.getKey(line_styles, lineInstance.get_linestyle())

        match_index = self.lstyle_comboBox.findText(str(key))
        self.lstyle_comboBox.setCurrentIndex(match_index)

        self.lw_spinBox.setValue(lineInstance.get_linewidth())
        self.ms_spinBox.setValue(lineInstance.get_markersize())

        if lineInstance.get_color() is None:
            pass
        else:
            lcolor = lineInstance.get_color()
            print "Line Color 1", lcolor, type(lcolor)
            if lineColorDict.has_key(lcolor):
                lcolor = lineColorDict.get(lineInstance.get_color())
            #lcolor = QColor(lineInstance.get_color())
            print "Line Color 2", lcolor
            self.lineColorBtn.setColor(QColor(lcolor))

        if lineInstance.get_markerfacecolor() is None:
            pass
        else:
            mcolor = lineInstance.get_markerfacecolor()
            if lineColorDict.has_key(mcolor):
                mcolor = lineColorDict.get(lineInstance.get_markerfacecolor())
            self.markerColorBtn.setColor(QColor(mcolor))

    def populate_dialog(self):
        #populate first tab
        self.plottitle_lineEdit.setText(self.plotTitle)

        #Keeping the axis limits as strings
        #to avoid any problems with the min and maximum of the QT Dialog
        self.xmin_lineEdit.setText(str(self.xmin))
        self.xmax_lineEdit.setText(str(self.xmax))
        self.xlabel_lineEdit.setText(self.xtitle)

        self.ymin_lineEdit.setText(str(self.ymin))
        self.ymax_lineEdit.setText(str(self.ymax))
        self.ylabel_lineEdit.setText(self.ytitle)

        xScale = self.curAx.get_xscale()
        if xScale == 'linear':
            self.logx_cb.setCheckState(Qt.Unchecked)
        elif xScale == 'log':
            self.logx_cb.setCheckState(Qt.Checked)

        yScale = self.curAx.get_yscale()
        if yScale == 'linear':
            self.logy_cb.setCheckState(Qt.Unchecked)
        elif yScale == 'log':
            self.logy_cb.setCheckState(Qt.Checked)


        #populate second tab
        self.lstyle_comboBox.addItems(line_styles.keys())
        self.mstyle_comboBox.addItems(marker_styles.keys())
        if self.activeplots is not None and type(self.activeplots) is dict:
            activeList = self.activeplots.keys()
            for i,activeLine in enumerate(activeList):
                if activeLine == '_nolegend_':
                    activeList.pop(i)
            activeList.sort()
            if len(activeList) > 0:
                self.activePlotListWidget.addItems(activeList)
                self.activePlotListWidget.setCurrentRow(0)
                self.getPlotItem(self.activePlotListWidget.currentItem())


if __name__ == "__main__":
    dialog = QApplication(sys.argv)
    mydialog = Plot_Options_Dialog()
    mydialog.show()
    sys.exit(dialog.exec_())
