from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

sourcefiles = ["decoder.py"]

extensions = cythonize(Extension(
    name="libdecoder",
    sources=sourcefiles
))

kwargs = {
    "name": "libdecoder",
    "packages": find_packages(),
    "ext_modules": extensions
}

setup(**kwargs)
