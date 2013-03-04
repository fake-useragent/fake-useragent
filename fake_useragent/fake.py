import random
try:
    import json
except ImportError:
    import simplejson as json
from fake_useragent import settings
from fake_useragent.utils import load_cached, load


class UserAgent(object):
    def __init__(self, cache=True):
        super(UserAgent, self).__init__()

        if cache:
            self.data = load_cached()
        else:
            self.data = load()

    def __getattr__(self, attr):
        attr = attr.replace(' ', '').replace('_', '').lower()

        if attr == 'random':
            attr = self.data['randomize'][
                str(random.randint(0, len(self.data['randomize']) - 1))
            ]
        elif attr == 'ie':
            attr = 'internetexplorer'
        elif attr == 'msie':
            attr = 'internetexplorer'
        elif attr == 'google':
            attr = 'chrome'
        elif attr == 'ff':
            attr = 'firefox'

        try:
            return self.data['browsers'][attr][
                random.randint(0, settings.BROWSERS_COUNT_LIMIT - 1)
            ]
        except KeyError:
            return None
