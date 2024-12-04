"""General utils for the fake_useragent package."""

import json
import sys
from typing import TypedDict, Union

# We need files() from Python 3.10 or higher
if sys.version_info >= (3, 10):
    import importlib.resources as ilr
else:
    import importlib_resources as ilr

from fake_useragent.errors import FakeUserAgentError
from fake_useragent.log import logger


class BrowserUserAgentData(TypedDict):
    """The schema for the browser user agent data that the `browsers.jsonl` file must follow."""

    useragent: str
    """The user agent string."""
    percent: float
    """The usage percentage of the user agent."""
    type: str
    """The device type for this user agent (eg. mobile or desktop)."""
    device_brand: str
    """Brand name for the device (eg. Generic_Android)."""
    browser: str
    """Browser name for the user agent (eg. Chrome Mobile)."""
    browser_version: str
    """Version of the browser (eg. "100.0.4896.60")."""
    browser_version_major_minor: float
    """Major and minor version of the browser (eg. 100.0)."""
    os: str
    """OS name for the user agent (eg. Android)."""
    os_version: str
    """OS version (eg. 10)."""
    platform: str
    """Platform for the user agent (eg. Linux armv81)."""


def load() -> list[BrowserUserAgentData]:
    """Load the included `browsers.jsonl` file into memory..

    Raises:
        FakeUserAgentError: If unable to find the data.

    Returns:
        list[BrowserUserAgentData]: The list of browser user agent data, following the
            `BrowserUserAgentData` schema.
    """
    data = []
    ret: Union[list[BrowserUserAgentData], None] = None
    try:
        json_lines = (
            ilr.files("fake_useragent.data").joinpath("browsers.jsonl").read_text()
        )
        for line in json_lines.splitlines():
            data.append(json.loads(line))
        ret = data
    except Exception as exc:
        # Empty data just to be sure
        data = []
        logger.warning(
            "Unable to find local data/json file or could not parse the contents using importlib-resources. Try pkg-resource next.",
            exc_info=exc,
        )
        try:
            from pkg_resources import resource_filename

            with open(
                resource_filename("fake_useragent", "data/browsers.jsonl")
            ) as file:
                json_lines = file.read()
                for line in json_lines.splitlines():
                    data.append(json.loads(line))
            ret = data
        except Exception as exc2:
            # Empty data just to be sure
            data = []
            logger.warning(
                "Could not find local data/json file or could not parse the contents using pkg-resource.",
                exc_info=exc2,
            )

    if not ret:
        raise FakeUserAgentError("Data list is empty", ret)

    if not isinstance(ret, list):
        raise FakeUserAgentError("Data is not a list ", ret)
    return ret
