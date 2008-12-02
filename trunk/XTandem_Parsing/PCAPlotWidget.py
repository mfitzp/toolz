
from PyQt4 import QtCore,  QtGui

from mpl_custom_widget import MPL_Widget
import PCA.pca_module as pca
import numpy as N
from matplotlib.mlab import load

class PCA_Widget(MPL_Widget):
    def __init__(self,  data = None,  parent = None):
        '''data is a multidimensional numpy array and parent is the calling window'''
        QtGui.QWidget.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle('PCA Plot')
        self.resize(800, 400)
        self.pcaPlot = MPL_Widget(self)


        self.scores = None
        self.loading = None
        self.explanation = None

        if data != None:
            self.data = data
            self.executePCA()
            self.initializePlot()

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.pcaPlot)
        self.setLayout(layout)
        self.show()

    def executePCA(self):
        if len(self.data[0]) < 2:
            raise "More than 1 dimension of data is necessary for PCA"
        else:
            self.scores,  self.loading,  self.explanation = pca.PCA_nipals2(self.data, standardize=True, E_matrices=True)


    def initializePlot(self):
        '''Sets up the plot variables used for interaction'''
        self.handleA,  = self.pcaPlot.canvas.ax.plot([0], [0], 'o',\
                                        ms=8, alpha=.5, color='yellow', visible=False,  label = 'Cursor A')
        self.is_hZoom = False
        self.pcaPlot.canvas.mpl_connect('pick_event', self.OnPickPlot)

        if self.scores != None:#you can just use "if self.scores" It raises an error
            self.x = self.scores[:, 0]
            self.y = self.scores[:, 1]
            self.pcaPlot.canvas.xtitle = 'PC1'
            self.pcaPlot.canvas.ytitle = 'PC2'
            self.pcaPlot.canvas.PlotTitle = ''
            self.pcaPlot.canvas.ax.grid()
            self.pcaPlot.canvas.ax.scatter(self.x, self.y,  color = 'r',alpha = 0.3, picker = 5)


            self.pcaPlot.canvas.format_labels()
            self.pcaPlot.canvas.draw()

    def OnPickPlot(self, event):
        self.pickIndex = event.ind[0]
#        try:
#            self.textHandle.remove()
#        except:
#            pass
#        self.curTbl = event.artist.get_label()
#        if self.clearPlotCB.isChecked():
#            #I'd rather do the following ALWAYS but it seems difficult to do in terms of keeping track of which arrays were plotted when multiple plots are present
        self.handleA.set_data(N.take(self.x, [self.pickIndex]), N.take(self.y, [self.pickIndex]))
#        else:
#            self.handleA.set_data([event.mouseevent.xdata], [event.mouseevent.ydata])

        self.handleA.set_visible(True)
#        showText = '%s'%(self.activeDict[self.curTbl].dataDict.get('pepIDs')[self.pickIndex])
#        self.textHandle = self.plotWidget.canvas.ax.text(0.03, 0.95, showText, fontsize=9,\
#                                        bbox=dict(facecolor='yellow', alpha=0.1),\
#                                        transform=self.plotWidget.canvas.ax.transAxes, va='top')
#        self.updateSelectInfo(self.pickIndex,  self.curTbl)
        self.pcaPlot.canvas.draw()

def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    data = load('PCA_Matrix_noProE.csv',  delimiter = ',',  skiprows = 1)
    w = PCA_Widget(data)
    #w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


