"""Fake User Agent retriever."""

import random
from collections.abc import Iterable
from typing import Any, Optional, Union

from fake_useragent import settings
from fake_useragent.log import logger
from fake_useragent.utils import BrowserUserAgentData, load


def _ensure_iterable(
    *, default: Iterable[str], **kwarg: Optional[Iterable[str]]
) -> list[str]:
    """Ensure the given value is an Iterable and convert it to a list.

    Args:
        default (Iterable[str]): Default iterable to use if value is `None`.
        **kwarg (Optional[Iterable[str]]): A single keyword argument containing the value to check
            and convert.

    Raises:
        ValueError: If more than one keyword argument is provided.
        TypeError: If the value is not None, not a str, and not iterable.

    Returns:
        list[str]: A list containing the items from the iterable.
    """
    if len(kwarg) != 1:
        raise ValueError(
            f"ensure_iterable expects exactly one keyword argument but got {len(kwarg)}."
        )

    param_name, value = next(iter(kwarg.items()))

    if value is None:
        return list(default)
    if isinstance(value, str):
        return [value]

    try:
        return list(value)
    except TypeError as te:
        raise TypeError(
            f"'{param_name}' must be an iterable of str, a single str, or None but got "
            f"{type(value).__name__}."
        ) from te


def _ensure_float(value: Any) -> float:
    """Ensure the given value is a float.

    Args:
        value (Any): The value to check and convert.

    Raises:
        ValueError: If the value is not a float.

    Returns:
        float: The float value.
    """
    try:
        return float(value)
    except ValueError as ve:
        msg = f"Value must be convertible to float but got {value}."
        raise ValueError(msg) from ve


