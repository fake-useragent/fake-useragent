from __future__ import absolute_import, unicode_literals

import os
import tempfile
import uuid

import mock

from fake_useragent import (
    VERSION, FakeUserAgent, FakeUserAgentError, UserAgent, UserAgentError,
    settings, utils,
)
from tests import BaseTestCase

try:  # Python 2
    from urllib2 import Request

except ImportError:  # Python 3
    from urllib.request import Request


class FakeTestCase(
    BaseTestCase,
):
    def setUp(self):
        self.clear_db()

        self.example_website = 'http://google.com'

        self.service_failed = False

    def tearDown(self):
        self.clear_db()

    def test_fake_user_agent(self):
        self.assertFalse(utils.exist(self.db))

        ua = UserAgent(cache=False)

        probes = [
            ua.ie,
            ua.msie,
            ua.internetexplorer,
            ua.internet_explorer,
            ua['internet explorer'],
            ua.google,
            ua.chrome,
            ua.googlechrome,
            ua.google_chrome,
            ua['google chrome'],
            ua.firefox,
            ua.ff,
            ua.ie,
            ua.safari,
            ua.random,
            ua['random'],
        ]

        for probe in probes:
            self.assertIsNotNone(probe)

        with self.assertRaises(FakeUserAgentError):
            ua.non_existing

            ua['non_existing']

        data1 = ua.data

        ua.update(self.db)

        data2 = ua.data

        self.assertEqual(data1, data2)

        self.assertIsNot(data1, data2)

        self.clear_db()

        ua = UserAgent()

        self.assertTrue(utils.exist(self.db))

        data1 = ua.data

        self.clear_db()

        ua.update(self.db)

        self.assertTrue(utils.exist(self.db))

        data2 = ua.data

        self.assertEqual(data1, data2)

        self.assertIsNot(data1, data2)

    def test_fake_custom_path(self):
        custom_path = os.path.join(
            tempfile.gettempdir(),
            'fake_useragent_' + uuid.uuid1().hex + '.json',
        )

        ua = UserAgent(path=custom_path)

        self.assertTrue(utils.exist(custom_path))

        expected = {
            'randomize': mock.ANY,
            'browsers': {
                'chrome': mock.ANY,
                'firefox': mock.ANY,
                'opera': mock.ANY,
                'safari': mock.ANY,
                'internetexplorer': mock.ANY,
            }
        }

        self.assertEqual(expected, ua.data)

        mtime = os.path.getmtime(custom_path)

        ua.update()

        self.assertNotEqual(os.path.getmtime(custom_path), mtime)

        self.clear_db(path=custom_path)

    def test_fake_cache_server(self):
        def _request(*args, **kwargs):
            denied_urls = [
                'http://www.w3schools.com/browsers/browsers_stats.asp',
                'http://useragentstring.com/pages/useragentstring.php',
            ]

            requested_url = args[0]

            for url in denied_urls:
                if url in requested_url:
                    return Request('http://0.0.0.0')

            return Request(requested_url)

        with mock.patch(
            'fake_useragent.utils.Request',
            side_effect=_request,
        ):
            ua = UserAgent()

        expected = {
            'randomize': mock.ANY,
            'browsers': {
                'chrome': mock.ANY,
                'firefox': mock.ANY,
                'opera': mock.ANY,
                'safari': mock.ANY,
                'internetexplorer': mock.ANY,
            }
        }

        self.assertEqual(expected, ua.data)

    def test_fake_fallback(self):
        fallback = 'Foo Browser'

        def _request(*args, **kwargs):
            return Request('http://0.0.0.0')

        with mock.patch(
            'fake_useragent.utils.Request',
            side_effect=_request,
        ):
            ua = UserAgent(fallback=fallback)

        self.assertEqual(ua.random, fallback)

        self.assertEqual(ua.ie, fallback)

        with self.assertRaises(AssertionError):
            ua = UserAgent(fallback=True)

        def _request(*args, **kwargs):
            denied_urls = [
                'http://www.w3schools.com/browsers/browsers_stats.asp',
                'http://useragentstring.com/pages/useragentstring.php',
            ]

            requested_url = args[0]

            for url in denied_urls:
                if url in requested_url:
                    return Request('http://0.0.0.0')

            if 'https://fake-useragent.herokuapp.com/browsers/' in requested_url:  # noqa
                return Request('https://httpbin.org/get')

            return Request(requested_url)

        with mock.patch(
            'fake_useragent.utils.Request',
            side_effect=_request,
        ):
            ua = UserAgent(fallback=fallback)

        self.assertEqual(ua.random, fallback)

        self.assertEqual(ua.ie, fallback)

    def test_fake_safe_attrs(self):
        ua = UserAgent(safe_attrs=('foo',))

        with self.assertRaises(AttributeError):
            ua.foo

    def test_fake_version(self):
        self.assertEqual(VERSION, settings.__version__)

    def test_fake_aliases(self):
        self.assertIs(FakeUserAgentError, UserAgentError)

        self.assertIs(FakeUserAgent, UserAgent)
