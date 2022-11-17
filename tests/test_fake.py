import os
import urllib
from urllib import request
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

        try:
            os.remove("/tmp/custom.json")
        except OSError:
            pass

    def tearDown(self):
        try:
            os.remove(settings.DB)
        except OSError:
            pass

        try:
            os.remove("/tmp/custom.json")
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

    def test_fake_init(self):
        ua = UserAgent()

        self.assertTrue(ua.chrome)
        self.assertIsInstance(ua.chrome, str)
        self.assertTrue(ua.edge)
        self.assertIsInstance(ua.edge, str)
        self.assertTrue(ua["internet explorer"])
        self.assertIsInstance(ua["internet explorer"], str)
        self.assertTrue(ua.firefox)
        self.assertIsInstance(ua.firefox, str)
        self.assertTrue(ua.safari)
        self.assertIsInstance(ua.safari, str)
        self.assertTrue(ua.opera)
        self.assertIsInstance(ua.opera, str)
        self.assertTrue(ua.random)
        self.assertIsInstance(ua.random, str)

    def test_fake_user_agent_browsers(self):
        ua = UserAgent()

        self._probe(ua)

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

    def test_fake_default_path(self):
        assert not os.path.isfile(settings.DB)

        data = open("tests/assets/chrome.html", "r", encoding="utf-8")
        with patch.object(urllib.request, "urlopen", return_value=data):
            ua = UserAgent(use_external_data=True, browsers=["chrome"])

        assert settings.DB == ua.cache_path

        assert os.path.isfile(settings.DB)

    def test_fake_fallback(self):
        fallback = "Foo Browser"

        denied_urls = [
            "https://useragentstring.com",
        ]

        with patch.object(
            request,
            "Request",
            side_effect=partial(_request, denied_urls=denied_urls),
        ):
            # This should trigger an error internally (since the site url is denied), causing to call the fallback string
            ua = UserAgent(use_external_data=True, fallback=fallback)

        assert ua.random == fallback

        assert ua.ie == fallback

    def test_fake_no_fallback(self):
        denied_urls = [
            "https://useragentstring.com",
        ]

        with patch.object(
            request,
            "Request",
            side_effect=partial(_request, denied_urls=denied_urls),
        ):
            # Since the website is denied and we didn't specify a fallback string,
            # this should raise an error
            with pytest.raises(FakeUserAgentError):
                UserAgent(use_external_data=True)

    def test_fake_update_external(self):
        data = open("tests/assets/chrome.html", "r", encoding="utf-8")
        with patch.object(urllib.request, "urlopen", return_value=data):
            ua = UserAgent(use_external_data=True, browsers=["chrome"])

        # Open the chrome.html file for 2nd time, for the update()
        data = open("tests/assets/chrome.html", "r", encoding="utf-8")
        with patch.object(urllib.request, "urlopen", return_value=data):
            ua.update()

        self.assertTrue(ua.chrome)
        self.assertIsInstance(ua.chrome, str)

    def test_fake_check_cache_path_external_data(self):
        custom_path = "/tmp/custom.json"
        assert not os.path.isfile(custom_path)

        data = open("tests/assets/chrome.html", "r", encoding="utf-8")
        with patch.object(urllib.request, "urlopen", return_value=data):
            ua = UserAgent(
                cache_path=custom_path, use_external_data=True, browsers=["chrome"]
            )

            assert custom_path == ua.cache_path

        assert os.path.isfile(custom_path)

    def test_fake_update_external_chrome_only(self):
        data = open("tests/assets/chrome.html", "r", encoding="utf-8")
        with patch.object(urllib.request, "urlopen", return_value=data):
            ua = UserAgent(use_external_data=True, browsers=["chrome"])

        # Open the chrome.html file for 2nd time, for the update()
        data = open("tests/assets/chrome.html", "r", encoding="utf-8")
        with patch.object(urllib.request, "urlopen", return_value=data):
            ua.update()

        # Check not being empty
        self.assertTrue(ua.chrome)
        # Is string
        self.assertIsInstance(ua.chrome, str)

    def test_fake_update_external_data_cache(self):
        custom_path = "/tmp/custom.json"
        assert not os.path.isfile(custom_path)

        data = open("tests/assets/chrome.html", "r", encoding="utf-8")
        with patch.object(urllib.request, "urlopen", return_value=data):
            ua = UserAgent(
                cache_path=custom_path, use_external_data=True, browsers=["chrome"]
            )

        with pytest.raises(AssertionError):
            ua.update(use_external_data="y")

        # Open the chrome.html file for 2nd time, for the update()
        data = open("tests/assets/chrome.html", "r", encoding="utf-8")
        with patch.object(urllib.request, "urlopen", return_value=data):
            ua.update(use_external_data=True)

        assert os.path.isfile(custom_path)

        self.assertTrue(ua.chrome)
        self.assertIsInstance(ua.chrome, str)
        self.assertTrue(ua.random)
        self.assertIsInstance(ua.random, str)

    def test_fake_update_external_data_cache_bad_weather(self):
        denied_urls = [
            "https://useragentstring.com",
        ]

        with patch.object(
            request,
            "Request",
            side_effect=partial(_request, denied_urls=denied_urls),
        ):
            with pytest.raises(FakeUserAgentError):
                ua = UserAgent(use_external_data=True)

    def test_fake_external_data_boolean(self):
        with pytest.raises(AssertionError):
            UserAgent(use_external_data="y")

    def test_fake_path_str_types(self):
        with pytest.raises(AssertionError):
            UserAgent(cache_path=10)

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
