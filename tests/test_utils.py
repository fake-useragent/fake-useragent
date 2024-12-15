import atexit
import sys
import unittest
from contextlib import contextmanager
from importlib import invalidate_caches
from pathlib import Path
from shutil import make_archive
from tempfile import TemporaryDirectory
from typing import List

from fake_useragent import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_utils_load(self):
        data = utils.load()

        self.assertGreater(len(data), 1000)

        if sys.version_info < (3, 12):
            from pytest import skip

            skip(
                "pydantic only supports `typing_extensions.TypedDict` instead of `typing.TypedDict` on Python < 3.12."
            )

        from pydantic import TypeAdapter

        TypeAdapter(List[utils.BrowserUserAgentData]).validate_python(data, strict=True)

    def test_utils_load_from_zipimport(self):
        with make_temporary_directory() as temp_dir:
            zip_filename = str(Path(temp_dir, "module.zip"))

            make_archive(zip_filename.removesuffix(".zip"), "zip", "src")

            unload_module("fake_useragent")  # cleanup previous imports

            sys.path.insert(0, zip_filename)

            from fake_useragent import utils

            self.assertIn(
                "module.zip",
                utils.__file__,
                "utils should be imported from the zip file",
            )

            data = utils.load()

        self.assertGreater(len(data), 1000)

        # cleanup
        unload_module("fake_useragent")
        sys.path.remove(zip_filename)


def unload_module(name: str):
    for module in tuple(sys.modules):
        if name in module:
            del sys.modules[module]


@contextmanager
def make_temporary_directory():
    d = TemporaryDirectory()
    try:
        yield d.name
    finally:
        try:
            d.cleanup()
        except PermissionError:
            # Windows users will fail to remove the temporary directory
            # because the module is still in use
            invalidate_caches()
            atexit.register(d.cleanup)
