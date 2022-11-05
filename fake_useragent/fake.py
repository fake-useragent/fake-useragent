import random
from threading import Lock

from fake_useragent import settings
from fake_useragent.errors import FakeUserAgentError
from fake_useragent.log import logger
from fake_useragent.utils import load, load_cached, str_types, update


class FakeUserAgent:
    def __init__(
        self,
        cache=True,
        use_cache_server=True,
        path=settings.DB,
        fallback=None,
        browsers=["chrome", "edge", "internet explorer", "firefox", "safari", "opera"],
        verify_ssl=True,
        safe_attrs=tuple(),
    ):
        assert isinstance(cache, bool), "cache must be True or False"

        self.cache = cache

        assert isinstance(
            use_cache_server, bool
        ), "use_cache_server must be True or False"

        self.use_cache_server = use_cache_server

        assert isinstance(path, str_types), "path must be string or unicode"

        self.path = path

        if fallback is not None:
            assert isinstance(fallback, str_types), "fallback must be string or unicode"

        self.fallback = fallback

        assert isinstance(browsers, (list, str)), "browsers must be list or string"

        self.browsers = browsers

        assert isinstance(verify_ssl, bool), "verify_ssl must be True or False"

        self.verify_ssl = verify_ssl

        assert isinstance(
            safe_attrs, (list, set, tuple)
        ), "safe_attrs must be list\\tuple\\set of strings or unicode"

        if safe_attrs:
            str_types_safe_attrs = [isinstance(attr, str_types) for attr in safe_attrs]

            assert all(
                str_types_safe_attrs
            ), "safe_attrs must be list\\tuple\\set of strings or unicode"

        self.safe_attrs = set(safe_attrs)

        # initial empty data
        self.data_browsers = {}

        self.load()

    def load(self):
        try:
            with self.load.lock:
                if self.cache:
                    self.data_browsers = load_cached(
                        self.path,
                        self.browsers,
                        use_cache_server=self.use_cache_server,
                        verify_ssl=self.verify_ssl,
                    )
                else:
                    self.data_browsers = load(
                        self.browsers,
                        use_cache_server=self.use_cache_server,
                        verify_ssl=self.verify_ssl,
                    )
        except FakeUserAgentError:
            if self.fallback is None:
                raise
            else:
                logger.warning(
                    "Error occurred during fetching data, "
                    "but was suppressed with fallback.",
                )

    load.lock = Lock()

    def update(self, cache=None):
        with self.update.lock:
            if cache is not None:
                assert isinstance(cache, bool), "cache must be True or False"

                self.cache = cache

            if self.cache:
                update(
                    self.path,
                    self.browsers,
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

            if attr == "random":
                # Pick a random browser from the browsers argument list
                browser_name = random.choice(self.browsers)
            else:
                browser_name = settings.SHORTCUTS.get(attr, attr)

            # Pick a random user-agent string for a specific browser
            return random.choice(self.data_browsers[browser_name])
        except (KeyError, IndexError):
            if self.fallback is None:
                raise FakeUserAgentError(
                    f"Error occurred during getting browser: {attr}"
                )  # noqa
            else:
                logger.warning(
                    f"Error occurred during getting browser: {attr}, "
                    "but was suppressed with fallback.",
                )

                return self.fallback


# common alias
UserAgent = FakeUserAgent
