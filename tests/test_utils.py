from __future__ import absolute_import, unicode_literals

import json
import os

import mock
import unittest2

from fake_useragent import settings, utils

try:
    from tests.base import BaseTestCase
except ImportError:
    from base import BaseTestCase


class UtilsTestCase(BaseTestCase):
    def setUp(self):
        self.clear_db()

        self.example_website = 'http://google.com'

    def tearDown(self):
        self.clear_db()

    def test_utils_get(self):
        self.assertIsNotNone(utils.get(self.example_website))

    def test_utils_get_cache(self):
        html = utils.get(settings.CACHE_SERVER)

        data = json.loads(html.decode('utf-8'))

        expected = {
            'randomize': mock.ANY,
            'browsers': {
                'chrome': mock.ANY,
                'firefox': mock.ANY,
                'opera': mock.ANY,
                'safari': mock.ANY,
                'ie/edge': mock.ANY,
            },
        }

        self.assertEqual(expected, data)

    def test_utils_get_browsers(self):
        browser_list = [browser[0] for browser in utils.get_browsers()]

        self.assertEqual(len(browser_list), 5)

        expected = [
            'Firefox', 'Opera', 'Chrome', 'Internet Explorer', 'Safari',
        ]

        self.assertItemsEqual(expected, browser_list)

    def test_utils_get_browser_versions(self):
        browser_list = [browser[0] for browser in utils.get_browsers()]

        for browser in browser_list:
            self.assertEqual(
                len(utils.get_browser_versions(browser)),
                settings.BROWSERS_COUNT_LIMIT,
            )

    def test_utils_db(self):
        data = utils.load()

        expected = {
            'randomize': mock.ANY,
            'browsers': {
                'chrome': mock.ANY,
                'firefox': mock.ANY,
                'opera': mock.ANY,
                'safari': mock.ANY,
                'internetexplorer': mock.ANY,
            },
        }

        self.assertEqual(expected, data)

        utils.write(self.db, data)

        self.assertTrue(os.path.isfile(self.db))

        self.assertTrue(utils.exist(self.db))

        self.assertEqual(expected, utils.read(self.db))

        self.clear_db()

        self.assertFalse(utils.exist(self.db))

        utils.update(self.db)

        self.assertTrue(utils.exist(self.db))

        self.clear_db()

        self.assertFalse(utils.exist(self.db))

        self.assertEqual(expected, utils.load_cached(self.db))


if __name__ == '__main__':
    unittest2.main(module=__name__)
