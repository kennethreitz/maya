from freezegun import freeze_time
import pytest


@pytest.fixture(params=[
    "2018-03-25T00:00:00",
    "2018-03-25T01:00:00",
    "2018-03-25T02:00:00",
    "2018-03-25T02:30:00",
    "2018-03-25T03:00:00",
    "2018-03-25T04:00:00",
])
def now_string(request):
    return request.param


@pytest.fixture(params=[0, 1, 2, 3, 4, -1, -2, -3, 10, 11, -10, -11])
def tz_offset(request):
    return request.param


@pytest.fixture
def frozen_now(now_string, tz_offset):
    with freeze_time(now_string, tz_offset=tz_offset):
        yield
