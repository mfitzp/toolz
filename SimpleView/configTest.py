import ConfigParser
import string

config = ConfigParser.ConfigParser()

'''
[USERDIRS]
FPDIR:'\home\clowers\FPs'
DATADIR:'home\clowers\SVTest'

[waveletPeaks]
MINROWNOISE:1
MINROWTOL:3
MINCLUST:4
DISTTHRESH:-1
SPLITFACTOR:10
STATICCUTOFF:100
SNRNOISEEST:3.0
DEFAULTSCALES:True
AUTOSAVEPEAKS:False
SHOWSNREST:False
SCALESTART:2
SCALEEND:64
SCALEFACTOR:4

[eicPrefs]
MZLO:1295.000
MZHI:1297.000

[plotOptions]
PLOTPEAKLIST:True
PLOTLEGEND:True
INVERTCOMP:True

[fileHandlers]
LOADMZXML:True
EXCLUDELIFT:False

[fpHandler]
AUTOLOADFP:False
'''


config.read("svconfig.ini")

# print summary
#print
#print string.upper(config.get("book", "title"))
#print "by", config.get("book", "author"),
#print  "(" + config.get("book", "email") + ")"
#print
#print config.get("ematter", "pages"), "pages"
#print
print config.sections()
# dump entire config file
for section in config.sections():
    print '\t',config.options(section)
    for option in config.options(section):
        val = None
        try:
            val = config.getboolean(section, option)
        except:
            pass

        try:
            val = config.getfloat(section, option)
        except:
            pass

        try:
            val = config.getint(section, option)
        except:
            pass

        if val != None:
            print " ", option, "=", val, type(val)