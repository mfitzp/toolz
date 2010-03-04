# -------------------------------------------------------------------------
#     Copyright (C) 2008-2010 Martin Strohalm <mmass@biographics.cz>

#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#     GNU General Public License for more details.

#     Complete text of GNU GPL can be found in the file LICENSE in the
#     main directory of the program
# -------------------------------------------------------------------------

# load libs
import wx
import numpy
import calculations


class container:
    """Container to hold plot objects and graph labels."""
    
    def __init__(self, objects=[]):
        self.objects = objects
    # ----
    
    
    def getBoundingBox(self, minX=None, maxX=None):
        """Get container bounding box"""
        
        # init values if no data in objects
        rect = [numpy.array([0, 0]), numpy.array([1, 1])]
        
        # get bouding boxes from objects
        have = False
        for obj in self.objects:
            if obj.isVisible():
                oRect = obj.getBoundingBox(minX, maxX)
                if have and oRect:
                    rect[0] = numpy.minimum(rect[0], oRect[0])
                    rect[1] = numpy.maximum(rect[1], oRect[1])
                elif oRect:
                    rect = oRect
                    have = True
                
        # check scale
        if rect[0][0] == rect[1][0]:
            rect[0][0] -= 0.5
            rect[1][0] += 0.5
        if rect[0][1] == rect[1][1]:
            rect[1][1] += 0.5
        
        return rect
    # ----
    
    
    def getLegend(self):
        """Get a list of legend names"""
        
        # get names
        names = []
        for obj in self.objects:
            if obj.isVisible():
                legend = obj.getLegend()
                if legend[0] != '':
                    names.append(obj.getLegend())
            
        return names
    # ----
    
    
    def getPoint(self, obj, xPos, userCoord=False):
        """Get point coordinates in selected object"""
        
        point = self.objects[obj].getPoint(xPos, userCoord)
        return point
    # ----
    
    
    def countGels(self):
        """Get number of visible gels."""
        
        count = 0
        for obj in self.objects:
            if obj.isVisible() and obj.properties['showInGel']:
                count += 1
        
        return max(count,1)
    # ----
    
    
    def cropPoints(self, minX, maxX):
        """Crop points in all objects"""
        
        for obj in self.objects:
            if obj.isVisible():
                obj.cropPoints(minX, maxX)
    # ----
    
    
    def scaleAndShift(self, scale, shift):
        """Scale and shift points in all objects"""
        
        for obj in self.objects:
            if obj.isVisible():
                obj.scaleAndShift(scale, shift)
    # ----
    
    
    def filterPoints(self, filterSize):
        """Filter points in all objects"""
        
        for obj in self.objects:
            if obj.isVisible():
                obj.filterPoints(filterSize)
    # ----
    
    
    def draw(self, dc, printerScale, overlapLabels, reverse):
        """Draw each object in container"""
        
        # draw in reverse order
        if reverse:
            self.objects.reverse()
            
        # draw objects
        for obj in self.objects:
            if obj.isVisible():
                obj.draw(dc, printerScale)
        
        # draw object's labels
        self.drawLabels(dc, printerScale, overlapLabels)
        
        # reverse back order
        if reverse:
            self.objects.reverse()
    # ----
    
    
    def drawLabels(self, dc, printerScale, overlapLabels):
        """Draw labels for each object in container."""
        
        labels = []
        
        # get labels from objects
        for obj in self.objects:
            if obj.isVisible():
                labels += obj.makeLabels(dc, printerScale)
        
        # check labels
        if not labels:
            return
        
        # sort labels
        labels.sort()
        labels.reverse()
        
        # preset font by first label
        font = labels[0][4]['labelFont']
        colour = labels[0][4]['labelColour']
        bgr = labels[0][4]['labelBgr']
        bgrColour = labels[0][4]['labelBgrColour']
        
        dc.SetFont(_scaleFont(font, printerScale))
        dc.SetTextForeground(colour)
        dc.SetTextBackground(bgrColour)
        
        if bgr:
            dc.SetBackgroundMode(wx.SOLID)
        
        # draw labels
        occupied = []
        for label in labels:
            text = label[1]
            textPos = label[2]
            textSize = label[3]
            properties = label[4]
            
            # check free space and draw label
            if overlapLabels or _checkFreeSpace(textPos, textSize, occupied):
                
                # check pen
                if properties['labelFont'] != font:
                    font = properties['labelFont']
                    dc.SetFont(_scaleFont(font, printerScale))
                
                if properties['labelColour'] != colour:
                    colour = properties['labelColour']
                    dc.SetTextForeground(colour)
                
                #if properties['labelBgrColour'] != bgrColour:
                #    bgrColour = properties['labelBgrColour']
                #    dc.SetTextBackground(bgrColour)
                
                if properties['labelBgr'] != bgr:
                    bgr = properties['labelBgr']
                    if bgr:
                        dc.SetBackgroundMode(wx.SOLID)
                    else:
                        dc.SetBackgroundMode(wx.TRANSPARENT)
                
                # draw label
                dc.DrawRotatedText(text, textPos[0], textPos[1], properties['labelAngle'])
                occupied.append((textPos, textSize))
        
        dc.SetBackgroundMode(wx.TRANSPARENT)
    # ----
    
    
    def drawGel(self, dc, gelCoords, gelHeight, printerScale):
        """Draw gel for objects in container"""
        
        # draw objects
        for obj in self.objects:
            if obj.isVisible() and obj.properties['showInGel']:
                obj.drawGel(dc, gelCoords, gelHeight, printerScale)
                gelCoords[0] += gelHeight
    # ----
    
    
    def append(self, obj):
        self.objects.append(obj)
    # ----
    
    
    def __additem__(self, obj):
        self.objects.append(obj)
    # ----
    
    
    def __delitem__(self, index):
        del self.objects[index]
    # ----
    
    
    def __setitem__(self, index, obj):
        self.objects[index] = obj
    # ----
    
    
    def __getitem__(self, index):
        return self.objects[index]
    # ----
    
    
    def __len__(self):
        return len(self.objects)
    # ----
    