class FakeUserAgent:
    """Fake User Agent retriever.

    Args:
        browsers (Optional[Iterable[str]], optional): If given, will only ever return user agents
            from these browsers. If None, set to `["chrome", "firefox", "safari", "edge"]`. Defaults
            to None.
        os (Optional[Iterable[str]], optional): If given, will only ever return user agents from
            these operating systems. You can pass values in the data file or those in
            `settings.OS_REPLACEMENTS`. If None, set to `["win10", "macos", "linux"]`. Defaults to
            None.
        min_version (float, optional): Will only ever return user agents with versions greater than
            this one. Defaults to 0.0.
        min_percentage (float, optional): Legacy setting to filter user agents based on a sampling
            probability. Current data has all percentages set to 100, so this should have no effect.
            Defaults to 0.0.
        platforms (Optional[Iterable[str]], optional): If given, will only ever return user agents
            from these browsers. If None, set to `["pc", "mobile", "tablet"]`. Defaults to None.
        fallback (str, optional): User agent to use if there are any issues retrieving a user agent.
            Defaults to `"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like
            Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"`.
        safe_attrs (Optional[Iterable[str]], optional): `FakeUserAgent` uses a custom `__getattr__`
            to facilitate retrieval of user agents by browser. If you need to prevent some
            attributes from being treated as browsers, pass them here. If None, all attributes will
            be treated as browsers. Defaults to None.

    Raises:
        TypeError: If `fallback` isn't a `str` or `safe_attrs` contains non-`str` values.
    """

    def __init__(
        self,
        browsers: Optional[Iterable[str]] = None,
        os: Optional[Iterable[str]] = None,
        min_version: float = 0.0,
        min_percentage: float = 0.0,
        platforms: Optional[Iterable[str]] = None,
        fallback: str = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
        ),
        safe_attrs: Optional[Iterable[str]] = None,
    ):
        self.browsers = _ensure_iterable(
            browsers=browsers, default=["chrome", "firefox", "safari", "edge"]
        )

        os = _ensure_iterable(os=os, default=["win10", "macos", "linux"])
        self.os = [
            item
            for os_name in os
            for item in settings.OS_REPLACEMENTS.get(os_name, [os_name])
        ]

        self.min_percentage = _ensure_float(min_percentage)
        self.min_version = _ensure_float(min_version)

        self.platforms = _ensure_iterable(
            platforms=platforms, default=["pc", "mobile", "tablet"]
        )

        if not isinstance(fallback, str):
            msg = f"fallback must be a str but got {type(fallback).__name__}."
            raise TypeError(msg)
        self.fallback = fallback

        safe_attrs = _ensure_iterable(safe_attrs=safe_attrs, default=set())
        str_safe_attrs = [isinstance(attr, str) for attr in safe_attrs]
        if not all(str_safe_attrs):
            bad_indices = [
                idx for idx, is_str in enumerate(str_safe_attrs) if not is_str
            ]
            msg = f"safe_attrs must be an iterable of str but indices {bad_indices} are not."
            raise TypeError(msg)
        self.safe_attrs = set(safe_attrs)

        # Next, load our local data file into memory (browsers.json)
        self.data_browsers = load()

    # This method will return a filtered list of user agents.
    # The request parameter can be used to specify a browser.
    def _filter_useragents(
        self, request: Union[str, None] = None
    ) -> list[BrowserUserAgentData]:
        """Filter the user agents based on filters set in the instance, and an optional request.

        User agents from the data file are filtered based on the attributes passed upon
        instantiation.

        Args:
            request (Union[str, None], optional): A specific browser name you want results for in
                this particular call. If None, don't apply extra filters. Defaults to None.

        Returns:
            list[BrowserUserAgentData]: A list of browser user agent data filtered down to match
                all criteria.
        """
        # filter based on browser, os, platform and version.
        filtered_useragents = list(
            filter(
                lambda x: x["browser"] in self.browsers
                and x["os"] in self.os
                and x["type"] in self.platforms
                and x["version"] >= self.min_version
                and x["percent"] >= self.min_percentage,
                self.data_browsers,
            )
        )
        # filter based on a specific browser request
        if request:
            filtered_useragents = list(
                filter(lambda x: x["browser"] == request, filtered_useragents)
            )

        return filtered_useragents

    def getBrowser(self, request: str) -> BrowserUserAgentData:
        """Get a random browser user agent with additional data.

        Args:
            request (str): The browser name to get. Special keyword "random" will return a user
                agent from any browser allowed by the instance's `self.browsers` filter.

        Returns:
            BrowserUserAgentData: The user agent with additional data.
        """
        try:
            # Handle request value
            for value, replacement in settings.REPLACEMENTS.items():
                request = request.replace(value, replacement)
            request = request.lower()
            request = settings.SHORTCUTS.get(request, request)

            if request == "random":
                # Filter the browser list based on the browsers array using lambda
                # And based on OS list
                # And percentage is bigger then min percentage
                # And convert the iterator back to a list
                filtered_browsers = self._filter_useragents()
            else:
                # Or when random isn't select, we filter the browsers array based on the 'request' using lamba
                # And based on OS list
                # And percentage is bigger then min percentage
                # And convert the iterator back to a list
                filtered_browsers = self._filter_useragents(request=request)

            # Pick a random browser user-agent from the filtered browsers
            # And return the full dict
            return random.choice(filtered_browsers)  # noqa: S311
        except (KeyError, IndexError):
            logger.warning(
                f"Error occurred during getting browser: {request}, "
                "but was suppressed with fallback.",
            )
            # Return fallback object
            return {
                "useragent": self.fallback,
                "percent": 100.0,
                "type": "pc",
                "system": "Chrome 122.0 Win10",
                "browser": "chrome",
                "version": 122.0,
                "os": "win10",
            }

    def __getitem__(self, attr: str) -> Union[str, Any]:
        """Get a user agent by key lookup, as if it were a dictionary (i.e., `ua['random']`).

        Args:
            attr (str): Browser name to get.

        Returns:
            Union[str, Any]: The user agent string if not a `self.safe_attr`, otherwise the
                attribute value.
        """
        return self.__getattr__(attr)

    def __getattr__(self, attr: str) -> Union[str, Any]:
        """Get a user agent by attribute lookup.

        Args:
            attr (str): Browser name to get. Special keyword "random" will return a user agent from
                any browser allowed by the instance's `self.browsers` filter.

        Returns:
            Union[str, Any]: The user agent string if not a `self.safe_attr`, otherwise the
                attribute value.
        """
        if attr in self.safe_attrs:
            return super(UserAgent, self).__getattribute__(attr)

        try:
            # Handle input value
            for value, replacement in settings.REPLACEMENTS.items():
                attr = attr.replace(value, replacement)
            attr = attr.lower()
            attr = settings.SHORTCUTS.get(attr, attr)

            if attr == "random":
                # Filter the browser list based on the browsers array using lambda
                # And based on OS list
                # And percentage is bigger then min percentage
                # And convert the iterator back to a list
                filtered_browsers = self._filter_useragents()
            else:
                # Or when random isn't select, we filter the browsers array based on the 'attr' using lamba
                # And based on OS list
                # And percentage is bigger then min percentage
                # And convert the iterator back to a list
                filtered_browsers = self._filter_useragents(request=attr)

            # Pick a random browser user-agent from the filtered browsers
            # And return the useragent string.
            return random.choice(filtered_browsers).get("useragent")  # noqa: S311
        except (KeyError, IndexError):
            logger.warning(
                f"Error occurred during getting browser: {attr}, "
                "but was suppressed with fallback.",
            )
            return self.fallback

    @property
    def chrome(self) -> str:
        """Get a random Chrome user agent."""
        return self.__getattr__("chrome")

    @property
    def googlechrome(self) -> str:
        """Get a random Chrome user agent."""
        return self.chrome

    @property
    def edge(self) -> str:
        """Get a random Edge user agent."""
        return self.__getattr__("edge")

    @property
    def firefox(self) -> str:
        """Get a random Firefox user agent."""
        return self.__getattr__("firefox")

    @property
    def ff(self) -> str:
        """Get a random Firefox user agent."""
        return self.firefox

    @property
    def safari(self) -> str:
        """Get a random Safari user agent."""
        return self.__getattr__("safari")

    @property
    def random(self) -> str:
        """Get a random user agent."""
        return self.__getattr__("random")

    @property
    def getFirefox(self) -> BrowserUserAgentData:
        """Get a random Firefox user agent, with additional data."""
        return self.getBrowser("firefox")

    @property
    def getChrome(self) -> BrowserUserAgentData:
        """Get a random Chrome user agent, with additional data."""
        return self.getBrowser("chrome")

    @property
    def getEdge(self) -> BrowserUserAgentData:
        """Get a random Edge user agent, with additional data."""
        return self.getBrowser("edge")

    @property
    def getSafari(self) -> BrowserUserAgentData:
        """Get a random Safari user agent, with additional data."""
        return self.getBrowser("safari")

    @property
    def getRandom(self) -> BrowserUserAgentData:
        """Get a random user agent, with additional data."""
        return self.getBrowser("random")


# common alias
UserAgent = FakeUserAgent
