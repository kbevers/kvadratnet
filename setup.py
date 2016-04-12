"""
Setup script for the kvadratnet module.
"""

from setuptools import setup

def readme():
    """
    Return a properly formatted readme text, if possible, that can be used
    as the long description for setuptools.setup.
    """
    try:
        import pypandoc
        return pypandoc.convert('readme..md', 'rst', format='md')
    except (IOError, ImportError):
        with open('readme.md') as f:
            return f.read()

setup(name='kvadratnet',
      version='0.1',
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
      download_url='https://github.com/kbevers/kvadratnet/tarball/0.1',
      license='ISC',
      py_modules=['kvadratnet'],
      test_suite='nose.collector',
      tests_require=['nose'])
