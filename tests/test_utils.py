import atexit
import sys
import unittest
from importlib import invalidate_caches
from pathlib import Path
from shutil import rmtree
from tempfile import TemporaryDirectory
from zipfile import ZipFile

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

    def test_utils_load_from_zipimport(self):
        with TemporaryDirectory(ignore_cleanup_errors=True) as d:
            filename = Path(d, "module.zip")
            with ZipFile(filename, "w") as z:
                for file in Path("src").rglob("*"):
                    z.write(file, file.relative_to("src"))

            unload_module("fake_useragent")  # cleanup previous imports

            sys.path.insert(0, str(filename))

            from fake_useragent import utils

            self.assertIn(
                "module.zip",
                utils.__file__,
                "utils should be imported from the zip file",
            )

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

        # cleanup
        unload_module("fake_useragent")
        sys.path.remove(str(filename))

        if filename.exists():
            # Windows users will fail to remove the temporary directory
            # because the module is still in use
            invalidate_caches()

            @atexit.register
            def _():
                rmtree(d)


def unload_module(name: str):
    for module in tuple(sys.modules):
        if name in module:
            del sys.modules[module]
