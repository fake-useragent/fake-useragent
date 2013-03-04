import os
import random
try:
    import json
except ImportError:
    import simplejson as json
from fake_useragent import settings
from fake_useragent.build import build_db


class UserAgent(object):
    def __init__(self):
        super(UserAgent, self).__init__()

        # check db json file exists
        if not os.path.isfile(settings.DB):
            build_db()

        # no codecs\with for python 2.5
        f = open(settings.DB, 'r')
        self.data = json.loads(f.read())
        f.close()

    def __getattr__(self, attr):
        attr = attr.replace(' ', '').replace('_', '').lower()

        if attr == 'random':
            attr = self.data['randomize'][
                str(random.randint(0, self.data['max_random'] - 1))
            ]
        elif attr == 'ie':
            attr = 'internetexplorer'
        elif attr == 'msie':
            attr = 'internetexplorer'
        elif attr == 'google':
            attr = 'chrome'
        elif attr == 'ff':
            attr = 'firefox'

        return self.data['browsers'][attr][
            random.randint(0, settings.BROWSERS_COUNT_LIMIT - 1)
        ]
