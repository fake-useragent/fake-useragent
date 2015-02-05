import random

from . import settings
from .utils import load, load_cached, update


class UserAgent(object):
    def __init__(self, cache=True):
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
        for replacement in settings.REPLACEMENTS:
            attr = attr.replace(replacement, '')

        attr = attr.lower()

        if attr == 'random':
            attr = self.data['randomize'][
                str(random.randint(0, len(self.data['randomize']) - 1))
            ]
        else:
            for shortcut, value in settings.SHORTCUTS:
                if attr == shortcut:
                    attr = value
                    break

        try:
            return self.data['browsers'][attr][
                random.randint(
                    0, len(self.data['browsers'][attr]) - 1
                )
            ]
        except KeyError:
            return None
