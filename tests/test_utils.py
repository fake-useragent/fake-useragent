import sys

if sys.version_info >= (3, 10):
    import importlib.resources as ilr
else:
    import importlib_resources as ilr

import unittest
from unittest.mock import patch

from fake_useragent import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_utils_load(self):
        data = utils.load()

        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 10)
        self.assertIsInstance(data[0], object)
        self.assertIsInstance(data[0]["useragent"], str)

    # https://github.com/python/cpython/issues/95299
    @unittest.skipIf(
        sys.version_info >= (3, 12), "not compatible with Python 3.12 (or higher)"
    )
    def test_utils_load_pkg_resource_fallback(self):
        # By default use_local_file is also True during production
        # We will not allow the default importlib resources to be used, by triggering an Exception
        with patch.object(ilr, "files") as mocked_importlib_resources_files:
            # This exception should trigger the alternative path, trying to use pkg_resource as fallback
            mocked_importlib_resources_files.side_effect = Exception("Error")
            data = utils.load()

        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], object)
        self.assertIsInstance(data[0]["useragent"], str)
