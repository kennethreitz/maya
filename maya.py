
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

__epoch_start = (1970, 1, 1)

class MayaDT(object):
    """The Maya Datetime object."""

    def __init__(self, epoch):
        super(MayaDT, self).__init__()
        self._epoch = epoch

    def __repr__(self):
        return '<MayaDT epoch={}>'.format(self._epoch)

    def datetime(self, to_timezone=None):

        # self.timezone.localize(dt)

        if to_timezone:

            return self.datetime().astimezone(pytz.timezone(to_timezone))

        dt = Datetime.utcfromtimestamp(self._epoch)
        return dt.replace(tzinfo=self.timezone)


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
    def timezone(self):
        return pytz.timezone('UTC')

    def iso8601(self):
        return '{}Z'.format(self.datetime().isoformat())

    def epoch(self):
        return self._epoch

    def slang_date(self):
        return humanize.naturaldate(self.datetime())

    def slang_time(self):
        return humanize.naturaldate(self.datetime())

    def rfc2822(self):
        tt = self.datetime().timetuple()
        ts = time.mktime(tt)
        return email.utils.formatdate(ts)


def now():
    """Returns MayaDT for right now."""
    epoch = time.time()
    return MayaDT(epoch=epoch)

def when(string, timezone='UTC'):
    dt = dateparser.parse(string, settings={'TIMEZONE': timezone, 'RETURN_AS_TIMEZONE_AWARE': True, 'TO_TIMEZONE': 'UTC'})

    if dt is None:
        raise ValueError('invalid datetime input specified.')

    epoch_start = Datetime(*__epoch_start, tzinfo=pytz.timezone('UTC'))
    epoch = (dt - epoch_start).total_seconds()

    return MayaDT(epoch)
