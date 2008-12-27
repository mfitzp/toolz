"""
Show how to use a lasso to select a set of points and get the indices
of the selected points.  A callback is used to change the color of the
selected points

This is currently a proof-of-concept implementation (though it is
usable as is).  There will be some refinement of the API and the
inside polygon detection routine.
"""
from matplotlib.widgets_bhc import Lasso
import matplotlib.mlab
from matplotlib.nxutils import points_inside_poly
from matplotlib.colors import colorConverter
from matplotlib.collections import RegularPolyCollection

from matplotlib.pyplot import figure, show
from numpy import nonzero
from numpy.random import rand

from PyQt4 import QtCore, QtGui

import hcluster as H
import scipy as S

class Datum:
    colorin = colorConverter.to_rgba('red')
    colorout = colorConverter.to_rgba('green')
    def __init__(self, x, y, include=False):
        self.x = x
        self.y = y
        if include: self.color = self.colorin
        else: self.color = self.colorout


class LassoManager(QtCore.QObject):#the QObject subclass is used so you can emit a signal
#    def __init__(self):
    def __init__(self, data, ax = None, main = None, parent = None):
        QtCore.QObject.__init__(self, parent)
        self.ind = None
        self.selectPoints = None
        self.setupOk = False



#    def setup(self, ax, data):
        self.ax = ax
        self.canvas = self.ax.figure.canvas
        self.data = data
        #the lasso lock boolean is used to tell whether another
        #widget event has priority
        self.lassoLock = False


        self.releaseOK = False
        self.Nxy = data.shape[0]

        self.xys = [(d[0], d[1]) for d in data]

        self.cid = self.canvas.mpl_connect('button_press_event', self.onpress)
        self.cidRelease = self.canvas.mpl_connect('button_release_event', self.onrelease)

        self.setupOk = True

    def update(self, data, ax):
        print "update"
        try:
            self.canvas.mpl_disconnect(self.cid)#
            self.canvas.mpl_disconnect(self.cidRelease)#'button_release_event', self.onrelease)
        except:
            print "error removing axis connect"
        self.ax = ax
        self.canvas = self.ax.figure.canvas
        self.data = data
        #the lasso lock boolean is used to tell whether another
        #widget event has priority
        self.lassoLock = False


        self.releaseOK = False
        self.Nxy = data.shape[0]

        self.xys = [(d[0], d[1]) for d in data]

        self.cid = self.canvas.mpl_connect('button_press_event', self.onpress)
        self.cidRelease = self.canvas.mpl_connect('button_release_event', self.onrelease)

    def callback(self, verts):
        '''
        This needs to be run before the release event otherwise no indices will be set.
        '''

        print "callback"
#        print verts
#        facecolors = self.collection.get_facecolors()
        ind = nonzero(points_inside_poly(self.xys, verts))[0]
#        for i in range(self.Nxy):
#            if i in ind:
#                facecolors[i] = Datum.colorin
#            else:
#                facecolors[i] = Datum.colorout
#
        self.canvas.draw_idle()
        self.canvas.widgetlock.release(self.lasso)
#        #del self.lasso
        self.ind = ind
        print "self.ind", self.ind
        if self.releaseOK:
            self.onrelease()
        self.releaseOK = False

    def onpress(self, event):
        if self.canvas.widgetlock.locked(): return
        if event.inaxes is None: return
        self.lasso = Lasso(event.inaxes, (event.xdata, event.ydata), self.callback, color = 'red', alpha = 0.8)
        # acquire a lock on the widget drawing
        self.canvas.widgetlock(self.lasso)
        # establish boolean that can be used to release the widgetlock
        self.lassoLock = True

    def onrelease(self, event = None):
        'on release we reset the press data'
#        print 'release'
        self.releaseOK = True
        # test whether the widgetlock was initiated by the lasso
        if self.lassoLock:
            self.canvas.widgetlock.release(self.lasso)
            self.lassoLock = False

        if self.ind != None:
#            if len(self.ind) == 1:
#                print "self.ind, self.data ",self.ind, self.data[self.ind[0]]
#            else:
#                print "self.ind ", self.ind
            self.selectPoints = self.data[self.ind]
            self.emit(QtCore.SIGNAL("LassoUpdate(PyQt_PyObject)"),self.selectPoints)
    #        print selectPoint
#            try:
#                self.selected.remove()
#            except:
#                print "No selection to remove."
#                pass
#            self.selected, = self.ax.plot(self.selectPoints[:,0], self.selectPoints[:,1], 'bo', alpha = 0.5)

    def setActive(self, boolState):
        if boolState:
            self.cid = self.canvas.mpl_connect('button_press_event', self.onpress)
            self.cidRelease = self.canvas.mpl_connect('button_release_event', self.onrelease)
        else:
            self.canvas.mpl_disconnect(self.cid)
            self.canvas.mpl_disconnect(self.cidRelease)


if __name__ == '__main__':
    from mpl_pyqt4_widget import MPL_Widget
    import sys
    import numpy as N
    app = QtGui.QApplication(sys.argv)
    w = MPL_Widget()
    w.canvas.setupSub(1)
    ax = w.canvas.axDict['ax1']



#    data = [Datum(*xy) for xy in rand(100, 2)]
    data = S.rand(100,2)

#    ax = fig.add_subplot(111, xlim=(0,1), ylim=(0,1), autoscale_on=False)
    ax.plot(data[:,0],data[:,1], 'ro')
    lman = LassoManager(data, ax)

    w.show()
    sys.exit(app.exec_())
