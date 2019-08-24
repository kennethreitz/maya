import random
from datetime import datetime, timedelta

import pytest
import pytz

import maya
from maya.compat import cmp

Los_Angeles = pytz.timezone("America/Los_Angeles")
New_York = pytz.timezone("America/New_York")
Melbourne = pytz.timezone("Australia/Melbourne")


def test_interval_requires_2_of_start_end_duration():
    start = maya.now()
    end = start.add(hours=1)
    with pytest.raises(ValueError):
        maya.MayaInterval(start=start)
    with pytest.raises(ValueError):
        maya.MayaInterval(end=end)
    with pytest.raises(ValueError):
        maya.MayaInterval(duration=60)
    with pytest.raises(ValueError):
        maya.MayaInterval(start=start, end=end, duration=60)
    maya.MayaInterval(start=start, end=end)
    maya.MayaInterval(start=start, duration=60)
    maya.MayaInterval(end=end, duration=60)


def test_interval_requires_end_time_after_or_on_start_time():
    with pytest.raises(ValueError):
        maya.MayaInterval(start=maya.now(), duration=0)
        maya.MayaInterval(start=maya.now(), duration=-1)


def test_interval_init_start_end():
    start = maya.now()
    end = start.add(hours=1)
    interval = maya.MayaInterval(start=start, end=end)
    assert interval.start == start
    assert interval.end == end


def test_interval_init_start_duration():
    start = maya.now()
    duration = 1
    interval = maya.MayaInterval(start=start, duration=duration)
    assert interval.start == start
    assert interval.end == start.add(seconds=duration)


def test_interval_init_end_duration():
    end = maya.now()
    duration = 1
    interval = maya.MayaInterval(end=end, duration=duration)
    assert interval.end == end
    assert interval.start == end.subtract(seconds=duration)


@pytest.mark.parametrize(
    "start_doy1,end_doy1,start_doy2,end_doy2,intersection_doys",
    (
        (0, 2, 1, 3, (1, 2)),
        (0, 2, 3, 4, None),
        (0, 2, 2, 3, None),
        (0, 1, 0, 1, (0, 1)),
        (1, 1, 1, 3, (1, 1)),
        (1, 1, 1, 1, (1, 1)),
        (1, 1, 2, 3, None),
        (2, 2, 1, 3, (2, 2)),
        (1, 3, 1, 1, (1, 1)),
        (2, 3, 1, 1, None),
        (1, 3, 2, 2, (2, 2)),
    ),
    ids=(
        "overlapping",
        "non-overlapping",
        "adjacent",
        "equal",
        "instant overlapping start only",
        "instant equal",
        "instant disjoint",
        "instant overlapping",
        "instant overlapping start only (left)",
        "instant disjoint (left)",
        "instant overlapping (left)",
    ),
)
def test_interval_intersection(
    start_doy1, end_doy1, start_doy2, end_doy2, intersection_doys
):
    base = maya.MayaDT.from_datetime(datetime(2016, 1, 1))
    interval1 = maya.MayaInterval(base.add(days=start_doy1), base.add(days=end_doy1))
    interval2 = maya.MayaInterval(base.add(days=start_doy2), base.add(days=end_doy2))
    if intersection_doys:
        start_doy_intersection, end_doy_intersection = intersection_doys
        assert interval1 & interval2 == maya.MayaInterval(
            base.add(days=start_doy_intersection), base.add(days=end_doy_intersection)
        )
    else:
        assert (interval1 & interval2) is None
    # check invalid argument
    with pytest.raises(TypeError):
        interval1 & "invalid type"


def test_interval_intersects():
    base = maya.MayaDT.from_datetime(datetime(2016, 1, 1))
    interval = maya.MayaInterval(base, base.add(days=1))
    assert interval.intersects(interval)
    assert not interval.intersects(
        maya.MayaInterval(base.add(days=2), base.add(days=3))
    )
    # check invalid argument
    with pytest.raises(TypeError):
        interval.intersects("invalid type")


def test_and_operator():
    base = maya.MayaDT.from_datetime(datetime(2016, 1, 1))
    interval1 = maya.MayaInterval(base, base.add(days=2))
    interval2 = maya.MayaInterval(base.add(days=1), base.add(days=3))
    assert (
        interval1 & interval2
        == interval2 & interval1  # noqa
        == interval1.intersection(interval2)  # noqa
    )
    # check invalid argument
    with pytest.raises(TypeError):
        interval1.intersection("invalid type")


