#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Author: Melroy van den Berg

"""Description: Convert the user-agents.json file to JSONlines and directly remaps the keys."""
import json

from ua_parser import parse

data = []
new_data = []


def process_item(item):
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
        return None

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


# Load data into memory
print("Reading data from disk")
with open("user-agents.json", "r") as f:
    data = json.load(f)

# Process data in parallel is for some reason slower!?
# with ThreadPoolExecutor() as executor:
#     futures = {executor.submit(process_item, item) for item in data}
#     print("Processing data...")
#     for future in as_completed(futures):
#         try:
#             result = future.result()
#             if result is not None:
#                 new_data.append(result)
#         except Exception as exc:
#             print(f"Generated an exception: {exc}")
#             raise
print("Processing data...")
for item in data:
    result = process_item(item)
    if result is not None:
        new_data.append(result)

# Write JSONlines to new file
print("Writing data to disk")
with open("browsers.jsonl", "w") as f:
    for item in new_data:
        f.write(json.dumps(item) + "\n")

print("Done!")
