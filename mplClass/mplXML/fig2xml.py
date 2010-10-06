import matplotlib
#import iplot
#from iplot.obj2xml import xmlel, get_xmltype, get_xmlid, Obj2XML
#from iplot.mpl.backend_iplot import FigureCanvasLabplot
from obj2xml import xmlel, get_xmltype, get_xmlid
from obj2xml import Object2Xml
#from backend_iplot import FigureCanvasIPlot
import re
from xml.sax.saxutils import escape

import zlib
import numpy

'''
import fig2xml
import numpy as N
a = N.arange(20)
b = N.arange(20)
ax = gca()
v = ax.vlines(a,0,b)
ans = fig2xml.Figure2XML(v, 'vlines')
ans.prettyPrint('vlines.xml')

fig = gcf()
ans = fig2xml.Figure2XML(fig)
ans.saveXML('barErr.xml.gz')
'''


class Figure2XML(Object2Xml):
    
    def __init__(self,obj,objname='figure',ignore=[]):
        ignore = [None.__class__]
        
#        ignore = [FigureCanvasIPlot,
#                  #matplotlib.transforms.Bbox,
#                  None.__class__,
#                  ]
        Object2Xml.__init__(self,obj,objname,ignore)
        
        #self._adapt[numpy.ma.MaskedArray] = self._getXML_MA
        self._firstcall = True
        self._refs = []
        self._vars = []
        self.ignoretype = re.compile("("+
                                     "function|instancemethod|module|method|type|"+
                                     "matplotlib.cbook|matplotlib.path|"+
                                     "matplotlib.backends|"+
                                     "matplotlib.transforms.BlendedGenericTransform|"+
                                     "matplotlib.transforms.BboxTransformFrom|"+
                                     "matplotlib.transforms.CompositeGenericTransform|"+
                                     "matplotlib.transforms.BlendedAffine2D|"+
                                     "matplotlib.transforms.TransformWrapper|"+
                                     "matplotlib.transforms.TransformedPath|"+
                                     "matplotlib.transforms.BboxTransformTo|"+
                                     "matplotlib.transforms.TransformedBbox|"+
                                     "matplotlib.transforms.Affine2D|"+
                                     "matplotlib.transforms.IdentityTransform|"+
                                     "matplotlib.transforms.ScaledTranslation|"+
                                     "matplotlib.transforms.CompositeAffine2D"+
                                     ")")

        self._ignoreattr = [
                            "%s.figurePatch" % objname,
                            "%s.bbox" % objname,
                            "%s.bbox_inches" % objname,
                            #"%s.patch" % objname,
                            "%s._axstack" % objname,
                            "%s.callbacks" % objname,
                            "%s.artists" % objname,
                            "%s._cachedRenderer" % objname,
                            #'axes.axesPatch',
                            'axes.patch',
                            'axes.spines',
                            #'axes._position',
                            'axes._originalPosition',
                            'axes._get_lines',
                            'axes._get_patches_for_fill',
                            'axes.callbacks',
                            'axes.figbox',
                            'axes.dataLim',
                            #'lines._markers',
                            #'lines.markers',
                            #'lines.filled_markers',
                            #'lines.lineStyles',
                            'lines.validCap',
                            'lines.validJoin',
                            'lines._xorig',
                            'lines._yorig',
                            'lines._x',
                            'lines._y',
                            '_xy.T', '_xy.base', '_xy.imag','_xy.real','_xy._data',
                            'xaxis.majorTicks', 'xaxis.minorTicks','xaxis.callbacks','xaxis.converter',
                            #'xaxis.major','xaxis.minor',
                            'yaxis.majorTicks', 'yaxis.minorTicks','yaxis.callbacks','yaxis.converter',
                            #'yaxis.major','yaxis.minor',
                            
                            ]
        
        #self._ignoreattr = []
        #self.ignoretype = []
        self.xmlobj = self.getXML(obj,objname)
        
    
#    def _getXML_MA(self,obj,objname=None):
#        pat = re.compile('\s')
#        id = get_xmlid(obj)
#        typ = get_xmltype(obj)
#        self._create_element(objname,id,typ,None)
