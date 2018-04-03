from freezegun import freeze_time
import pytest


@pytest.fixture(params=[
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

], ids=lambda x: x[0] + "_off_" + str(x[1]))
def frozen_now(request):
    now_string, tz_offset = request.param
    with freeze_time(now_string, tz_offset=tz_offset):
        yield
