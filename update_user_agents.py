#!/usr/bin/env python3
import argparse
import json
import re
import time
from enum import Enum
from itertools import cycle
from pathlib import Path
from typing import Union

import requests
from user_agents.parsers import UserAgent, parse


class Browser(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    SAFARI = "safari"

    @classmethod
    def _missing_(cls, value):
        """This method makes the Enum case-insensitive."""
        value = str(value).lower()
        for member in cls:
            if member.value == value:
                return member
        return None


class UserAgentUpdater:
    UPDATE_USERAGENT_URL = r"https://user-agents.net/download"
    USERAGENT_VERSION_URL = r"https://www.browsers.fyi/api/"

    def __init__(
        self,
        timeout: float = 100.0,
        output_name: str = "browsers.json",
        append: bool = True,
    ):
        self.timeout = timeout
        self.ua_list = []
        self.output_name = output_name
        self.append = append
        # An unique list of user agents to avoid adding any duplicates.
        self.seen_useragents = set()

        # Regex patterns
        self.chrome_pattern = re.compile(r"chrome", re.IGNORECASE)
        self.firefox_pattern = re.compile(r"firefox", re.IGNORECASE)
        self.safari_pattern = re.compile(r"safari", re.IGNORECASE)
        self.edge_pattern = re.compile(r"edge", re.IGNORECASE)

        self.ios_pattern = re.compile(r"ios", re.IGNORECASE)
        self.linux_pattern = re.compile(
            r"Linux|Ubuntu|Arch|Fedora|OpenSuse|Debian", re.IGNORECASE
        )
        self.macos_pattern = re.compile(r"Mac", re.IGNORECASE)
        self.windows_pattern = re.compile(r"Windows|win10|win11|win7", re.IGNORECASE)
        self.android_pattern = re.compile(r"android", re.IGNORECASE)

    def send_get_request(self, url: str):
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def send_post_request(self, url: str, query_parameters: dict):
        response = requests.post(url, data=query_parameters, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def send_version_request(self, browser: Browser) -> float:
        current_browser_versions = self.send_get_request(self.USERAGENT_VERSION_URL)
        version = current_browser_versions.get(browser.value).get("version")

        try:
            version = float(version)
        except TypeError as e:
            print(e)
        except ValueError as e:
            print(e)

        return version

    def get_user_agents(
        self,
        browser_type: str,
        version: Union[float, None] = None,
        max_version_lag: float = 0.0,
        limit: int = 200,
        remember: bool = False,
    ) -> list[dict]:
        """Send an API request and return a list of user agent dictionaries."""
        browser = Browser(browser_type)

        if not version:
            version = self.send_version_request(browser)

        user_agents = self.send_user_agent_request(
            browser=browser, version=version, limit=limit
        )
        parsed_user_agents = self.parse_user_agents(user_agents=user_agents)
        filtered_user_agents = self.filter_user_agents(
            user_agents=parsed_user_agents,
            browser=browser,
            version=version,
            max_version_lag=max_version_lag,
            limit=limit,
        )

        if remember:
            # remember the user agents for next write
            self.ua_list.extend(filtered_user_agents)

        return filtered_user_agents

    def send_user_agent_request(
        self,
        browser: Browser,
        version: float,
        limit: int,
    ) -> list[str]:
        """Send an API request to get the specified user agents."""

        if browser == Browser.SAFARI:
            # Specifying a version of a browser does
            # not work well for Safari. Therefore for
            # Safari all the available user agents are
            # downloaded. Selecting a subset with the
            # correct version happens downstream.
            input_query_parameters = {
                "browser": "safari",
                "browser_type": "browser",
                "download": "json",
            }
        else:
            input_query_parameters = {
                "browser": browser.value,
                "version": str(version),
                "limit": str(limit),
                "download": "json",
            }

        user_agents = self.send_post_request(
            self.UPDATE_USERAGENT_URL, input_query_parameters
        )

        return user_agents

    def parse_user_agents(self, user_agents: list[str]) -> list[dict]:
        """Parse a list of user agent strings and return them as dictionaries."""
        parsed_user_agents = []

        for user_agent_string in user_agents:
            try:
                # replace extra info between square brackets
                # (usually ip address) and slashes
                # and remove trailing whitespace
                user_agent_string = re.sub(r"\[.*?\]|\\", "", user_agent_string)
                user_agent_string = user_agent_string.strip()

                # retrieve all the info we need from the user agent string
                user_agent = parse(user_agent_string)
                platform = self._get_platform(user_agent)
                browser = self._get_browser(user_agent)
                version = self._get_version(user_agent)
                os = self._get_os(user_agent)
                system = " ".join(
                    [user_agent.browser.family, str(version), user_agent.os.family]
                )
                ua_parsed = {
                    "useragent": user_agent_string,
                    "percent": 100.0,
                    "type": platform,
                    "system": system,
                    "browser": browser,
                    "version": version,
                    "os": os,
                }

                parsed_user_agents.append(ua_parsed)
            except Exception as e:
                print(e)

        return parsed_user_agents

    def filter_user_agents(
        self,
        user_agents: list[dict],
        browser: Browser,
        version: float,
        max_version_lag: float,
        limit: int,
    ) -> list[dict]:
        """Filter the user agents based on the version and browser type."""
        filter_criteria = lambda x: (  # noqa: E731
            x["version"] >= (version - max_version_lag)
            and x["version"] <= version
            and x["browser"] == browser.value
        )
        filtered_useragents = list(filter(filter_criteria, user_agents))
        return filtered_useragents[:limit]

    def write_useragents(self, file_path: Path) -> None:
        """Write all the user agents downloaded so far to disk at the specified path."""
        full_path = file_path.joinpath(self.output_name)

        # A list of JSON objects, also known as JSONlines format
        unique_ua_list = []
        # Check for duplicates and only add unique user agents to the list
        # Add the user agents to a set, which is very efficient for checking uniqueness O(1)
        for ua in self.ua_list:
            if "useragent" in ua and ua["useragent"] not in self.seen_useragents:
                unique_ua_list.append(json.dumps(ua))
                self.seen_useragents.add(ua["useragent"])

        # Check that some user agents have been found before writing
        if len(unique_ua_list) > 0:
            print(f"Writing {len(unique_ua_list)} user agents to {full_path}")
            if self.append:
                with open(full_path, "a") as writer:
                    writer.write("\n".join(unique_ua_list))
            else:
                with open(full_path, "w") as writer:
                    writer.write("\n".join(unique_ua_list))

    @staticmethod
    def _get_platform(user_agent: UserAgent):
        """Get the platform as a string."""
        if user_agent.is_mobile:
            return "mobile"
        elif user_agent.is_tablet:
            return "tablet"
        elif user_agent.is_pc:
            return "pc"
        elif user_agent.is_bot:
            return "bot"
        else:
            return "other"

    def _get_browser(self, user_agent: UserAgent) -> str:
        """Get the browser as a string."""
        browser = user_agent.browser.family

        if re.search(self.chrome_pattern, browser):
            return "chrome"
        elif re.search(self.firefox_pattern, browser):
            return "firefox"
        elif re.search(self.safari_pattern, browser):
            return "safari"
        elif re.search(self.edge_pattern, browser):
            return "edge"

        return browser

    def _get_os(self, user_agent: UserAgent) -> str:
        """Get the operating system as a string."""
        os = user_agent.os.family
        if re.search(self.ios_pattern, os):
            return "ios"
        elif re.search(self.linux_pattern, os):
            return "linux"
        elif re.search(self.macos_pattern, os):
            return "macos"
        elif re.search(self.windows_pattern, os):
            return "win10"
        elif re.search(self.android_pattern, os):
            return "android"

        return os

    @staticmethod
    def _get_version(user_agent: UserAgent) -> float:
        "Get the browser version as a float."
        version_groups = user_agent.browser.version_string.split(".")
        if len(version_groups) == 0 or version_groups[0] == "":
            return 0.0
        if len(version_groups) == 1:
            return float(version_groups[0])
        else:
            return float(".".join(version_groups[:2]))


if __name__ == "__main__":
    updater = UserAgentUpdater()

    # Parse the command line arguments, if provided.
    parser = argparse.ArgumentParser(
        description="Script to update the list of user agents."
    )
    # File storage path
    parser.add_argument(
        "--output_folder",
        type=str,
        default=".",
        help="The path to the folder where the user agents will be stored",
    )
    parser.add_argument(
        "browser_args",
        nargs="*",
        default=[],
        help="Arbitrary number of browsers to include in the update",
    )
    parser.add_argument(
        "--limit",
        default=200,
        type=int,
        help="The max number of user agents per browser",
    )
    parser.add_argument(
        "--max_version_lag",
        type=float,
        nargs="*",
        default=0.0,
        help="The max version lag for the user agents, older versions will be excluded",
    )

    args = parser.parse_args()
    possible_browsers = [
        "chrome",
        "edge",
        "safari",
        "firefox",
        "samsung-browser",
    ]

    output_folder = args.output_folder
    if not isinstance(output_folder, str):
        raise TypeError("The specified output folder should be a string.")
    else:
        output_folder = Path(output_folder)
    if not output_folder.exists():
        raise NameError("The specified folder does not exist.")
    if not output_folder.is_dir():
        raise TypeError("The specified path should be a folder.")

    requested_browsers = [
        browser for browser in args.browser_args if browser in possible_browsers
    ]
    max_version_lags = args.max_version_lag
    if not isinstance(max_version_lags, list):
        max_version_lags = [max_version_lags]
    limit = args.limit

    if len(requested_browsers) > 0:
        for requested_browser, max_version_lag in zip(
            requested_browsers, cycle(max_version_lags)
        ):
            updater.get_user_agents(
                browser_type=requested_browser,
                limit=limit,
                remember=True,
                max_version_lag=max_version_lag,
            )
            # Sleep on purpose for 5 sec to avoid being blocked or rate limited.
            time.sleep(5)

    else:
        # If no command line arguments are given (so if you just run this script),
        # only run the update script for Firefox.
        new_firefox_useragents = updater.get_user_agents(
            browser_type="firefox", max_version_lag=1.0, limit=200, remember=True
        )
    # write the new user agents to disk
    updater.write_useragents(output_folder)