def test_interval_eq_operator():
    start = maya.now()
    end = start.add(hours=1)
    interval = maya.MayaInterval(start=start, end=end)
    assert interval == maya.MayaInterval(start=start, end=end)
    assert interval != maya.MayaInterval(start=start, end=end.add(days=1))
    # check invalid argument
    with pytest.raises(TypeError):
        interval == "invalid type"
    with pytest.raises(TypeError):
        interval != "invalid type"


def test_interval_timedelta():
    start = maya.now()
    delta = timedelta(hours=1)
    interval = maya.MayaInterval(start=start, duration=delta)
    assert interval.timedelta == delta


def test_interval_duration():
    start = maya.now()
    delta = timedelta(hours=1)
    interval = maya.MayaInterval(start=start, duration=delta)
    assert interval.duration == delta.total_seconds()


@pytest.mark.parametrize(
    "start_doy1,end_doy1,start_doy2,end_doy2,expected",
    (
        (0, 2, 1, 3, False),
        (0, 2, 3, 4, False),
        (0, 2, 2, 3, False),
        (0, 1, 0, 1, True),
        (0, 3, 1, 2, True),
    ),
    ids=("overlapping", "non-overlapping", "adjacent", "equal", "subset"),
)
def test_interval_contains(start_doy1, end_doy1, start_doy2, end_doy2, expected):
    base = maya.MayaDT.from_datetime(datetime(2016, 1, 1))
    interval1 = maya.MayaInterval(base.add(days=start_doy1), base.add(days=end_doy1))
    interval2 = maya.MayaInterval(base.add(days=start_doy2), base.add(days=end_doy2))
    assert interval1.contains(interval2) is expected
    assert (interval2 in interval1) is expected
    # check invalid argument
    with pytest.raises(TypeError):
        interval1.contains("invalid type")


@pytest.mark.parametrize(
    "start_doy,end_doy,dt_doy,expected",
    (
        (2, 4, 1, False),
        (2, 4, 2, True),
        (2, 4, 3, True),
        (2, 4, 4, False),
        (2, 4, 5, False),
    ),
    ids=("before-start", "on-start", "during", "on-end", "after-end"),
)
def test_interval_in_operator_maya_dt(start_doy, end_doy, dt_doy, expected):
    base = maya.MayaDT.from_datetime(datetime(2016, 1, 1))
    interval = maya.MayaInterval(
        start=base.add(days=start_doy), end=base.add(days=end_doy)
    )
    dt = base.add(days=dt_doy)
    assert (dt in interval) is expected
    # check invalid argument
    with pytest.raises(TypeError):
        "invalid type" in interval


def test_interval_hash():
    start = maya.now()
    end = start.add(hours=1)
    interval = maya.MayaInterval(start=start, end=end)
    assert hash(interval) == hash(maya.MayaInterval(start=start, end=end))
    assert hash(interval) != hash(maya.MayaInterval(start=start, end=end.add(days=1)))


def test_interval_iter():
    start = maya.now()
    end = start.add(days=1)
    assert tuple(maya.MayaInterval(start=start, end=end)) == (start, end)


@pytest.mark.parametrize(
    "start1,end1,start2,end2,expected",
    [(1, 2, 1, 2, 0), (1, 3, 2, 4, -1), (2, 4, 1, 3, 1), (1, 2, 1, 3, -1)],
    ids=("equal", "less-than", "greater-than", "use-end-time-if-start-time-identical"),
)
def test_interval_cmp(start1, end1, start2, end2, expected):
    base = maya.now()
    interval1 = maya.MayaInterval(start=base.add(days=start1), end=base.add(days=end1))
    interval2 = maya.MayaInterval(start=base.add(days=start2), end=base.add(days=end2))
    assert cmp(interval1, interval2) == expected
    # check invalid argument
    with pytest.raises(TypeError):
        cmp(interval1, "invalid type")


