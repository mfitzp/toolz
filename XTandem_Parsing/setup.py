# Used successfully in Python2.5 with matplotlib 0.91.2 and PyQt4 (and Qt 4.3.3)
# run as python25 setup.py py2exe
#C:\Python25\python setup.py py2exe
from distutils.core import setup
import py2exe

# We need to import the glob module to search for all files.
import glob

# We need to exclude matplotlib backends not being used by this executable.  You may find
# that you need different excludes to create a working executable with your chosen backend.
# We also need to include include various numerix libraries that the other functions call.

opts = {
    'py2exe': { "includes" : ["sip", "PyQt4._qt", "matplotlib.backends.backend_qt4agg", "matplotlib.backends.backend_qt4",
                               "matplotlib.figure", "numpy", "matplotlib.numerix.fft", "sqlite3", "encodings.*",
                               "matplotlib.numerix.linear_algebra", "matplotlib.numerix.random_array",
                               "matplotlib.backends.backend_tkagg","xml.etree.cElementTree","xml.etree.ElementTree"],
                'excludes': ['_gtkagg', '_tkagg', '_agg2', '_cairo', '_cocoaagg',
                             '_fltkagg', '_gtk', '_gtkcairo', '_wxagg'],
                'dll_excludes': ['libgdk-win32-2.0-0.dll',
                                 'libgobject-2.0-0.dll',
                                 'mswsock.dll', 
                                 'powrprof.dll'],
                'skip_archive':True
              }
       }

# Save matplotlib-data to mpl-data ( It is located in the matplotlib\mpl-data
# folder and the compiled programs will look for it in \mpl-data
# note: using matplotlib.get_mpldata_info
data_files = [(r'mpl-data', glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\*.*')),
                    # Because matplotlibrc does not have an extension, glob does not find it (at least I think that's why)
                    # So add it manually here:
                  (r'mpl-data', [r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\matplotlibrc']),
                  (r'mpl-data\images',glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\images\*.*')),
                  (r'mpl-data\fonts',glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\fonts\*.*')),
                  (r'FragmentPlot\mspy',glob.glob(r'C:\Documents and Settings\d3p483\My Documents\Python\XTandem_Parsing\FragmentPlot\mspy\config.pyc')),
                  (r'FragmentPlot\configs',glob.glob(r'C:\Documents and Settings\d3p483\My Documents\Python\XTandem_Parsing\FragmentPlot\configs\*.*')),
                  (r'FragmentPlot\mspy\blocks',glob.glob(r'C:\Documents and Settings\d3p483\My Documents\Python\XTandem_Parsing\FragmentPlot\mspy\blocks\*.*')),
                  (r'FragmentPlot\mspy\plot',glob.glob(r'C:\Documents and Settings\d3p483\My Documents\Python\XTandem_Parsing\FragmentPlot\mspy\plot\*.*'))]




# for console program use 'console = [{"script" : "scriptname.py"}]
setup(windows=[{
                "script" : "XT_Viewer.py",
                "icon_resources":[(1, "xtIcon.ico")]
                }],
                options=opts,
                data_files=data_files)

