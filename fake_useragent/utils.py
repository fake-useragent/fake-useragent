import os
import re

from . import settings

try:  # Python 2
    from urllib import urlopen, quote_plus
except ImportError:  # Python 3
    from urllib.request import urlopen
    from urllib.parse import quote_plus
try:
    import json
except ImportError:
    import simplejson as json


def get(url, annex=None):
    if annex is not None:
        url = url % (quote_plus(annex), )
    return urlopen(url).read()


def get_browsers():
    """
    very very hardcoded/dirty re/split stuff, but no dependencies
    """
    html = get(settings.BROWSERS_STATS_PAGE)
    html = html.decode('windows-1252')
    html = html.split('<table class="w3-table-all notranslate">')[1]
    html = html.split('</table>')[0]

    browsers = re.findall(r'\.asp">(.+?)<', html, re.UNICODE)

    for value, override in settings.OVERRIDES:
        browsers = [
            value if browser == override else browser
            for browser in browsers
        ]

    browsers_statistics = re.findall(
        r'td\sclass="right">(.+?)\s', html, re.UNICODE
    )

    # TODO: ensure encoding

    return list(zip(browsers, browsers_statistics))


def get_browser_versions(browser):
    """
    very very hardcoded/dirty re/split stuff, but no dependencies
    """
    html = get(settings.BROWSER_BASE_PAGE, browser)
    html = html.decode('iso-8859-1')
    html = html.split('<div id=\'liste\'>')[1]
    html = html.split('</div>')[0]

    browsers_iter = re.finditer(r'\.php\'>(.+?)</a', html, re.UNICODE)

    count = 0

    browsers = []

    for browser in browsers_iter:
        if 'more' in browser.group(1).lower():
            continue

        # TODO: ensure encoding
        browsers.append(browser.group(1))
        count += 1

        if count == settings.BROWSERS_COUNT_LIMIT:
            break

    return browsers


def load():
    browsers_dict = {}
    randomize_dict = {}

    for item in get_browsers():
        browser, percent = item

        browser_key = browser

        for replacement in settings.REPLACEMENTS:
            browser_key = browser_key.replace(replacement, '')

        browser_key = browser_key.lower()

        browsers_dict[browser_key] = get_browser_versions(browser)

        for counter in range(int(float(percent))):
            randomize_dict[str(len(randomize_dict))] = browser_key

    db = {}
    db['browsers'] = browsers_dict
    db['randomize'] = randomize_dict

    return db


def write(data):
    data = json.dumps(data, ensure_ascii=False)

    # no codecs\with for python 2.5
    f = open(settings.DB, 'w+')
    f.write(data)
    f.close()


def read():
    # no codecs\with for python 2.5
    f = open(settings.DB, 'r')
    data = f.read()
    f.close()

    return json.loads(data)


def exist():
    return os.path.isfile(settings.DB)


def rm():
    if exist():
        os.remove(settings.DB)


def update():
    if exist():
        rm()

    write(load())


def load_cached():
    if not exist():
        update()

    return read()
