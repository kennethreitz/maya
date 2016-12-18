Maya: Datetime for Humans™
==========================

Datetimes are very frustrating to work with in Python, especially when dealing
with different locales on different systems. This library exists to make the 
simple things **much** easier, while admitting that time is an illusion 
(timezones doubly so). 

Datetimes should be interacted with via an API written for humans.

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

    >>> tomorrrow.rfc2822()
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
- Datetimes can very easily be generated, with our without tzinfo attached.
- This library is based around epoch time, but dates before Jan 1 1970 are indeed supported, via negative integers.
- Maya never panics, and always carrys a towel.

☤ Installing Maya
-----------------

Maya hasn't been released yet, but will be very soon!

✨🍰✨
