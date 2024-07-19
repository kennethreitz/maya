import datetime

import pytz
from freezegun import freeze_time
import pytest


@pytest.fixture(
    params=[
        ("2018-03-25T00:00:00", 2),
        ("2018-03-25T01:00:00", 2),
        ("2018-03-25T02:00:00", 2),
        ("2018-03-25T02:30:00", 2),
        ("2018-03-25T03:00:00", 2),
        ("2018-03-25T04:00:00", 2),
        ("2018-10-28T00:00:00", 2),
        ("2018-10-28T01:00:00", 2),
        ("2018-10-28T02:00:00", 2),
        ("2018-10-28T02:30:00", 2),
        ("2018-10-28T03:00:00", 2),
        ("2018-10-28T04:00:00", 2),
    ],
    ids=lambda x: x[0] + "_off_" + str(x[1]),
)
def frozen_now(request):
    now_string, tz_offset = request.param
    with freeze_time(now_string, tz_offset=tz_offset):
        yield


@pytest.fixture(params=[
    datetime.datetime(2020, 8, 10, 22, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 10, 23, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 0, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 1, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 2, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 3, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 4, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 5, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 6, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 7, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 8, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 9, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 10, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 11, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 12, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 13, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 14, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 15, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 16, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 17, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 18, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 19, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 20, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 8, 11, 21, 2, 0, tzinfo=pytz.timezone('UTC')),
], ids=str)
def frozen_2020_08_11_in_paris(request):
    """
    fixture setting datetime.now() to every hour of the 11th of august 2020 in Paris
    (summer time, GMT+2)
    """
    with freeze_time(request.param):
        yield


@pytest.fixture(params=[
    datetime.datetime(2020, 2, 10, 23, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 0, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 1, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 2, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 3, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 4, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 5, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 6, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 7, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 8, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 9, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 10, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 11, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 12, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 13, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 14, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 15, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 16, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 17, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 18, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 19, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 20, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 21, 2, 0, tzinfo=pytz.timezone('UTC')),
    datetime.datetime(2020, 2, 11, 22, 2, 0, tzinfo=pytz.timezone('UTC')),
], ids=str)
def frozen_2020_02_11_in_paris(request):
    """
    fixture setting datetime.now() to every hour of the 11th of february 2020 in Paris
    (winter time, GMT+1)
    """
    with freeze_time(request.param):
        yield
