import sys
import numpy
from distutils.core import setup
from distutils.extension import Extension

# Build on WIN using MinGW:
# python setup.py build --compiler=mingw32
# Copy calculations.pyd to plot directory

# Build on Mac:
# python setup.py build
# Copy calculations.so to plot directory


# make include paths
numpyInclude = numpy.get_include() + '/numpy'
pythonInclude = sys.prefix + '/include'

# make setup
setup(name = 'calculations',
    version = '1.1',
    author = "Daniel Kavan",
    maintainer = 'Martin Strohalm',
    maintainer_email = 'mmass@biographics.cz',
    description = "Fast points calculations for mspy plot.",
    ext_modules=[
        Extension('calculations', ['calculations.c'],
            include_dirs=[numpyInclude, pythonInclude]
        )
    ],
)
