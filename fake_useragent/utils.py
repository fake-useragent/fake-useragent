from __future__ import absolute_import, unicode_literals

import io
import json
import os
import re

from fake_useragent.log import logger

try:  # Python 2
    from urllib2 import urlopen, Request, URLError
    from urllib import quote_plus

    str_types = (unicode, str)  # noqa
    text = unicode  # noqa
except ImportError:  # Python 3
    from urllib.request import urlopen, Request
    from urllib.parse import quote_plus
    from urllib.error import URLError

    str_types = (str,)
    text = str

try:  # gevent monkey patched environment check
    import socket
    import gevent.socket

    if socket.socket is gevent.socket.socket:
        from gevent import sleep
    else:
        from time import sleep
except (ImportError, AttributeError):
    from time import sleep


def get(url):
    request = Request(url)

    attempt = 0

    while True:
        attempt += 1

        try:
            return urlopen(request, timeout=settings.HTTP_TIMEOUT).read()
        except (URLError, OSError) as exc:
            logger.debug(
                'Error occurred during fetching %s',
                url,
                exc_info=exc,
            )

            if attempt == settings.HTTP_RETRIES:
                raise FakeUserAgentError('Maximum amount of retries reached')
            else:
                logger.debug(
                    'Sleeping for %s secconds',
                    settings.HTTP_TIMEOUT,
                )
                sleep(settings.HTTP_TIMEOUT)


def get_browsers():
    """
    very very hardcoded/dirty re/split stuff, but no dependencies
    """
    html = get(settings.BROWSERS_STATS_PAGE)
    html = html.decode('windows-1252')
    html = html.split('<table class="w3-table-all notranslate">')[1]
    html = html.split('</table>')[0]

    pattern = r'\.asp">(.+?)<'
    browsers = re.findall(pattern, html, re.UNICODE)

    browsers = [
        settings.OVERRIDES.get(browser, browser)
        for browser in browsers
    ]

    pattern = r'td\sclass="right">(.+?)\s'
    browsers_statistics = re.findall(pattern, html, re.UNICODE)

    return list(zip(browsers, browsers_statistics))


def get_browser_versions(browser):
    """
    very very hardcoded/dirty re/split stuff, but no dependencies
    """
    html = get(settings.BROWSER_BASE_PAGE.format(browser=quote_plus(browser)))
    html = html.decode('iso-8859-1')
    html = html.split('<div id=\'liste\'>')[1]
    html = html.split('</div>')[0]

    pattern = r'\?id=\d+\'>(.+?)</a'
    browsers_iter = re.finditer(pattern, html, re.UNICODE)

    browsers = []

    for browser in browsers_iter:
        if 'more' in browser.group(1).lower():
            continue

        browsers.append(browser.group(1))

        if len(browsers) == settings.BROWSERS_COUNT_LIMIT:
            break

    return browsers


def load():
    browsers_dict = {}
    randomize_dict = {}

    try:
        for item in get_browsers():
            browser, percent = item

            browser_key = browser

            for value, replacement in settings.REPLACEMENTS.items():
                browser_key = browser_key.replace(value, replacement)

            browser_key = browser_key.lower()

            browsers_dict[browser_key] = get_browser_versions(browser)

            # it is actually so bad way for randomizing, simple list with
            # browser_key's is event better
            # I've failed so much a lot of years ago.
            # Ideas for refactoring
            # {'chrome': <percantage|int>, 'firefox': '<percatage|int>'}
            for _ in range(int(float(percent) * 10)):
                randomize_dict[str(len(randomize_dict))] = browser_key
    except Exception as exc:
        logger.warning(
            'Error occurred during formatting data. '
            'Trying to use fallback server %s',
            settings.CACHE_SERVER,
            exc_info=exc,
        )
        try:
            ret = json.loads(get(settings.CACHE_SERVER).decode('utf-8'))
        except (UnicodeDecodeError, TypeError, ValueError):
            raise FakeUserAgentError('Can not load data from cached server')
    else:
        ret = {
            'browsers': browsers_dict,
            'randomize': randomize_dict,
        }

    if not isinstance(ret, dict):
        raise FakeUserAgentError('Data is not dictionary ', ret)

    for param in ['browsers', 'randomize']:
        if param not in ret:
            raise FakeUserAgentError('Missing data param: ', param)

        if not isinstance(ret[param], dict):
            raise FakeUserAgentError('Data param is not dictionary', ret[param])  # noqa

        if not ret[param]:
            raise FakeUserAgentError('Data param is empty', ret[param])

    return ret


# TODO: drop these useless functions


def write(path, data):
    with io.open(path, encoding='utf-8', mode='wt') as fp:
        dumped = json.dumps(data)

        if not isinstance(dumped, text):
            dumped = dumped.decode('utf-8')

        fp.write(dumped)


def read(path):
    with io.open(path, encoding='utf-8', mode='rt') as fp:
        return json.loads(fp.read())


def exist(path):
    return os.path.isfile(path)


def rm(path):
    if exist(path):
        os.remove(path)


def update(path):
    rm(path)

    write(path, load())


def load_cached(path):
    if not exist(path):
        update(path)

    return read(path)


from fake_useragent import settings  # noqa # isort:skip
from fake_useragent.errors import FakeUserAgentError  # noqa # isort:skip
