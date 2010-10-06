#log# Automatic Logger file. *** THIS MUST BE THE FIRST LINE ***
#log# DO NOT CHANGE THIS LINE OR THE TWO BELOW
#log# opts = Struct({'__allownew': True, 'logfile': 'ipython_log.py', 'pylab': 1})
#log# args = []
#log# It is safe to make manual edits below here.
#log#-----------------------------------------------------------------------
import fig2xml
import numpy as N
_ip.magic("logstart ")

a = N.arange(20)
b = N.arange(20)
ax = gca()
v = ax.vlines(a,0,b)
ans = fig2xml.Figure2XML(v, 'vlines')
ans.prettyPrint('vlines.xml')
_ip.magic("history ")
exit()