class points:
    """Base class for simple points drawing."""
    
    def __init__(self, points, **attr):
        
        # convert points to array
        points.sort()
        self.points = numpy.array(points)
        self.cropped = self.points
        self.scaled = self.cropped
        
        self.currentScale = (1, 1)
        self.currentShift = (0, 0)
        
        # set default params
        self.properties = {
                            'legend': '',
                            'visible': True,
                            'showInGel': False,
                            'exactFit': False,
                            'pointColour': (0, 0, 255),
                            'pointSize': 3,
                            }
        
        # get new attributes
        for name, value in attr.items():
            self.properties[name] = value
    # ----
    
    
    def setProperties(self, **attr):
        """Set object properties."""
        
        for name, value in attr.items():
            self.properties[name] = value
    # ----
    
    
    def isVisible(self):
        """Return object visibility"""
        
        return self.properties['visible']
    # ----
    
    
    def getBoundingBox(self, minX=None, maxX=None):
        """Get bounding box for whole data or X selection"""
        
        # use relevant data
        if minX!=None and maxX!=None:
            self.cropPoints(minX, maxX)
            return self._calcBoundingBox(self.cropped)
        else:
            return self._calcBoundingBox(self.points)
    # ----
    
    
    def getLegend(self):
        """Get legend"""
        
        return (self.properties['legend'], self.properties['pointColour'])
    # ----
    
    
    def cropPoints(self, minX, maxX):
        """Crop spectrum points to current view coordinations"""
        
        # if no data
        if len(self.points)==0:
            self.cropped = self.points
        
        # get index of points in selection
        else:
            length = len(self.points)
            
            # interval halving
            int1 = [0,length]
            while int1[1] - int1[0] > 1:
                i1 = int( sum( int1) / 2)
                if self.points[i1][0] < minX:
                    int1[0] = i1
                else:
                    int1[1] = i1
            
            int2 = [0,length]
            while int2[1] - int2[0] > 1:
                i2 = int( sum( int2) / 2)
                if self.points[i2][0] > maxX:
                    int2[1] = i2
                else:
                    int2[0] = i2
            
            i1 = int1[0]
            i2 = int2[1]
            
            if self.points[i1][0] < minX:
                i1 = int1[1]
            if self.points[i2-1][0] > maxX:
                i2 = int2[0]
            
            self.cropped = self.points[i1:i2]
    # ----
    
    
    def scaleAndShift(self, scale, shift):
        """Scale and shift points"""
        
        # recalculate data
        if len(self.points) != 0:
            self.scaled = calculations.scaleAndShift(self.cropped, scale[0], scale[1], shift[0], shift[1])
        
        self.currentScale = scale
        self.currentShift = shift
    # ----
    
    
    def filterPoints(self, filterSize):
        """Filter points for printing and exporting"""
        pass
    # ----
    
    
    def draw(self, dc, printerScale):
        """Define how to draw points"""
        
        # escape no data
        if len(self.scaled) == 0:
            return
        
        # set pen and brush
        pencolour = [max(x-70,0) for x in self.properties['pointColour']]
        pen = wx.Pen(pencolour, 1*printerScale, wx.SOLID)
        brush = wx.Brush(self.properties['pointColour'], wx.SOLID)
        dc.SetPen(pen)
        dc.SetBrush(brush)
        
        # draw points
        for point in self.scaled:
            dc.DrawCircle(point[0], point[1], self.properties['pointSize']*printerScale)
    # ----
    
    
    def drawGel(self, dc, printerScale):
        """Define how to draw gel."""
        pass
    # ----
    
    
    def makeLabels(self, dc, printerScale):
        """Return object labels."""
        return []
    # ----
    
    
    def _calcBoundingBox(self, data):
        """Calculate max ranges for given data"""
        
        if len(data) == 0:
            return False
        
        minXY = numpy.minimum.reduce(data)
        maxXY = numpy.maximum.reduce(data)
        
        # extend values slightly to fit data
        if not self.properties['exactFit']:
            xExtend = (maxXY[0] - minXY[0]) * 0.05
            yExtend = (maxXY[1] - minXY[1]) * 0.05
            minXY[0] -= xExtend
            maxXY[0] += xExtend
            minXY[1] -= yExtend
            maxXY[1] += yExtend
        
        # check axis
        if minXY[0] == maxXY[0]:
            minXY[0] -= 0.5
            maxXY[0] += 0.5
        if minXY[1] == maxXY[1]:
            maxXY[1] += 0.5
        
        return [minXY, maxXY]
    # ----
    


