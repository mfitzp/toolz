# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\d3p483\workspace\NoiseProject\Plot_Options.ui'
#
# Created: Wed Apr 22 14:54:12 2009
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Plot_Options_Dialog(object):
    def setupUi(self, Plot_Options_Dialog):
        Plot_Options_Dialog.setObjectName("Plot_Options_Dialog")
        Plot_Options_Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Plot_Options_Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,570,358).size()).expandedTo(Plot_Options_Dialog.minimumSizeHint()))
        Plot_Options_Dialog.setFocusPolicy(QtCore.Qt.TabFocus)

        self.vboxlayout = QtGui.QVBoxLayout(Plot_Options_Dialog)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tabWidget = QtGui.QTabWidget(Plot_Options_Dialog)
        self.tabWidget.setMinimumSize(QtCore.QSize(0,30))
        self.tabWidget.setObjectName("tabWidget")

        self.gen_options_tab = QtGui.QWidget()
        self.gen_options_tab.setObjectName("gen_options_tab")

        self.layoutWidget = QtGui.QWidget(self.gen_options_tab)
        self.layoutWidget.setGeometry(QtCore.QRect(33,50,295,124))
        self.layoutWidget.setObjectName("layoutWidget")

        self.gridlayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridlayout.setObjectName("gridlayout")

        self.label_3 = QtGui.QLabel(self.layoutWidget)

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,0,1,1,1)

        self.label_4 = QtGui.QLabel(self.layoutWidget)

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,0,2,1,1)

        self.min_label = QtGui.QLabel(self.layoutWidget)
        self.min_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.min_label.setObjectName("min_label")
        self.gridlayout.addWidget(self.min_label,1,0,1,1)

        self.xmin_lineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.xmin_lineEdit.setObjectName("xmin_lineEdit")
        self.gridlayout.addWidget(self.xmin_lineEdit,1,1,1,1)

        self.ymin_lineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.ymin_lineEdit.setObjectName("ymin_lineEdit")
        self.gridlayout.addWidget(self.ymin_lineEdit,1,2,1,1)

        self.max_label = QtGui.QLabel(self.layoutWidget)
        self.max_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.max_label.setObjectName("max_label")
        self.gridlayout.addWidget(self.max_label,2,0,1,1)

        self.xmax_lineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.xmax_lineEdit.setObjectName("xmax_lineEdit")
        self.gridlayout.addWidget(self.xmax_lineEdit,2,1,1,1)

        self.ymax_lineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.ymax_lineEdit.setObjectName("ymax_lineEdit")
        self.gridlayout.addWidget(self.ymax_lineEdit,2,2,1,1)

        self.axis_text_label = QtGui.QLabel(self.layoutWidget)
        self.axis_text_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.axis_text_label.setObjectName("axis_text_label")
        self.gridlayout.addWidget(self.axis_text_label,3,0,1,1)

        self.xlabel_lineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.xlabel_lineEdit.setObjectName("xlabel_lineEdit")
        self.gridlayout.addWidget(self.xlabel_lineEdit,3,1,1,1)

        self.ylabel_lineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.ylabel_lineEdit.setObjectName("ylabel_lineEdit")
        self.gridlayout.addWidget(self.ylabel_lineEdit,3,2,1,1)

        self.logy_cb = QtGui.QCheckBox(self.gen_options_tab)
        self.logy_cb.setGeometry(QtCore.QRect(43,220,83,23))
        self.logy_cb.setObjectName("logy_cb")

        self.plot_title_label = QtGui.QLabel(self.gen_options_tab)
        self.plot_title_label.setGeometry(QtCore.QRect(33,10,61,27))
        self.plot_title_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.plot_title_label.setObjectName("plot_title_label")

        self.logx_cb = QtGui.QCheckBox(self.gen_options_tab)
        self.logx_cb.setGeometry(QtCore.QRect(43,190,83,23))
        self.logx_cb.setObjectName("logx_cb")

        self.plottitle_lineEdit = QtGui.QLineEdit(self.gen_options_tab)
        self.plottitle_lineEdit.setGeometry(QtCore.QRect(100,10,291,27))
        self.plottitle_lineEdit.setObjectName("plottitle_lineEdit")

        self.toggleGrid_btn = QtGui.QPushButton(self.gen_options_tab)
        self.toggleGrid_btn.setGeometry(QtCore.QRect(150,190,75,23))
        self.toggleGrid_btn.setObjectName("toggleGrid_btn")
        self.tabWidget.addTab(self.gen_options_tab,"")

        self.trace_options_tab = QtGui.QWidget()
        self.trace_options_tab.setObjectName("trace_options_tab")

        self.gridlayout1 = QtGui.QGridLayout(self.trace_options_tab)
        self.gridlayout1.setObjectName("gridlayout1")

        self.gridlayout2 = QtGui.QGridLayout()
        self.gridlayout2.setObjectName("gridlayout2")

        self.label_11 = QtGui.QLabel(self.trace_options_tab)
        self.label_11.setObjectName("label_11")
        self.gridlayout2.addWidget(self.label_11,0,0,1,1)

        self.activePlotListWidget = QtGui.QListWidget(self.trace_options_tab)
        self.activePlotListWidget.setObjectName("activePlotListWidget")
        self.gridlayout2.addWidget(self.activePlotListWidget,1,0,1,1)
        self.gridlayout1.addLayout(self.gridlayout2,0,0,4,1)

        self.label = QtGui.QLabel(self.trace_options_tab)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,1,1,1)

        self.lstyle_comboBox = QtGui.QComboBox(self.trace_options_tab)
        self.lstyle_comboBox.setObjectName("lstyle_comboBox")
        self.gridlayout1.addWidget(self.lstyle_comboBox,0,2,1,1)

        self.label_8 = QtGui.QLabel(self.trace_options_tab)
        self.label_8.setObjectName("label_8")
        self.gridlayout1.addWidget(self.label_8,1,1,1,1)

        self.label_5 = QtGui.QLabel(self.trace_options_tab)
        self.label_5.setObjectName("label_5")
        self.gridlayout1.addWidget(self.label_5,2,1,1,1)

        self.mstyle_comboBox = QtGui.QComboBox(self.trace_options_tab)
        self.mstyle_comboBox.setObjectName("mstyle_comboBox")
        self.gridlayout1.addWidget(self.mstyle_comboBox,2,2,1,1)

        self.label_2 = QtGui.QLabel(self.trace_options_tab)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,3,1,1,1)

        self.lw_spinBox = QtGui.QDoubleSpinBox(self.trace_options_tab)
        self.lw_spinBox.setMinimum(0.25)
        self.lw_spinBox.setMaximum(50.0)
        self.lw_spinBox.setSingleStep(0.25)
        self.lw_spinBox.setProperty("value",QtCore.QVariant(1.0))
        self.lw_spinBox.setObjectName("lw_spinBox")
        self.gridlayout1.addWidget(self.lw_spinBox,1,2,1,1)

        self.ms_spinBox = QtGui.QDoubleSpinBox(self.trace_options_tab)
        self.ms_spinBox.setMinimum(0.25)
        self.ms_spinBox.setMaximum(50.0)
        self.ms_spinBox.setSingleStep(0.25)
        self.ms_spinBox.setProperty("value",QtCore.QVariant(1.0))
        self.ms_spinBox.setObjectName("ms_spinBox")
        self.gridlayout1.addWidget(self.ms_spinBox,3,2,1,1)

        self.lineColorBtn = ColorButton(self.trace_options_tab)
        self.lineColorBtn.setEnabled(True)
        self.lineColorBtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.lineColorBtn.setObjectName("lineColorBtn")
        self.gridlayout1.addWidget(self.lineColorBtn,4,1,1,1)

        self.markerColorBtn = ColorButton(self.trace_options_tab)
        self.markerColorBtn.setEnabled(True)
        self.markerColorBtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.markerColorBtn.setObjectName("markerColorBtn")
        self.gridlayout1.addWidget(self.markerColorBtn,4,2,1,1)
        self.tabWidget.addTab(self.trace_options_tab,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.buttonBox = QtGui.QDialogButtonBox(Plot_Options_Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(Plot_Options_Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),Plot_Options_Dialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),Plot_Options_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Plot_Options_Dialog)

    def retranslateUi(self, Plot_Options_Dialog):
        Plot_Options_Dialog.setWindowTitle(QtGui.QApplication.translate("Plot_Options_Dialog", "Plot Options", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "X Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "Y Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.min_label.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "Minimum:", None, QtGui.QApplication.UnicodeUTF8))
        self.max_label.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "Maximum:", None, QtGui.QApplication.UnicodeUTF8))
        self.axis_text_label.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "Label:", None, QtGui.QApplication.UnicodeUTF8))
        self.xlabel_lineEdit.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "x-axis", None, QtGui.QApplication.UnicodeUTF8))
        self.ylabel_lineEdit.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "y-axis", None, QtGui.QApplication.UnicodeUTF8))
        self.logy_cb.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "Log Y Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.plot_title_label.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "Plot Title:", None, QtGui.QApplication.UnicodeUTF8))
        self.logx_cb.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "Log X Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.plottitle_lineEdit.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "Plot Title", None, QtGui.QApplication.UnicodeUTF8))
        self.toggleGrid_btn.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "Toggle Grids", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.gen_options_tab), QtGui.QApplication.translate("Plot_Options_Dialog", "General Options", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "Active Plot Traces", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "Line Style:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "Line Width:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "Marker Style:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "Marker Size:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineColorBtn.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "Line Color...", None, QtGui.QApplication.UnicodeUTF8))
        self.markerColorBtn.setText(QtGui.QApplication.translate("Plot_Options_Dialog", "Marker Color...", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.trace_options_tab), QtGui.QApplication.translate("Plot_Options_Dialog", "Trace Options", None, QtGui.QApplication.UnicodeUTF8))

from colorbutton import ColorButton
