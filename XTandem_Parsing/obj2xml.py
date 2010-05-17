import re
from xml.sax.saxutils import escape
import xml.dom.minidom

import zlib


def xmlel(objname):
    if objname.startswith('<'):
        objname = objname[1:-1]
    #objname = objname.replace(' ','_')
    #objname = objname.replace('\'','')
    
    invalid_char = re.compile('\W')
    if invalid_char.search(objname):
        return '_invalid_element_name'
    
    number_pattern = re.compile('[0-9]')
    if number_pattern.match(objname) is not None:
        objname = 'x'+objname
    return objname

def get_xmltype(obj):
    
    instance = re.compile("instance")
    _type = str(type(obj))
    
    if instance.search(_type) is not None:
        _type = str(obj.__class__)
    #print "_type: ",_type
    
    pat = re.compile("'[^']*'")
    xmltype = pat.search(_type)
    if xmltype is None:
            xmltype = _type
    else:    
            xmltype = xmltype.group()
            xmltype = xmltype[1:-1]

    return escape(xmltype)
    
def get_xmlid(obj):
    return str(id(obj))
    

class Object2Xml:
    
    def __init__(self,obj,objname,ignoreclass=[],ignoreattr=[]):
        
        self._adapt={
                    dict: self._get_xml_dict,
                    list: self._get_xml_list,
                    tuple: self._get_xml_tuple,
                    str: self._get_xml_str,
                    
                }
        
        self._doc = xml.dom.minidom.Document()
    
        self._ignoreclass = ignoreclass
        self._ignoreattr = ignoreattr
        #self._refs = []
        self._vars = []
        self.xmlobj = None
        self.ignoretype = re.compile('')
        self.invalid_char = re.compile('\W')
        
        #print self._xmlstr

        
    def print_xml(self,filename,**kwargs):
        f = open(filename,'w')
        if self.xmlobj is not None:
            f.write(self.xmlobj.toxml())
        f.close()
        
    def test_ignore(self,obj,objname):
        _xmltype = get_xmltype(obj)
        nametest = objname is ''
        classtest = obj.__class__ in self._ignoreclass    
        typetest = self.ignoretype.search(_xmltype) is not None
        return nametest or classtest or typetest

        
    def getXML(self, obj, objname):
        """getXML(obj, objname=None)
        returns an object as XML where Python object names are the tags.
        >>> u={'UserID':10,'Name':'Mark','Group':['Admin','Webmaster']}
        >>> getXML(u,'User')
        '<User><UserID>10</UserID><Name>Mark</Name><Group>Admin</Group><Group>Webmaster</Group></User>'
        """
        
        _xmltype = get_xmltype(obj)
        _xmlid = get_xmlid(obj)

        objname = xmlel(str(objname))
        
        if self.test_ignore(obj, objname):
            return None
            
#        if objname is '': return None
#        
#        if self.ignoretype.search(_xmltype) is not None: return None
#        
#        elif obj.__class__ in self._ignoreclass:
#            #print obj.__class__
#            return None
        
        if id(obj) in self._vars:
            return self._create_element(objname, _xmlid, None, None)
        else:
            self._vars.append(id(obj))
        
        if getattr(obj,'__class__',None) is None:
            return self._create_element(objname,_xmlid,_xmltype,'')
        
            
        if self._adapt.has_key(obj.__class__):
            return self._adapt[obj.__class__](obj, objname)
        
        elif getattr(obj,'__dict__',None) is None: #scalars arrays etc...
            
            if obj is None:
                o = None
                #print _xmltype,objname
            elif getattr(obj,'__repr__',None) is None:
                o = str(obj)
            else:
                o = obj.__repr__()
                pat = re.compile('\s')
                o = pat.sub('',o)
            return self._create_element(objname, _xmlid, _xmltype, o)
        
        else:
            return self._get_xml_object(obj,objname)
        
    def _create_element(self,name,id,typ=None,content=None):
        element = self._doc.createElement(name)
        if content is not None: 
            content = self._doc.createTextNode(content)
            element.appendChild(content)
        element.setAttribute('id',id)
        if typ is not None:
            element.setAttribute('type',typ)
        return element
        
    def _get_xml_str(self,s,objname=None):
        if s == '':
            s = "''"
        return self._create_element(objname,get_xmlid(s),get_xmltype(s),s)

    def _get_xml_dict(self,indict, objname=None):
        element = self._create_element(objname,get_xmlid(indict),'dict',None)   
        for k, v in indict.items():
            #print "attribute: ",k
            if self.invalid_char.search(str(k)):
                continue
            else:
                child = self.getXML(v, k)
                if child is not None:
                    element.appendChild(child)
        return element
    
    def _get_xml_tuple(self,intuple,objname=None):
        return self._get_xml_sequence(intuple, objname,'tuple')
    
    def _get_xml_list(self,inlist,objname=None):
        return self._get_xml_sequence(inlist, objname,'list')

    def _get_xml_sequence(self,seq, objname,typ):
        element = self._create_element(objname,get_xmlid(seq),typ,None)
        for i in seq:
            child = self.getXML(i, objname)
            if child is not None:
                element.appendChild(child)
        return element
        

    def _get_xml_object(self,obj, objname):
        
        element = self._create_element(objname,get_xmlid(obj),get_xmltype(obj),None)
        #if id(obj) not in self._refs:
        #    self._refs.append(id(obj))
        for k in obj.__dict__:
            #print k
            if type(k) != type(''):
                continue
            if k.startswith('__') and k.endswith('__'):
                continue
            if self.invalid_char.search(k) is not None:
                continue
                
            if objname+ '.' + k in self._ignoreattr:
                #print objname+ '.' + k
                continue
                
            try:
                v = getattr(obj,k)
                vk = getattr(v,k,None)
                if vk is not None and id(v) != id(vk) and v.__class__ is vk.__class__:  #attempt to  avoid recursion limit error.
                    #print 'recursion of',type(obj),'::',type(v),'::',type(vk),':::',k
                    v = escape(v.__repr__())
            except Exception, e:
                #print type(obj)
                #print k
                #print str(e)
                continue
            child = self.getXML(v, k)
            if child is not None:
                element.appendChild(child)
        return element