class lines:
    """Base class for simple lines drawing."""
    
    def __init__(self, points, **attr):
        
        # convert points to array
        self.points = numpy.array(points)
        self.cropped = self.points
        self.scaled = self.cropped
        
        self.currentScale = (1, 1)
        self.currentShift = (0, 0)
        
        # set default params
        self.properties = {
                            'legend': '',
                            'visible':True,
                            'showInGel': True,
                            'showPoints': True,
                            'lineColour': (0, 0, 255),
                            'lineWidth': 1,
                            'lineStyle': wx.SOLID
                            }
        
        # get new attributes
        for name, value in attr.items():
            self.properties[name] = value
    # ----
    
    
    def setProperties(self, **attr):
        """Set object properties."""
        
        for name, value in attr.items():
            self.properties[name] = value
    # ----
    
    
    def isVisible(self):
        """Return object visibility"""
        
        return self.properties['visible']
    # ----
    
    
    def getBoundingBox(self, minX=None, maxX=None):
        """Get bounding box for whole data or X selection"""
        
        # use relevant data
        if minX!=None and maxX!=None:
            self.cropPoints(minX, maxX)
            return self._calcBoundingBox(self.cropped)
        else:
            return self._calcBoundingBox(self.points)
    # ----
    
    
    def getLegend(self):
        """Get legend"""
        
        return (self.properties['legend'], self.properties['lineColour'])
    # ----
    
    
    def getPoint(self, xPos, userCoord=False):
        """Get interpolated y position for given x."""
        
        # find Y coordinations
        pointsLen = len(self.points)
        if pointsLen != 0:
            
            # get relevant sub-part to speed-up the process
            startIndex = 0
            for i in range(0, pointsLen, 500):
                if self.points[i][0] > xPos:
                    break
                else:
                    startIndex = i
            
            # get index of nearest higher point
            index = 0
            for i in range(startIndex, pointsLen):
                if self.points[i][0] > xPos:
                    index = i
                    break
            
            # interpolate between two points
            x1 = self.points[index-1][0]
            y1 = self.points[index-1][1]
            x2 = self.points[index][0]
            y2 = self.points[index][1]
            yPos = y1 + ((xPos - x1) * (y2 - y1)/(x2 - x1))
            
            # get point values and coordinates
            point = []
            if userCoord:
                point.append(self.currentScale[0] * xPos + self.currentShift[0])
                point.append(self.currentScale[1] * yPos + self.currentShift[1])
            else:
                point.append(xPos)
                point.append(yPos)
            
        # no points in object
        else:
            if userCoord:
                point = [xPos, 0, 0, 0]
            else:
                point = [xPos, 0]
            
        return point
    # ----
    
    
    def cropPoints(self, minX, maxX):
        """Crop spectrum points to current view coordinations"""
        
        # if no data
        if len(self.points)==0:
            self.cropped = self.points[:]
        
        # get index of points in selection
        else:
            length = len(self.points)
            
            # interval halving
            int1 = [0,length]
            while int1[1] - int1[0] > 1:
                i1 = int( sum( int1) / 2)
                if self.points[i1][0] < minX:
                    int1[0] = i1
                else:
                    int1[1] = i1
            
            int2 = [0,length]
            while int2[1] - int2[0] > 1:
                i2 = int( sum( int2) / 2)
                if self.points[i2][0] > maxX:
                    int2[1] = i2
                else:
                    int2[0] = i2
            
            i1 = int1[0]
            i2 = int2[1]+1
            
            # set crop
            self.cropped = self.points[i1:i2]
    # ----
    
    
    def scaleAndShift(self, scale, shift):
        """Scale and shift points"""
        
        # recalculate data
        if len(self.cropped)==0:
            self.scaled = self.cropped
        else:
            self.scaled = calculations.scaleAndShift(self.cropped, scale[0], scale[1], shift[0], shift[1])
        
        self.currentScale = scale
        self.currentShift = shift
    # ----
    
    
    def filterPoints(self, filterSize):
        """Filter points for printing and exporting"""
        
        # filter data
        if len(self.scaled) > 0:
            self.scaled = calculations.filterPoints(self.scaled, filterSize)
    # ----
    
    
    def draw(self, dc, printerScale):
        """Define how to draw points"""
        
        # escape no data
        if len(self.scaled) < 2:
            return
        
        # set pen and brush
        pen = wx.Pen(self.properties['lineColour'], self.properties['lineWidth']*printerScale, self.properties['lineStyle'])
        dc.SetPen(pen)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        
        # draw lines
        dc.DrawLines(self.scaled)
        
        # draw points
        if self.properties['showPoints'] and len(self.scaled)>3:
            resolution = self.scaled[-1][0] - self.scaled[0][0]
            if resolution/len(self.scaled) > (3*printerScale):
                for point in self.scaled:
                    dc.DrawCircle(point[0], point[1], 2*printerScale)
    # ----
    
    
    def drawGel(self, dc, gelCoords, gelHeight, printerScale):
        """Define how to draw gel"""
        
        # draw spectrum gel
        if not len(self.scaled) > 0:
            return
        
        # get plot coordinates
        gelY1, plotX1, plotY1, plotX2, plotY2 = gelCoords
        
        # set color step
        step = (plotY2 - plotY1) / 255
        if step == 0:
            return False
        
        # init brush
        dc.SetPen(wx.TRANSPARENT_PEN)
        brush = wx.Brush((255,255,255), wx.SOLID)
        dc.SetBrush(brush)
        
        # get first point and color
        lastX = round(self.scaled[0][0])
        lastY = 255
        maxY = 255
        
        # draw rectangles
        for point in self.scaled:
            
            # get point
            xPos = round(point[0])
            intens = round((point[1] - plotY1)/step)
            intens = min(intens, 255)
            intens = max(intens, 0)
            
            # filter points
            if xPos-lastX >= printerScale:
                
                # set color if different
                if lastY != maxY:
                    brush.SetColour((maxY, maxY, maxY))
                    dc.SetBrush(brush)
                    
                # draw point rectangle
                dc.DrawRectangle(lastX, gelY1, xPos-lastX, gelHeight)
                
                # save last
                lastX = xPos
                lastY = maxY
                maxY = intens
                continue
                
            # get highest intensity
            maxY = min(intens, maxY)
            
        # draw legend circle
        x = plotX2 - 9 * printerScale
        y = gelY1 + (gelHeight)/2
        pencolour = [max(i-70,0) for i in self.properties['lineColour']]
        pen = wx.Pen(pencolour, 1*printerScale, wx.SOLID)
        brush = wx.Brush(self.properties['lineColour'], wx.SOLID)
        dc.SetPen(pen)
        dc.SetBrush(brush)
        dc.DrawCircle(x, y, 3*printerScale)
    # ----
    
    
    def makeLabels(self, dc, printerScale):
        """Return object labels."""
        return []
    # ----
    
    
    def _calcBoundingBox(self, data):
        """Calculate max ranges for given data"""
        
        if len(data) == 0:
            return False
        
        minXY = numpy.minimum.reduce(data)
        maxXY = numpy.maximum.reduce(data)
        
        # extend Y values slightly
        yExtend = (maxXY[1] - minXY[1]) * 0.05
        if yExtend:
            maxXY[1] += yExtend
        else:
            maxXY[1] += 1
        
        return [minXY, maxXY]
    # ----
    


