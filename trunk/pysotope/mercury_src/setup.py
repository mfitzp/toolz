# setup.py
import distutils
from distutils.core import setup, Extension

setup(name = "Simple example from the SWIG website",
      version = "2.5",
      ext_modules = [Extension("libmercury", ["libmercury.i","libmercury.cpp"], swig_opts=['-c++'])])

	  