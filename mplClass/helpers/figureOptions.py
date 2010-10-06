# -*- coding: utf-8 -*-
#
# Copyright © 2009 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see pydeelib/__init__.py for details)

"""
Module that provides a GUI-based editor for matplotlib's figure options

Apparently there is still a problem with setting the color of the vlines from the edit dialog....9/28/2010

"""

from formlayout import fedit
import matplotlib.colors as C
from matplotlib import collections as COLLECTIONS_MPL

LINESTYLES = {
              '-': 'Solid',
              '--': 'Dashed',
              '-.': 'DashDot',
              ':': 'Dotted',
              'steps': 'Steps',
              'none': 'None',
              }

MARKERS = {
           'none': 'None',
           'o': 'circles',
           '^': 'triangle_up',
           'v': 'triangle_down',
           '<': 'triangle_left',
           '>': 'triangle_right',
           's': 'square',
           '+': 'plus',
           'x': 'cross',
           '*': 'star',
           'D': 'diamond',
           'd': 'thin_diamond',
           '1': 'tripod_down',
           '2': 'tripod_up',
           '3': 'tripod_left',
           '4': 'tripod_right',
           'h': 'hexagon',
           'H': 'rotated_hexagon',
           'p': 'pentagon',
           '|': 'vertical_line',
           '_': 'horizontal_line',
           '.': 'dots',
           }

COLORS = {'b': '#0000ff', 'g': '#00ff00', 'r': '#ff0000', 'c': '#ff00ff',
          'm': '#ff00ff', 'y': '#ffff00', 'k': '#000000', 'w': '#ffffff'}

