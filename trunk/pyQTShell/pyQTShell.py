#!/usr/bin/env python
import sys
from os.path import isfile
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as N
import scipy as S
import pylab as P


import shell
from Python_Highlighter import TextEdit, PythonHighlighter
from code import InteractiveInterpreter as Interpreter

from ui_pyQtShell import Ui_pyQTShell


def isAlive(qobj):#new
    import sip
    try:
        sip.unwrapinstance(qobj)
    except RuntimeError:
        return False
    return True

class pyQTShell(QWidget):
    NextId = 1
    
    Instances = set()
    '''pyQTShell instance.'''
    def __init__(self, parent = None,  varDict = None):
        super(pyQTShell, self).__init__(None)#new  new^2:changed from parent
        self.setAttribute(Qt.WA_DeleteOnClose)#new
        pyQTShell.Instances.add(self)#new
        
        self.ui = Ui_pyQTShell()
        self.ui.setupUi(self)
        self.parent = None
        self.varDict = {}
        if varDict:
            self.varDict = varDict
        if parent:
            self.parent = parent
            self.varDict = parent.localVars.getPubDict()
            #print parent.dialog_test
            parent.topPlot = self.ui
            #print parent.localVars.getPubDict().keys()
        #self.windowTitle = "Plot%d" % pyQTShell.NextId
        self.setWindowTitle("Python Shell")
        pyQTShell.NextId +=1
          
        
        self.xlist = {}#used just for reference
        
        self.__initLocalVars__()
        self.__addWidgets__()
        self.__initConnections__()
        self.__initContextMenus__()
    

    def __initContextMenus__(self):
        self.SP_Edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.SP_Edit.connect(self.SP_Edit, SIGNAL("customContextMenuRequested(QPoint)"), self.scratchPadContext)
        
        #self.tableWidgetContext()

    def scratchPadContext(self, point):
        '''Create a menu for the scratch pad and associated actions'''
        sp_menu = QMenu("Menu", self.SP_Edit)
        sp_menu.addAction(self.actionTransfer)
        sp_menu.exec_(self.SP_Edit.mapToGlobal(point))

    def __addWidgets__(self):
        '''adds all of the custom widgets not specified in the .ui file'''
        #interpreter = Interpreter(self.localVars.__dict__)#original
        interpreter = Interpreter(self.varDict)
        #interpreter = Interpreter()
        shellClass = shell.get_shell_class()
        
        self.shell = shellClass(interpreter,parent=self.ui.pyDockWidget)
        self.shell.setObjectName("shell")
        self.ui.pyDockWidget.setWidget(self.shell)
        ############################################
        #print type(self.sp_widget)
        self.SP_Edit = TextEdit(self.ui.sp_widget)
        self.highlighter = PythonHighlighter(self.SP_Edit.document())
        
        self.SP_Edit.setObjectName("SP_Edit")
        self.ui.vboxlayout.addWidget(self.SP_Edit)
        
        self.ui.script_name_cb.addItem(QString('New Script Name'))
        
    def __initConnections__(self):
        self.actionTransfer = QAction("Run Scratch Pad Script",  self)#self)
        self.ui.sp_widget.addAction(self.actionTransfer)
        QObject.connect(self.actionTransfer,SIGNAL("triggered()"),self.__runScratchScript__)
        
        QObject.connect(self.ui.btn_saveScript, SIGNAL("clicked()"), self.__saveSP2Disk__)
        QObject.connect(self.ui.btn_scratch2Mem, SIGNAL("clicked()"), self.__saveSP2Mem__)
        QObject.connect(self.ui.script_name_cb, SIGNAL("currentIndexChanged(QString)"), self.__scratchComboAction__)        
        
        
        QMetaObject.connectSlotsByName(self)
 
    def __scratchComboAction__(self, entry):
        #print "Combo Index"
        if entry and self.userScratchDict.has_key(entry):# is not self.script_name_cb.currentText():            
            self.SP_Edit.setPlainText(self.userScratchDict.get(entry))#self.script_name_cb.currentText()))

    def __updateScratchScripts__(self):
        self.ui.script_name_cb.clear()
        self.ui.script_name_cb.addItems(self.userScratchDict.keys())

    def __saveSP2Mem__(self):
        if self.ui.script_name_cb.currentText():
            print '\nScratch Pad saved as %s'%(self.ui.script_name_cb.currentText())

            self.userScratchDict[self.ui.script_name_cb.currentText()] = self.SP_Edit.document().toPlainText()
            self.__updateScratchScripts__()

            
        else:
            return QtGui.QMessageBox.warning(self.MainWindow,\
                                                 "That action is Verbotten",\
                                                 "You need to enter a script name first!",\
                                                 QtGui.QMessageBox.Ok)
        
    def __saveSP2Disk__(self):
        if self.ui.script_name_cb.currentText():
            
            spFilePath = '/'.join([os.getcwd(),  str(self.ui.script_name_cb.currentText())])
        else:
            spFilePath = '/'.join([os.getcwd(),''])
        
        dataFileName = QtGui.QFileDialog.getSaveFileName(self,\
                                                 self.ScratchSavePrompt,\
                                                 spFilePath,'Python File (*.py)')
        if dataFileName:
            scratch_text = self.SP_Edit.document().toPlainText()
            #lines = unicode((script_text.toPlainText()).splitlines(True))
            try:
                if os.path.isfile(dataFileName):
                    fout = open(dataFileName, 'a')
                    fout.write(scratch_text)
                    fout.close()
                    print "Scratch Pad appended to: %s"%(dataFileName)
                else:
                    fout = open(dataFileName, 'w')
                    fout.write(scratch_text)
                    fout.close()
                    print "Scratch Pad written to: %s"%(dataFileName)
            except:
                print "Error writing scratch pad to file."
            
            finally:
                    self.userScratchDict[self.script_name_cb.currentText()]=scratch_text
                    

    def __runScratchScript__(self):
        '''script_text is of type QDocument which must be changed to
        unicode before the splitlines operation may be used.  The TRUE
        at the end of this command keeps the end of line character intact
        so the fakeUser command can add the text to the shell properly'''
        script_text = self.SP_Edit.document()
        lines = unicode(script_text.toPlainText()).splitlines(True)
        self.shell.setFocus()
        self.ui.tabWidget.setCurrentIndex(0)
        #print type(lines)
        #print lines
        return self.shell.fakeUser(lines)

    
    def __initLocalVars__(self):
        '''Initialization of variables
        All of those variables specified below will be avialable to the user
        '''
        self.ScratchSavePrompt = "Choose file name to save the scratch pad:"
        #self.localVars.setPubTypes(self.localVarTypes)
        self.userScratchDict = {}
        self.varDict['__ghost__'] = []
        #self.localVars['P'] = P
        self.varDict['N'] = N
        self.varDict['S'] = S


            
    @staticmethod
    def updateInstances(qobj):
        pyQTShell.Instances = set([window for window \
                in pyQTShell.Instances if isAlive(window)])
                        

    def dict_value(self, dictionary):
        return dictionary.values()[0]
    
    def dict_key(self, dictionary):
        return dictionary.keys()[0]
              

        
if __name__ == "__main__":
    
    #from scipy import rand
    app = QApplication(sys.argv)

    
    # make x data
    num = 100
    x = S.linspace(-10, 10, num=num)
    distancePerLag = x[1]-x[0]
    
    # make two gaussians, with different means
    offset = 2.0
    y1 = S.exp(-x**2/8.0)
    y2 = S.exp(-(x-offset)**2/1.0)

    #ydict = {'y2':y2, 'y3':y3}
    #ydict = {'y2':y2, 'y3':y3, 'y4':y4, 'y5':y5, 'y6':y6,'y7':y7, 'y8':y8}
    totaldict = {'x':x,'y1':y1,'y2':y2}

    shell = pyQTShell(varDict = totaldict)
    #plot = pyQTShell(varDict = totaldict)
    #plot = pyQTShell()
    shell.show()
    #print plot.plotscript
    sys.exit(app.exec_())     
