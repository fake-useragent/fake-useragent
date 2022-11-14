import os
from functools import partial

import unittest
from unittest.mock import patch
import pytest

from fake_useragent import (
    VERSION,
    FakeUserAgent,
    FakeUserAgentError,
    UserAgent,
    settings,
)
from tests.utils import _request


class TestFake(unittest.TestCase):
    def setUp(self):
        try:
            os.remove(settings.DB)
        except OSError:
            pass

    def tearDown(self):
        try:
            os.remove(settings.DB)
        except OSError:
            pass

    def _probe(self, ua):
        ua.ie
        ua.msie
        ua.internetexplorer
        ua.internet_explorer
        ua["internet explorer"]
        ua.edge
        ua.google
        ua.chrome
        ua.googlechrome
        ua.google_chrome
        ua["google chrome"]
        ua.firefox
        ua.ff
        ua.safari
        ua.random
        ua["random"]
        ua.edge

    def test_fake_user_agent_browsers(self):
        ua = UserAgent()

        _probe(ua)

        with pytest.raises(FakeUserAgentError):
            ua.non_existing

        with pytest.raises(FakeUserAgentError):
            ua["non_existing"]

        data1 = ua.data_browsers

        # Will no do much by default
        ua.update()

        data2 = ua.data_browsers

        assert data1 == data2

        assert data1 is not data2

    def test_fake_user_agent_path(self, path):
        assert not os.path.isfile(path)

        ua = UserAgent(tmp_path=path, use_external_data=True)

        assert path == ua.tmp_path

        assert os.path.isfile(path)

    def test_fake_default_path(self):
        assert not os.path.isfile(settings.DB)

        ua = UserAgent(use_external_data=True)

        assert settings.DB == ua.tmp_path

        assert os.path.isfile(settings.DB)

    def test_fake_fallback(self):
        fallback = "Foo Browser"

        denied_urls = [
            "https://useragentstring.com",
        ]

        with patch(
            "fake_useragent.utils.Request",
            side_effect=partial(_request, denied_urls=denied_urls),
        ):
            # Raise error
            ua = self.assertRaises(FakeUserAgentError, UserAgent, fallback=fallback)

        assert ua.random == fallback

        assert ua.ie == fallback

    def test_fake_no_fallback(self):
        denied_urls = [
            "https://useragentstring.com",
        ]

        with patch(
            "fake_useragent.utils.Request",
            side_effect=partial(_request, denied_urls=denied_urls),
        ):
            with pytest.raises(FakeUserAgentError):
                UserAgent()

    def test_fake_update(self):
        ua = UserAgent(use_external_data=True)

        ua.update()

        _probe(ua)

    def test_fake_update_cache(self, path):
        assert not os.path.isfile(path)

        ua = UserAgent(tmp_path=path, use_external_data=True)

        assert not os.path.isfile(path)

        with pytest.raises(AssertionError):
            ua.update(cache="y")

        ua.update(cache=True)

        assert os.path.isfile(path)

        _probe(ua)

    def test_fake_update_use_external_data(self):
        ua = UserAgent(use_external_data=True)

        denied_urls = [
            "https://useragentstring.com",
        ]

        with patch(
            "fake_useragent.utils.Request",
            side_effect=partial(_request, denied_urls=denied_urls),
        ):
            ua.update()

            _probe(ua)

        denied_urls = [
            "https://useragentstring.com",
        ]

        with patch(
            "fake_useragent.utils.Request",
            side_effect=partial(_request, denied_urls=denied_urls),
        ):
            with pytest.raises(FakeUserAgentError):
                ua.update()

    def test_fake_use_external_data(self):
        denied_urls = [
            "https://useragentstring.com",
        ]

        with patch(
            "fake_useragent.utils.Request",
            side_effect=partial(_request, denied_urls=denied_urls),
        ):
            ua = UserAgent(cache=False, use_external_data=True)

        _probe(ua)

    def test_fake_external_data_boolean(self):
        with pytest.raises(AssertionError):
            UserAgent(use_external_data="y")

    def test_fake_path_str_types(self):
        with pytest.raises(AssertionError):
            UserAgent(tmp_path=10)

    def test_fake_fallback_str_types(self):
        with pytest.raises(AssertionError):
            UserAgent(fallback=True)

    def test_fake_safe_attrs_iterable_str_types(self):
        with pytest.raises(AssertionError):
            UserAgent(safe_attrs={})

        with pytest.raises(AssertionError):
            UserAgent(safe_attrs=[66])

    def test_fake_safe_attrs(self):
        ua = UserAgent(safe_attrs=("__injections__",))

        with pytest.raises(AttributeError):
            ua.__injections__

    def test_fake_version(self):
        assert VERSION == settings.__version__

    def test_fake_aliases(self):
        assert FakeUserAgent is UserAgent