@pytest.mark.parametrize(
    "start1,end1,start2,end2,expected",
    [
        (1, 2, 2, 3, [(1, 3)]),
        (1, 3, 2, 4, [(1, 4)]),
        (1, 2, 3, 4, [(1, 2), (3, 4)]),
        (1, 5, 2, 3, [(1, 5)]),
    ],
    ids=("adjacent", "overlapping", "non-overlapping", "contains"),
)
def test_interval_combine(start1, end1, start2, end2, expected):
    base = maya.now()
    interval1 = maya.MayaInterval(start=base.add(days=start1), end=base.add(days=end1))
    interval2 = maya.MayaInterval(start=base.add(days=start2), end=base.add(days=end2))
    expected_intervals = [
        maya.MayaInterval(start=base.add(days=start), end=base.add(days=end))
        for start, end in expected
    ]
    assert interval1.combine(interval2) == expected_intervals
    assert interval2.combine(interval1) == expected_intervals
    # check invalid argument
    with pytest.raises(TypeError):
        interval2.combine("invalid type")


@pytest.mark.parametrize(
    "start1,end1,start2,end2,expected",
    [
        (1, 2, 3, 4, [(1, 2)]),
        (1, 2, 2, 4, [(1, 2)]),
        (2, 3, 1, 4, []),
        (1, 4, 2, 3, [(1, 2), (3, 4)]),
        (1, 4, 0, 2, [(2, 4)]),
        (1, 4, 3, 5, [(1, 3)]),
        (1, 4, 1, 2, [(2, 4)]),
        (1, 4, 3, 4, [(1, 3)]),
    ],
    ids=(
        "non-overlapping",
        "adjacent",
        "contains",
        "splits",
        "overlaps-left",
        "overlaps-right",
        "overlaps-left-identical-start",
        "overlaps-right-identical-end",
    ),
)
def test_interval_subtract(start1, end1, start2, end2, expected):
    base = maya.now()
    interval1 = maya.MayaInterval(start=base.add(days=start1), end=base.add(days=end1))
    interval2 = maya.MayaInterval(start=base.add(days=start2), end=base.add(days=end2))
    expected_intervals = [
        maya.MayaInterval(start=base.add(days=start), end=base.add(days=end))
        for start, end in expected
    ]
    assert interval1.subtract(interval2) == expected_intervals
    # check invalid argument
    with pytest.raises(TypeError):
        interval1.subtract("invalid type")


@pytest.mark.parametrize(
    "start1,end1,start2,end2,expected",
    [(1, 2, 2, 3, True), (2, 3, 1, 2, True), (1, 3, 2, 3, False), (2, 3, 4, 5, False)],
    ids=("adjacent-right", "adjacent-left", "overlapping", "non-overlapping"),
)
def test_interval_is_adjacent(start1, end1, start2, end2, expected):
    base = maya.now()
    interval1 = maya.MayaInterval(start=base.add(days=start1), end=base.add(days=end1))
    interval2 = maya.MayaInterval(start=base.add(days=start2), end=base.add(days=end2))
    assert interval1.is_adjacent(interval2) == expected
    # check invalid argument
    with pytest.raises(TypeError):
        interval1.is_adjacent("invalid type")


@pytest.mark.parametrize(
    "start,end,delta,include_remainder,expected",
    [
        (0, 10, 5, False, [(0, 5), (5, 10)]),
        (0, 10, 5, True, [(0, 5), (5, 10)]),
        (0, 10, 3, False, [(0, 3), (3, 6), (6, 9)]),
        (0, 10, 3, True, [(0, 3), (3, 6), (6, 9), (9, 10)]),
        (0, 2, 5, False, []),
        (0, 2, 5, True, [(0, 2)]),
    ],
    ids=(
        "even-split",
        "even-split-include-partial",
        "uneven-split-do-not-include-partial",
        "uneven-split-include-partial",
        "delta-larger-than-timepsan-do-not-include-partial",
        "delta-larger-than-timepsan-include-partial",
    ),
)
def test_interval_split(start, end, delta, include_remainder, expected):
    base = maya.now()
    interval = maya.MayaInterval(start=base.add(days=start), end=base.add(days=end))
    delta = timedelta(days=delta)
    expected_intervals = [
        maya.MayaInterval(start=base.add(days=s), end=base.add(days=e))
        for s, e in expected
    ]
    assert expected_intervals == list(
        interval.split(delta, include_remainder=include_remainder)
    )


