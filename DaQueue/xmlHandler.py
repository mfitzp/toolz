"""
Thunder Chen<nkchenz@gmail.com> 2007.9.1
"""
try:
    import xml.etree.ElementTree as ET
except:
    import cElementTree as ET # for 2.4

import re


class object_dict(dict):
    """object view of dict, you can
>>> a = object_dict()
>>> a.fish = 'fish'
>>> a['fish']
'fish'
>>> a['water'] = 'water'
>>> a.water
'water'
>>> a.test = {'value': 1}
>>> a.test2 = object_dict({'name': 'test2', 'value': 2})
>>> a.test, a.test2.name, a.test2.value
(1, 'test2', 2)
"""
    def __init__(self, initd=None):
        if initd is None:
            initd = {}
        dict.__init__(self, initd)

    def __getattr__(self, item):
        d = self.__getitem__(item)
        # if value is the only key in object, you can omit it
        if isinstance(d, dict) and 'value' in d and len(d) == 1:
            return d['value']
        else:
            return d

    def __setattr__(self, item, value):
        self.__setitem__(item, value)


class XML2Dict(object):

    def __init__(self):
        pass

    def _parse_node(self, node):
        node_tree = object_dict()
        # Save attrs and text, hope there will not be a child with same name
        if node.text:
            node_tree.value = node.text
        for (k,v) in node.attrib.items():
            k,v = self._namespace_split(k, object_dict({'value':v}))
            node_tree[k] = v
        #Save childrens
        for child in node.getchildren():
            tag, tree = self._namespace_split(child.tag, self._parse_node(child))
            if tag not in node_tree: # the first time, so store it in dict
                node_tree[tag] = tree
                continue
            old = node_tree[tag]
            if not isinstance(old, list):
                node_tree.pop(tag)
                node_tree[tag] = [old] # multi times, so change old dict to a list
            node_tree[tag].append(tree) # add the new one

        return node_tree


    def _namespace_split(self, tag, value):
        """
Split the tag '{http://cs.sfsu.edu/csc867/myscheduler}patients'
ns = http://cs.sfsu.edu/csc867/myscheduler
name = patients
"""
        result = re.compile("\{(.*)\}(.*)").search(tag)
        if result:
            value.namespace, tag = result.groups()
        return (tag, value)

    def parse(self, file):
        """parse a xml file to a dict"""
        f = open(file, 'r')
        return self.fromstring(f.read())

    def fromstring(self, s):
        """parse a string"""
        t = ET.fromstring(s)
        root_tag, root_tree = self._namespace_split(t.tag, self._parse_node(t))
        return object_dict({root_tag: root_tree})



''' Dictionary to XML - Library to convert a python dictionary to XML output
    Copyleft (C) 2007 Pianfetti Maurizio <boymix81@gmail.com>
    Package site : http://boymix81.altervista.org/files/dict2xml.tar.gz

    Revision 1.0  2007/12/15 11:57:20  Maurizio
    - First stable version

__author__ = "Pianfetti Maurizio <boymix81@gmail.com>"
__contributors__ = []
__date__    = "$Date: 2007/12/15 11:57:20  $"
__credits__ = """..."""
__version__ = "$Revision: 1.0.0 $"

'''

class Dict2XML:
    #XML output
    xml = ""

    #Tab level
    level = 0

    def __init__(self):
        self.xml = ""
        self.level = 0
    #end def

    def __del__(self):
        pass
    #end def

    def setXml(self,Xml):
        self.xml = Xml
    #end if

    def setLevel(self,Level):
        self.level = Level
    #end if

    def typeCheck(self, item):
        if (str(type(item)) == "<class 'object_dict.object_dict'>"
            or str(type(item)) == "<type 'dict'>"
            or str(type(item)) == "<class 'object_dict'>"
            or str(type(item)) == "<class '__main__.object_dict'>"):
            return True
        else:
            return False

    def dict2xml(self,map):
        if self.typeCheck(map):
            for key, value in map.items():
                if self.typeCheck(value):
                    if(len(value) > 0):
                        self.xml += "\t"*self.level
                        self.xml += "<%s>\n" % (key)
                        self.level += 1
                        self.dict2xml(value)
                        self.level -= 1
                        self.xml += "\t"*self.level
                        self.xml += "</%s>\n" % (key)
                    else:
                        self.xml += "\t"*(self.level)
                        self.xml += "<%s></%s>\n" % (key,key)
                    #end if
                else:
                    self.xml += "\t"*(self.level)
                    self.xml += "<%s>%s</%s>\n" % (key,value, key)
                #end if
        else:
            print type(map)
#            self.xml += "\t"*self.level
#            self.xml += "<%s>%s</%s>\n" % (key,value, key)
        #end if
        return self.xml
    #end def

#end class

def createXML(dict,xml):
    xmlout = Dict2XML()
    xmlout.setXml(xml)
    return xmlout.dict2xml(dict)
#end def

#if __name__ == "__main__":
#
#    #Define the dict
#    d={}
#    d['root'] = {}
#    d['root']['v1'] = "";
#    d['root']['v2'] = "hi";
#    d['root']['v3'] = {};
#    d['root']['v3']['v31']="hi";
#
#    #xml='<?xml version="1.0"?>\n'
#    xml = ""
#    print createXML(d,xml)

#end if


if __name__ == '__main__':
    from pprint import pprint
#    from dict2xml import verbose_dict2xml
    # Test file parsing
    xml = XML2Dict()
    xmlDict = xml.parse('config.xml')
    pprint(xmlDict)
#    print type(xmlDict)
#    print '\n\n'
#    xmlHeader = ''
#    xmlStr = createXML(xmlDict, xmlHeader)
#    print xmlStr

#    xmlOut = verbose_dict2xml(xmlDict)
#    print(xmlOut.toprettyxml())
#    print("done")


