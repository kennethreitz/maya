Maya: Datetimes for Humans™
===========================

.. image:: https://img.shields.io/pypi/v/maya.svg
    :target: https://pypi.python.org/pypi/maya

.. image:: https://travis-ci.org/kennethreitz/maya.svg?branch=master
    :target: https://travis-ci.org/kennethreitz/maya

.. image:: https://img.shields.io/badge/SayThanks-!-1EAEDB.svg
    :target: https://saythanks.io/to/kennethreitz


Datetimes are very frustrating to work with in Python, especially when dealing
with different locales on different systems. This library exists to make the
simple things **much** easier, while admitting that time is an illusion
(timezones doubly so).

Datetimes should be interacted with via an API written for humans.

Maya is mostly built around the headaches and use-cases around parsing datetime data from websites.

.. image:: https://farm4.staticflickr.com/3702/33288285996_5b69d2b8f7_k_d.jpg

Art by `Sam Flores
<https://www.instagram.com/samagram12/>`_ (Photo by `Kenneth Reitz
<https://www.instagram.com/kennethreitz/>`_). 

If you're interested in financially supporting Kenneth Reitz open source, consider `visiting this link <https://cash.me/$KennethReitz>`_. Your support helps tremendously with sustainability of motivation, as Open Source is no longer part of my day job.

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

    # Maya speaks Python.
    >>> m = maya.MayaDT.from_datetime(datetime.utcnow())
    >>> print(m)
    Wed, 20 Sep 2017 17:24:32 GMT

    >>> m = maya.MayaDT.from_struct(time.gmtime())
    >>> print(m)
    Wed, 20 Sep 2017 17:24:32 GMT
    
    >>> m = maya.MayaDT(time.time())
    >>> print(m)
    Wed, 20 Sep 2017 17:24:32 GMT

    >>> rand_day.day
    7

    >>> rand_day.add(days=10).day
    17

    # Always.
    >>> rand_day.timezone
    UTC

    # Range of hours in a day:
    >>> maya.intervals(start=maya.now(), end=maya.now().add(days=1), interval=60*60)
    <generator object intervals at 0x105ba5820>

    # snap modifiers
    >>> dt = maya.when('Mon, 21 Feb 1994 21:21:42 GMT')
    >>> dt.snap('@d+3h').rfc2822()
    'Mon, 21 Feb 1994 03:00:00 GMT'

☤ Advanced Usage of Maya
------------------------

In addition to timestamps, Maya also includes a wonderfully powerful ``MayaInterval`` class, which represents a range of time (e.g. an event). With this class, you can perform a multitude of advanced calendar calculations with finesse and ease.

For example:

.. code-block:: pycon

    >>> from maya import MayaInterval

    # Create an event that is one hour long, starting now.
    >>> event_start = maya.now()
    >>> event_end = event_start.add(hours=1)

    >>> event = MayaInterval(start=event_start, end=event_end)

From here, there are a number of methods available to you, which you can use to compare this event to another event.



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

All these projects complement each other, and are friends. Pendulum, for example, helps power Maya's parsing.

Arrow, for example, is a fantastic library, but isn't what I wanted in a datetime library. In many ways, it's better than Maya for certain things. In some ways, in my opinion, it's not.

I simply desire a sane API for datetimes that made sense to me for all the things I'd ever want to do—especially when dealing with timezone algebra. Arrow doesn't do all of the things I need (but it does a lot more!). Maya does do exactly what I need.

I think these projects complement each-other, personally. Maya is great for parsing websites, and dealing with calendar events!


☤ Installing Maya
-----------------

Installation is easy, with `pipenv <http://pipenv.org/>`_::

    $ pipenv install maya

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
