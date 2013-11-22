import re
import os
try:  # Python 2
    from urllib import urlopen, quote_plus
except ImportError:  # Python 3
    from urllib.request import urlopen
    from urllib.parse import quote_plus
try:
    import json
except ImportError:
    import simplejson as json

from fake_useragent import settings


def get(url, annex=None):
    if not annex is None:
        url = url % (quote_plus(annex), )
    return urlopen(url).read()


def get_browsers():
    '''
    very very hardcoded/dirty re/split stuff, but no dependencies
    '''
    html = get(settings.BROWSERS_STATS_PAGE)
    html = html.decode('windows-1252')
    html = html.split('<table class="reference notranslate">')[1]
    html = html.split('<td>&nbsp;</td>')[0]

    browsers = re.findall(r'\.asp">(.+?)<', html, re.UNICODE)
    browsers_statistics = re.findall(r'"right">(.+?)\s', html, re.UNICODE)

    # TODO: ensure encoding
    # browsers = list(map(
    #     lambda stat: stat.encode('utf-8', 'ignore'), browsers)
    # )
    # browsers_statistics = list(
    #     map(
    #         lambda stat: stat.encode('utf-8', 'ignore'),
    #         browsers_statistics
    #     )
    # )

    return list(zip(browsers, browsers_statistics))


def get_browser_versions(browser):
    '''
    very very hardcoded/dirty re/split stuff, but no dependencies
    '''
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
        # browser.group(1).encode('utf-8', 'ignore')
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
        clear_browser = browser.replace(' ', '').lower()

        browsers_dict[clear_browser] = get_browser_versions(browser)

        for counter in range(int(float(percent))):
            randomize_dict[str(len(randomize_dict))] = clear_browser

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

    return json.loads(data, 'utf-8')


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
