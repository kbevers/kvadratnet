"""
Setup script for the kvadratnet module.
"""

import os
import subprocess
from setuptools import setup

import kvadratnet

def readme():
    """
    Return a properly formatted readme text, if possible, that can be used
    as the long description for setuptools.setup.
    """
    # This will fail if pandoc is not in system path.
    subprocess.call(['pandoc', 'readme.md', '--from', 'markdown', '--to', 'rst', '-s', '-o', 'readme.rst'])
    with open('readme.rst') as f:
        readme = f.read()
    os.remove('readme.rst')
    return readme

setup(
    name='kvadratnet',
    version=kvadratnet.__version__,
    description='Python tools for working with the Danish Kvadratnet tiling scheme.',
    long_description=readme(),
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: ISC License (ISCL)',
      'Topic :: Scientific/Engineering :: GIS',
      'Topic :: Utilities'
    ],
    entry_points = {
      'console_scripts': ['knet=knet:main']
    },
    keywords='kvadratnet gis tiling',
    url='https://github.com/kbevers/kvadratnet',
    author='Kristian Evers',
    author_email='kristianevers@gmail.com',
    license='ISC',
    py_modules=['kvadratnet', 'knet'],
    test_suite='nose.collector',
    tests_require=['nose']
)
