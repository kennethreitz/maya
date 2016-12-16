
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

import dateparser

class MayaDT(object):
    """The Maya Datetime object."""
    def __init__(self, epoch):
        super(MayaDT, self).__init__()
        self._epoch = epoch

    def __repr__(self):
        return '<MayaDT epoch={}>'.format(self._epoch)

    def datetime(self):
        return Datetime.fromtimestamp(self._epoch)

    def iso8601(self):
        return '{}Z'.format(self.datetime().isoformat())

    def epoch(self):
        return self._epoch

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

def when(string):
    dt = dateparser.parse(string)
    if dt is None:
        raise ValueError('invalid datetime input specified.')
    epoch = (dt - Datetime(1970, 1, 1)).total_seconds()
    return MayaDT(epoch)