def test_interval_split_non_positive_delta():
    start = maya.now()
    end = start.add(days=1)
    interval = maya.MayaInterval(start=start, end=end)
    with pytest.raises(ValueError):
        list(interval.split(timedelta(seconds=0)))
    with pytest.raises(ValueError):
        list(interval.split(timedelta(seconds=-10)))


@pytest.mark.parametrize(
    "start,end,minutes,timezone,snap_out,expected_start,expected_end",
    [
        ((5, 12), (8, 48), 30, None, False, (5, 30), (8, 30)),
        ((5, 12), (8, 48), 30, None, True, (5, 0), (9, 0)),
        ((5, 15), (9, 0), 15, None, False, (5, 15), (9, 0)),
        ((5, 15), (9, 0), 15, None, True, (5, 15), (9, 0)),
        ((6, 50), (9, 15), 60, "America/New_York", False, (7, 0), (9, 0)),
        ((6, 50), (9, 15), 60, "America/New_York", True, (6, 0), (10, 0)),
        ((6, 20), (6, 50), 60, None, False, (6, 0), (6, 0)),
        ((6, 20), (6, 50), 60, None, True, (6, 0), (7, 0)),
        ((6, 20), (6, 50), 60, "America/Chicago", False, (6, 0), (6, 0)),
        ((6, 20), (6, 50), 60, "America/Chicago", True, (6, 0), (7, 0)),
    ],
    ids=(
        "normal",
        "normal-snap_out",
        "already-quantized",
        "already-quantized-snap_out",
        "with-timezone",
        "with-timezone-snap_out",
        "too-small",
        "too-small-snap_out",
        "too-small-with-timezone",
        "too-small-with-timezone-snap_out",
    ),
)
def test_quantize(
    start, end, minutes, timezone, snap_out, expected_start, expected_end
):
    base = maya.MayaDT.from_datetime(datetime(2017, 1, 1))
    interval = maya.MayaInterval(
        start=base.add(hours=start[0], minutes=start[1]),
        end=base.add(hours=end[0], minutes=end[1]),
    )
    kwargs = {"timezone": timezone} if timezone is not None else {}
    quantized_interval = interval.quantize(
        timedelta(minutes=minutes), snap_out=snap_out, **kwargs
    )
    assert quantized_interval == maya.MayaInterval(
        start=base.add(hours=expected_start[0], minutes=expected_start[1]),
        end=base.add(hours=expected_end[0], minutes=expected_end[1]),
    )


def test_quantize_invalid_delta():
    start = maya.now()
    end = start.add(days=1)
    interval = maya.MayaInterval(start=start, end=end)
    with pytest.raises(ValueError):
        interval.quantize(timedelta(minutes=0))
    with pytest.raises(ValueError):
        interval.quantize(timedelta(minutes=-1))


def test_interval_flatten_non_overlapping():
    step = 2
    max_hour = 20
    base = maya.now()
    intervals = [
        maya.MayaInterval(
            start=base.add(hours=hour), duration=timedelta(hours=step - 1)
        )
        for hour in range(0, max_hour, step)
    ]
    random.shuffle(intervals)
    assert maya.MayaInterval.flatten(intervals) == sorted(intervals)


def test_interval_flatten_adjacent():
    step = 2
    max_hour = 20
    base = maya.when("jan/1/2011")
    intervals = [
        maya.MayaInterval(start=base.add(hours=hour), duration=timedelta(hours=step))
        for hour in range(0, max_hour, step)
    ]
    random.shuffle(intervals)
    assert maya.MayaInterval.flatten(intervals) == [
        maya.MayaInterval(start=base, duration=timedelta(hours=max_hour))
    ]


def test_interval_flatten_intersecting():
    step = 2
    max_hour = 20
    base = maya.now()
    intervals = [
        maya.MayaInterval(
            start=base.add(hours=hour), duration=timedelta(hours=step, minutes=30)
        )
        for hour in range(0, max_hour, step)
    ]
    random.shuffle(intervals)
    assert maya.MayaInterval.flatten(intervals) == [
        maya.MayaInterval(start=base, duration=timedelta(hours=max_hour, minutes=30))
    ]


