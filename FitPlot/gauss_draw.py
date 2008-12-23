"""
Do a mouseclick somewhere, move the mouse to some destination, release
the button.  This class gives click- and release-events and also draws
a line or a box from the click-point to the actual mouseposition
(within the same axes) until the button is released.  Within the
method 'self.ignore()' it is checked wether the button from eventpress
and eventrelease are the same.

"""
from matplotlib.widgets import RectangleSelector
from pylab import subplot, arange, plot, sin, cos, pi, show, absolute
import scipy as S
import numpy as N
def line_select_callback(event1, event2):
    'event1 and event2 are the press and release events'
    x1, y1 = event1.xdata, event1.ydata
    x2, y2 = event2.xdata, event2.ydata
    width = absolute(x2-x1)
    startp = (x2-x1)
    #print width
    xr = arange(x1-startp, x2, 0.01*width)
    #print xr
    #print "Width: ", width,  "Length ", len(xr)
    gauss = y1*S.exp(-(xr-x1)**2/(width/2))
    gline.set_data(xr, gauss)
    #gline.set_data(xr, 0)
    test.set_data([x1,x2],[y1,0])
    #print "(%3.2f, %3.2f) --> (%3.2f, %3.2f)"%(x1,y1,x2,y2)
    #print " The button you used were: ",event1.button, event2.button



current_ax=subplot(111)                    # make a new plotingrange
N=100000                                   # If N is large one can see improvement
x=10.0*arange(N)/(N-1)                     # by use blitting!

plot(x,sin(.2*pi*x),lw=3,c='b',alpha=.7)   # plot something
plot(x,cos(.2*pi*x),lw=3.5,c='r',alpha=.5)
plot(x,-sin(.2*pi*x),lw=3.5,c='g',alpha=.3)
test, = plot([0],[0],'o')
width = 2.0
gauss = 2*S.exp(-(x-4)**2/(width))
#print len(x)
#print len(gauss)
gline, = plot(x,gauss)
#fit = lambda t : max*exp(-(t-x)**2/(2*width**2))


print "\n      click  -->  release"

# drawtype is 'box' or 'line' or 'none'
LS = RectangleSelector(current_ax, line_select_callback,
                      drawtype='box',useblit=True)
show()
