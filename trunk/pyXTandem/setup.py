# Used successfully in Python2.5 with matplotlib 0.91.2 and PyQt4 (and Qt 4.3.3)
# run as python25 setup.py py2exe
#as of yet python2.6 does not work, problems with the compiling of the libmercury interface with SWIG
#lzo1.dll needed for pytables
'''
>>> import scipy as S
>>> import numpy as N
>>> import tables as T
>>> import matplotlib as M
>>> M.__version__
'0.98.5.3'
>>> S.__version__
'0.7.1'
>>> N.__version__
'1.3.0'
>>> T.__version__
'2.0.4'
>>>

scipy factorial error can be rectified by changing the import to
from scipy.misc.common import factorial
'''

from distutils.core import setup
import py2exe

# We need to import the glob module to search for all files.
import glob

# We need to exclude matplotlib backends not being used by this executable.  You may find
# that you need different excludes to create a working executable with your chosen backend.
# We also need to include include various numerix libraries that the other functions call.

opts = {
    'py2exe': { "includes" : ["sip", "PyQt4._qt","xml.etree.cElementTree","xml.etree.ElementTree"],
                'dll_excludes': ['libgdk-win32-2.0-0.dll',
                                 'libgobject-2.0-0.dll']
              }
       }

# Save matplotlib-data to mpl-data ( It is located in the matplotlib\mpl-data
# folder and the compiled programs will look for it in \mpl-data
# note: using matplotlib.get_mpldata_info
data_files = [(r'', glob.glob(r'default.ini')),(r'', glob.glob(r'taxonomy.xml')) ]
#                    # Because matplotlibrc does not have an extension, glob does not find it (at least I think that's why)
#                    # So add it manually here:
#                  (r'mpl-data', [r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\matplotlibrc']),
#                  (r'mpl-data\images',glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\images\*.*')),
#                  (r'mpl-data\fonts',glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\fonts\*.*'))]



# for console program use 'console = [{"script" : "scriptname.py"}]
setup(windows=[{"script" : "main.py",
                "icon_resources":[(1, "PepeLePew.ico")]
                }],
                options=opts,
                data_files=data_files)

