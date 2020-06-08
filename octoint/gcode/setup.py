# python3 ./octoint/gcode/setup.py build_ext --inplace

from distutils.core import setup
from Cython.Build import cythonize

setup(name='gcode_analyser', ext_modules=cythonize('./octoint/gcode/parse_gcode_cy.pyx', build_dir="build"))
