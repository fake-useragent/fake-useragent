from __future__ import absolute_import, unicode_literals

import random

from fake_useragent import settings
from fake_useragent.utils import load, load_cached, update


class UserAgent(object):
    def __init__(self, cache=True):
        self.cache = cache

        self.load()

    def load(self):
        if self.cache:
            self.data = load_cached()
        else:
            self.data = load()

    def update(self, cache=None):
        if cache is not None:
            self.cache = cache

        if self.cache:
            update()

        self.load()

    def __getitem__(self, attr):
        return self.__getattr__(attr)

    def __getattr__(self, attr):
        for value, replacement in settings.REPLACEMENTS.items():
            attr = attr.replace(value, replacement)

        attr = attr.lower()

        if attr == 'random':
            attr = self.data['randomize'][
                str(random.randint(0, len(self.data['randomize']) - 1))
            ]
        else:
            if attr in settings.SHORTCUTS:
                attr = settings.SHORTCUTS[attr]

        try:
            return self.data['browsers'][attr][
                random.randint(
                    0, len(self.data['browsers'][attr]) - 1
                )
            ]
        except KeyError:
            return None
