
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

    def __init__(self, epoch, timezone='UTC'):
        super(MayaDT, self).__init__()
        self._timezone = timezone
        self._epoch = epoch

    def __repr__(self):
        return '<MayaDT epoch={}>'.format(self._epoch)

    def datetime(self):
        dt = Datetime.fromtimestamp(self._epoch)
        return dt.replace(tzinfo=self.timezone)

    @property
    def year(self):
        self.datetime().year

    @property
    def month(self):
        self.datetime().month

    @property
    def day(self):
        self.datetime().day

    @property
    def hour(self):
        self.datetime().hour

    @property
    def minute(self):
        self.datetime().minute

    @property
    def second(self):
        self.datetime().second

    @property
    def microsecond(self):
        self.datetime().microsecond

    @property
    def timezone(self):
        return pytz.timezone(self._timezone)

    def iso8601(self):
        return '{}Z'.format(self.datetime().isoformat())

    def epoch(self):
        return self._epoch

    def human_date(self):
        return humanize.naturaldate(self.datetime())

    def human_time(self):
        return humanize.naturaldate(self.datetime())

    def rfc2822(self):
        tt = self.datetime().timetuple()
        ts = time.mktime(tt)
        return email.utils.formatdate(ts)


    def adjust(adjustment, positive=True):
        pass


def now():
    """Returns MayaDT for right now."""
    epoch = time.time()
    return MayaDT(epoch=epoch)

def when(string, timezone='UTC'):
    dt = dateparser.parse(string, settings={'TIMEZONE': timezone})
    if dt is None:
        raise ValueError('invalid datetime input specified.')
    epoch = (dt - Datetime(*__epoch_start)).total_seconds()
    return MayaDT(epoch)