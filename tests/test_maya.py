import copy
import time
import calendar
from datetime import timedelta, datetime as Datetime

import pytz
import pytest

import maya
from maya.core import _seconds_or_timedelta  # import private function


@pytest.mark.parametrize(
    "string,expected", [("February 21, 1994", "Mon, 21 Feb 1994 00:00:00 GMT")]
)
def test_rfc2822(string, expected):
    r = maya.parse(string).rfc2822()
    d = maya.MayaDT.from_rfc2822(r)
    assert r == expected
    assert r == d.rfc2822()


@pytest.mark.parametrize(
    "string,expected", [("February 21, 1994", "1994-02-21T00:00:00Z")]
)
def test_iso8601(string, expected):
    r = maya.parse(string).iso8601()
    d = maya.MayaDT.from_iso8601(r)
    assert r == expected
    assert r == d.iso8601()


@pytest.mark.parametrize(
    "string,expected",
    [
        ('January 1, 1970', "12.17.16.7.5"),
        ('December 21, 2012', "13.0.0.0.0"),
        ('March 4, 1900', "12.14.5.10.0"),
    ],
)
def test_long_count(string, expected):
    r = maya.parse(string).long_count()
    d = maya.MayaDT.from_long_count(r)
    assert r == expected
    assert r == d.long_count()


@pytest.mark.parametrize(
    "string,expected",
    [
        ("20161001T1430.4+05:30", "2016-10-01T09:00:00.400000Z"),
        ("2016T14", "2016-01-01T14:00:00Z"),
        ("2016-10T14", "2016-10-01T14:00:00Z"),
        ("2012W05", "2012-01-30T00:00:00Z"),
        ("2012W055", "2012-02-03T00:00:00Z"),
        ("2012007", "2012-01-07T00:00:00Z"),
        ("2016-W07T09", "2016-02-15T09:00:00Z"),
    ],
)
def test_parse_iso8601(string, expected):
    d = maya.MayaDT.from_iso8601(string)
    assert expected == d.iso8601()


@pytest.mark.usefixtures("frozen_now")
def test_struct():
    now = round(time.time())
    ts = time.gmtime(now)
    m = maya.MayaDT.from_struct(ts)
    dt = Datetime.fromtimestamp(now, pytz.UTC)
    assert m._epoch is not None
    assert m.datetime() == dt
    ts = time.localtime(now)
    m = maya.MayaDT.from_struct(ts)
    dt = Datetime.fromtimestamp(time.mktime(ts) - maya.core.utc_offset(ts), pytz.UTC)
    assert m._epoch is not None
    assert m.datetime() == dt


def test_issue_104():
    e = 1507756331
    t = Datetime.utcfromtimestamp(e)
    t = maya.MayaDT.from_datetime(t)
    assert str(t) == "Wed, 11 Oct 2017 21:12:11 GMT"
    t = time.gmtime(e)
    t = maya.MayaDT.from_struct(t)
    assert str(t) == "Wed, 11 Oct 2017 21:12:11 GMT"


def test_human_when():
    r1 = maya.when("yesterday")
    r2 = maya.when("today")
    assert (r2.day - r1.day) in (1, -30, -29, -28, -27)


def test_machine_parse():
    r1 = maya.parse("August 14, 2015")
    assert r1.day == 14
    r2 = maya.parse("August 15, 2015")
    assert r2.day == 15


@pytest.mark.usefixtures("frozen_now")
def test_dt_tz_translation():
    d1 = maya.now().datetime()
    d2 = maya.now().datetime(to_timezone="EST")
    assert (d1.hour - d2.hour) % 24 == 5


@pytest.mark.usefixtures("frozen_now")
def test_dt_tz_naive():
    d1 = maya.now().datetime(naive=True)
    assert d1.tzinfo is None
    d2 = maya.now().datetime(to_timezone="EST", naive=True)
    assert d2.tzinfo is None
    assert (d1.hour - d2.hour) % 24 == 5


def test_random_date():
    # Test properties for maya.when()
    d1 = maya.when("11-17-11 08:09:10")
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
    d2 = maya.parse("February 29, 1992 13:12:34")
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
    d = maya.when("11-17-11")
    print(d)
    out, err = capsys.readouterr()
    assert out == "Thu, 17 Nov 2011 00:00:00 GMT\n"
    assert repr(d) == "<MayaDT epoch=1321488000.0>"


def test_invalid_date():
    with pytest.raises(ValueError):
        maya.when("another day")


def test_slang_date():
    d = maya.when("tomorrow")
    assert d.slang_date() == "tomorrow"


def test_slang_date_locale():
    d = maya.when("tomorrow")
    assert d.slang_date(locale="fr") == "demain"


def test_slang_time():
    d = maya.when("1 hour ago")
    assert d.slang_time() == "1 hour ago"


def test_slang_time_locale():
    d = maya.when("1 hour ago")
    assert d.slang_time(locale="de") == "vor 1 Stunde"


@pytest.mark.parametrize(
    "string,kwds,expected",
    [
        ("February 21, 1994", {}, "1994-02-21 00:00:00+00:00"),
        ("01/05/2016", {}, "2016-01-05 00:00:00+00:00"),
        ("01/05/2016", dict(day_first=True), "2016-05-01 00:00:00+00:00"),
        (
            "2016/05/01",
            dict(year_first=True, day_first=False),
            "2016-05-01 00:00:00+00:00",
        ),
        (
            "2016/01/05",
            dict(year_first=True, day_first=True),
            "2016-05-01 00:00:00+00:00",
        ),
        ("01/05/2016", dict(timezone="UTC"), "2016-01-05 00:00:00+00:00"),
        ("01/05/2016", dict(timezone="US/Central"), "2016-01-05 06:00:00+00:00"),
    ],
)
def test_parse(string, kwds, expected):
    d = maya.parse(string, **kwds)
    assert format(d) == expected


