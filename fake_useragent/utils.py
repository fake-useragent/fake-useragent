# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import contextlib
import inspect
import io
import json
import os
import re
import ssl

from fake_useragent.log import logger


try:  # Python 2 # pragma: no cover
    from urllib2 import urlopen, Request, URLError

    str_types = (unicode, str)  # noqa
    text = unicode  # noqa
except ImportError:  # Python 3 # pragma: no cover
    from urllib.request import urlopen, Request
    from urllib.error import URLError

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

urlopen_has_ssl_context = 'context' in urlopen_args


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

                with contextlib.closing(urlopen(
                    request,
                    timeout=settings.HTTP_TIMEOUT,
                    context=context,
                )) as response:
                    return response.read()
            else:  # ssl context is not supported ;(
                with contextlib.closing(urlopen(
                    request,
                    timeout=settings.HTTP_TIMEOUT,
                )) as response:
                    return response.read()
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
                    'Sleeping for %s seconds',
                    settings.HTTP_DELAY,
                )
                sleep(settings.HTTP_DELAY)


def get_browsers(verify_ssl=True):
    """
    very very hardcoded/dirty re/split stuff, but no dependencies
    """
    html = get(settings.BROWSERS_STATS_PAGE, verify_ssl=verify_ssl)
    html = html.decode('utf-8')
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


def get_version(browser, info):
    try:
        # serach smth like "Chrome/60"
        temp = re.search(re.escape(browser.capitalize()) + r'/(\d+)', info)
        # getting only version digits
        return int(temp.group(0)[len(browser)+1:])
    except AttributeError:  # there are chrome/v1.0.0 and this handels it
        temp = re.search(re.escape(browser.capitalize()) + r'/v(\d+)', info)
        return int(temp.group(0)[len(browser)+2:])


def get_browser_versions(browser, verify_ssl=True):

        useragents_list = []

        # Because ie fucking special and we must handel it another way
        if browser == 'internet-explorer':
            return get_browser_versions_ie(browser)

        for page in range(1, 4):  # getting info from first 3 pages
            html = get(
                    "{}{}/{}?order_by=-times_seen".format(settings.BROWSER_BASE_PAGE, browser, page),
                    verify_ssl=verify_ssl,
                    )

            html = html.decode('utf-8')

            # getting td and than tr tags
            table = re.findall(r'<table class="table table-striped table-hover table-bordered table-useragents">(.*?)</table>', html, re.DOTALL)[0]
            match_obj = re.findall(r'<tr>(.*?)</tr>', table, re.M|re.I|re.S)

            for obj in match_obj[1:]:
                tds = re.findall(r'<td(.*?)</td>', obj, re.DOTALL)
                if tds[3][1:] == "Computer":
                    # deleting tags and stuff like that around info we need
                    info = re.sub(r'><a href=(.*?)>', '', tds[0])
                    info = re.sub('class="useragent"', '', info)
                    info = re.sub('</a>', '', info)
                    useragents_list.append(info)

            # bubble sort by versions
            for elem in range(len(useragents_list)-1, 0, -1):
                for i in range(elem):
                    if get_version(browser, useragents_list[i]) > get_version(browser, useragents_list[i+1]):
                        temp = useragents_list[i]
                        useragents_list[i] = useragents_list[i+1]
                        useragents_list[i+1] = temp

        return useragents_list[len(useragents_list):len(useragents_list)-50:-1]


def get_version_ie(info):
    if info[1].isdigit():
        return int(info[:2])
    else:
        return int(info[0])


def get_browser_versions_ie(browser, verify_ssl=True):

    useragents_list = []

    for page in range(1, 4):  # getting info from first 3 pages
        html = get(
                "{}{}/{}?order_by=-times_seen".format(settings.BROWSER_BASE_PAGE, browser, page),
                verify_ssl=verify_ssl,
                )

        html = html.decode('utf-8')

        # getting td and than tr tags
        table = re.findall(r'<table class="table table-striped table-hover table-bordered table-useragents">(.*?)</table>', html, re.DOTALL)[0]
        match_obj = re.findall(r'<tr>(.*?)</tr>', table, re.M|re.I|re.S)

        for obj in match_obj[1:]:
            tds = re.findall(r'<td(.*?)</td>', obj, re.DOTALL)
            if tds[3][1:] == "Computer":
                # deleting tags and stuff like that around info we need
                info = re.sub(r'><a href=(.*?)>', '', tds[0])
                info = re.sub('class="useragent"', '', info)
                info = re.sub('</a>', '', info)

                if tds[1][-2] == ' ':
                    continue

                if tds[1][-2] == '>':  # some versions are 1-digit, some 2-digit
                    useragents_list.append(info + ' ' + str(tds[1][-1:]))
                elif tds[1][-2] == '.':  # some looks like '5.5'
                    useragents_list.append(info + ' ' + str(tds[1][-3:]))
                else:
                    useragents_list.append(info + ' ' + str(tds[1][-2:]))

    counter = 0
    result = []
    for elem in useragents_list:
        if '11' in elem[:-4] or '10' in elem[:-4]:
            result.append(elem[:-3])
            counter += 1
        if counter == 50:
            break

    return result


def load(use_cache_server=True, verify_ssl=True):
    browsers_dict = {}
    randomize_dict = {}

    try:
        for item in get_browsers(verify_ssl=verify_ssl):
            browser, percent = item

            browser_key = browser

            for value, replacement in settings.REPLACEMENTS.items():
                browser_key = browser_key.replace(value, replacement)

            browser_key = browser_key.lower()

            browsers_dict[browser_key] = get_browser_versions(
                browser,
                verify_ssl=verify_ssl,
            )

            # it is actually so bad way for randomizing, simple list with
            # browser_key's is event better
            # I've failed so much a lot of years ago.
            # Ideas for refactoring
            # {'chrome': <percantage|int>, 'firefox': '<percatage|int>'}
            for _ in range(int(float(percent) * 10)):
                randomize_dict[str(len(randomize_dict))] = browser_key
    except Exception as exc:
        if not use_cache_server:
            raise exc

        logger.warning(
            'Error occurred during loading data. '
            'Trying to use cache server %s',
            settings.CACHE_SERVER,
            exc_info=exc,
        )
        try:
            ret = json.loads(get(
                settings.CACHE_SERVER,
                verify_ssl=verify_ssl,
            ).decode('utf-8'))
        except (TypeError, ValueError):
            raise FakeUserAgentError('Can not load data from cache server')
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

        if not isinstance(dumped, text):  # Python 2
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


def update(path, use_cache_server=True, verify_ssl=True):
    rm(path)

    write(path, load(use_cache_server=use_cache_server, verify_ssl=verify_ssl))


def load_cached(path, use_cache_server=True, verify_ssl=True):
    if not exist(path):
        update(path, use_cache_server=use_cache_server, verify_ssl=verify_ssl)

    return read(path)


from fake_useragent import settings  # noqa # isort:skip
from fake_useragent.errors import FakeUserAgentError  # noqa # isort:skip
