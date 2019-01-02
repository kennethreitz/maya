# ___  __  ___  _  _  ___
# || \/ | ||=|| \\// ||=||
# ||    | || ||  //  || ||
import email.utils
import time
import functools
from datetime import timedelta, datetime as Datetime

import re
import pytz
import humanize
import dateparser
import pendulum
import snaptime
from tzlocal import get_localzone
from dateutil.relativedelta import relativedelta
from dateparser.languages.loader import default_loader

from .compat import cmp, comparable


def validate_class_type_arguments(operator):
    """
    Decorator to validate all the arguments to function
    are of the type of calling class for passed operator
    """

    def inner(function):

        def wrapper(self, *args, **kwargs):
            for arg in args + tuple(kwargs.values()):
                if not isinstance(arg, self.__class__):
                    raise TypeError(
                        'unorderable types: {}() {} {}()'.format(
                            type(self).__name__, operator, type(arg).__name__
                        )
                    )

            return function(self, *args, **kwargs)

        return wrapper

    return inner


def validate_arguments_type_of_function(param_type=None):
    """
    Decorator to validate the <type> of arguments in
    the calling function are of the `param_type` class.

    if `param_type` is None, uses `param_type` as the class where it is used.

    Note: Use this decorator on the functions of the class.
    """

    def inner(function):

        def wrapper(self, *args, **kwargs):
            type_ = param_type or type(self)
            for arg in args + tuple(kwargs.values()):
                if not isinstance(arg, type_):
                    raise TypeError(
                        (
                            'Invalid Type: {}.{}() accepts only the '
                            'arguments of type "<{}>"'
                        ).format(
                            type(self).__name__,
                            function.__name__,
                            type_.__name__,
                        )
                    )

            return function(self, *args, **kwargs)

        return wrapper

    return inner


