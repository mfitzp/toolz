# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\d3p483\workspace\XTandem_Parsing\Field_Dialog.ui'
#
# Created: Mon Nov 02 09:17:30 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_fieldDialog(object):
    def setupUi(self, fieldDialog):
        fieldDialog.setObjectName("fieldDialog")
        fieldDialog.setWindowModality(QtCore.Qt.WindowModal)
        fieldDialog.resize(246, 157)
        fieldDialog.setFocusPolicy(QtCore.Qt.TabFocus)
        self.verticalLayout_2 = QtGui.QVBoxLayout(fieldDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")
        self.label_3 = QtGui.QLabel(fieldDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.min_label = QtGui.QLabel(fieldDialog)
        self.min_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.min_label.setObjectName("min_label")
        self.gridlayout.addWidget(self.min_label, 1, 0, 1, 1)
        self.xmin_lineEdit = QtGui.QLineEdit(fieldDialog)
        self.xmin_lineEdit.setObjectName("xmin_lineEdit")
        self.gridlayout.addWidget(self.xmin_lineEdit, 1, 1, 1, 1)
        self.max_label = QtGui.QLabel(fieldDialog)
        self.max_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.max_label.setObjectName("max_label")
        self.gridlayout.addWidget(self.max_label, 2, 0, 1, 1)
        self.xmax_lineEdit = QtGui.QLineEdit(fieldDialog)
        self.xmax_lineEdit.setObjectName("xmax_lineEdit")
        self.gridlayout.addWidget(self.xmax_lineEdit, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridlayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(fieldDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(fieldDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), fieldDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), fieldDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(fieldDialog)

    def retranslateUi(self, fieldDialog):
        fieldDialog.setWindowTitle(QtGui.QApplication.translate("fieldDialog", "Field Options", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("fieldDialog", "Field Values", None, QtGui.QApplication.UnicodeUTF8))
        self.min_label.setText(QtGui.QApplication.translate("fieldDialog", "Lo Value:", None, QtGui.QApplication.UnicodeUTF8))
        self.max_label.setText(QtGui.QApplication.translate("fieldDialog", "Hi Value:", None, QtGui.QApplication.UnicodeUTF8))

