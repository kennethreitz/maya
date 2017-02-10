
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
import pendulum
from tzlocal import get_localzone

_EPOCH_START = (1970, 1, 1)


def validate_class_type_arguments(operator):
    """
    Decorator to validate all the arguments to function
    are of the type of calling class
    """

    def inner(function):
        def wrapper(self, *args, **kwargs):
            for arg in args + tuple(kwargs.values()):
                if not isinstance(arg, self.__class__):
                    raise TypeError('unorderable types: {}() {} {}()'.format(
                        type(self).__name__, operator, type(arg).__name__))
            return function(self, *args, **kwargs)

        return wrapper

    return inner



class MayaDT(object):
    """The Maya Datetime object."""

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
        return self._epoch == maya_dt._epoch

    @validate_class_type_arguments('!=')
    def __ne__(self, maya_dt):
        return self._epoch != maya_dt._epoch

    @validate_class_type_arguments('<')
    def __lt__(self, maya_dt):
        return self._epoch < maya_dt._epoch

    @validate_class_type_arguments('<=')
    def __le__(self, maya_dt):
        return self._epoch <= maya_dt._epoch

    @validate_class_type_arguments('>')
    def __gt__(self, maya_dt):
        return self._epoch > maya_dt._epoch

    @validate_class_type_arguments('>=')
    def __ge__(self, maya_dt):
        return self._epoch >= maya_dt._epoch

    def add(self, **kwargs):
        """"Returns a new MayaDT object with the given offsets."""
        return self.from_datetime(pendulum.instance(self.datetime()).add(**kwargs))

    def subtract(self, **kwargs):
        """"Returns a new MayaDT object with the given offsets."""
        return self.from_datetime(pendulum.instance(self.datetime()).subtract(**kwargs))

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
        return parse(string)

    @staticmethod
    def from_rfc2822(string):
        """Returns MayaDT instance from rfc2822 string."""
        return parse(string)

    @staticmethod
    def from_rfc3339(string):
        """Returns MayaDT instance from rfc3339 string."""
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
        return self.datetime().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]+"Z"

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
    def week(self):
        return self.datetime().isocalendar()[1]

    @property
    def weekday(self):
        """Return the day of the week as an integer. Monday is 1 and Sunday is 7"""
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
        return self._epoch

    # Human Slang Extras
    # ------------------

    def slang_date(self):
        """"Returns human slang representation of date."""
        dt = self.datetime(naive=True, to_timezone=self.local_timezone)
        return humanize.naturaldate(dt)

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

    Powered by pendulum. Accepts most known formats. Useful for working with data.

    Keyword Arguments:
        string -- string to be parsed
        day_first -- if true, the first value (e.g. 01/05/2016) is parsed as day (default: False)
    """
    dt = pendulum.parse(string, day_first=day_first)
    return MayaDT.from_datetime(dt)
