# -*- coding: utf-8 -*-
"""
maya.compat
~~~~~~~~~~~~~~~
This module handles import compatibility issues between Python 2 and
Python 3.
"""

import sys

# -------
# Pythons
# -------
# Syntax sugar.
_ver = sys.version_info
# : Python 2.x?
is_py2 = (_ver[0] == 2)
# : Python 3.x?
is_py3 = (_ver[0] == 3)
# ---------
# Specifics
# ---------
if is_py2:
    cmp = cmp
elif is_py3:

    def cmp(a, b):
        """
        Compare two objects.
        Returns a negative number if C{a < b}, zero if they are equal, and a
        positive number if C{a > b}.
        """
        if a < b:
            return -1

        elif a == b:
            return 0

        else:
            return 1


def comparable(klass):
    """
    Class decorator that ensures support for the special C{__cmp__} method.
    On Python 2 this does nothing.
    On Python 3, C{__eq__}, C{__lt__}, etc. methods are added to the class,
    relying on C{__cmp__} to implement their comparisons.
    """
    # On Python 2, __cmp__ will just work, so no need to add extra methods:
    if not is_py3:
        return klass

    def __eq__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c

        return c == 0

    def __ne__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c

        return c != 0

    def __lt__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c

        return c < 0

    def __le__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c

        return c <= 0

    def __gt__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c

        return c > 0

    def __ge__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c

        return c >= 0

    klass.__lt__ = __lt__
    klass.__gt__ = __gt__
    klass.__le__ = __le__
    klass.__ge__ = __ge__
    klass.__eq__ = __eq__
    klass.__ne__ = __ne__
    return klass
