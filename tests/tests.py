from __future__ import absolute_import, unicode_literals

import os
import json
import tempfile
import uuid

from fake_useragent import FakeUserAgentError, UserAgent, settings, utils

settings.HTTP_TIMEOUT = 2

settings.HTTP_RETRIES = 1

settings.HTTP_DELAY = 0


def clear(path):
    try:
        os.remove(path)
    except OSError:
        pass


def check_dict(data):
    assert isinstance(data, dict)
    assert data.get('randomize')
    assert data.get('browsers')
    assert data.get('browsers').get('chrome')
    assert data.get('browsers').get('firefox')
    assert data.get('browsers').get('opera')
    assert data.get('browsers').get('safari')
    assert data.get('browsers').get('internetexplorer')


def test_get_cache():
    html = utils.get(settings.CACHE_SERVER)

    data = json.loads(html.decode('utf-8'))

    check_dict(data)


def test_get_services():
    service_failed = False

    global service_failed

    try:
        html = utils.get(settings.BROWSERS_STATS_PAGE)

        assert len(html) > 0

        html = utils.get(settings.BROWSER_BASE_PAGE.format(browser='Firefox'))

        assert len(html) > 0

    except FakeUserAgentError:
        service_failed = True


def test_get_browsers():
    if not service_failed:
        browsers = utils.get_browsers()

        browser_list = []

        for browser in browsers:
            # ie becomes popular !? xD
            if browser[0] == 'Internet Explorer':
                assert int(float(browser[1])) < 20
            browser_list.append(browser[0])

        assert len(browser_list) == 5

        assert 'Firefox' in browser_list
        assert 'Opera' in browser_list
        assert 'Chrome' in browser_list
        assert 'Internet Explorer' in browser_list
        assert 'Safari' in browser_list

        global browser_list


def test_get_browser_versions():
    if not service_failed:
        for browser in browser_list:
            assert len(utils.get_browser_versions(browser)) == settings.BROWSERS_COUNT_LIMIT  # noqa


def test_load():
    fake_useragent_dict = utils.load()

    check_dict(fake_useragent_dict)

    global fake_useragent_dict


def test_write():
    clear(settings.DB)

    utils.write(settings.DB, fake_useragent_dict)

    assert os.path.isfile(settings.DB)


def test_exists():
    assert utils.exist(settings.DB)


def test_read():
    check_dict(utils.read(settings.DB))


def test_rm():
    assert utils.exist(settings.DB)
    clear(settings.DB)
    assert not utils.exist(settings.DB)


def test_update():
    assert not utils.exist(settings.DB)
    utils.update(settings.DB)
    assert utils.exist(settings.DB)
    utils.update(settings.DB)
    assert utils.exist(settings.DB)


def test_load_cached():
    data = utils.load_cached(settings.DB)

    check_dict(data)

    clear(settings.DB)

    data = utils.load_cached(settings.DB)

    check_dict(data)


def test_safe_attrs():
    clear(settings.DB)

    ua = UserAgent(safe_attrs=('foo',))

    try:
        ua.foo
    except AttributeError:
        pass


def test_user_agent():
    clear(settings.DB)
    assert not utils.exist(settings.DB)

    ua = UserAgent(cache=False)

    assert ua.ie is not None
    assert ua.msie is not None
    assert ua.internetexplorer is not None
    assert ua.internet_explorer is not None
    assert ua['internet explorer'] is not None
    assert ua.google is not None
    assert ua.chrome is not None
    assert ua.googlechrome is not None
    assert ua.google_chrome is not None
    assert ua['google chrome'] is not None
    assert ua.firefox is not None
    assert ua.ff is not None
    assert ua.ie is not None
    assert ua.safari is not None
    assert ua.random is not None
    assert ua['random'] is not None

    try:
        ua.non_existing
    except FakeUserAgentError:
        pass
    else:
        assert False

    try:
        assert ua['non_existing']
    except FakeUserAgentError:
        pass
    else:
        assert False

    data1 = ua.data

    ua.update(settings.DB)

    data2 = ua.data

    assert data1 == data2
    assert data1 is not data2

    clear(settings.DB)
    del ua

    ua = UserAgent()

    assert utils.exist(settings.DB)

    data1 = ua.data

    clear(settings.DB)

    ua.update(settings.DB)

    assert utils.exist(settings.DB)

    data2 = ua.data

    assert data1 == data2
    assert data1 is not data2

    clear(settings.DB)


def test_custom_path():
    location = os.path.join(
        tempfile.gettempdir(),
        'fake_useragent' + uuid.uuid1().hex + '.json',
    )

    ua = UserAgent(path=location)

    assert utils.exist(location)

    check_dict(ua.data)

    mtime = os.path.getmtime(location)

    ua.update()

    assert os.path.getmtime(location) != mtime

    clear(location)


def test_cache_server():
    clear(settings.DB)

    settings.BROWSER_BASE_PAGE = 'http://example.com/'

    settings.BROWSERS_STATS_PAGE = 'http://example.com/'

    ua = UserAgent()

    check_dict(ua.data)

    clear(settings.DB)


def test_fallback():
    clear(settings.DB)

    fallback = 'Foo Browser'

    settings.CACHE_SERVER = 'http://example.com/'

    ua = UserAgent(fallback=fallback)

    assert ua.random == fallback

    assert ua.ie == fallback

    try:
        ua = UserAgent(fallback=True)
    except AssertionError:
        pass
    else:
        assert False

    clear(settings.DB)

    # json cached server response

    settings.CACHE_SERVER = 'https://httpbin.org/get'

    ua = UserAgent(fallback=fallback)

    assert ua.random == fallback

    assert ua.ie == fallback


def test_version():
    import fake_useragent

    assert fake_useragent.VERSION == settings.__version__


def test_aliases():
    from fake_useragent import FakeUserAgent, UserAgentError

    assert FakeUserAgentError is UserAgentError

    assert UserAgent is FakeUserAgent
