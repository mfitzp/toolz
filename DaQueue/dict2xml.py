"""
A super-simple minidom recipe for translating a dict to xml. It's simple
to add any feature (recursive conversion, pickle etc) to this if you need.

>>> dict2xml({"ok": 123, 12323: "haha"}).toprettyxml()
<?xml version="1.0" ?>
<dictionary>
    <12323>
        haha
    </12323>
    <ok>
        123
    </ok>
</dictionary>

>>> verbose_dict2xml({"ok": 123, 12323: "haha"}).toprettyxml()
<?xml version="1.0" ?>
<dictionary>
    <item>
        <name>
            12323
        </name>
        <value>
            haha
        </value>
    </item>
    <item>
        <name>
            ok
        </name>
        <value>
            123
        </value>
    </item>
</dictionary>

"""
from xmlHandler import object_dict
from xml.dom.minidom import Document


def dict2xml(dictionary, name="dictionary"):
    "The keys are element names and the values are text"
    xml = Document()
    items = xml.createElement(name)
    xml.appendChild(items)
    for key, val in dictionary.items():
        node = xml.createElement(str(key))
        node.appendChild(xml.createTextNode(str(val)))
        items.appendChild(node)
    return xml

def typeCheck(item):
    if (str(type(item)) == "<class 'object_dict.object_dict'>"
        or str(type(item)) == "<type 'dict'>"
        or str(type(item)) == "<class 'object_dict'>"
        or str(type(item)) == "<class '__main__.object_dict'>"):
        return True
    else:
        return False

def recurseXML(dictionary, items, xml):
    for key, val in dictionary.items():
#        print "\tVal Type2", type(val)
        if typeCheck(val):
            recurseXML(val, items, xml)
        else:
            item = xml.createElement("item")
            items.appendChild(item)
            name_node = xml.createElement("name")
            name_node.appendChild(xml.createTextNode(str(key)))
            value_node = xml.createElement("value")
            value_node.appendChild(xml.createTextNode(str(val)))
            item.appendChild(name_node)
            item.appendChild(value_node)

def verbose_dict2xml(dictionary, name="dictionary"):
    "2 nodes per item - one for the name and one for the value"
    xml = Document()
    items = xml.createElement(name)
    xml.appendChild(items)
    for key, val in dictionary.items():
        if typeCheck(val):
            recurseXML(val, items, xml)
        else:
            item = xml.createElement("item")
            items.appendChild(item)
            name_node = xml.createElement("name")
            name_node.appendChild(xml.createTextNode(str(key)))
            value_node = xml.createElement("value")
            value_node.appendChild(xml.createTextNode(str(val)))
            item.appendChild(name_node)
            item.appendChild(value_node)
    return xml


if __name__ == "__main__":
    print("haha")
    xml = dict2xml({"ok": 123, 12323: "haha"})
    print(xml.toprettyxml())
    xml = verbose_dict2xml({"ok": 123, 12323: {"haha":"Go Joe", "Try Again":{"hahaha":"Super Efficiency", 'gaga':"Tired"}}})
    print(xml.toprettyxml())
    print("done")