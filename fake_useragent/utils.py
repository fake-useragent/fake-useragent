# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import io
import json
import os
import re
from typing import Dict, List
import urllib
import random
from urllib.error import URLError, HTTPError
from time import sleep

from fake_useragent.log import logger
from .randomize import DataRandomize, AbstractRandomize
from bs4 import BeautifulSoup 
import requests
from requests.exceptions import ReadTimeout, RequestException

def read(path: str) -> Dict[str, List]:
    with io.open(path, encoding='utf-8', mode='rt') as fp:
        return json.loads(fp.read())


def get_with_agent(url: str, user_agents: Dict[str, List]):
    """
    takes a url and returns the response if 200 else raise exception
    """
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': random.choices(
            user_agents['browsers'],
            user_agents['percents'])[0]
        })
    attempt = 0
    while True:

        attempt += 1
        try:
            return requests.get(url=url, headers=headers, timeout=settings.HTTP_TIMEOUT)

        except (ReadTimeout, RequestException) as exc:
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


def get_browsers(useragents):
    """
    very very hardcoded/dirty re/split stuff, but no dependencies
    """
    html = get_with_agent(settings.BROWSERS_STATS_PAGE, useragents)
    html = html.text
    html = html.split('<table class="ws-table-all notranslate">')[1]
    html = html.split('</table>')[0]

    pattern = r'\.asp">(.+?)<'
    browsers = re.findall(pattern, html, re.UNICODE)

    pattern = r'td\sclass="right">(.+?)\s'
    browsers_statistics = re.findall(pattern, html, re.UNICODE)
    return list(zip(browsers, browsers_statistics))


def get_browser_versions(browser, useragents):
    """
    very very hardcoded/dirty re/split stuff, but no dependencies
    """
    browsers = []
    html = get_with_agent(
        settings.BROWSER_BASE_PAGE.format(browser=browser),
        user_agents=useragents,
    ).text
    versions_links = BeautifulSoup(html, 'html.parser').select(".compact_list li a ")[:11]
    for link in versions_links:
        html = get_with_agent(settings.BROWSER_HOST+link.get('href'), useragents)

        html = html.text
        html = html.split('<ul class=\'agents_list\'>')[1]
        html = html.split('</ul>')[0]

        pattern = r"'>(.+?)<"
        browsers_iter = re.finditer(pattern, html, re.UNICODE)

        for browser in browsers_iter:
            browsers.append(browser.group(1))

            if len(browsers) == settings.BROWSERS_COUNT_LIMIT:
                return browsers

    if not browsers:
        raise FakeUserAgentError(
            'No browsers version found for {browser}'.format(browser=browser))

    return browsers


# browser_dict {"<browser>: ["<useragents>"]}
# randomize_dict {'percents': [<n|float>], 'browsers' : ['<browser_key|str>']}


def load(use_fallback=True):
    browsers_dict = dict()
    randomize_dict = {'percents': [], 'browsers': []}
    stored_useragents = read(settings.FALLBACK_PATH)

    try:
        for item in get_browsers(stored_useragents):
            browser, percent = item

            browser_key = browser.lower()

            browsers_dict[browser_key] = get_browser_versions(
                browser_key,
                stored_useragents
                )

            randomize_dict['percents'].append(float(percent))
            randomize_dict['browsers'].append(browser_key)
    except Exception as exc:
        if not use_fallback:
            raise exc

        logger.warning(
            'Error occurred during loading data. '
            'Trying to use Fallback useragents %s',
            settings.FALLBACK_PATH,
            exc_info=exc,
        )
        try:
            print("here")
            ret = DataRandomize.fallback(stored_useragents)
        except Exception:
            raise FakeUserAgentError('Can not load data from cache server')
    else:
        ret = DataRandomize.parsed(
                randomize_dict=randomize_dict,
                browsers_dict=browsers_dict
            )

    if not isinstance(ret, AbstractRandomize):
        raise FakeUserAgentError('Data is not valid ', ret)
    print(ret.useragents)
    return ret


# TODO: drop these useless functions


def write(path, data):
    with io.open(path, encoding='utf-8', mode='wt') as fp:
        dumped = json.dumps(data)

        if not isinstance(dumped, text):  # Python 2
            dumped = dumped.decode('utf-8')

        fp.write(dumped)


def read(path: str) -> List[Dict]:
    with io.open(path, encoding='utf-8', mode='rt') as fp:
        return json.loads(fp.read())


def exist(path):
    return os.path.isfile(path)


def rm(path):
    if exist(path):
        os.remove(path)


def update(path, use_cache_server=True):
    rm(path)

    write(path, load(use_cache_server=use_cache_server))


def load_cached(path, use_cache_server=True):
    if not exist(path):
        update(path, use_cache_server=use_cache_server)

    return read(path)


from fake_useragent import settings  # noqa # isort:skip
from fake_useragent.errors import FakeUserAgentError  # noqa # isort:skip
