import sys
from PyQt4.QtCore import QSize, Qt
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from mpl_custom_widget import MPL_Widget
from webTable import DataTableWindow

html = \
"""<html>
<head>
<title>Python Web Plugin Test</title>
</head>

<body>
<h1>Python Web Plugin Test</h1>
<object type="x-pyqt/widget" width="200" height="200"></object>
<p>This is a Web plugin written in Python.</p>
</body>
</html>
"""

class WebWidget(QWidget):

    def paintEvent(self, event):
        painter = DataTableWindow()
#        painter = MPL_Widget()

#        painter = QPainter()
#        painter.begin(self)
#        painter.setBrush(Qt.white)
#        painter.setPen(Qt.black)
#        painter.drawRect(self.rect().adjusted(0, 0, -1, -1))
#        painter.setBrush(Qt.red)
#        painter.setPen(Qt.NoPen)
#        painter.drawRect(self.width()/4, self.height()/4,
#                         self.width()/2, self.height()/2)
#        painter.end()

    def sizeHint(self):
        return QSize(100, 100)


class WebPluginFactory(QWebPluginFactory):

    def __init__(self, parent = None):
        QWebPluginFactory.__init__(self, parent)

    def create(self, mimeType, url, names, values):
        if mimeType == "x-pyqt/widget":
            return WebWidget()

    def plugins(self):
        plugin = QWebPluginFactory.Plugin()
        plugin.name = "PyQt Widget"
        plugin.description = "An example Web plugin written with PyQt."
        mimeType = QWebPluginFactory.MimeType()
        mimeType.name = "x-pyqt/widget"
        mimeType.description = "PyQt widget"
        mimeType.fileExtensions = []
        plugin.mimeTypes = [mimeType]
        print "plugins"
        return [plugin]


if __name__ == "__main__":

    app = QApplication(sys.argv)
    QWebSettings.globalSettings().setAttribute(QWebSettings.PluginsEnabled, True)
    view = QWebView()
    factory = WebPluginFactory()
    view.page().setPluginFactory(factory)
    view.setHtml(html)
    view.show()
    sys.exit(app.exec_())