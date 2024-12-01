#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Author: Melroy van den Berg

"""Description: Convert the user-agents.json file to JSONlines and directly remaps the keys."""
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from ua_parser import parse

data = []
new_data = []


def process_item(item):
    """Process a single item and return the transformed item."""
    # Parse the user agent string
    ua_result = parse(item["userAgent"])

    if not ua_result.user_agent:
        return None

    if ua_result.user_agent:
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
        try:
            browser_version_major_minor = float(
                ".".join(
                    part
                    for part in [
                        ua_result.user_agent.major,
                        ua_result.user_agent.minor,
                    ]
                    if part is not None
                )
            )
        except TypeError:
            return None
    else:
        browser_version = None
        browser_version_major_minor = 0.0

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


# Load data into memory
print("Reading data from disk")
with open("user-agents.json", "r") as f:
    data = json.load(f)

# Process data in parallel
with ThreadPoolExecutor() as executor:
    futures = {executor.submit(process_item, item) for item in data}
    print("Processing data...")
    for future in as_completed(futures):
        try:
            result = future.result()
            if result is not None:
                new_data.append(result)
        except Exception as exc:
            print(f"Generated an exception: {exc}")
            raise

# Write JSONlines to new file
print("Writing data to disk")
with open("browsers.jsonl", "w") as f:
    for item in new_data:
        f.write(json.dumps(item) + "\n")

print("Done!")
