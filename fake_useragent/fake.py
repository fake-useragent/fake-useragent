# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import random
from threading import Lock

from fake_useragent import settings
from fake_useragent.errors import FakeUserAgentError
from fake_useragent.log import logger
from fake_useragent.utils import load, load_cached, str_types, update


class FakeUserAgent(object):
    def __init__(
        self,
        cache=True,
        use_cache_server=True,
        path=settings.DB,
        fallback=None,
        verify_ssl=True,
        safe_attrs=tuple(),
    ):
        assert isinstance(cache, bool), \
            'cache must be True or False'

        self.cache = cache

        assert isinstance(use_cache_server, bool), \
            'use_cache_server must be True or False'

        self.use_cache_server = use_cache_server

        assert isinstance(path, str_types), \
            'path must be string or unicode'

        self.path = path

        if fallback is not None:
            assert isinstance(fallback, str_types), \
                'fallback must be string or unicode'

        self.fallback = fallback

        assert isinstance(verify_ssl, bool), \
            'verify_ssl must be True or False'

        self.verify_ssl = verify_ssl

        assert isinstance(safe_attrs, (list, set, tuple)), \
            'safe_attrs must be list\\tuple\\set of strings or unicode'

        if safe_attrs:
            str_types_safe_attrs = [
                isinstance(attr, str_types) for attr in safe_attrs
            ]

            assert all(str_types_safe_attrs), \
                'safe_attrs must be list\\tuple\\set of strings or unicode'

        self.safe_attrs = set(safe_attrs)

        # initial empty data
        self.data = {}
        # TODO: change source file format
        # version 0.1.4+ migration tool
        self.data_randomize = []
        self.data_browsers = {}

        self.load()

    def load(self):
        try:
            with self.load.lock:
                if self.cache:
                    self.data = load_cached(
                        self.path,
                        use_cache_server=self.use_cache_server,
                        verify_ssl=self.verify_ssl,
                    )
                else:
                    self.data = load(
                        use_cache_server=self.use_cache_server,
                        verify_ssl=self.verify_ssl,
                    )

                # TODO: change source file format
                # version 0.1.4+ migration tool
                self.data_randomize = list(self.data['randomize'].values())
                self.data_browsers = self.data['browsers']
        except FakeUserAgentError:
            if self.fallback is None:
                raise
            else:
                logger.warning(
                    'Error occurred during fetching data, '
                    'but was suppressed with fallback.',
                )
    load.lock = Lock()

    def update(self, cache=None):
        with self.update.lock:
            if cache is not None:
                assert isinstance(cache, bool), \
                    'cache must be True or False'

                self.cache = cache

            if self.cache:
                update(
                    self.path,
                    use_cache_server=self.use_cache_server,
                    verify_ssl=self.verify_ssl,
                )

            self.load()
    update.lock = Lock()

    def __getitem__(self, attr):
        return self.__getattr__(attr)

    def __getattr__(self, attr):
        if attr in self.safe_attrs:
            return super(UserAgent, self).__getattr__(attr)

        try:
            for value, replacement in settings.REPLACEMENTS.items():
                attr = attr.replace(value, replacement)

            attr = attr.lower()

            if attr == 'random':
                browser = random.choice(self.data_randomize)
            else:
                browser = settings.SHORTCUTS.get(attr, attr)

            return random.choice(self.data_browsers[browser])
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