class MayaDT(object):
    """The Maya Datetime object."""
    __EPOCH_START = (1970, 1, 1)

    def __init__(self, epoch):
        super(MayaDT, self).__init__()
        self._epoch = epoch

    def __repr__(self):
        return '<MayaDT epoch={}>'.format(self._epoch)

    def __str__(self):
        return self.rfc2822()

    def __format__(self, *args, **kwargs):
        """Return's the datetime's format"""
        return format(self.datetime(), *args, **kwargs)

    @validate_class_type_arguments('==')
    def __eq__(self, maya_dt):
        return int(self._epoch) == int(maya_dt._epoch)

    @validate_class_type_arguments('!=')
    def __ne__(self, maya_dt):
        return int(self._epoch) != int(maya_dt._epoch)

    @validate_class_type_arguments('<')
    def __lt__(self, maya_dt):
        return int(self._epoch) < int(maya_dt._epoch)

    @validate_class_type_arguments('<=')
    def __le__(self, maya_dt):
        return int(self._epoch) <= int(maya_dt._epoch)

    @validate_class_type_arguments('>')
    def __gt__(self, maya_dt):
        return int(self._epoch) > int(maya_dt._epoch)

    @validate_class_type_arguments('>=')
    def __ge__(self, maya_dt):
        return int(self._epoch) >= int(maya_dt._epoch)

    def __hash__(self):
        return hash(int(self.epoch))

    def __add__(self, duration):
        return self.add(
            seconds=_seconds_or_timedelta(duration).total_seconds()
        )

    def __radd__(self, duration):
        return self + duration

    def __sub__(self, duration_or_date):
        if isinstance(duration_or_date, MayaDT):
            return self.subtract_date(dt=duration_or_date)

        else:
            return self.subtract(
                seconds=_seconds_or_timedelta(duration_or_date).total_seconds()
            )

    def add(self, **kwargs):
        """Returns a new MayaDT object with the given offsets."""
        return self.from_datetime(
            pendulum.instance(self.datetime()).add(**kwargs)
        )

    def subtract(self, **kwargs):
        """Returns a new MayaDT object with the given offsets."""
        return self.from_datetime(
            pendulum.instance(self.datetime()).subtract(**kwargs)
        )

    def subtract_date(self, **kwargs):
        """Returns a timedelta object with the duration between the dates"""
        return timedelta(seconds=self.epoch - kwargs['dt'].epoch)

    def snap(self, instruction):
        """
        Returns a new MayaDT object modified by the given instruction.

        Powered by snaptime.  See https://github.com/zartstrom/snaptime
        for a complete documentation about the snaptime instructions.
        """
        return self.from_datetime(snaptime.snap(self.datetime(), instruction))

    # Timezone Crap
    # -------------
    @property
    def timezone(self):
        """Returns the UTC tzinfo name. It's always UTC. Always."""
        return 'UTC'

    @property
    def _tz(self):
        """Returns the UTC tzinfo object."""
        return pytz.timezone(self.timezone)

    @property
    def local_timezone(self):
        """Returns the name of the local timezone."""
        if self._local_tz.zone in pytz.all_timezones:
            return self._local_tz.zone

        return self.timezone

    @property
    def _local_tz(self):
        """Returns the local timezone."""
        return get_localzone()

    @staticmethod
    @validate_arguments_type_of_function(Datetime)
    def __dt_to_epoch(dt):
        """Converts a datetime into an epoch."""
        # Assume UTC if no datetime is provided.
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=pytz.utc)
        epoch_start = Datetime(*MayaDT.__EPOCH_START, tzinfo=pytz.timezone('UTC'))
        return (dt - epoch_start).total_seconds()

    # Importers
    # ---------
    @classmethod
    @validate_arguments_type_of_function(Datetime)
    def from_datetime(klass, dt):
        """Returns MayaDT instance from datetime."""
        return klass(klass.__dt_to_epoch(dt))

    @classmethod
    @validate_arguments_type_of_function(time.struct_time)
    def from_struct(klass, struct, timezone=pytz.UTC):
        """Returns MayaDT instance from a 9-tuple struct

        It's assumed to be from gmtime().
        """
        struct_time = time.mktime(struct) - utc_offset(struct)
        dt = Datetime.fromtimestamp(struct_time, timezone)
        return klass(klass.__dt_to_epoch(dt))

    @classmethod
    def from_iso8601(klass, iso8601_string):
        """Returns MayaDT instance from iso8601 string."""
        return parse(iso8601_string)

    @staticmethod
    def from_rfc2822(rfc2822_string):
        """Returns MayaDT instance from rfc2822 string."""
        return parse(rfc2822_string)

    @staticmethod
    def from_rfc3339(rfc3339_string):
        """Returns MayaDT instance from rfc3339 string."""
        return parse(rfc3339_string)

    # Exporters
    # ---------
    def datetime(self, to_timezone=None, naive=False):
        """Returns a timezone-aware datetime...
        Defaulting to UTC (as it should).

        Keyword Arguments:
            to_timezone {str} -- timezone to convert to (default: None/UTC)
            naive {bool} -- if True,
                            the tzinfo is simply dropped (default: False)
        """
        if to_timezone:
            dt = self.datetime().astimezone(pytz.timezone(to_timezone))
        else:
            dt = Datetime.utcfromtimestamp(self._epoch)
            dt.replace(tzinfo=self._tz)
        # Strip the timezone info if requested to do so.
        if naive:
            return dt.replace(tzinfo=None)

        else:
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=self._tz)
        return dt

    def local_datetime(self):
        """Returns a local timezone-aware datetime object

        It's the same as:
        mayaDt.datetime(to_timezone=mayaDt.local_timezone)
        """
        return self.datetime(to_timezone=self.local_timezone, naive=False)

    def iso8601(self):
        """Returns an ISO 8601 representation of the MayaDT."""
        # Get a timezone-naive datetime.
        dt = self.datetime(naive=True)
        return '{}Z'.format(dt.isoformat())

    def rfc2822(self):
        """Returns an RFC 2822 representation of the MayaDT."""
        return email.utils.formatdate(self.epoch, usegmt=True)

    def rfc3339(self):
        """Returns an RFC 3339 representation of the MayaDT."""
        return self.datetime().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-5] + "Z"

    # Properties
    # ----------
    @property
    def year(self):
        return self.datetime().year

    @property
    def month(self):
        return self.datetime().month

    @property
    def day(self):
        return self.datetime().day

    @property
    def date(self):
        return self.datetime().date()

    @property
    def week(self):
        return self.datetime().isocalendar()[1]

    @property
    def weekday(self):
        """Return the day of the week as an integer.

        Monday is 1 and Sunday is 7.
        """
        return self.datetime().isoweekday()

    @property
    def hour(self):
        return self.datetime().hour

    @property
    def minute(self):
        return self.datetime().minute

    @property
    def second(self):
        return self.datetime().second

    @property
    def microsecond(self):
        return self.datetime().microsecond

    @property
    def epoch(self):
        return int(self._epoch)

    # Human Slang Extras
    # ------------------
    def slang_date(self, locale="en"):
        """"Returns human slang representation of date.

        Keyword Arguments:
            locale -- locale to translate to, e.g. 'fr' for french.
                       (default: 'en' - English)
        """
        dt = pendulum.instance(self.datetime())

        try:
            return _translate(dt, locale)
        except KeyError:
            pass

        delta = humanize.time.abs_timedelta(
            timedelta(seconds=(self.epoch - now().epoch)))

        format_string = "DD MMM"
        if delta.days >= 365:
            format_string += " YYYY"

        return dt.format(format_string, locale=locale).title()

    def slang_time(self, locale="en"):
        """"Returns human slang representation of time.

        Keyword Arguments:
            locale -- locale to translate to, e.g. 'fr' for french.
                       (default: 'en' - English)
        """
        dt = self.datetime()
        return pendulum.instance(dt).diff_for_humans(locale=locale)


