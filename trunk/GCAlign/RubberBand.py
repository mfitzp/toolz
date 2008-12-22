"""
Do a mouseclick somewhere, move the mouse to some destination, release the
button.
This class gives click- and release-events and also draws a line or a box
from the click-point to the actual mouseposition (within the same axes)
until the button is released.
Within the method 'self.ignore()' it is checked wether the button from eventpress and
eventrelease are the same.

(This is based on HorizontalSpanSelectory.py)
"""

from pylab import *

class LineSelector:
    """
    Select a min/max range of the x axes for a matplotlib Axes

    Example usage:

      ax = subplot(111)
      ax.plot(x,y)

      def onselect(event_click, event_release):
          print 'startposition : (%f,%f)'%(event_click.xdata, event_click.ydata)
          print 'endposition   : (%f,%f)'%(event_release.xdata, event_release.ydata)
          print 'used button   : ', event_click.button
      span = Selector(ax, onselect,drawtype='box')
      show()

    """
    def __init__(self, ax, onselect, drawtype='box',
                 minspan_x=None, minspan_y=None, useblit=False,
                 lineprops=None, rectprops=None):

        """
        Create a selector in ax.  When a selection is made, clear
        the span and call onselect with

          onselect(pos_1, pos_2)

        and clear the drawn box/line. There pos_i are arrays of length 2
        containing the x- and y-coordinate.

        If minspan_x is not None then events smaller than minspan_x
        in x direction are ignored(it's the same for y).

        The rect is drawn with rectprops; default
          rectprops = dict(facecolor='red', edgecolor = 'black', alpha=0.5, fill=False)
        The line is drawn with lineprops; default
          lineprops = dict(color='black', linestyle='-',
                             linewidth = 2, alpha=0.5)

        Use type if you want the mouse to draw a line, a box or nothing
        between click and actual position ny setting
        drawtype = 'line', drawtype='box' or drawtype = 'none'.


        """
        self.ax = ax
        self.visible = True
        self.canvas = ax.figure.canvas
        self.canvas.mpl_connect('motion_notify_event', self.onmove)
        self.canvas.mpl_connect('button_press_event', self.press)
        self.canvas.mpl_connect('button_release_event', self.release)
        self.canvas.mpl_connect('draw_event', self.update_background)

        self.to_draw = None
        self.background = None

        if drawtype == 'none':
            drawtype = 'line'                        # draw a line but make it
            self.visible = False                     # invisible

        if drawtype == 'box':
            if rectprops is None:
                rectprops = dict(facecolor='white', edgecolor = 'black',
                                 alpha=0.5, fill=False)
            self.rectprops = rectprops
            self.to_draw = Rectangle((0,0), 0, 1,visible=False,**self.rectprops)
            self.ax.add_patch(self.to_draw)
        if drawtype == 'line':
            if lineprops is None:
                lineprops = dict(color='black', linestyle='-',
                                 linewidth = 2, alpha=0.5)
            self.lineprops = lineprops
            self.to_draw = Line2D([0,0],[0,0],visible=False,**self.lineprops)
            self.ax.add_line(self.to_draw)

        self.onselect = onselect
        self.useblit = useblit
        self.minspan_x = minspan_x
        self.minspan_y = minspan_y
        self.drawtype = drawtype
        self.eventpress = None            # will safe the data (position at mouseclick)
        self.eventrelease = None          # will safe the data (pos. at mouserelease)

    def update_background(self, event):
        'force an update of the background'
        if self.useblit:
            self.background = self.canvas.copy_from_bbox(self.ax.bbox)


    def ignore(self, event):
        'return True if event should be ignored'
        if self.eventpress == None:           # If no button was pressed yet ignore the
          return event.inaxes!= self.ax       #   event if it was out of the axes
                                              # If a button was pressed, check if the
                                              #   release-button is the same.
        return  event.inaxes!=self.ax or event.button != self.eventpress.button

    def press(self, event):
        'on button press event'
        if self.ignore(event): return         # Is the correct button pressed?
                                              # Within the correct axes?
        self.to_draw.set_visible(self.visible)# make the drawed box/line visible
        self.eventpress = event               # get the click-coordinates, button, ...
        return False


    def release(self, event):
        'on button release event'
        if self.eventpress is None or self.ignore(event): return
        self.to_draw.set_visible(False)       # make the box/line invisible again
        self.canvas.draw()
        self.eventrelease = event             # release coordinates, button, ...
        xmin, ymin = self.eventpress.xdata, self.eventpress.ydata
        xmax, ymax = self.eventrelease.xdata, self.eventrelease.ydata
                                              # calculate dimensions of drawed
                                              #   box (or line respectively)
        if xmin>xmax: xmin, xmax = xmax, xmin # get values in the right order
        if ymin>ymax: ymin, ymax = ymax, ymin
        span_x = xmax - xmin                  # calculate the difference
        span_y = ymax - ymin
        x_problems = self.minspan_x is not None and span_x<self.minspan_x
        y_problems = self.minspan_y is not None and span_y<self.minspan_y
        if (self.drawtype=='box')  and (x_problems or  y_problems):
            """Box to small"""     # check if drawed distance (if it exists) is
            return                 # not to small in neither x nor y-direction
        if (self.drawtype=='line') and (x_problems and y_problems):
            """Line to small"""    # check if drawed distance (if it exists) is
            return                 # not to small in neither x nor y-direction
        self.onselect(self.eventpress, self.eventrelease)
                                              # call desired function
        self.eventpress = None                # reset the variables to their
        self.eventrelease = None              #   inital values
        return False

    def update(self):
        'draw using newfangled blit or oldfangled draw depending on useblit'
        if self.useblit:
            if self.background is not None:
                self.canvas.restore_region(self.background)
            self.ax.draw_artist(self.to_draw)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()
        return False


    def onmove(self, event):
        'on motion notify event if box/line is wanted'
        if self.eventpress is None or self.ignore(event): return
        x,y = event.xdata, event.ydata            # actual position (with
                                                  #   (button still pressed)
        if self.drawtype == 'box':
            minx, maxx = self.eventpress.xdata, x # click-x and actual mouse-x
            miny, maxy = self.eventpress.ydata, y # click-y and actual mouse-y
            if minx>maxx: minx, maxx = maxx, minx # get them in the right order
            if miny>maxy: miny, maxy = maxy, miny
            self.to_draw.xy[0] = minx             # set lower left of box
            self.to_draw.xy[1] = miny
            self.to_draw.set_width(maxx-minx)     # set width and height of box
            self.to_draw.set_height(maxy-miny)
            self.update()
            return False
        if self.drawtype == 'line':
            self.to_draw.set_data([self.eventpress.xdata, x],
                                  [self.eventpress.ydata, y])
            self.update()
            return False

#-------------------------------------------------------------------------------

if __name__=="__main__":

    def line_select_callback(event_1, event_2):
        """ What should be done with the coordinates of mouseclick and -release?"""
        x1, y1 = event_1.xdata, event_1.ydata
        x2, y2 = event_2.xdata, event_2.ydata
        print "(%3.2f, %3.2f) --> (%3.2f, %3.2f)"%(x1,y1,x2,y2)
        print " The button you used were: ",event_1.button, event_2.button


    current_ax=subplot(111)                    # make a new plotingrange
    N=100000                                   # If N is large one can see improvement
    x=10.0*arange(N)/(N-1)                     #   by use blitting!

    plot(x,sin(.2*pi*x),lw=3,c='b',alpha=.7)   # plot something
    plot(x,cos(.2*pi*x),lw=3.5,c='r',alpha=.5)
    plot(x,-sin(.2*pi*x),lw=3.5,c='g',alpha=.3)

    print "\n      click  -->  release"
    LS = LineSelector(current_ax, line_select_callback,
                      drawtype='line',useblit=True)
    show()