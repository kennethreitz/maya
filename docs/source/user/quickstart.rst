.. _quickstart:

Quickstart
==========

.. module::maya

Ready for a simple datetime tool? This doc provides some tools to use in your
busy workflow.

Parse a Date
------------
Parsing a date from a string with Maya is 🍰!

First, you'll need to import maya::

   >>> import maya

There are currently two ways to make sense of datetime:

- ``maya.parse``
- ``maya.when``

A simple answer is that you should use parse on machine output, and when on human input.

Use as follows::

   >>> recent_win = maya.parse('2016-11-02T20:00PM')
   >>> old_win = maya.when('October 14, 1908')
   >>> grandpas_date = maya.when('108 years ago')
