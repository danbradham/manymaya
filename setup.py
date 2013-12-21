import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='manymaya',
    version=0.2,
    description="A fast and light-weight wrapper for Autodesk Maya's standalone extension.",
    long_description=open('README.md').read(),
    author='Dan Bradham',
    author_email='danielbradham@gmail.com',
    url='http://www.danbradham.com',
    packages=['manymaya'],
    package_data={'': ['LICENSE']},
    package_dir={'manymaya': 'manymaya'},
    include_package_data=True,
    license=open('LICENSE').read(),
    zip_safe=False)