def hex_to_rgb(rgbVal):
    rgbVal = rgbVal.lstrip('#')
    lv = len(rgbVal)
    return tuple(int(rgbVal[i:i+lv/3], 16) for i in range(0, lv, lv/3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def col2hex(color):
    """Convert matplotlib color to hex"""
    return COLORS.get(color, color)

def convertMPLColor(cValue, useRGBA = False):
    converter = C.ColorConverter()
    if useRGBA:
        return converter.to_rgba(cValue)
    else:
        return converter.to_rgb(cValue)

def getMPLColor(cValue):
    #print cValue
    if type(cValue) is str or type(cValue) is unicode:
        if "#" in cValue:
            return cValue
        elif COLORS.has_key(cValue):
            return COLORS[cValue]
    elif type(cValue) is list:
        tempColor = []
        for i in cValue[:3]:
            tempColor.append(int(i*255))
        return rgb_to_hex(tuple(tempColor))
    else:
        print type(cValue), "Failed reverting to black"
        return rgb_to_hex((0.0,0.0,0.0))
        

def setVLines(canvas, axes, status = False):
    '''
    CircleCollections get an error when converting back...from vlines
    '''
    has_curve = len(axes.get_lines())>0
    has_collection = len(axes.collections)>0
    if has_curve and status:
        xmin, xmax = axes.get_xlim()
        for line in axes.get_lines():
            label = line.get_label()
            color = getMPLColor(line.get_color())
            linewidth = line.get_linewidth()
            alpha = line.get_alpha()
            xData = line.get_xdata()
            yData = line.get_ydata()
            axes.lines.remove(line)
            v = axes.vlines(xData, xmin, yData, alpha = alpha, linewidth = linewidth, label = label)
            #print "VLINES COLOR", color, convertMPLColor(color)
            v.set_color(convertMPLColor(color))#for some reason setting this in the kwargs fails
        
        canvas.draw()
                
    elif has_collection and not status:
        for col in axes.collections:
            if isinstance(col, COLLECTIONS_MPL.LineCollection):
                label = col.get_label()
                color = getMPLColor(col.get_color()[0].tolist())
                linewidth = col.get_linewidth()[0]
                alpha = col.get_alpha()         
                paths = col.get_paths()
                xData = []
                yData = []            
                for p in paths:
                    for val in p.iter_segments():
                        if val[1] == 2:
                            xData.append(val[0][0])
                            yData.append(val[0][1])
                axes.collections.remove(col)                        
                axes.plot(xData, yData, color = color, alpha = alpha, linewidth = linewidth, label = label)


            canvas.draw()


def editTexts(canvas, axes, parent=None):
    """
    Edit matplotlib figure options
    Need add case for multiple axes....
    """
    axes = axes
    sep = (None, None) # separator
    
    has_text = len(axes.texts)>0
    
    if has_text:
        textDict = {}
        for i,t in enumerate(axes.texts):
            textDict['label %s'%(i+1)] = t
        texts = []
        textLabels = sorted(textDict.keys())
        for label in textLabels:
            t = textDict[label]
            textdata = [
                        ('Label', label),#Doesn't matter if this is changed...
                        sep,
                        (None, '<b>Edit Text</b>'),
                        ('Text', t.get_text()),
                        ('Size', t.get_fontsize()),
                        ('Color', getMPLColor(t.get_color())),
                        sep,
                        ('Alpha', t.get_alpha()),
                        ('Rotation', t.get_rotation()),
                        ('X Position', t.get_position()[0]),
                        ('Y Position', t.get_position()[1]),
                        ('Remove', False),
                        
                        #~ ('Facecolor', getMPLColor(line.get_markerfacecolor())),
                        #~ ('Edgecolor', getMPLColor(line.get_markeredgecolor()))
                        ]
            texts.append([textdata, label, ""])
        
        datalist = [(texts, "Texts", "")]
        result = fedit(datalist, title="Text Options", parent=parent)
        #~ print result
        if result is None:
            return        
        
        textVals, = result
        for i, text in enumerate(textVals):
            label, textStr, fontsize, color, alpha, rotation, xPos, yPos, removeBool= text
            t = textDict[textLabels[i]]
            setTextProperties(axes, t, label, str(textStr), fontsize, color, alpha, rotation, xPos, yPos, removeBool)
        
        canvas.draw()
        
def figure_edit(canvas, axes, parent=None):
    """Edit matplotlib figure options"""
    axes = axes
    sep = (None, None) # separator
    
    has_curve = len(axes.get_lines())>0
    has_collection = len(axes.collections)>0
    
    # Get / General
    xmin, xmax = axes.get_xlim()
    ymin, ymax = axes.get_ylim()
    general = [('Title', axes.get_title()),
               ('Font Size', axes.title.get_fontsize()),
               sep,
               (None, "<b>X-Axis</b>"),
               ('Min', xmin), ('Max', xmax),
               ('Label', axes.get_xlabel()),
               ('Label Size', axes.xaxis.label.get_fontsize()),
               ('Tick Label Size', axes.get_xticklabels()[0].get_fontsize()),
               ('Scale', [axes.get_xscale(), 'linear', 'log']),
               sep,
               (None, "<b>Y-Axis</b>"),
               ('Min', ymin), ('Max', ymax),
               ('Label', axes.get_ylabel()),
               ('Label Size', axes.yaxis.label.get_fontsize()),
               ('Tick Label Size', axes.get_yticklabels()[0].get_fontsize()),
               ('Scale', [axes.get_yscale(), 'linear', 'log'])
               ]

    if has_curve:
        # Get / Curves
        linedict = {}
        for line in axes.get_lines():
            label = line.get_label()
            if label == '_nolegend_':
                continue
            linedict[label] = line
        curves = []
        linestyles = LINESTYLES.items()
        markers = MARKERS.items()
        curvelabels = sorted(linedict.keys())
        for label in curvelabels:
            line = linedict[label]
            curvedata = [
                         ('Label', label),
                         sep,
                         (None, '<b>Line</b>'),
                         ('Style', [line.get_linestyle()] + linestyles),
                         ('Width', line.get_linewidth()),
                         ('Color', getMPLColor(line.get_color())),
                         ('Alpha', line.get_alpha()),
                         sep,
                         (None, '<b>Marker</b>'),
                         ('Style', [line.get_marker()] + markers),
                         ('Size', line.get_markersize()),
                         ('Facecolor', getMPLColor(line.get_markerfacecolor())),
                         ('Edgecolor', getMPLColor(line.get_markeredgecolor()))
                         ]
            curves.append([curvedata, label, ""])
        
    if has_collection:
        colDict = {}
        for col in axes.collections:
            if isinstance(col, COLLECTIONS_MPL.LineCollection):
                label = col.get_label()
                if label == '_nolegend_':
                    continue
                colDict[label] = col
        if len(colDict) == 0:
            has_collection = False
        collections = []
        linestyles = LINESTYLES.items()
        colLabels = sorted(colDict.keys())
        for label in colLabels:
            col = colDict[label]
            colData = [
                       ('Label', label),
                       sep,
                       (None, '<b>Line</b>'),
                       #('Style', [col.get_linestyle()] + linestyles),#Ignoring as this is returning None
                       ('Style', ['Solid'] + linestyles),
                       ('Width', col.get_linewidth()[0]),#because it returns a tuple
                       ('Color', getMPLColor(col.get_color()[0].tolist())),
                       ('Alpha', col.get_alpha())                       
                       ]
            collections.append([colData, label, ""])
        
    datalist = [(general, "Axes", "")]    
    if has_curve:
        datalist.append((curves, "Curves", ""))
    if has_collection:
        datalist.append((collections, "Lines", ""))        
        
    #~ print collections
    #~ print "Collections\n\n"
    #~ for i in datalist:
        #~ print i
        #~ print "\n\n"       
    result = fedit(datalist, title="Figure Options", parent=parent)
    #~ print result
    if result is None:
        return
    
    if has_curve and not has_collection:
        general, curves = result
        collections = None
    elif not has_curve and has_collection:
        general, collections = result
        curves = None
    elif has_curve and has_collection:
        general, curves, collections = result
    else:
        general, = result
        curves = None
        collections = None
    
    #print general, curves
    # Set / General
    title, titleSize, xmin, xmax, xlabel, xlabelSize, xtickLabelSize, xscale, ymin, ymax, ylabel, ylabelSize, ytickLabelSize, yscale = general
    setFigProperties(axes, title, titleSize, xmin, xmax, xlabel, xlabelSize, xtickLabelSize, xscale, ymin, ymax, ylabel, ylabelSize, ytickLabelSize, yscale)

    
    if has_curve:
        # Set / Curves
        for index, curve in enumerate(curves):
            line = linedict[curvelabels[index]]
            label, linestyle, linewidth, color, alpha,\
                marker, markersize, markerfacecolor, markeredgecolor = curve
                
            setLineProperties(line, label, linestyle, linewidth, color,\
                              alpha, marker, markersize, markerfacecolor,\
                              markeredgecolor)
    if has_collection:
        for index, collect in enumerate(collections):
            col = colDict[colLabels[index]]
            label, linestyle, linewidth, color, alpha = collect
            # collect
            setVLineProperties(col, label, linestyle, linewidth, str(color), alpha)
    
    # Redraw
    canvas.draw()
    return general, curves, collections

def setTextProperties(axes, text, label, textStr, fontsize, color, alpha, rotation, xPos, yPos, removeBool):
    '''
    Set parameters for a text instance
    '''
    if removeBool:
        text.remove()
    else:
        text.set_label(label)
        text.set_text(textStr)
        text.set_color(color)
        text.set_alpha(alpha)
        text.set_fontsize(fontsize)
        text.set_rotation(rotation)
        text.set_position((xPos, yPos))
    

def setFigProperties(axes, title, titleSize, xmin, xmax, xlabel, xlabelSize, xtickLabelSize, xscale, ymin, ymax, ylabel, ylabelSize, ytickLabelSize, yscale):
    '''
    Set user supplied figure parameters
    '''
    axes.set_xscale(xscale)
    axes.set_yscale(yscale)
    axes.set_title(title, fontsize = titleSize)
    axes.set_xlim(xmin, xmax)
    axes.set_xlabel(xlabel, fontsize = xlabelSize)
    axes.set_ylim(ymin, ymax)
    axes.set_ylabel(ylabel, fontsize = ylabelSize)
    labels_x = axes.get_xticklabels()
    labels_y = axes.get_yticklabels()
    for xlabel in labels_x:
        xlabel.set_fontsize(xtickLabelSize)
    for ylabel in labels_y:
        ylabel.set_fontsize(ytickLabelSize)
        #~ ylabel.set_color('b')    

def setLineProperties(line, label, linestyle, linewidth, color, alpha,\
                      marker, markersize, markerfacecolor, markeredgecolor):
    '''
    Set line properties
    '''
    line.set_label(label)
    line.set_linestyle(linestyle)
    line.set_linewidth(linewidth)
    line.set_color(color)
    line.set_alpha(alpha)
    if marker is not 'none':
        line.set_marker(marker)
        line.set_markersize(markersize)
        line.set_markerfacecolor(markerfacecolor)
        line.set_markeredgecolor(markeredgecolor)
        
def setVLineProperties(collection, label, linestyle, linewidth, color, alpha):
    '''
    Set vline properties
    For some reason these are not updating.....
    '''
    collection.set_label(str(label))
    collection.set_linestyle(linestyle)
    #print linewidth
    collection.set_linewidth(linewidth)
    collection.set_color(convertMPLColor(color))
    collection.set_alpha(alpha)
    #print collection.get_color(), color
    #print collection.get_linewidth(), linewidth
    #print collection.get_alpha(), alpha 
                          