def test_interval_flatten_containing():
    step = 2
    max_hour = 20
    base = maya.now()
    containing_interval = maya.MayaInterval(
        start=base, end=base.add(hours=max_hour + step)
    )
    intervals = [
        maya.MayaInterval(
            start=base.add(hours=hour), duration=timedelta(hours=step - 1)
        )
        for hour in range(2, max_hour, step)
    ]
    intervals.append(containing_interval)
    random.shuffle(intervals)
    assert maya.MayaInterval.flatten(intervals) == [containing_interval]


def test_interval_from_datetime():
    start = maya.now()
    duration = timedelta(hours=1)
    end = start + duration
    interval = maya.MayaInterval.from_datetime(
        start_dt=start.datetime(naive=False), end_dt=end.datetime(naive=False)
    )
    assert interval.start == start
    assert interval.end == end
    interval2 = maya.MayaInterval.from_datetime(
        start_dt=start.datetime(naive=False), duration=duration
    )
    assert interval2.start == start
    assert interval2.end == end
    interval3 = maya.MayaInterval.from_datetime(
        end_dt=end.datetime(naive=False), duration=duration
    )
    assert interval3.start == start
    assert interval3.end == end


def test_interval_iso8601():
    start = maya.when("11-17-11 08:09:10")
    interval = maya.MayaInterval(start=start, duration=1)
    assert interval.iso8601() == "2011-11-17T08:09:10Z/2011-11-17T08:09:11Z"


def test_interval_from_iso8601():
    interval = maya.MayaInterval.from_iso8601(
        "2018-03-18T14:27:18Z/2018-04-01T04:15:27Z"
    )
    s = maya.when("2018-03-18T14:27:18Z")
    e = maya.when("2018-04-01T04:15:27Z")

    assert interval.start == s
    assert interval.end == e


def test_interval_from_iso8601_duration():
    interval = maya.MayaInterval.from_iso8601("2018-03-18T14:27:18Z/P13DT13H48M9S")
    s = maya.when("2018-03-18T14:27:18Z")
    e = maya.when("2018-04-01T04:15:27Z")

    assert interval.start == s
    assert interval.end == e

    interval = maya.MayaInterval.from_iso8601("2018-03-05T14:27:18Z/P2W")
    s = maya.when("2018-03-05T14:27:18Z")
    e = maya.when("2018-03-19T14:27:18Z")

    assert interval.start == s
    assert interval.end == e


@pytest.mark.parametrize(
    "start_string,end_string,interval,expected_count",
    [
        ("2019-01-03 11:40:00Z", "2019-01-03 11:40:20Z", 2, 10),
        ("2019-01-03 11:40:00Z", "2019-01-03 11:40:30Z", timedelta(seconds=2), 15),
        ("2019-01-03 11:40:00Z", "2019-01-03 11:45:00Z", 2 * 60, 3),
        ("2019-01-03 11:40:00Z", "2019-01-03 11:51:00Z", timedelta(minutes=1), 11),
        ("2019-01-03 11:40:00Z", "2019-01-03 21:40:00Z", 3 * 60 * 60, 4),
        ("2019-01-03 11:40:00Z", "2019-01-03 13:41:00Z", timedelta(hours=1), 3),
        ("2019-01-03 11:40:00Z", "2019-01-09 11:40:00Z", 3 * 60 * 60 * 24, 2),
        ("2019-01-03 11:40:00Z", "2019-01-05 12:00:00Z", timedelta(days=2), 2),
    ],
    ids=(
        "seconds",
        "seconds-timedelta",
        "minutes",
        "minutes-timedelta",
        "hours",
        "hours-timedelta",
        "days",
        "days-timedelta",
    ),
)
def test_intervals(start_string, end_string, interval, expected_count):
    start = maya.parse(start_string)
    end = maya.parse(end_string)
    assert len(list(maya.intervals(start, end, interval))) == expected_count


def test_issue_168_regression():
    start = maya.now()
    end = start.add(weeks=1)
    gen = maya.intervals(start=start, end=end, interval=60 * 60 * 24)
    # Since the bug causes the generator to never end, first sanity
    # check that two results are not the same.
    assert next(gen) != next(gen)
    assert len(list(maya.intervals(start=start, end=end, interval=60 * 60 * 24))) == 7
