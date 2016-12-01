from __future__ import absolute_import, unicode_literals

import logging
import random
from threading import Lock

from fake_useragent import settings
from fake_useragent.errors import FakeUserAgentError
from fake_useragent.utils import load, load_cached, str_types, update


logger = logging.getLogger(__name__)


class FakeUserAgent(object):
    def __init__(self, cache=True, path=settings.DB, fallback=None):
        self.cache = cache
        self.path = path

        if fallback is not None:
            assert isinstance(fallback, str_types), \
                'fallback must be string or unicode'

        self.fallback = fallback

        # initial empty data
        self.data = {}
        self.data_randomize = []
        self.data_browsers = {}

        self.load()

    def load(self):
        try:
            with self.load.lock:
                if self.cache:
                    self.data = load_cached(self.path)
                else:
                    self.data = load()

                # TODO: change source file format
                # version 0.1.4- migration tool
                self.data_randomize = list(self.data['randomize'].values())
                self.data_browsers = self.data['browsers']
        except FakeUserAgentError as exc:
            if self.fallback is None:
                logger.error(
                    'Error occurred during fetching data...',
                    exc_info=exc,
                )

                raise
            else:
                logger.warning(
                    'Error occurred but was suppressed with fallback...',
                    exc_info=exc,
                )
    load.lock = Lock()

    def update(self, cache=None):
        with self.update.lock:
            if cache is not None:
                self.cache = cache

            if self.cache:
                update(self.path)

            self.load()
    update.lock = Lock()

    def __getitem__(self, attr):
        return self.__getattr__(attr)

    def __getattr__(self, attr):
        try:
            for value, replacement in settings.REPLACEMENTS.items():
                attr = attr.replace(value, replacement)

            attr = attr.lower()

            if attr == 'random':
                browser = random.choice(self.data_randomize)
            else:
                browser = settings.SHORTCUTS.get(attr, attr)

            return random.choice(self.data_browsers[browser])
        except (KeyError, IndexError) as exc:
            if self.fallback is None:
                logger.error(
                    'Error occurred during getting browser...',
                    exc_info=exc,
                )

                raise FakeUserAgentError
            else:
                logger.warning(
                    'Error occurred but was suppressed with fallback...',
                    exc_info=exc,
                )

                return self.fallback


# common alias
UserAgent = FakeUserAgent
