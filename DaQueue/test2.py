import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from QTermWidget import QTermWidget
from PyQt4.QtWebKit import *

app = QApplication(sys.argv)

QT_DOCUMENTATION = "file:///usr/share/doc/PyQt4/doc/html/"

myMainWindow = QMainWindow()

mySplitter = QSplitter()
mySplitter.setOrientation(Qt.Vertical)

myMainWindow.setCentralWidget(mySplitter)

mySplitterHorizontal = QSplitter()
mySplitterHorizontal.setOrientation(Qt.Horizontal)

mySplitter.addWidget(mySplitterHorizontal)

myLabel = QLabel("Hello world!")
myLabel.setMinimumHeight(300)
myLabel.setMinimumWidth(300)
mySplitterHorizontal.addWidget(myLabel)

myWebKit = QWebView()
myDock = QDockWidget("WebKit Documentation")
myDock.setObjectName("WebKitDocumentation")
myDock.setAllowedAreas(Qt.RightDockWidgetArea)
myDock.setWidget(myWebKit)
mySplitterHorizontal.addWidget(myDock)
myWebKit.setUrl(QUrl(QT_DOCUMENTATION + "qwebview.html"))

myTerm = QTermWidget()
myCodec = QTextCodec.codecForName("UTF-8")
myTerm.setTextCodec(myCodec)
myFont = QFont("Terminus")
myFont.setPixelSize(18)
myTerm.setTerminalFont(myFont)
myTerm.setMinimumHeight(300)
mySplitter.addWidget(myTerm)

myMainWindow.menuBar().addMenu("Foo")

myStatusLabel = QLabel()
myStatusLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
myStatus = myMainWindow.statusBar()
myStatus.setSizeGripEnabled(False)
myStatus.addPermanentWidget(myStatusLabel)
myStatus.showMessage("The text to be displayed in status bar.")

myMainWindow.show()

def qtdoc(param):
  if type(param) is str:
    myWebKit.setUrl(QUrl("%s%s.html" % (QT_DOCUMENTATION, param.lower())))
  elif isinstance(param, QObject):
    myWebKit.setUrl(QUrl("%s%s.html" % (QT_DOCUMENTATION, param.__class__.__name__.lower())))
  elif type(param) == QObject.__class__:
    myWebKit.setUrl(QUrl("%s%s.html" % (QT_DOCUMENTATION, param.__name__.lower())))
