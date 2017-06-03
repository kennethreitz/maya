import copy
from datetime import timedelta

import pytest

import maya
from maya.core import _seconds_or_timedelta  # import private function


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


def test_parse_iso8601():
    string = '20161001T1430.4+05:30'
    expected = '2016-10-01T09:00:00.400000Z'
    d = maya.MayaDT.from_iso8601(string)

    assert expected == d.iso8601()

    string = '2016T14'
    expected = '2016-01-01T14:00:00Z'
    d = maya.MayaDT.from_iso8601(string)

    assert expected == d.iso8601()

    string = '2016-10T14'
    expected = '2016-10-01T14:00:00Z'
    d = maya.MayaDT.from_iso8601(string)

    assert expected == d.iso8601()

    string = '2012W05'
    expected = '2012-01-30T00:00:00Z'
    d = maya.MayaDT.from_iso8601(string)

    assert expected == d.iso8601()

    string = '2012W055'
    expected = '2012-02-03T00:00:00Z'
    d = maya.MayaDT.from_iso8601(string)

    assert expected == d.iso8601()

    string = '2012007'
    expected = '2012-01-07T00:00:00Z'
    d = maya.MayaDT.from_iso8601(string)

    assert expected == d.iso8601()

    string = '2016-W07T09'
    expected = '2016-02-15T09:00:00Z'
    d = maya.MayaDT.from_iso8601(string)

    assert expected == d.iso8601()


def test_human_when():
    r1 = maya.when('yesterday')
    r2 = maya.when('today')

    assert (r2.day - r1.day) in (1, -30, -29, -28, -27)


def test_machine_parse():
    r1 = maya.parse('August 14, 2015')
    assert r1.day == 14

    r2 = maya.parse('August 15, 2015')
    assert r2.day == 15


def test_dt_tz_translation():
    d1 = maya.now().datetime()
    d2 = maya.now().datetime(to_timezone='EST')
    assert (d1.hour - d2.hour) % 24 == 5


def test_dt_tz_naive():
    d1 = maya.now().datetime(naive=True)
    assert d1.tzinfo is None

    d2 = maya.now().datetime(to_timezone='EST', naive=True)
    assert d2.tzinfo is None
    assert (d1.hour - d2.hour) % 24 == 5


def test_random_date():
    # Test properties for maya.when()
    d1 = maya.when('11-17-11 08:09:10')
    assert d1.year == 2011
    assert d1.month == 11
    assert d1.day == 17
    assert d1.week == 46
    assert d1.weekday == 4
    assert d1.hour == 8
    assert d1.minute == 9
    assert d1.second == 10
    assert d1.microsecond == 0

    # Test properties for maya.parse()
    d2 = maya.parse('February 29, 1992 13:12:34')
    assert d2.year == 1992
    assert d2.month == 2
    assert d2.day == 29
    assert d2.week == 9
    assert d2.weekday == 6
    assert d2.hour == 13
    assert d2.minute == 12
    assert d2.second == 34
    assert d2.microsecond == 0


def test_print_date(capsys):
    d = maya.when('11-17-11')

    print(d)
    out, err = capsys.readouterr()

    assert out == 'Thu, 17 Nov 2011 00:00:00 GMT\n'
    assert repr(d) == '<MayaDT epoch=1321488000.0>'


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


def test_rfc3339():
    mdt = maya.when('2016-01-01')
    out = mdt.rfc3339()
    mdt2 = maya.MayaDT.from_rfc3339(out)
    assert mdt.epoch == mdt2.epoch


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

    # Check Exceptions
    with pytest.raises(TypeError):
        now == 1
    with pytest.raises(TypeError):
        now != 1
    with pytest.raises(TypeError):
        now < 1
    with pytest.raises(TypeError):
        now <= 1
    with pytest.raises(TypeError):
        now > 1
    with pytest.raises(TypeError):
        now >= 1


def test_seconds_or_timedelta():
    # test for value in seconds
    assert _seconds_or_timedelta(1234) == timedelta(0, 1234)
    # test for value as `datetime.timedelta`
    assert _seconds_or_timedelta(timedelta(0, 1234)) == timedelta(0, 1234)
    # test for invalid value
    with pytest.raises(TypeError):
        _seconds_or_timedelta('invalid interval')


def test_intervals():
    now = maya.now()
    tomorrow = now.add(days=1)

    assert len(list(maya.intervals(now, tomorrow, 60 * 60))) == 24


def test_dunder_add():
    now = maya.now()
    assert now + 1 == now.add(seconds=1)
    assert now + timedelta(seconds=1) == now.add(seconds=1)


def test_dunder_radd():
    now = maya.now()
    assert now.add(seconds=1) == now + 1
    assert now.add(seconds=1) == now + timedelta(seconds=1)


def test_dunder_sub():
    now = maya.now()
    assert now - 1 == now.subtract(seconds=1)
    assert now - timedelta(seconds=1) == now.subtract(seconds=1)


def test_anywhere_on_earth():
    now = maya.now()
    assert now.aoe is True
    assert now.add(days=1).aoe is False
    assert now.subtract(days=1).aoe is False