def utc_offset(time_struct=None):
    """
    Returns the time offset from UTC accounting for DST

    Keyword Arguments:
        time_struct {time.struct_time} -- the struct time for which to
                                          return the UTC offset.
                                          If None, use current local time.
    """
    if time_struct:
        ts = time_struct
    else:
        ts = time.localtime()

    if ts[-1]:
        offset = time.altzone
    else:
        offset = time.timezone
    return offset


def to_utc_offset_naive(dt):
    if dt.tzinfo is None:
        return dt

    return dt.astimezone(pytz.utc).replace(tzinfo=None)


def to_utc_offset_aware(dt):
    if dt.tzinfo is not None:
        return dt

    return pytz.utc.localize(dt)


def to_iso8601(dt):
    return to_utc_offset_naive(dt).isoformat() + 'Z'


def end_of_day_midnight(dt):
    if dt.time() == time.min:
        return dt

    else:
        return (
            dt.replace(hour=0, minute=0, second=0, microsecond=0) +
            timedelta(days=1)
        )


@comparable
class MayaInterval(object):
    """
    A MayaInterval represents a range between two datetimes,
    inclusive of the start and exclusive of the end.
    """

    def __init__(self, start=None, end=None, duration=None):
        try:
            # Ensure that proper arguments were passed.
            assert any(
                (
                    (start and end),
                    (start and duration is not None),
                    (end and duration is not None),
                )
            )
            assert not all((start, end, duration is not None))
        except AssertionError:
            raise ValueError(
                'Exactly 2 of start, end, and duration must be specified'
            )

        # Convert duration to timedelta if seconds were provided.
        if duration:
            duration = _seconds_or_timedelta(duration)
        if not start:
            start = end - duration
        if not end:
            end = start + duration
        if start > end:
            raise ValueError('MayaInterval cannot end before it starts')

        self.start = start
        self.end = end

    def __repr__(self):
        return '<MayaInterval start={0!r} end={1!r}>'.format(
            self.start, self.end
        )

    def iso8601(self):
        """Returns an ISO 8601 representation of the MayaInterval."""
        return '{0}/{1}'.format(self.start.iso8601(), self.end.iso8601())

    @classmethod
    def parse_iso8601_duration(cls, duration, start=None, end=None):
        match = re.match(
            r'(?:P(?P<weeks>\d+)W)|(?:P(?:(?:(?P<years>\d+)Y)?(?:(?P<months>\d+)M)?(?:(?P<days>\d+)D))?(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?)?)',
            duration
        )

        time_components = {}
        if match:
            time_components = match.groupdict(0)
            for key, value in time_components.items():
                time_components[key] = int(value)

            duration = relativedelta(**time_components)

            if start:
                return parse(start.datetime() + duration)

            if end:
                return parse(end.datetime() - duration)

        return None

    @classmethod
    def from_iso8601(cls, s):
        # # Start and end, such as "2007-03-01T13:00:00Z/2008-05-11T15:30:00Z"
        start, end = s.split('/')
        try:
            start = parse(start)
        except pendulum.parsing.exceptions.ParserError:
            # start = self._parse_iso8601_duration(start, end=end)
            raise NotImplementedError()

        try:
            end = parse(end)
        except (pendulum.parsing.exceptions.ParserError, TypeError) as e:
            end = cls.parse_iso8601_duration(end, start=start)

        return cls(start=start, end=end)

        # # Start and duration, such as "2007-03-01T13:00:00Z/P1Y2M10DT2H30M"
        # # Duration and end, such as "P1Y2M10DT2H30M/2008-05-11T15:30:00Z"

    @validate_arguments_type_of_function()
    def __and__(self, maya_interval):
        return self.intersection(maya_interval)

    @validate_arguments_type_of_function()
    def __or__(self, maya_interval):
        return self.combine(maya_interval)

    @validate_arguments_type_of_function()
    def __eq__(self, maya_interval):
        return (
            self.start == maya_interval.start and self.end == maya_interval.end
        )

    def __hash__(self):
        return hash((self.start, self.end))

    def __iter__(self):
        yield self.start
        yield self.end

    @validate_arguments_type_of_function()
    def __cmp__(self, maya_interval):
        return (
            cmp(self.start, maya_interval.start)
            or cmp(self.end, maya_interval.end)
        )

    @property
    def duration(self):
        return self.timedelta.total_seconds()

    @property
    def timedelta(self):
        return timedelta(seconds=(self.end.epoch - self.start.epoch))

    @property
    def is_instant(self):
        return self.timedelta == timedelta(seconds=0)

    def intersects(self, maya_interval):
        return self & maya_interval is not None

    @property
    def midpoint(self):
        return self.start.add(seconds=(self.duration / 2))

    @validate_arguments_type_of_function()
    def combine(self, maya_interval):
        """Returns a combined list of timespans, merged together."""
        interval_list = sorted([self, maya_interval])
        if self & maya_interval or self.is_adjacent(maya_interval):
            return [
                MayaInterval(
                    interval_list[0].start,
                    max(interval_list[0].end, interval_list[1].end),
                )
            ]

        return interval_list

    @validate_arguments_type_of_function()
    def subtract(self, maya_interval):
        """"Removes the given interval."""
        if not self & maya_interval:
            return [self]

        elif maya_interval.contains(self):
            return []

        interval_list = []
        if self.start < maya_interval.start:
            interval_list.append(MayaInterval(self.start, maya_interval.start))
        if self.end > maya_interval.end:
            interval_list.append(MayaInterval(maya_interval.end, self.end))
        return interval_list

    def split(self, duration, include_remainder=True):
        # Convert seconds to timedelta, if appropriate.
        duration = _seconds_or_timedelta(duration)
        if duration <= timedelta(seconds=0):
            raise ValueError('cannot call split with a non-positive timedelta')

        start = self.start
        while start < self.end:
            if start + duration <= self.end:
                yield MayaInterval(start, start + duration)

            elif include_remainder:
                yield MayaInterval(start, self.end)

            start += duration

    def quantize(self, duration, snap_out=False, timezone='UTC'):
        """Returns a quanitzed interval."""
        # Convert seconds to timedelta, if appropriate.
        duration = _seconds_or_timedelta(duration)
        timezone = pytz.timezone(timezone)
        if duration <= timedelta(seconds=0):
            raise ValueError('cannot quantize by non-positive timedelta')

        epoch = timezone.localize(Datetime(1970, 1, 1))
        seconds = int(duration.total_seconds())
        start_seconds = int(
            (self.start.datetime(naive=False) - epoch).total_seconds()
        )
        end_seconds = int(
            (self.end.datetime(naive=False) - epoch).total_seconds()
        )
        if start_seconds % seconds and not snap_out:
            start_seconds += seconds
        if end_seconds % seconds and snap_out:
            end_seconds += seconds
        start_seconds -= start_seconds % seconds
        end_seconds -= end_seconds % seconds
        if start_seconds > end_seconds:
            start_seconds = end_seconds
        return MayaInterval(
            start=MayaDT.from_datetime(epoch).add(seconds=start_seconds),
            end=MayaDT.from_datetime(epoch).add(seconds=end_seconds),
        )

    @validate_arguments_type_of_function()
    def intersection(self, maya_interval):
        """Returns the intersection between two intervals."""
        start = max(self.start, maya_interval.start)
        end = min(self.end, maya_interval.end)
        either_instant = self.is_instant or maya_interval.is_instant
        instant_overlap = (self.start == maya_interval.start or start <= end)
        if (either_instant and instant_overlap) or (start < end):
            return MayaInterval(start, end)

    @validate_arguments_type_of_function()
    def contains(self, maya_interval):
        return (
            self.start <= maya_interval.start and self.end >= maya_interval.end
        )

    def __contains__(self, maya_dt):
        if isinstance(maya_dt, MayaDT):
            return self.contains_dt(maya_dt)

        return self.contains(maya_dt)

    def contains_dt(self, dt):
        return self.start <= dt < self.end

    @validate_arguments_type_of_function()
    def is_adjacent(self, maya_interval):
        return (
            self.start == maya_interval.end or self.end == maya_interval.start
        )

    @property
    def icalendar(self):
        ical_dt_format = '%Y%m%dT%H%M%SZ'
        return """
        BEGIN:VCALENDAR
        VERSION:2.0
        BEGIN:VEVENT
        DTSTART:{0}
        DTEND:{1}
        END:VEVENT
        END:VCALENDAR
        """.format(
            self.start.datetime().strftime(ical_dt_format),
            self.end.datetime().strftime(ical_dt_format),
        ).replace(
            ' ', ''
        ).strip(
            '\r\n'
        ).replace(
            '\n', '\r\n'
        )

    @staticmethod
    def flatten(interval_list):
        return functools.reduce(
            lambda reduced,
            maya_interval: (
                (
                    reduced[:-1] + maya_interval.combine(reduced[-1])
                ) if reduced else [
                    maya_interval
                ]
            ),
            sorted(interval_list),
            [],
        )

    @classmethod
    def from_datetime(cls, start_dt=None, end_dt=None, duration=None):
        start = MayaDT.from_datetime(start_dt) if start_dt else None
        end = MayaDT.from_datetime(end_dt) if end_dt else None
        return cls(start=start, end=end, duration=duration)