class spectrum:
    """Base class for spectrum drawing."""
    
    def __init__(self, scan, **attr):
        
        # convert spectrum points to array
        self.spectrumPoints = numpy.array(scan.points)
        self.spectrumCropped = self.spectrumPoints
        self.spectrumScaled = self.spectrumCropped
        
        # convert peaklist points to array
        self.peaklist = scan.peaklist
        self.peaklistPoints = numpy.array([[peak.mz, peak.intensity, peak.baseline] for peak in scan.peaklist])
        self.peaklistCropped = self.peaklistPoints
        self.peaklistScaled = self.peaklistCropped
        self.peaklistCroppedPeaks = self.peaklist
        
        self.currentScale = (1, 1)
        self.currentShift = (0, 0)
        
        # set default params
        self.properties = {
                            'legend': '',
                            'visible': True,
                            'showInGel': True,
                            'showSpectrum': True,
                            'showPoints': True,
                            'showLabels': True,
                            'showTicks': True,
                            'showGelLegend': True,
                            
                            'spectrumColour': (0, 0, 255),
                            'spectrumWidth': 1,
                            'spectrumStyle': wx.SOLID,
                            
                            'labelAngle': 90,
                            'labelDigits': 2,
                            'labelCharge': False,
                            'labelBgr': True,
                            'labelColour': (0, 0, 0),
                            'labelBgrColour': (255, 255, 255),
                            'labelFont': wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0),
                            
                            'tickColour': (200, 200, 200),
                            'tickWidth': 1,
                            'tickStyle': wx.SOLID,
                            }
        
        # get new attributes
        for name, value in attr.items():
            self.properties[name] = value
    # ----
    
    
    def setProperties(self, **attr):
        """Set object properties."""
        
        for name, value in attr.items():
            self.properties[name] = value
    # ----
    
    
    def isVisible(self):
        """Return object visibility."""
        
        return self.properties['visible']
    # ----
    
    
    def getBoundingBox(self, minX=None, maxX=None):
        """Get bounding box for whole data or x-axis selection."""
        
        # use relevant data
        if minX!=None and maxX!=None:
            self.cropPoints(minX, maxX)
            return self._calcBoundingBox('cropped')
        else:
            return self._calcBoundingBox('points')
    # ----
    
    
    def getLegend(self):
        """Get legend."""
        
        # spectrum visible
        if len(self.spectrumPoints) > 0 and self.properties['showSpectrum']:
            return (self.properties['legend'], self.properties['spectrumColour'])
        
        # only peaklist visible
        elif len(self.peaklistPoints) > 0 and self.properties['showTicks']:
            return (self.properties['legend'], self.properties['tickColour'])
        
        else:
            return (self.properties['legend'], self.properties['tickColour'])
    # ----
    
    
    def getPoint(self, xPos, userCoord=False):
        """Get interpolated y position for given x."""
        
        # find Y coordinations
        pointsLen = len(self.spectrumPoints)
        if pointsLen != 0:
            
            # get relevant sub-part to speed-up the process
            startIndex = 0
            for i in range(0, pointsLen, 500):
                if self.spectrumPoints[i][0] > xPos:
                    break
                else:
                    startIndex = i
            
            # get index of nearest higher point
            index = 0
            for i in range(startIndex, pointsLen):
                if self.spectrumPoints[i][0] > xPos:
                    index = i
                    break
            
            # interpolate between two points
            x1 = self.spectrumPoints[index-1][0]
            y1 = self.spectrumPoints[index-1][1]
            x2 = self.spectrumPoints[index][0]
            y2 = self.spectrumPoints[index][1]
            yPos = y1 + ((xPos - x1) * (y2 - y1)/(x2 - x1))
            
            # get point values and coordinates
            point = []
            if userCoord:
                point.append(self.currentScale[0] * xPos + self.currentShift[0])
                point.append(self.currentScale[1] * yPos + self.currentShift[1])
            else:
                point.append(xPos)
                point.append(yPos)
            
        # no points in object
        else:
            if userCoord:
                point = [xPos, 0, 0, 0]
            else:
                point = [xPos, 0]
            
        return point
    # ----
    
    
    def cropPoints(self, minX, maxX):
        """Crop spectrum points to current view coordinations"""
        
        # crop spectrum data
        if self.properties['showSpectrum']:
            self._cropSpectrumPoints(minX, maxX)
        
        # crop peaklist data
        if self.properties['showSpectrum'] or self.properties['showLabels'] or self.properties['showTicks']:
            self._cropPeaklistPoints(minX, maxX)
    # ----
    
    
    def scaleAndShift(self, scale, shift):
        """Scale and shift spectrum points"""
        
        # scale and shift spectrum data
        if self.properties['showSpectrum']:
            
            # if no data
            if len(self.spectrumCropped)==0:
                self.spectrumScaled = self.spectrumCropped
            else:
                self.spectrumScaled = calculations.scaleAndShift(self.spectrumCropped, scale[0], scale[1], shift[0], shift[1])
                
        # scale and shift peaklist data
        if self.properties['showSpectrum'] or self.properties['showLabels'] or self.properties['showTicks']:
            
            # if no data
            if len(self.peaklistCropped)==0:
                self.peaklistScaled = self.peaklistCropped
            else:
                scale = numpy.array((scale[0], scale[1], scale[1]))
                shift = numpy.array((shift[0], shift[1], shift[1]))
                self.peaklistScaled = scale * self.peaklistCropped + shift
        
        self.currentScale = scale
        self.currentShift = shift
    # ----
    
    
    def filterPoints(self, filterSize):
        """Delete all spectrum points invisible in current resolution"""
        
        # filter spectrum data
        if len(self.spectrumScaled) > 0 and self.properties['showSpectrum']:
            self.spectrumScaled = calculations.filterPoints(self.spectrumScaled, filterSize)
    # ----
    
    
    def draw(self, dc, printerScale):
        """Define how to draw spectrum lines"""
        
        # draw line spectrum
        if len(self.spectrumScaled) > 2 and self.properties['showSpectrum']:
            self._drawSpectrum(dc, printerScale)
        
        # draw peaklist ticks
        if len(self.peaklistScaled) > 0 and (self.properties['showTicks'] or len(self.spectrumPoints)==0):
            self._drawPeaklistTicks(dc, printerScale)
    # ----
    
    
    def drawGel(self, dc, gelCoords, gelHeight, printerScale):
        """Define how to draw spectrum gel"""
        
        # draw line spectrum gel
        if len(self.spectrumScaled) > 0 and self.properties['showSpectrum']:
            self._drawSpectrumGel(dc, gelCoords, gelHeight, printerScale)
        
        # draw peaklist gel
        elif len(self.peaklistScaled) > 0 and (self.properties['showSpectrum'] or self.properties['showLabels'] or self.properties['showTicks']):
            self._drawPeaklistGel(dc, gelCoords, gelHeight, printerScale)
        
    # ----
    
    
    def makeLabels(self, dc, printerScale):
        """Return object labels."""
        
        # check labels
        if not self.properties['showLabels'] or len(self.peaklistScaled) == 0:
            return []
        
        # set font
        if printerScale != 1:
            dc.SetFont(_scaleFont(self.properties['labelFont'], printerScale))
        else:
            dc.SetFont(self.properties['labelFont'])
        
        # prepare labels
        labels = []
        format = '%0.'+`self.properties['labelDigits']`+'f'
        for x, peak in enumerate(self.peaklistScaled):
            
            # get position
            xPos = peak[0]
            yPos = peak[1]
            
            # get label
            label = format % self.peaklistCroppedPeaks[x].mz
            
            # add charge to label
            if self.properties['labelCharge'] and self.peaklistCroppedPeaks[x].charge != None:
                label += ' (%d)' % self.peaklistCroppedPeaks[x].charge
            
            # get text position
            textSize = dc.GetTextExtent(label)
            if self.properties['labelAngle'] == 90:
                textXPos = xPos - textSize[1]*0.5
                textYPos = yPos - 5*printerScale
                textSize = (textSize[1], textSize[0])
            elif self.properties['labelAngle'] == 0:
                textXPos = xPos - textSize[0]*0.5
                textYPos = yPos - textSize[1] - 4*printerScale
            
            # add label and sort by intensity
            labels.append((self.peaklistCroppedPeaks[x].intensity, label, (textXPos,textYPos), textSize, self.properties))
            
        return labels
    # ----
    
    
    def _calcBoundingBox(self, datatype='points'):
        """Calculate bounding box for spectrum and peaklist together."""
        
        spectrumBox = None
        peaklistBox = None
        
        # use cropped data (selection)
        if datatype == 'cropped':
            if self.properties['showSpectrum']:
                spectrumBox = self._calcSpectrumBoundingBox(self.spectrumCropped)
            if self.properties['showSpectrum'] or self.properties['showLabels'] or self.properties['showTicks']:
                peaklistBox = self._calcPeaklistBoundingBox(self.peaklistCropped)
        
        # use raw data (all)
        else:
            if self.properties['showSpectrum']:
                spectrumBox = self._calcSpectrumBoundingBox(self.spectrumPoints)
            if self.properties['showSpectrum'] or self.properties['showLabels'] or self.properties['showTicks']:
                peaklistBox = self._calcPeaklistBoundingBox(self.peaklistPoints)
        
        # use both
        box = [numpy.array([0, 0]), numpy.array([1, 1])]
        if spectrumBox and peaklistBox:
            box[0] = numpy.minimum(spectrumBox[0], peaklistBox[0])
            box[1] = numpy.maximum(spectrumBox[1], peaklistBox[1])
            return box
        elif spectrumBox:
            return spectrumBox
        elif peaklistBox:
            return peaklistBox
        else:
            return False
    # ----
    
    
    def _calcSpectrumBoundingBox(self, data):
        """Calculate max ranges for given spectrum data"""
        
        if len(data) == 0:
            return False
        
        minXY = numpy.minimum.reduce(data)
        maxXY = numpy.maximum.reduce(data)
        
        # extend Y values slightly
        yExtend = (maxXY[1] - minXY[1]) * 0.05
        if yExtend:
            maxXY[1] += yExtend
        else:
            maxXY[1] += 1
        
        return [minXY, maxXY]
    # ----
    
    
    def _calcPeaklistBoundingBox(self, data):
        """Calculate max ranges for given peaklist data."""
        
        if len(data) == 0:
            return False
        
        minXY = numpy.minimum.reduce(data)
        minXY = [minXY[0], min(minXY[1:])]
        maxXY = numpy.maximum.reduce(data)
        maxXY = [maxXY[0], max(maxXY[1:])]
        
        # extend Y values to fit labels
        factor = 0
        if self.properties['showLabels'] and self.properties['labelAngle']==0:
            factor += 0.1
        elif self.properties['showLabels'] and self.properties['labelAngle']==90:
            factor += 0.4
        maxXY[1] += (maxXY[1] - minXY[1]) * factor
        
        # extend X values to fit labels
        xExtend = (maxXY[0] - minXY[0]) * 0.02
        minXY[0] -= xExtend
        maxXY[0] += xExtend
        
        return [minXY, maxXY]
    # ----
    
    
    def _cropSpectrumPoints(self, minX, maxX):
        """Crop spectrum points to current view coordinations"""
        
        # if no data
        if len(self.spectrumPoints)==0:
            self.spectrumCropped = self.spectrumPoints
        
        # get index of points in selection
        else:
            length = len( self.spectrumPoints)
            
            # interval halving
            int1 = [0,length]
            while int1[1] - int1[0] > 1:
                i1 = int( sum( int1) / 2)
                if self.spectrumPoints[i1][0] < minX:
                    int1[0] = i1
                else:
                    int1[1] = i1
            
            int2 = [0,length]
            while int2[1] - int2[0] > 1:
                i2 = int( sum( int2) / 2)
                if self.spectrumPoints[i2][0] > maxX:
                    int2[1] = i2
                else:
                    int2[0] = i2
            
            i1 = int1[0]
            i2 = int2[1]+1
            
            # crop data
            self.spectrumCropped = self.spectrumPoints[i1:i2]
    # ----
    
    
    def _cropPeaklistPoints(self, minX, maxX):
        """Crop peaklist ponts."""
        
        # if no data
        if len(self.peaklistPoints)==0:
            self.peaklistCropped = self.peaklistPoints
            self.peaklistCroppedPeaks = self.peaklist
        
        # get index of points in selection
        else:
            length = len(self.peaklistPoints)
            
            # interval halving
            int1 = [0,length]
            while int1[1] - int1[0] > 1:
                i1 = int( sum( int1) / 2)
                if self.peaklistPoints[i1][0] < minX:
                    int1[0] = i1
                else:
                    int1[1] = i1
            
            int2 = [0,length]
            while int2[1] - int2[0] > 1:
                i2 = int( sum( int2) / 2)
                if self.peaklistPoints[i2][0] > maxX:
                    int2[1] = i2
                else:
                    int2[0] = i2
            
            i1 = int1[0]
            i2 = int2[1]
            
            if self.peaklistPoints[i1][0] < minX:
                i1 = int1[1]
            if self.peaklistPoints[i2-1][0] > maxX:
                i2 = int2[0]
            
            # crop data
            self.peaklistCropped = self.peaklistPoints[i1:i2]
            self.peaklistCroppedPeaks = self.peaklist[i1:i2]
    # ----
    
    
    def _drawSpectrum(self, dc, printerScale):
        """Define how to draw spectrum lines"""
        
        # set pen and brush
        pen = wx.Pen(self.properties['spectrumColour'], self.properties['spectrumWidth']*printerScale, self.properties['spectrumStyle'])
        brush = wx.Brush(self.properties['spectrumColour'], wx.SOLID)
        dc.SetPen(pen)
        dc.SetBrush(brush)
        
        # draw lines
        dc.DrawLines(self.spectrumScaled)
        
        # draw points
        if self.properties['showPoints'] and len(self.spectrumScaled)>3:
            resolution = self.spectrumScaled[-1][0] - self.spectrumScaled[0][0]
            if resolution/len(self.spectrumScaled) > (3*printerScale):
                for point in self.spectrumScaled:
                    dc.DrawCircle(point[0], point[1], 2*printerScale)
    # ----
    
    
    def _drawSpectrumGel(self, dc, gelCoords, gelHeight, printerScale):
        """Define how to draw spectrum gel"""
        
        # get plot coordinates
        gelY1, plotX1, plotY1, plotX2, plotY2 = gelCoords
        
        # set color step
        step = (plotY2 - plotY1) / 255
        if step == 0:
            return False
        
        # init brush
        dc.SetPen(wx.TRANSPARENT_PEN)
        brush = wx.Brush((255,255,255), wx.SOLID)
        dc.SetBrush(brush)
        
        # get first point and color
        lastX = round(self.spectrumScaled[0][0])
        lastY = 255
        maxY = 255
        
        # draw gel
        for point in self.spectrumScaled:
            
            # get point
            xPos = round(point[0])
            intens = round((point[1] - plotY1)/step)
            intens = min(intens, 255)
            intens = max(intens, 0)
            
            # filter points
            if xPos-lastX >= printerScale:
                
                # set color if different
                if lastY != maxY:
                    brush.SetColour((maxY, maxY, maxY))
                    dc.SetBrush(brush)
                    
                # draw point rectangle
                try: dc.DrawRectangle(lastX, gelY1, xPos-lastX, gelHeight)
                except: pass
                
                # save last
                lastX = xPos
                lastY = maxY
                maxY = intens
                continue
                
            # get highest intensity
            maxY = min(intens, maxY)
        
        # set dc for legend
        pencolour = [max(i-70,0) for i in self.properties['spectrumColour']]
        pen = wx.Pen(pencolour, 1*printerScale, wx.SOLID)
        dc.SetPen(pen)
        dc.SetTextForeground(self.properties['spectrumColour'])
        dc.SetBrush(wx.Brush(self.properties['spectrumColour'], wx.SOLID))
        
        # draw legend text
        if self.properties['showGelLegend'] and self.properties['legend']:
            textSize = dc.GetTextExtent(self.properties['legend'])
            x = plotX2 - textSize[0] - 17*printerScale
            y = gelY1 + gelHeight/2 - textSize[1]/2
            dc.DrawText(self.properties['legend'], x, y)
        
        # draw legend circle
        x = plotX2 - 9 * printerScale
        y = gelY1 + (gelHeight)/2
        dc.DrawCircle(x, y, 3*printerScale)
    # ----
    
    
    def _drawPeaklistTicks(self, dc, printerScale):
        """Define how to draw peaklist ticks"""
        
        # set pen params
        peakPen = wx.Pen(self.properties['tickColour'], self.properties['tickWidth']*printerScale, self.properties['tickStyle'])
        dc.SetPen(peakPen)
        
        peakBrush = wx.Brush(self.properties['tickColour'], wx.SOLID)
        dc.SetBrush(peakBrush)
        
        # draw ticks
        for x, peak in enumerate(self.peaklistScaled):
            dc.DrawLine(peak[0], peak[2], peak[0], peak[1])
            dc.DrawLine(peak[0]-3*printerScale, peak[2], peak[0]+3*printerScale, peak[2])
            
            # mark monoisotopic peak
            if self.peaklistCroppedPeaks[x].isotope == 0:
                dc.DrawRectangle(peak[0]-1*printerScale, peak[1]-1*printerScale, 3*printerScale, 3*printerScale)
    # ----
    
    
    def _drawPeaklistGel(self, dc, gelCoords, gelHeight, printerScale):
        """Define how to draw peaklist gel"""
        
        # get plot coordinates
        gelY1, plotX1, plotY1, plotX2, plotY2 = gelCoords
        
        # set color step
        step = (plotY2 - plotY1) / 255
        if step == 0:
            return False
        
        # init brush
        pen = wx.Pen((255,255,255), printerScale, wx.SOLID)
        brush = wx.TRANSPARENT_BRUSH
        dc.SetPen(pen)
        dc.SetBrush(brush)
        
        # get first point and color
        lastX = round(self.peaklistScaled[0][0])
        lastY = 255
        maxY = 255
        
        # draw rectangles
        last = len(self.peaklistScaled)-1
        for x, point in enumerate(self.peaklistScaled):
            
            # get intensity colour
            xPos = round(point[0])
            intens = round(((point[1] - plotY1)-(plotY2-point[2]))/step)
            intens = min(intens, 255)
            intens = max(intens, 0)
            
            # draw first
            if x==0:
                pen.SetColour((intens, intens, intens))
                dc.SetPen(pen)
                try: dc.DrawLine(xPos, gelY1, xPos, gelY1+gelHeight)
                except: pass
            
            # filter points
            if xPos-lastX >= printerScale:
                
                # set color if different
                if lastY != maxY:
                    pen.SetColour((maxY, maxY, maxY))
                    dc.SetPen(pen)
                    
                # draw peak line
                try: dc.DrawLine(lastX, gelY1, lastX, gelY1+gelHeight)
                except: pass
                
                # save last
                lastX = xPos
                lastY = maxY
                maxY = intens
                
                # draw last
                if x==last:
                    pen.SetColour((maxY, maxY, maxY))
                    dc.SetPen(pen)
                    try: dc.DrawLine(xPos, gelY1, xPos, gelY1+gelHeight)
                    except: pass
                
                continue
                
            # get highest intensity
            maxY = min(intens, maxY)
        
        # set dc for legend
        pencolour = [max(i-70,0) for i in self.properties['tickColour']]
        pen = wx.Pen(pencolour, 1*printerScale, wx.SOLID)
        dc.SetPen(pen)
        dc.SetTextForeground(self.properties['tickColour'])
        dc.SetBrush(wx.Brush(self.properties['tickColour'], wx.SOLID))
        
        # draw legend text
        if self.properties['showGelLegend'] and self.properties['legend']:
            textSize = dc.GetTextExtent(self.properties['legend'])
            x = plotX2 - textSize[0] - 17*printerScale
            y = gelY1 + gelHeight/2 - textSize[1]/2
            dc.DrawText(self.properties['legend'], x, y)
        
        # draw legend circle
        x = plotX2 - 9 * printerScale
        y = gelY1 + gelHeight/2
        dc.DrawCircle(x, y, 3*printerScale)
    # ----
    
    


