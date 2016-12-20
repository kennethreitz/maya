#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import codecs

from setuptools import setup


here = os.path.abspath(os.dirname(__file__))

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
    'ruamel.yaml'
]

setup(
    name='maya',
    version='0.1.1',
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
