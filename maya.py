
# ___  __  ___  _  _  ___
# || \/ | ||=|| \\// ||=||
# ||    | || ||  //  || ||

# Ignore warnings for yaml usage.
import warnings
import ruamel.yaml
warnings.simplefilter('ignore', ruamel.yaml.error.UnsafeLoaderWarning)


import email.utils
import time
from datetime import datetime as Datetime

import pytz
import humanize
import dateparser
import iso8601
import dateutil.parser
from tzlocal import get_localzone

_EPOCH_START = (1970, 1, 1)


def validate_type_mayadt(func):
    """
    Decorator to validate all the arguments to function
    are of type `MayaDT`
    """
    def inner(*args, **kwargs):
        for arg in args + tuple(kwargs.values()):
            if not isinstance(arg, MayaDT):
                raise ValueError("Operation allowed only on object of type '{}'".format(MayaDT.__name__))
        return func(*args, **kwargs)
    return inner


class MayaDT(object):
    """The Maya Datetime object."""

    __slots__ = ('_epoch', '_datetime')

    def __init__(self, epoch):
        super(MayaDT, self).__init__()
        self._epoch = epoch
        self._datetime = Datetime.utcfromtimestamp(self._epoch).replace(tzinfo=self._tz)

    def __repr__(self):
        return '<MayaDT epoch={}>'.format(self._epoch)

    def __format__(self, *args, **kwargs):
        """Return's the datetime's format"""
        return format(self._datetime, *args, **kwargs)

    @validate_type_mayadt
    def __eq__(self, maya_dt):
        return self._epoch == maya_dt._epoch

    @validate_type_mayadt
    def __ne__(self, maya_dt):
        return not self.__eq__(maya_dt)

    @validate_type_mayadt
    def __lt__(self, maya_dt):
        return self._epoch < maya_dt._epoch

    @validate_type_mayadt
    def __le__(self, maya_dt):
        return self.__lt__(maya_dt) or self.__eq__(maya_dt)

    @validate_type_mayadt
    def __gt__(self, maya_dt):
        return self._epoch > maya_dt._epoch

    @validate_type_mayadt
    def __ge__(self, maya_dt):
        return self.__gt__(maya_dt) or self.__eq__(maya_dt)


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
        """Returns the name of the local timezone, for informational purposes."""
        return self._local_tz.zone

    @property
    def _local_tz(self):
        """Returns the local timezone."""
        return get_localzone()

    @staticmethod
    def __dt_to_epoch(dt):
        """Converts a datetime into an epoch."""

        # Assume UTC if no datetime is provided.
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=pytz.utc)

        epoch_start = Datetime(*_EPOCH_START, tzinfo=pytz.timezone('UTC'))
        return (dt - epoch_start).total_seconds()

    # Importers
    # ---------

    @classmethod
    def from_datetime(klass, dt):
        """Returns MayaDT instance from datetime."""
        return klass(klass.__dt_to_epoch(dt))

    @classmethod
    def from_iso8601(klass, string):
        """Returns MayaDT instance from iso8601 string."""
        dt = iso8601.parse_date(string)
        return klass.from_datetime(dt)

    @staticmethod
    def from_rfc2822(string):
        """Returns MayaDT instance from rfc2822 string."""
        return parse(string)

    # Exporters
    # ---------

    def datetime(self, to_timezone=None, naive=False):
        """Returns a timezone-aware datetime...
        Defaulting to UTC (as it should).

        Keyword Arguments:
            to_timezone {string} -- timezone to convert to (default: None/UTC)
            naive {boolean} -- if True, the tzinfo is simply dropped (default: False)
        """
        if to_timezone:
            dt = self._datetime.astimezone(pytz.timezone(to_timezone))
        else:
            dt = self._datetime

        # Strip the timezone info if requested to do so.
        if naive:
            return dt.replace(tzinfo=None)
        else:
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=self._tz)

        return dt

    def iso8601(self):
        """Returns an ISO 8601 representation of the MayaDT."""
        # Get a timezone-naive datetime.
        dt = self.datetime(naive=True)
        return '{}Z'.format(dt.isoformat())

    def rfc2822(self):
        """Returns an RFC 2822 representation of the MayaDT."""
        return email.utils.formatdate(self.epoch, usegmt=True)

    # Properties
    # ----------

    @property
    def year(self):
        return self._datetime.year

    @property
    def month(self):
        return self._datetime.month

    @property
    def day(self):
        return self._datetime.day

    @property
    def week(self):
        return self._datetime.isocalendar()[1]

    @property
    def weekday(self):
        """Return the day of the week as an integer. Monday is 1 and Sunday is 7"""
        return self._datetime.isoweekday()

    @property
    def hour(self):
        return self._datetime.hour

    @property
    def minute(self):
        return self._datetime.minute

    @property
    def second(self):
        return self._datetime.second

    @property
    def microsecond(self):
        return self._datetime.microsecond

    @property
    def epoch(self):
        return self._epoch

    # Human Slang Extras
    # ------------------

    def slang_date(self):
        """"Returns human slang representation of date."""
        return humanize.naturaldate(self._datetime)

    def slang_time(self):
        """"Returns human slang representation of time."""
        dt = self.datetime(naive=True, to_timezone=self.local_timezone)
        return humanize.naturaltime(dt)


def now():
    """Returns a MayaDT instance for this exact moment."""
    epoch = time.time()
    return MayaDT(epoch=epoch)


def when(string, timezone='UTC'):
    """"Returns a MayaDT instance for the human moment specified.

    Powered by dateparser. Useful for scraping websites.

    Examples:
        'next week', 'now', 'tomorrow', '300 years ago', 'August 14, 2015'

    Keyword Arguments:
        string -- string to be parsed
        timezone -- timezone referenced from (default: 'UTC')

    """
    dt = dateparser.parse(string, settings={'TIMEZONE': timezone, 'RETURN_AS_TIMEZONE_AWARE': True, 'TO_TIMEZONE': 'UTC'})

    if dt is None:
        raise ValueError('invalid datetime input specified.')

    return MayaDT.from_datetime(dt)


def parse(string, day_first=False):
    """"Returns a MayaDT instance for the machine-produced moment specified.

    Powered by dateutil. Accepts most known formats. Useful for working with data.

    Keyword Arguments:
        string -- string to be parsed
        day_first -- if true, the first value (e.g. 01/05/2016) is parsed as day (default: False)
    """
    dt = dateutil.parser.parse(string, dayfirst=day_first)
    return MayaDT.from_datetime(dt)
