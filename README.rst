Maya: Datetime for Humans™
==========================

.. image:: https://img.shields.io/pypi/v/maya.svg
    :target: https://pypi.python.org/pypi/maya

.. image:: https://travis-ci.org/kennethreitz/maya.svg?branch=master
    :target: https://travis-ci.org/kennethreitz/maya

.. image:: https://img.shields.io/badge/SayThanks.io-☼-1EAEDB.svg
    :target: https://saythanks.io/to/kennethreitz


Datetimes are very frustrating to work with in Python, especially when dealing
with different locales on different systems. This library exists to make the
simple things **much** easier, while admitting that time is an illusion
(timezones doubly so).

Datetimes should be interacted with via an API written for humans.

Maya is mostly built around the headaches and use-cases around parsing datetime data from websites.


☤ Basic Usage of Maya
---------------------

Behold, datetimes for humans!

.. code-block:: pycon

    >>> now = maya.now()
    <MayaDT epoch=1481850660.9>

    >>> tomorrow = maya.when('tomorrow')
    <MayaDT epoch=1481919067.23>

    >>> tomorrow.slang_date()
    'tomorrow'

    >>> tomorrow.slang_time()
    '23 hours from now'

    >>> tomorrow.iso8601()
    '2016-12-16T15:11:30.263350Z'

    >>> tomorrow.rfc2822()
    'Fri, 16 Dec 2016 20:11:30 -0000'

    >>> tomorrow.datetime()
    datetime.datetime(2016, 12, 16, 15, 11, 30, 263350, tzinfo=<UTC>)

    # Automatically parse datetime strings and generate naive datetimes.
    >>> scraped = '2016-12-16 18:23:45.423992+00:00'
    >>> maya.parse(scraped).datetime(to_timezone='US/Eastern', naive=True)
    datetime.datetime(2016, 12, 16, 13, 23, 45, 423992)

    >>> rand_day = maya.when('2011-02-07', timezone='US/Eastern')
    <MayaDT epoch=1297036800.0>

    # Note how this is the 6th, not the 7th.
    >>> rand_day.day
    6

    # Always.
    >>> rand_day.timezone
    UTC

☤ Why is this useful?
---------------------

- All timezone algebra will behave identically on all machines, regardless of system locale.
- Complete symmetric import and export of both ISO 8601 and RFC 2822 datetime stamps.
- Fantastic parsing of both dates written for/by humans and machines (``maya.when()`` vs ``maya.parse()``).
- Support for human slang, both import and export (e.g. `an hour ago`).
- Datetimes can very easily be generated, with or without tzinfo attached.
- This library is based around epoch time, but dates before Jan 1 1970 are indeed supported, via negative integers.
- Maya never panics, and always carries a towel.


☤ What about Delorean, Arrow, & Pendulum?
-----------------------------------------

Arrow, for example, is a fantastic library, but isn't what I wanted in a datetime library. In many ways, it's better than Maya for certain things. In some ways, in my opinion, it's not.

I simply desire a sane API for datetimes that made sense to me for all the things I'd ever want to do—especially when dealing with timezone algebra. Arrow doesn't do all of the things I need (but it does a lot more!). Maya does do exactly what I need.

I think these projects complement each-other, personally. Maya is great for parsing websites. For example- Arrow supports floors and ceilings and spans of dates, which Maya does not at all.


☤ Installing Maya
-----------------

Installation is easy, with pip::

    $ pip install maya

✨🍰✨

☤ Like it?
----------

`Say Thanks <https://saythanks.io/to/kennethreitz>`_!


How to Contribute
-----------------

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
#. Fork `the repository`_ on GitHub to start making your changes to the **master** branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published. :) Make sure to add yourself to AUTHORS_.

.. _`the repository`: http://github.com/kennethreitz/maya
.. _AUTHORS: https://github.com/kennethreitz/maya/blob/master/AUTHORS.rst
