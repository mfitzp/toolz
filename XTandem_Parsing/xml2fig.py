import numpy
#from numpy import isscalar, iterable

from matplotlib.transforms import Bbox
from matplotlib.backends import pylab_setup
new_figure_manager, draw_if_interactive, show = pylab_setup()

from matplotlib.pyplot import figure

import re
import xml.dom.minidom
from xml.sax.handler import ContentHandler
from xml.sax import make_parser


def get_type(typestr):
    pass

class XMLFigure(ContentHandler):
    """
    The XML parser. Creates an expat parser, and then handles the defined
    tags specified in 'start_tags' and 'end_tags'. Currently the allowed
    tags are: figure, subplot, plot
    
    """
    
    def create_parser(self):
        parser = make_parser()
        parser.setContentHandler(self)
        return parser         
    
    def __init__(self, xmlfile):
        
        #xmlfig = zlib.decompress(xmlfig)
        self._dom = xml.dom.minidom.parse(xmlfile)
        self._xmlfig = self._dom.firstChild

        self.start_tags = {}

        self.end_tags = {}
        
        self._vars = {}
        self._xmlobjs = {}
        self._objs = {}
        self._current_tag = None
        self._current_attrs = None
        self._current_content = ''

        self.parser = self.create_parser()
        self.parser.parse(xmlfile)
        
        #print self._vars
        
        self.figmgr = None
        self.fig = None
        
        self.draw()


    def draw(self):
        if self._xmlfig is None:
            return
        self._figure()

    def characters(self, content):
        #pat = re.compile('\s')
        #content = pat.sub('',content)
        self._current_content += content
            
    def startElement(self, name, attrs):
        self._current_tag = name
        self._current_attrs = attrs
        self._current_content = ''
        if self.start_tags.has_key(name):            
            return self.start_tags[name](name, attrs)

    def endElement(self, name):
        if self._current_content is not '':
            #print "tag=",self._current_tag
            #print self._current_content
            #print type(self._current_content)
            v = self._current_content
            #print var
            attrs = self._current_attrs
            cmd = ''
            if attrs.has_key('id'):
                id = attrs['id']
                if attrs.has_key('type'):
                    typ = attrs['type']
                    if typ == 'numpy.ndarray':
                        #exec('from numpy import *')
                        cmd = 'v = numpy.'+v
                        #print "id=",id
                        #print "cmd=",cmd
                        #print self._current_tag
                        try:
                            exec(cmd)
                        except:
                            v = None
                        
                    elif typ == 'int':
                        v = int(v)
                    elif typ == 'str':
                        if v.startswith("'") and v.endswith("'"):
                            v = v[1:-1]
                    elif typ =='unicode':
                        v = v[2:-1]
                        
                    elif typ in ["numpy.bool_", "bool"]:
                        if v == 'False':
                            v = False
                        else:
                            v = True
                        
                    #print "cmd = ",cmd
                    
                    #if typ == 'unicode':
                    #    print var
                    
                if not self._vars.has_key(id):
                    self._vars[id] = v
        
        
        if self.end_tags.has_key(name):
            return self.end_tags[name](name)

    
    def _get_node_byname(self,nodename,xmlel):
        #return first
        xmlroot = self._get_object_node(self._xmlfig,xmlel.getAttribute('id'))
        nodes = xmlroot._get_childNodes()
        for node in nodes:
            if node.nodeName == nodename:
                return node
        return None
            
    def _get_node(self,nodepath,xmlroot):

        node = xmlroot
        for nod in nodepath.split('.'):
            
            node = self._get_node_byname(nod, node)
            if node is None:
                return None
            #else:
            #    node = self._get_object_node(self._xmlfig,node.getAttribute('id'))
        return node
    
    def _xml2seq(self,xmlel,seqtype,itemtype):
        typ = xmlel.getAttribute('type')
        if typ != 'tuple':
            return None
        seq = []
        for i in xmlel._get_childNodes():
            v = i.getText()
            v = itemtype(v)
            seq.append(v)
        return seqtype(seq)
            
    def _figure(self):
        kwargs = {
                'num': None,
                'figsize': None,
                'dpi': None,
                'facecolor': None,
                'edgecolor': None,
                'linewidth': 1.0,
                'frameon': True,
                'subplotpars': None
                }
        
        kwargs['dpi']= float(self._get_value('_dpi',self._xmlfig))
        
        left = float(self._get_value('subplotpars.left',self._xmlfig))
        right = float(self._get_value('subplotpars.right',self._xmlfig))
        bottom = float(self._get_value('subplotpars.bottom',self._xmlfig))
        top = float(self._get_value('subplotpars.top',self._xmlfig))
        wspace = float(self._get_value('subplotpars.wspace',self._xmlfig))
        hspace = float(self._get_value('subplotpars.hspace',self._xmlfig))
        
        #print 'figure'
        self.fig = figure(**kwargs)
        self.fig.subplots_adjust(left=left,bottom=bottom,right=right,wspace=wspace,hspace=hspace)
        self._add_axes()
        self.fig.canvas.draw()
    
    def _add_axes(self):
        if self.fig is None:
            return
        
        axlist = self._get_node_byname('axes',self._xmlfig)
        axlist = axlist._get_childNodes()
        #print axlist
        
        for _xmlaxes in axlist:
            
            kwargs = {
                'axisbg': None, # defaults to rc axes.facecolor
                'frameon': True,
                'sharex': None, # use Axes instance's xaxis info
                'sharey': None, # use Axes instance's yaxis info
                'label': '',
#                'xscale': None,
#                'yscale': None,
                }
            
            _xmlaxes = self._get_object_node(self._xmlfig, _xmlaxes.getAttribute('id'))
            Subplot = re.compile('matplotlib.axes.AxesSubplot')
            Axes = re.compile('matplotlib.axes.Axes')
            
            if Subplot.match(_xmlaxes.getAttribute('type')) is not None:
                
                add_func = self.fig.add_subplot
                numRows = self._get_value('numRows',_xmlaxes) 
                numCols = self._get_value('numCols',_xmlaxes)
                plotNum = self._get_value('_num',_xmlaxes) + 1
            
                args = (numRows,numCols,plotNum)
                
            elif Axes.match(_xmlaxes.getAttribute('type')) is not None:
                add_func = self.fig.add_axes
                _points = self._get_value('_position._points',_xmlaxes)
                rect = Bbox(_points)
                args = (rect,)

            else:
                continue
            
            axisbelow = self._get_value('_axisbelow',_xmlaxes)
            frameon = self._get_value('_frameon',_xmlaxes)
            kwargs['axisbelow'] = axisbelow
            kwargs['frameon'] = frameon
            
            xlabel = self._get_value('xaxis.label._text',_xmlaxes)
            kwargs['xlabel'] = xlabel
            
            ylabel = self._get_value('yaxis.label._text',_xmlaxes)
            kwargs['ylabel'] = ylabel
            
            _points = self._get_value('viewLim._points', _xmlaxes)
            #print _points
            #kwargs['xlim'] = _points[:,0]
            #kwargs['ylim'] = _points[:,1]
            
            
            axes = add_func(*args, **kwargs)
            _xmlid = _xmlaxes.getAttribute('id')
            self._objs[_xmlid] = axes
            self._add_lines(_xmlaxes,axes)
            axes.set_xlim(_points[:,0])
            axes.set_ylim(_points[:,1])
            
            _sharex = self._get_node('_sharex',_xmlaxes)
            if _sharex is not None: #twinx
                parentid = _sharex.getAttribute('id')
                parent_axes = self._objs[parentid]
                parent_axes.yaxis.tick_left()
                axes.yaxis.tick_right()
                axes.yaxis.set_label_position('right')
                axes.xaxis.set_visible(False)
            
    
    def _add_lines(self,_xmlaxes,axes):
        from matplotlib.lines import Line2D
        
        linelist = self._get_node_byname('lines',_xmlaxes)
        linelist = linelist._get_childNodes()
        for _xmlline in linelist:
            #print _xmlline
            kwargs = {
#                      'linewidth': None, # all Nones default to rc
                      'linestyle': None,
                      'color': None,
                      'marker': None,
#                      'markersize': None,
#                      'markeredgewidth': None,
#                      'markeredgecolor': None,
#                     'markerfacecolor': None,
#                      'antialiased': None,
#                      'dash_capstyle': 'butt',
#                      'solid_capstyle': 'projecting',
#                      'dash_joinstyle': 'round',
#                      'solid_joinstyle': 'round',
#                      'pickradius': 5,
#                      'drawstyle': None,
#                      'markevery': None,
                      'label': '',
                 }
            
            kwargs['color'] = self._get_value('_color',_xmlline)
            kwargs['marker'] = self._get_value('_marker',_xmlline)
            kwargs['linestyle'] = self._get_value('_linestyle',_xmlline)
            kwargs['label'] = self._get_value('_label',_xmlline)
            
            _xy = self._get_node_byname('_xy', _xmlline)
            #print _xy
            if _xy.getAttribute('type') == 'numpy.ma.core.MaskedArray':
                #print "_xy  masked array"
                data = self._get_value('data', _xy)
                mask = self._get_value('mask', _xy)
                #print "mask = ",mask
                _xy = numpy.ma.core.array(data,mask=mask)
                #print "masked _xy", _xy 
            else:
                #print "_xy array"
                _xy = self._get_value('_xy',_xmlline)
                
            #print 'real', _xy
            _x = _xy[:,0]
            _y = _xy[:,1]
            
            x_isdata = self._get_value('x_isdata',_xmlline)
            y_isdata = self._get_value('y_isdata',_xmlline)
            
            #print "x_isdata: ",x_isdata
            #print "y_isdata: ",y_isdata
            if x_isdata and y_isdata:
                #print kwargs
                axes.plot(_x,_y,**kwargs)
            elif not x_isdata:
                #print "hline",_x,_y
                axes.axhline(_y[0],_x[0],_x[1],**kwargs) 
            elif not y_isdata:
                #print "hline",_x,_y
                axes.axvline(_x[0],_y[0],_y[1],**kwargs)
                
        legend_ = self._get_node_byname('legend_',_xmlaxes)
        
        if legend_ is not None:
            _loc = self._get_value('_loc', legend_)
            axes.legend(loc=_loc)
        axes.autoscale_view()

    def _get_value(self,tag,_xml):
        node = self._get_node(tag,_xml)
        return self._vars[node.getAttribute('id')]
            
    
    def _get_object_node(self,node, id):
        
        if getattr(node,'attributes',None) is None:
            return None

        if self._xmlobjs.has_key(id):
            return self._xmlobjs[id]
        
        if node.getAttribute('id') == id and node.hasChildNodes():
            #print node
            self._xmlobjs[id] = node
            return node
        else:
            for n in node._get_childNodes():
                objnode = self._get_object_node(n,id)
                if objnode is not None:
                    return objnode
    
