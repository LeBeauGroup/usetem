#!/usr/bin/env python

from distutils.core import setup, Extension
from distutils.sysconfig import get_python_inc
import glob
import os.path
import sys

# Read version
with open("pyTiascript/version.py") as fp:
    exec(fp.read())


# Only build _temscript c++ adapter on windows platforms
if sys.platform == 'win32':
    py_includes = [os.path.join(get_python_inc(), '../Lib/site-packages/numpy/core/include/')]
    ext_modules = [Extension('_tiascript', glob.glob(os.path.join('_tiascript_module', '*.cpp')), include_dirs=py_includes)]
else:
    ext_modules = []

# Based on setup script from tore.niermann@tu-berlin.de

setup(name='tiascript',
      version=__version__,
      description='TIA Scripting adapter for FEI microscopes',
      author='James LeBeau',
      author_email='lebeau@mit.edu',
      packages=['pyTiascript'],
      license="BSD 3-Clause License",
      ext_modules=ext_modules,
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: Developers',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Software Development :: Libraries'
                   'License :: OSI Approved :: BSD License'],
      install_requires=['numpy', 'enum34;python_version<"3.4"'],
      entry_points={'console_scripts': ['tiascript-server = tiascript.server:run_server']},
      project_urls={"Source Code": ""}
      )
