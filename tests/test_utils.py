import io
import json
import os
import urllib.request
from functools import partial

import unittest
from unittest.mock import patch
import pytest

from fake_useragent import errors, settings, utils
from fake_useragent.utils import urlopen_has_ssl_context
from tests.utils import _request, find_unused_port, assets

try:  # Python 2 # pragma: no cover
    from urllib2 import Request
except ImportError:  # Python 3 # pragma: no cover
    from urllib.request import Request


class TestUtils(unittest.TestCase):
    def setUp(self):
        try:
            os.remove("/tmp/custom.json")
        except OSError:
            pass

    def tearDown(self):
        try:
            os.remove("/tmp/custom.json")
        except OSError:
            pass

    def test_utils_get(self):
        data = open("tests/assets/chrome.html", "r", encoding="utf-8")
        with patch.object(urllib.request, "urlopen", return_value=data):
            res = utils.get("https://websitethatmightexists.com")
            self.assertTrue(res)
            print(data)

    def test_utils_get_retries(self):
        def __retried_request(*args, **kwargs):  # noqa
            __retried_request.attempt += 1

            if __retried_request.attempt < settings.HTTP_RETRIES:
                return Request(
                    "http://0.0.0.0:{port}".format(
                        port=find_unused_port(),
                    )
                )

            return Request(*args, **kwargs)

        __retried_request.attempt = 0

        with patch(
            "fake_useragent.utils.Request",
            side_effect=__retried_request,
        ):
            assert utils.get("http://google.com") is not None

        assert __retried_request.attempt == 2

    def test_utils_load(self):
        _load = utils.load

        with patch(
            "fake_useragent.utils.load",
            side_effect=_load,
        ) as mocked:
            browsers = [
                "chrome",
                "edge",
                "internet explorer",
                "firefox",
                "safari",
                "opera",
            ]
            data = utils.load(browsers)

            mocked.assert_called()

        self.assertIsInstance(data["chrome"], list)
        self.assertIsInstance(data["edge"], list)
        self.assertIsInstance(data["firefox"], list)
        self.assertIsInstance(data["opera"], list)
        self.assertIsInstance(data["safari"], list)
        self.assertIsInstance(data["internet explorer"], list)

    def test_utils_write(self):
        path = "/tmp/custom.json"
        data = {"foo": "bar"}

        utils.write(path, data)

        with open(path, encoding="utf-8") as fp:
            expected = json.loads(fp.read())

        assert expected == data

    def test_utils_read(self):
        path = "/tmp/custom.json"
        data = {"foo": "bar"}

        with open(path, mode="w", encoding="utf-8") as fp:
            dumped = json.dumps(data)

            if not isinstance(dumped, utils.text):  # Python 2
                dumped = dumped.decode("utf-8")

            fp.write(dumped)

        expected = utils.read(path)

        assert expected == data

    def test_utils_exist(self):
        path = "/tmp/custom.json"

        assert not os.path.isfile(path)

        assert not utils.exist(path)

        with open(path, mode="wb") as fp:
            fp.write(b"\n")

        assert os.path.isfile(path)

        assert utils.exist(path)

    def test_utils_rm(self):
        path = "/tmp/custom.json"
        assert not os.path.isfile(path)

        with open(path, mode="wb") as fp:
            fp.write(b"\n")

        assert os.path.isfile(path)

        utils.rm(path)

        assert not os.path.isfile(path)

    def test_utils_update(self):
        path = "/tmp/custom.json"
        browsers = ["chrome", "edge", "internet explorer", "firefox", "safari", "opera"]
        utils.update(path, browsers)

        mtime = os.path.getmtime(path)

        _load = utils.load

        with patch(
            "fake_useragent.utils.load",
            side_effect=_load,
        ) as mocked:
            utils.update(path, browsers)

            mocked.assert_called()

        assert os.path.getmtime(path) != mtime

    def test_utils_load_use_local_file(self):
        browsers = [
            "chrome",
            "edge",
            "internet explorer",
            "firefox",
            "safari",
            "opera",
        ]
        # By default use_local_file is also True during production
        data = utils.load(browsers, use_local_file=True)

        self.assertIsInstance(data["chrome"], list)
        self.assertIsInstance(data["edge"], list)
        self.assertIsInstance(data["firefox"], list)
        self.assertIsInstance(data["opera"], list)
        self.assertIsInstance(data["safari"], list)
        self.assertIsInstance(data["internet explorer"], list)

    def test_utils_load_cached(self):
        path = "/tmp/custom.json"
        _load = utils.load

        with patch(
            "fake_useragent.utils.load",
            side_effect=_load,
        ) as mocked:
            browsers = [
                "chrome",
                "edge",
                "internet explorer",
                "firefox",
                "safari",
                "opera",
            ]
            data = utils.load_cached(path, browsers)

            mocked.assert_called()

        self.assertIsInstance(data["chrome"], list)
        self.assertIsInstance(data["edge"], list)
        self.assertIsInstance(data["firefox"], list)
        self.assertIsInstance(data["opera"], list)
        self.assertIsInstance(data["safari"], list)
        self.assertIsInstance(data["internet explorer"], list)

        data = []
        with patch("fake_useragent.utils.load") as mocked:
            browsers = [
                "chrome",
                "edge",
                "internet explorer",
                "firefox",
                "safari",
                "opera",
            ]
            data = utils.load_cached(path, browsers)

            mocked.assert_not_called()

        self.assertIsInstance(data["chrome"], list)
        self.assertIsInstance(data["edge"], list)
        self.assertIsInstance(data["firefox"], list)
        self.assertIsInstance(data["opera"], list)
        self.assertIsInstance(data["safari"], list)
        self.assertIsInstance(data["internet explorer"], list)

    def test_utils_load_no_local_file_external_data_bad_weather(self):
        path = "/tmp/custom.json"
        denied_urls = [
            "https://useragentstring.com",
        ]

        with patch(
            "fake_useragent.utils.Request",
            side_effect=partial(_request, denied_urls=denied_urls),
        ):
            browsers = [
                "chrome",
                "edge",
                "internet explorer",
                "firefox",
                "safari",
                "opera",
            ]
            with pytest.raises(errors.FakeUserAgentError):
                utils.load(browsers, use_local_file=False)

            with pytest.raises(errors.FakeUserAgentError):
                utils.load_cached(path, browsers)

            with pytest.raises(errors.FakeUserAgentError):
                utils.update(path, browsers)

    def test_utils_load_use_not_local_file_external_is_down(self):
        denied_urls = [
            "https://useragentstring.com/",
        ]

        with patch(
            "fake_useragent.utils.Request",
            side_effect=partial(_request, denied_urls=denied_urls),
        ):
            browsers = [
                "chrome",
                "edge",
                "internet explorer",
                "firefox",
                "safari",
                "opera",
            ]
            with pytest.raises(errors.FakeUserAgentError):
                utils.load(browsers, use_local_file=False)
