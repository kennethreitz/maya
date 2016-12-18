import pytest
from datetime import datetime

import maya


def test_rfc2822():
    r = maya.now().rfc2822()
    d = maya.MayaDT.from_rfc2822(r)
    assert r == d.rfc2822()


def test_iso8601():
    r = maya.now().iso8601()
    d = maya.MayaDT.from_iso8601(r)
    assert r == d.iso8601()


def test_human_when():
    r1 = maya.when('yesterday')
    r2 = maya.when('today')

    assert r2.day - r1.day == 1

def test_machine_parse():
    r1 = maya.parse('August 14, 2015')
    assert r1.day == 14

    r2 = maya.parse('August 15, 2015')
    assert r2.day == 15


def test_dt_tz_translation():
    d1 = maya.now().datetime()
    d2 = maya.now().datetime(to_timezone='US/Eastern')
    assert d1.hour - d2.hour == 5


def test_dt_tz_naive():
    d1 = maya.now().datetime(naive=True)
    assert d1.tzinfo is None

    d2 = maya.now().datetime(to_timezone='US/Eastern', naive=True)
    assert d2.tzinfo is None
    assert d1.hour - d2.hour == 5


def test_random_date():
    d = maya.when('11-17-11 08:09:10')
    assert d.year == 2011
    assert d.month == 11
    assert d.day == 17
    assert d.hour == 8
    assert d.minute == 9
    assert d.second == 10
    assert d.microsecond == 0


def test_print_date(capsys):
    d = maya.when('11-17-11')

    print(d)
    out, err = capsys.readouterr()
    assert out == '<MayaDT epoch=1321488000.0>\n'


def test_invalid_date():
    with pytest.raises(ValueError):
        d = maya.when('another day')


def test_slang_date():
    d = maya.when('tomorrow')
    assert d.slang_date() == 'tomorrow'


def test_slang_time():
    d = maya.when('one hour ago')
    assert d.slang_time() == 'an hour ago'


def test_format():
    d = maya.parse('February 21, 1994')
    assert format(d) == '1994-02-21 00:00:00+00:00'

# rand_day = maya.when('2011-02-07', timezone='US/Eastern')
