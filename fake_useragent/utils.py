import contextlib
import inspect
import io
import json
import os
import re
import ssl

from fake_useragent.log import logger

try:  # Python 2 # pragma: no cover
    from urllib import quote_plus

    from urllib2 import Request, URLError, urlopen

    str_types = (unicode, str)  # noqa
    text = unicode  # noqa
except ImportError:  # Python 3 # pragma: no cover
    from urllib.error import URLError
    from urllib.parse import quote_plus
    from urllib.request import Request, urlopen

    str_types = (str,)
    text = str

# gevent monkey patched environment check
try:  # pragma: no cover
    import socket

    import gevent.socket

    if socket.socket is gevent.socket.socket:
        from gevent import sleep
    else:
        from time import sleep
except (ImportError, AttributeError):  # pragma: no cover
    from time import sleep


try:
    urlopen_args = inspect.getfullargspec(urlopen).kwonlyargs
except AttributeError:
    urlopen_args = inspect.getargspec(urlopen).args

urlopen_has_ssl_context = "context" in urlopen_args


def get(url, verify_ssl=True):
    attempt = 0

    while True:
        request = Request(url)

        attempt += 1

        try:
            if urlopen_has_ssl_context:
                if not verify_ssl:
                    context = ssl._create_unverified_context()
                else:
                    context = None

                with contextlib.closing(
                    urlopen(
                        request,
                        timeout=settings.HTTP_TIMEOUT,
                        context=context,
                    )
                ) as response:
                    return response.read()
            else:  # ssl context is not supported ;(
                with contextlib.closing(
                    urlopen(
                        request,
                        timeout=settings.HTTP_TIMEOUT,
                    )
                ) as response:
                    return response.read()
        except (URLError, OSError) as exc:
            logger.debug(
                "Error occurred during fetching %s",
                url,
                exc_info=exc,
            )

            if attempt == settings.HTTP_RETRIES:
                raise FakeUserAgentError("Maximum amount of retries reached")
            else:
                logger.debug(
                    "Sleeping for %s seconds",
                    settings.HTTP_DELAY,
                )
                sleep(settings.HTTP_DELAY)


def get_browser_user_agents(browser, verify_ssl=True):
    """
    Retrieve browser user agent strings
    """
    html = get(
        settings.BROWSER_BASE_PAGE.format(browser=quote_plus(browser)),
        verify_ssl=verify_ssl,
    )
    html = html.decode("iso-8859-1")
    html = html.split("<div id='liste'>")[1]
    html = html.split("</div>")[0]

    pattern = r"<a href=\'/.*?>(.+?)</a>"
    browsers_iter = re.finditer(pattern, html, re.UNICODE)

    browsers = []

    for browser in browsers_iter:
        if "more" in browser.group(1).lower():
            continue

        browsers.append(browser.group(1))

        if len(browsers) == settings.BROWSERS_COUNT_LIMIT:
            break

    if not browsers:
        raise FakeUserAgentError(
            "No browser user-agent strings found for browser: {browser}".format(
                browser=browser
            )
        )

    return browsers


def load(browsers, use_cache_server=True, verify_ssl=True):
    browsers_dict = {}

    try:
        # For each browser receive the user-agent strings
        for browser_name in browsers:
            browser_name = browser_name.lower().strip()
            browsers_dict[browser_name] = get_browser_user_agents(
                browser_name,
                verify_ssl=verify_ssl,
            )
    except Exception as exc:
        if not use_cache_server:
            raise exc

        logger.warning(
            "Error occurred during loading data. Trying to use cache server file %s",
            settings.CACHE_SERVER,
            exc_info=exc,
        )
        try:
            data = {}
            jsonLines = get(
                settings.CACHE_SERVER,
                verify_ssl=verify_ssl,
            ).decode("utf-8")
            for line in jsonLines.splitlines():
                data.update(json.loads(line))
            ret = data
        except (TypeError, ValueError):
            raise FakeUserAgentError("Can not load JSON Lines data from cache server")
    else:
        ret = browsers_dict

    if not ret:
        raise FakeUserAgentError("Data dictionary is empty", ret)

    if not isinstance(ret, dict):
        raise FakeUserAgentError("Data is not dictionary ", ret)

    return ret


def write(path, data):
    with open(path, encoding="utf-8", mode="w") as fp:
        dumped = json.dumps(data)

        if not isinstance(dumped, text):  # Python 2
            dumped = dumped.decode("utf-8")

        fp.write(dumped)


def read(path):
    with open(path, encoding="utf-8") as fp:
        return json.loads(fp.read())


def exist(path):
    return os.path.isfile(path)


def rm(path):
    if exist(path):
        os.remove(path)


def update(path, browsers, use_cache_server=True, verify_ssl=True):
    rm(path)

    write(
        path, load(browsers, use_cache_server=use_cache_server, verify_ssl=verify_ssl)
    )


def load_cached(path, browsers, use_cache_server=True, verify_ssl=True):
    if not exist(path):
        update(path, browsers, use_cache_server=use_cache_server, verify_ssl=verify_ssl)

    return read(path)


from fake_useragent import settings  # noqa # isort:skip
from fake_useragent.errors import FakeUserAgentError  # noqa # isort:skip
