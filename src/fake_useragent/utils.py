"""General utils for the fake_useragent package."""

import json
from pkgutil import get_data
from typing import Optional, TypedDict

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
    device_brand: Optional[str]
    """Brand name for the device (eg. Generic_Android)."""
    browser: Optional[str]
    """Browser name for the user agent (eg. Chrome Mobile)."""
    browser_version: str
    """Version of the browser (eg. "100.0.4896.60")."""
    browser_version_major_minor: float
    """Major and minor version of the browser (eg. 100.0)."""
    os: Optional[str]
    """OS name for the user agent (eg. Android)."""
    os_version: Optional[str]
    """OS version (eg. 10)."""
    platform: str
    """Platform for the user agent (eg. Linux armv81)."""


def load() -> list[BrowserUserAgentData]:
    """Load the included `browser.jsonl` file into memory.

    Raises:
        FakeUserAgentError: If unable to load or parse the data.

    Returns:
        list[BrowserUserAgentData]: The list of browser user agent data, following the
            `BrowserUserAgentData` schema.
    """
    try:
        jsonl = get_data(__package__ or "fake_useragent", "data/browsers.jsonl")
        if jsonl is None:
            raise FakeUserAgentError("Failed to find browsers.jsonl")
        comma_joined_objects = jsonl.rstrip().decode().replace("\n", ",")
        json_list_string = f"[{comma_joined_objects}]"
        return json.loads(json_list_string)
    except Exception as exc:
        logger.warning("Could not find or parse browsers.jsonl", exc_info=exc)
    raise FakeUserAgentError("Failed to load the user agent data.")
