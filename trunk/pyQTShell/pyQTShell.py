#!/usr/bin/env python
import sys
from os.path import isfile

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
        #self.setWindowTitle(self.windowTitle)
        pyQTShell.NextId +=1
          
        
        self.xlist = {}#used just for reference
        
        self.__initLocalVars__()
        self.__addWidgets__()
    
 
    def __addWidgets__(self):
        '''adds all of the custom widgets not specified in the .ui file'''
        #interpreter = Interpreter(self.localVars.__dict__)#original
        interpreter = Interpreter(self.varDict)
        #interpreter = Interpreter()
        shellClass = shell.get_shell_class()
        
        self.shell = shellClass(interpreter,parent=self.ui.pyDockWidget)
        self.shell.setObjectName("shell")
        self.ui.pyDockWidget.setWidget(self.shell)
    
    def __initLocalVars__(self):
        '''Initialization of variables
        All of those variables specified below will be avialable to the user
        '''
        #self.localVars.setPubTypes(self.localVarTypes)
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
