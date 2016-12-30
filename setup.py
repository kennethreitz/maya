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

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


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
    version='0.1.5',
    description='Datetimes for Humans.',
    long_description=long_description,
    author='Kenneth Reitz',
    author_email='me@kennethreitz.com',
    url='https://github.com/kennethreitz/maya',
    py_modules=['maya'],
    install_requires=required,
    license='MIT',
    classifiers=(

    ),
)
