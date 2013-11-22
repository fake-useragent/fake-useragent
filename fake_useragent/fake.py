import random

from fake_useragent import settings
from fake_useragent.utils import load_cached, load, update


class UserAgent(object):
    def __init__(self, cache=True):
        super(UserAgent, self).__init__()

        if cache:
            self.data = load_cached()
        else:
            self.data = load()

        self.cache = cache

    def update(self, cache=None):
        if cache is None:
            cache = self.cache

        if self.cache:
            update()

        self.__init__(cache=cache)

    def __getitem__(self, attr):
        return self.__getattr__(attr)

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
        elif attr == 'googlechrome':
            attr = 'chrome'
        elif attr == 'ff':
            attr = 'firefox'

        try:
            return self.data['browsers'][attr][
                random.randint(0, settings.BROWSERS_COUNT_LIMIT - 1)
            ]
        except KeyError:
            return None
