# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import random
from threading import Lock
from .settings import BROWSERS_NAMES
from fake_useragent import settings
from fake_useragent.errors import FakeUserAgentError
from fake_useragent.log import logger
from fake_useragent.utils import load, load_cached, update


class FakeUserAgent(object):
    def __init__(
        self,
        cache=False,
        use_fallback=True,
        path=settings.DB,
        fallback=None,
    ):
        assert isinstance(cache, bool), \
            'cache must be True or False'

        self.cache = cache

        assert isinstance(use_fallback, bool), \
            'use_fallback must be True or False'

        self.use_fallback = use_fallback

        if fallback is not None:
            assert isinstance(fallback, str), \
                'fallback must be string or unicode'

        self.fallback = fallback

        # initial empty data
        self.data = None

        self.load()

    def load(self):
        try:
            with self.load.lock:
                # TODO : rewrite cache and update
                if self.cache:
                    self.data = load_cached(
                        self.path,
                        use_cache_server=self.use_cache_server,
                        verify_ssl=self.verify_ssl,
                    )
                else:
                    self.data = load(
                        use_fallback=self.use_fallback,
                    )
        except FakeUserAgentError:
            if self.fallback is None:
                raise
            else:
                logger.warning(
                    'Error occurred during fetching data, '
                    'but was suppressed with fallback.',
                )
    load.lock = Lock()

    # def update(self, cache=None):
    #     with self.update.lock:
    #         if cache is not None:
    #             assert isinstance(cache, bool), \
    #                 'cache must be True or False'

    #             self.cache = cache

    #         if self.cache:
    #             update(
    #                 self.path,
    #                 use_cache_server=self.use_cache_server,
    #                 verify_ssl=self.verify_ssl,
    #             )

    #         self.load()
    # update.lock = Lock()

    def __getitem__(self, attr):
        return self.__getattr__(attr)

    def __getattr__(self, attr):
        try:
            for value, replacement in settings.REPLACEMENTS.items():
                attr = attr.replace(value, replacement)

            attr = attr.lower()

            if attr == 'random':
                return self.data.randomize()
            else:
                browser = settings.SHORTCUTS.get(attr, attr)
                return random.choice(self.data.useragents[browser])
        except (KeyError, IndexError):
            if self.fallback is None:
                raise FakeUserAgentError('Error occurred during getting browser')  # noqa
            else:
                logger.warning(
                    'Error occurred during getting browser, '
                    'but was suppressed with fallback.',
                )

                return self.fallback


# common alias
UserAgent = FakeUserAgent
