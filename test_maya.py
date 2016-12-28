import pytest
import copy

import maya


def test_rfc2822():
    r = maya.parse('February 21, 1994').rfc2822()
    d = maya.MayaDT.from_rfc2822(r)
    assert r == 'Mon, 21 Feb 1994 00:00:00 GMT'
    assert r == d.rfc2822()


def test_iso8601():
    r = maya.parse('February 21, 1994').iso8601()
    d = maya.MayaDT.from_iso8601(r)
    assert r == '1994-02-21T00:00:00Z'
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
    assert (d1.hour - d2.hour) % 24 == 5


def test_dt_tz_naive():
    d1 = maya.now().datetime(naive=True)
    assert d1.tzinfo is None

    d2 = maya.now().datetime(to_timezone='US/Eastern', naive=True)
    assert d2.tzinfo is None
    assert (d1.hour - d2.hour) % 24 == 5


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
        maya.when('another day')


def test_slang_date():
    d = maya.when('tomorrow')
    assert d.slang_date() == 'tomorrow'


def test_slang_time():
    d = maya.when('one hour ago')
    assert d.slang_time() == 'an hour ago'


def test_parse():
    d = maya.parse('February 21, 1994')
    assert format(d) == '1994-02-21 00:00:00+00:00'

    d = maya.parse('01/05/2016')
    assert format(d) == '2016-01-05 00:00:00+00:00'

    d = maya.parse('01/05/2016', day_first=True)
    assert format(d) == '2016-05-01 00:00:00+00:00'


def test_datetime_to_timezone():
    dt = maya.when('2016-01-01').datetime(to_timezone='US/Eastern')
    assert dt.tzinfo.zone == 'US/Eastern'


def test_comparison_operations():
    now = maya.now()
    now_copy = copy.deepcopy(now)
    tomorrow = maya.when('tomorrow')

    assert (now == now_copy) is True
    assert (now == tomorrow) is False

    assert (now != now_copy) is False
    assert (now != tomorrow) is True

    assert (now < now_copy) is False
    assert (now < tomorrow) is True

    assert (now <= now_copy) is True
    assert (now <= tomorrow) is True

    assert (now > now_copy) is False
    assert (now > tomorrow) is False

    assert (now >= now_copy) is True
    assert (now >= tomorrow) is False


def test_weekday():
    dt = maya.parse('February 21, 1994')
    assert dt.weekday == 1  # was a Monday

    dt = maya.parse('February 29, 1992')
    assert dt.weekday == 6  # was a Saturday


def test_week():
    dt = maya.parse('February 21, 1994')
    assert dt.week == 8

    dt = maya.parse('May 29, 1992')
    assert dt.week == 22
