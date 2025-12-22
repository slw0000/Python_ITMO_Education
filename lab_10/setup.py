from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("iter_5_noGIL.pyx", annotate=True)
)