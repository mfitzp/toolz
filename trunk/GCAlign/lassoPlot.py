"""
Show how to use a lasso to select a set of points and get the indices
of the selected points.  A callback is used to change the color of the
selected points

This is currently a proof-of-concept implementation (though it is
usable as is).  There will be some refinement of the API and the
inside polygon detection routine.
"""
from matplotlib.widgets import Lasso
import matplotlib.mlab
from matplotlib.nxutils import points_inside_poly
from matplotlib.colors import colorConverter
from matplotlib.collections import RegularPolyCollection

from matplotlib.pyplot import figure, show
from numpy import nonzero
from numpy.random import rand

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


class LassoManager:
    def __init__(self, ax, data):
        self.ax = ax
        self.canvas = self.ax.figure.canvas
        self.data = data
        #the lasso lock boolean is used to tell whether another
        #widget event has priority
        self.lassoLock = False
#        self.ax.plot(data[:,0],data[:,1], 'ro')


        self.Nxy = data.shape[0]
#
#        facecolors = [d.color for d in data]
        self.xys = [(d[0], d[1]) for d in data]
#        print self.xys
#        fig = ax.figure
#        self.collection = RegularPolyCollection(
#            fig.dpi, 6, sizes=(100,),
#            facecolors=facecolors,
#            offsets = self.xys,
#            transOffset = ax.transData)
#
#        ax.add_collection(self.collection)

        self.cid = self.canvas.mpl_connect('button_press_event', self.onpress)
        self.cidRelease = self.canvas.mpl_connect('button_release_event', self.onrelease)

        self.ind = None

    def callback(self, verts):
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

    def onpress(self, event):
        if self.canvas.widgetlock.locked(): return
        if event.inaxes is None: return
        self.lasso = Lasso(event.inaxes, (event.xdata, event.ydata), self.callback, color = '#FF4500', alpha = 0.8)
        # acquire a lock on the widget drawing
        self.canvas.widgetlock(self.lasso)
        # establish boolean that can be used to release the widgetlock
        self.lassoLock = True

    def onrelease(self, event):
        'on release we reset the press data'
        print 'release'
        # test whether the widgetlock was initiated by the lasso
        if self.lassoLock:
            self.canvas.widgetlock.release(self.lasso)
            self.lassoLock = False

        if self.ind != None:
            if len(self.ind) == 1:
                print "self.ind, self.data ",self.ind, self.data[self.ind[0]]
            else:
                print "self.ind ", self.ind
            selectPoints = self.data[self.ind]
    #        print selectPoint
            try:
                self.selected.remove()
            except:
                print "No selection to remove."
                pass
            self.selected, = self.ax.plot(selectPoints[:,0], selectPoints[:,1], 'bo')

    def setActive(self, boolState):
        if boolState:
            self.cid = self.canvas.mpl_connect('button_press_event', self.onpress)
            self.cidRelease = self.canvas.mpl_connect('button_release_event', self.onrelease)
        else:
            self.canvas.mpl_disconnect(self.cid)
            self.canvas.mpl_disconnect(self.cidRelease)


if __name__ == '__main__':
    from PyQt4 import QtGui, QtCore
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
    lman = LassoManager(ax, data)

    w.show()
    sys.exit(app.exec_())
