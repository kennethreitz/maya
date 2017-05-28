.. maya documentation master file, created by
   sphinx-quickstart on Sun May 28 15:46:10 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Maya: Datetime for Humans
================================
Release v\ |version|. (:ref:`Installation <install>`)

.. image:: https://img.shields.io/pypi/v/maya.svg
    :target: https://pypi.python.org/pypi/maya

.. image:: https://travis-ci.org/kennethreitz/maya.svg?branch=master
    :target: https://travis-ci.org/kennethreitz/maya

.. image:: https://img.shields.io/badge/SayThanks-!-1EAEDB.svg
    :target: https://saythanks.io/to/kennethreitz

☤ Behold, datetimes for humans!
-------------------------------
.. code-block:: pycon

    >>> now = maya.now()
    <MayaDT epoch=1481850660.9>

    >>> tomorrow = maya.when('tomorrow')
    <MayaDT epoch=1481919067.23>

    >>> tomorrow.slang_date()
    'tomorrow'

    >>> tomorrow.slang_time()
    '23 hours from now'

    # Also: MayaDT.from_iso8601(...)
    >>> tomorrow.iso8601()
    '2017-02-10T22:17:01.445418Z'

    # Also: MayaDT.from_rfc2822(...)
    >>> tomorrow.rfc2822()
    'Fri, 10 Feb 2017 22:17:01 GMT'

    # Also: MayaDT.from_rfc3339(...)
    >>> tomorrow.rfc3339()
    '2017-02-10T22:17:01.44Z'

    >>> tomorrow.datetime()
    datetime.datetime(2016, 12, 16, 15, 11, 30, 263350, tzinfo=<UTC>)

    # Automatically parse datetime strings and generate naive datetimes.
    >>> scraped = '2016-12-16 18:23:45.423992+00:00'
    >>> maya.parse(scraped).datetime(to_timezone='US/Eastern', naive=True)
    datetime.datetime(2016, 12, 16, 13, 23, 45, 423992)

    >>> rand_day = maya.when('2011-02-07', timezone='US/Eastern')
    <MayaDT epoch=1297036800.0>

    >>> rand_day.day
    7

    >>> rand_day.add(days=10).day
    17

    # Always.
    >>> rand_day.timezone
    UTC

    # Range of hours in a day:
    >>> maya.interval(start=maya.now(), end=maya.now().add(days=1), interval=60*60)
    <generator object intervals at 0x105ba5820>


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   user/install


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