def now():
    """Returns a MayaDT instance for this exact moment."""
    epoch = time.time()
    return MayaDT(epoch=epoch)


def when(string, timezone='UTC', prefer_dates_from='current_period'):
    """"Returns a MayaDT instance for the human moment specified.

    Powered by dateparser. Useful for scraping websites.

    Examples:
        'next week', 'now', 'tomorrow', '300 years ago', 'August 14, 2015'

    Keyword Arguments:
        string -- string to be parsed
        timezone -- timezone referenced from (default: 'UTC')
        prefer_dates_from -- what dates are prefered when `string` is ambigous.
                             options are 'past', 'future', and 'current_period'
                             (default: 'current_period'). see: [1]

    Reference:
        [1] dateparser.readthedocs.io/en/latest/usage.html#handling-incomplete-dates
    """
    settings = {
        'TIMEZONE': timezone,
        'RETURN_AS_TIMEZONE_AWARE': True,
        'TO_TIMEZONE': 'UTC',
        'PREFER_DATES_FROM': prefer_dates_from,
    }

    dt = dateparser.parse(string, settings=settings)
    if dt is None:
        raise ValueError('invalid datetime input specified.')

    return MayaDT.from_datetime(dt)


def parse(string, timezone='UTC', day_first=False, year_first=True, strict=False):
    """"Returns a MayaDT instance for the machine-produced moment specified.

    Powered by pendulum.
    Accepts most known formats. Useful for working with data.

    Keyword Arguments:
        string -- string to be parsed
        timezone -- timezone referenced from (default: 'UTC')
        day_first -- if true, the first value (e.g. 01/05/2016)
                     is parsed as day.
                     if year_first is set to True, this distinguishes
                     between YDM and YMD. (default: False)
        year_first -- if true, the first value (e.g. 2016/05/01)
                      is parsed as year (default: True)
        strict -- if False, allow pendulum to fall back on datetime parsing
                  if pendulum's own parsing fails
    """
    options = {}
    options['tz'] = timezone
    options['day_first'] = day_first
    options['year_first'] = year_first
    options['strict'] = strict

    dt = pendulum.parse(str(string), **options)
    return MayaDT.from_datetime(dt)


def _seconds_or_timedelta(duration):
    """Returns `datetime.timedelta` object for the passed duration.

    Keyword Arguments:
        duration -- `datetime.timedelta` object or seconds in `int` format.
    """
    if isinstance(duration, int):
        dt_timedelta = timedelta(seconds=duration)
    elif isinstance(duration, timedelta):
        dt_timedelta = duration
    else:
        raise TypeError(
            'Expects argument as `datetime.timedelta` object '
            'or seconds in `int` format'
        )

    return dt_timedelta


def _translate(dt, target_locale):
    en = default_loader.get_locale("en")
    target = default_loader.get_locale(target_locale)
    naturaldate = humanize.naturaldate(dt)

    base = en.translate(naturaldate, settings=dateparser.conf.settings)

    return target.info["relative-type"][base][-1]


def intervals(start, end, interval):
    """
    Yields MayaDT objects between the start and end MayaDTs given,
    at a given interval (seconds or timedelta).
    """
    interval = _seconds_or_timedelta(interval)
    current_timestamp = start
    while current_timestamp.epoch < end.epoch:
        yield current_timestamp

        current_timestamp = current_timestamp.add(
            seconds=interval.total_seconds()
        )
