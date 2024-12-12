import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING
from zipfile import ZipFile
from zipimport import zipimporter

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
        with TemporaryDirectory() as d:
            filename = Path(d, "module.zip")
            with ZipFile(filename, "w") as z:
                for file in Path("src").rglob("*"):
                    z.write(file, file.relative_to("src"))

            unload_module("fake_useragent")  # cleanup previous imports

            importer = zipimporter(str(filename))
            spec = importer.find_spec("fake_useragent")
            self.assertIsNotNone(spec)
            loader = spec.loader
            self.assertIsNotNone(loader)
            if not TYPE_CHECKING:
                utils = loader.load_module("fake_useragent").utils

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

        unload_module("fake_useragent")  # cleanup


def unload_module(name: str):
    for module in tuple(sys.modules):
        if name in module:
            del sys.modules[module]
