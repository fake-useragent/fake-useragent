import sys

if sys.version_info >= (3, 10):
    import importlib.resources as ilr
else:
    import importlib_resources as ilr  # noqa: F401

import unittest

from fake_useragent import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_utils_load(self):
        data = utils.load()

        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 1000)
        self.assertIsInstance(data[0], object)
        self.assertIsInstance(data[0]["percent"], float)
        self.assertIsInstance(data[0]["type"], str)
        self.assertIsInstance(data[0]["device_brand"], str)
        self.assertIsInstance(data[0]["browser"], str)
        self.assertIsInstance(data[0]["browser_version"], str)
        self.assertIsInstance(data[0]["browser_version_major_minor"], float)
        self.assertIsInstance(data[0]["os"], str)
        self.assertIsInstance(data[0]["os_version"], str)
        self.assertIsInstance(data[0]["platform"], str)
