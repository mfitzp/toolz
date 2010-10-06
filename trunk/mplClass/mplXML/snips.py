import struct
import base64
import numpy as N
import scipy as S
import matplotlib.pyplot as P
import xml2fig
import fig2xml
import numpyXML#BHC
from IPython.Shell import IPShellEmbed, IPShellMatplotlibQt
import y_serial_v060 as y_serial
import os

reload(xml2fig)
reload(fig2xml)
reload(numpyXML)



#fig = P.figure()
#ax = fig.add_subplot(111)
#ans = N.loadtxt('A1.csv', delimiter = ',')
#ax.plot(ans[:,0], ans[:,1], 'bo-', ms = 1, linewidth = 1.0, alpha = 0.6, label = "YO JOE")
##ax.vlines(ans[:,0], 0, ans[:,1]*-1, label = "YO JOE 2")
#ax.plot(ans[:,0], ans[:,1]*-1, label = "YO JOE 2")
#ax.text(500, 500, "HELP ME MAKE THIS WORK")
#ax.text(1000, 1000, "HELP ME MAKE THIS WORK PLEASE!")
#ax.set_title("TEST ME")
#ax.set_xlabel("m/z")
#ax.legend()
#P.show()

ipshell = IPShellEmbed()
#xmlFig = fig2xml.Figure2XML(fig)
#xmlFig.print_xml('A1.xml')
# #nf = xml2fig.XMLFigure('mplFig.xml')
#~ nf = xml2fig.XMLFigure('A1.xml')
#~ nf = xml2fig.XMLFigure('A21.xml')
#~ P.show()
#~ print "OK"

#ipshell()



#~ fig = P.figure()
#~ ax = fig.add_subplot(111)
#~ a = S.rand(20)
#~ b = S.rand(20)
#~ c = S.rand(20)
#~ sc = ax.scatter(a,b,c*200, label = 'asdf')
#~ l, = ax.plot(a,b, '-og')
#~ ax.text(0.5, 0.5, "HELP ME MAKE THIS WORK")
#~ ax.text(0.1, 0.1, "HELP ME MAKE THIS WORK PLEASE!")
#~ xmlFig = fig2xml.Figure2XML(fig)
#~ xmlStr = xmlFig.saveXML('scatter.xml.gz')
#~ xmlFig.print_xml('scatter.xml')


#~ plotDB = y_serial.Main(os.path.join(os.getcwd(),'plot.sqlite'))
#~ dataDict = {}
#~ dataDict['mplAx'] = xmlStr
#~ plotDB.insert(dataDict, "#plan agent007 #london", 'dataTable' )

#~ eg2 = plotDB.selectdic( "*", 'dataTable' )

#~ xmlDict = eg2[eg2.keys()[0]][2]
#~ xmlStr2 = xmlDict[xmlDict.keys()[0]]

#~ print xmlStr == xmlStr2
#print type(xmlStr2)

nf = xml2fig.XMLFigure('scatter.xml.gz')
P.show()
#ipshell()



'''	
a = N.arange(30)
b = N.cos(a)

P.plot(a,b, alpha = 0.5)

a2 = encodeArray(a)
b2 = encodeArray(b)

a3 = decodeData(a2)
b3 = decodeData(b2)

P.plot(a3,b3, '--r')
P.show()
'''


'''
a = S.rand(20,2)
a2 = numpyXML.encodeArray(a)
a3 = numpyXML.decodeArray(a2)
'''
