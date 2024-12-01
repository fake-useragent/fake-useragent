#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Author: Melroy van den Berg

"""Description: Convert the user-agents.json file to JSONlines and directly remaps the keys."""
import argparse
import json
from pathlib import Path
from typing import Optional, TypedDict

from ua_parser import parse

from fake_useragent.utils import BrowserUserAgentData, find_browser_json_path


class SourceItem(TypedDict):
    """The schema for the source item that the source file must (at least) follow."""

    userAgent: str
    """The user agent string."""
    weight: float
    """Sampling probability for this user agent when random sampling. Currently has no effect."""
    deviceCategory: str
    """The device type for this user agent."""
    platform: str
    """System name for the user agent."""


def process_item(item: SourceItem) -> Optional[BrowserUserAgentData]:
    """Process a single item and return the transformed item."""
    # Parse the user agent string
    ua_result = parse(item["userAgent"])
    # Example output:
    # Result(
    #     user_agent=UserAgent(
    #         family="Mobile Safari", major="16", minor="2", patch=None, patch_minor=None
    #     ),
    #     os=OS(family="iOS", major="16", minor="2", patch=None, patch_minor=None),
    #     device=Device(family="iPhone", brand="Apple", model="iPhone"),
    #     string="Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X)
    #       AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.1",
    # )

    if not ua_result.user_agent:
        return None  # Skip this user-agent string

    browser_version = ".".join(
        part
        for part in [
            ua_result.user_agent.major,
            ua_result.user_agent.minor,
            ua_result.user_agent.patch,
            ua_result.user_agent.patch_minor,
        ]
        if part is not None
    )
    major_minor_version = ".".join(
        part
        for part in [
            ua_result.user_agent.major,
            ua_result.user_agent.minor,
        ]
        if part is not None
    )
    # The major_minor_version gets converted to a float to make it easier to compare
    if major_minor_version:
        browser_version_major_minor = float(major_minor_version)
    else:
        return None  # Skip this user-agent string

    if ua_result.os:
        os_version = ".".join(
            part
            for part in [
                ua_result.os.major,
                ua_result.os.minor,
                ua_result.os.patch,
                ua_result.os.patch_minor,
            ]
            if part is not None
        )
    else:
        os_version = None

    return {
        "useragent": item["userAgent"],
        "percent": item["weight"] * 100,
        "type": item["deviceCategory"],
        "device_brand": ua_result.device.brand if ua_result.device else None,
        "browser": ua_result.user_agent.family if ua_result.user_agent else None,
        "browser_version": browser_version,
        "browser_version_major_minor": browser_version_major_minor,
        "os": ua_result.os.family if ua_result.os else None,
        "os_version": os_version,
        "platform": item["platform"],
    }


def convert_useragents_file_format(source: Path, destination: Path) -> None:
    """Convert the `source` file in Intoli's format to a JSONL file in our format in `destination`.

    Args:
        source (Path): The path to the file with updated user agent data. We use Intoli's
            [user-agents](https://github.com/intoli/user-agents) library, so this file must comply
            with their format.
        destination (Path): Where to output the JSONL converted to our format.
    """
    print(f"Reading data from {source}.")
    with open(source, "r") as f:
        data = json.load(f)

    # Process data. For some reason, ThreadPoolExecutor parallel execution is slower.
    print("Processing data...")
    new_data = [result for item in data if (result := process_item(item)) if not None]

    print(f"Writing data to {destination}")
    with open(destination, "w") as f:
        for item in new_data:
            f.write(json.dumps(item) + "\n")

    print("Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert Intoli's user agent data to our JSONL format.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Input JSON file.",
        default=Path("user-agents.json"),
        type=Path,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output JSONL file.",
        default=find_browser_json_path(),
        type=Path,
    )
    args = parser.parse_args()

    convert_useragents_file_format(args.input, args.output)
