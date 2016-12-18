#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()

required = [
    'humanize',
    'pytz',
    'dateparser',
    'iso8601',
    'python-dateutil'
]

setup(
    name='maya',
    version='0.1.1',
    description='Datetimes for Humans.',
    long_description=open('README.rst').read(),
    author='Kenneth Reitz',
    author_email='me@kennethreitz.com',
    url='https://github.com/kennethreitz/maya',
    py_modules=['maya'],
    install_requires=required,
    license='MIT',
    classifiers=(

    ),
)
