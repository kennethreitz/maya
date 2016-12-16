Maya: Datetime for Humans™
==========================

Datetimes are very frustrating to work with in Python, especially when dealing
with different locales on different systems. This library exists to


Note that outputs are fuzzy and made up, just playing with an API here::

    >>> now = maya.now()
    <MayaDT epoch=1481847021>

    >>> tomorrow = now.forwards('one day')
    <MayaDT epoch=1481977021>

    >>> tomorrow.iso8601()
    2016-12-16T00:12:54+00:00

    >>> tomorrrow.iso8601()
    Fri, 17 Dec 2016 00:12:54 +0000

    >>> tomorrow = maya.adjust('tomorrow').datetime
    datetime.datetime(2016, 12, 16, 0, 14, 33, 950436)

Timezones fit in here somewhere.