@pytest.mark.usefixtures("frozen_now")
def test_when_past():
    two_days_away = maya.now().add(days=2)

    past_date = maya.when(two_days_away.slang_date(), prefer_dates_from="past")

    assert past_date < maya.now()


@pytest.mark.usefixtures("frozen_now")
def test_when_future():
    two_days_away = maya.now().add(days=2)

    future_date = maya.when(two_days_away.slang_date(), prefer_dates_from="future")

    assert future_date > maya.now()


@pytest.mark.usefixtures("frozen_now")
def test_when_past_day_name():
    two_days_away = maya.now().add(days=2)

    past_date = maya.when(
        calendar.day_name[two_days_away.weekday], prefer_dates_from="past"
    )

    assert past_date < maya.now()


@pytest.mark.usefixtures("frozen_now")
def test_when_future_day_name():
    two_days_away = maya.now().add(days=2)

    future_date = maya.when(
        calendar.day_name[two_days_away.weekday], prefer_dates_from="future"
    )

    assert future_date > maya.now()


def test_datetime_to_timezone():
    dt = maya.when("2016-01-01").datetime(to_timezone="US/Eastern")
    assert dt.tzinfo.zone == "US/Eastern"


def test_rfc3339_epoch():
    mdt = maya.when("2016-01-01")
    out = mdt.rfc3339()
    mdt2 = maya.MayaDT.from_rfc3339(out)
    assert mdt.epoch == mdt2.epoch


def test_rfc3339_format():
    rfc3339 = maya.MayaDT.rfc3339(maya.when("2016-01-01T12:03:03Z"))
    # it's important that the string has got a "max 1-digit millis" fragment
    # as per https://tools.ietf.org/html/rfc3339#section-5.6
    assert rfc3339 == "2016-01-01T12:03:03.0Z"


@pytest.mark.usefixtures("frozen_now")
def test_comparison_operations():
    now = maya.now()
    now_copy = copy.deepcopy(now)
    tomorrow = maya.when("tomorrow")
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
        _seconds_or_timedelta("invalid interval")


@pytest.mark.usefixtures("frozen_now")
def test_intervals():
    now = maya.now()
    tomorrow = now.add(days=1)
    assert len(list(maya.intervals(now, tomorrow, 60 * 60))) == 24


@pytest.mark.usefixtures("frozen_now")
def test_dunder_add():
    now = maya.now()
    assert now + 1 == now.add(seconds=1)
    assert now + timedelta(seconds=1) == now.add(seconds=1)


@pytest.mark.usefixtures("frozen_now")
def test_dunder_radd():
    now = maya.now()
    assert now.add(seconds=1) == now + 1
    assert now.add(seconds=1) == now + timedelta(seconds=1)


@pytest.mark.usefixtures("frozen_now")
def test_dunder_sub():
    now = maya.now()
    assert now - 1 == now.subtract(seconds=1)
    assert now - timedelta(seconds=1) == now.subtract(seconds=1)


@pytest.mark.usefixtures("frozen_now")
def test_mayaDT_sub():
    now = maya.now()
    then = now.add(days=1)
    assert then - now == timedelta(seconds=24 * 60 * 60)
    assert now - then == timedelta(seconds=-24 * 60 * 60)


def test_core_local_timezone(monkeypatch):
    @property
    def mock_local_tz(self):
        class StaticTzInfo(object):
            zone = "local"

            def __repr__(self):
                return "<StaticTzInfo 'local'>"

        return StaticTzInfo()

    monkeypatch.setattr(maya.MayaDT, "_local_tz", mock_local_tz)
    mdt = maya.MayaDT(0)
    assert mdt.local_timezone == "UTC"


def test_getting_datetime_for_local_timezone(monkeypatch):
    @property
    def mock_local_tz(self):
        class StaticTzInfo(object):
            zone = "Europe/Zurich"

            def __repr__(self):
                return "<StaticTzInfo 'Europe/Zurich'>"

        return StaticTzInfo()

    monkeypatch.setattr(maya.MayaDT, "_local_tz", mock_local_tz)

    d = maya.parse("1994-02-21T12:00:00+05:30")

    dt = pytz.timezone("Europe/Zurich").localize(Datetime(1994, 2, 21, 7, 30))

    assert d.local_datetime() == dt


@pytest.mark.parametrize(
    "when_str,snap_str,expected_when",
    [("Mon, 21 Feb 1994 21:21:42 GMT", "@d", "Mon, 21 Feb 1994 00:00:00 GMT")],
)
def test_snaptime(when_str, snap_str, expected_when):
    # given
    dt = maya.when(when_str)
    # when
    dt = dt.snap(snap_str)
    # then
    assert dt == maya.when(expected_when)


@pytest.mark.parametrize(
    "when_str,snap_str,timezone,expected_when",
    [
        (
            "Mon, 21 Feb 1994 21:21:42 GMT",
            "@d",
            "Australia/Perth",
            "Mon, 21 Feb 1994 16:00:00 GMT",
        )
    ],
)
def test_snaptime_tz(when_str, snap_str, timezone, expected_when):
    # given
    dt = maya.when(when_str)
    # when
    dt = dt.snap_tz(snap_str, timezone)
    # then
    assert dt == maya.when(expected_when)
