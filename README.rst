Maya: Datetime for Humans™
==========================

Datetimes are very frustrating to work with in Python, especially when dealing
with different locales on different systems. This library exists to make the simple things easier, while admitting that time (especially timezones) are an illusion, and should be interacted with via an API for humans (not machines).

The Usage
---------

Just playing with an API here::

    >>> now = maya.now()
    <MayaDT epoch=1481850660.9>

    >>> tomorrow = maya.when('tomorrow')
    <MayaDT epoch=1481919067.23>

    >>> tomorrow.iso8601()
    '2016-12-16T15:11:30.263350Z'

    >>> tomorrrow.rfc2822()
    'Fri, 16 Dec 2016 20:11:30 -0000'

    >>> tomorrow.datetime()
    datetime.datetime(2016, 12, 16, 15, 11, 30, 263350)

Timezones fit in here somewhere...