#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import codecs

from setuptools import setup

try:
    # Python 3
    from os import dirname
except ImportError:
    # Python 2
    from os.path import dirname

here = os.path.abspath(dirname(__file__))

def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()

required = [
    'humanize',
    'pytz',
    'dateparser',
    'iso8601',
    'python-dateutil',
    'ruamel.yaml',
    'tzlocal'
]

setup(
    name='maya',
    version='0.1.4',
    description='Datetimes for Humans.',
    long_description= '\n' + read('README.rst'),
    author='Kenneth Reitz',
    author_email='me@kennethreitz.com',
    url='https://github.com/kennethreitz/maya',
    py_modules=['maya'],
    install_requires=required,
    license='MIT',
    classifiers=(

    ),
)