# UTILITIES
# ---------

def _scaleFont(font, printerScale):
    """Scale font for printing"""
    
    # check printerScale
    if printerScale == 1:
        return font
    
    # get font
    pointSize = font.GetPointSize()
    family = font.GetFamily()
    style = font.GetStyle()
    weight = font.GetWeight()
    underline = font.GetUnderlined()
    faceName = font.GetFaceName()
    encoding = font.GetDefaultEncoding()
    
    # scale pointSize
    pointSize = pointSize * printerScale * 1.3
    
    # make print font
    printerFont = wx.Font(pointSize, family, style, weight, underline, faceName, encoding)
    
    return printerFont
# ----


def _checkFreeSpace(pos, size, occupied):
    """Check free space for label."""
    
    xPos = True
    yPos = True
    
    curX1 = pos[0]
    curX2 = pos[0] + size[0]
    curY1 = pos[1]
    curY2 = pos[1] - size[1]
    
    # check occupied space
    for occ in occupied:
        
        # check X
        occX1 = occ[0][0]
        occX2 = occ[0][0] + occ[1][0]
        if ((curX1 >= occX1) and (curX1 <= occX2)) or ((curX2 >= occX1) and (curX2 <= occX2)):
            xPos = False
            
            # check Y
            occY1 = occ[0][1]
            occY2 = occ[0][1] - occ[1][1]
            if ((curY1 <= occY1) and (curY1 >= occY2)) or ((curY2 <= occY1) and (curY2 >= occY2)):
                yPos = False
                break
    
    if xPos or yPos:
        return True
    else:
        return False
# ----



