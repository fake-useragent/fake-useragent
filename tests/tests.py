import os
from fake_useragent import UserAgent
from fake_useragent import settings
from fake_useragent import utils


def clear():
    try:
        os.unlink((settings.DB))
    except OSError:
        pass


def check_dict(data):
    assert data.get('randomize')
    assert data.get('browsers')
    assert data.get('browsers').get('chrome')
    assert data.get('browsers').get('firefox')
    assert data.get('browsers').get('opera')
    assert data.get('browsers').get('safari')
    assert data.get('browsers').get('internetexplorer')


def test_get_no_args():
    html = utils.get(settings.BROWSERS_STATS_PAGE)

    assert len(html) > 0


def test_get_args():
    html = utils.get(settings.BROWSER_BASE_PAGE, 'Firefox')

    assert len(html) > 0


def test_get_browsers():
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
    for browser in browser_list:
        assert len(utils.get_browser_versions(browser)) == \
            settings.BROWSERS_COUNT_LIMIT


def test_load():
    fake_useragent_dict = utils.load()

    check_dict(fake_useragent_dict)

    global fake_useragent_dict


def test_write():
    clear()

    assert not os.path.isfile(settings.DB)

    utils.write(fake_useragent_dict)

    assert os.path.isfile(settings.DB)


def test_read():
    data = utils.read()

    check_dict(data)

    assert os.path.isfile(settings.DB)


def test_exists():
    assert utils.exist()


def test_rm():
    assert utils.exist()
    utils.rm()
    assert not utils.exist()


def test_update():
    assert not utils.exist()
    utils.update()
    assert utils.exist()
    utils.update()
    assert utils.exist()


def test_load_cached():
    data = utils.load_cached()

    check_dict(data)

    clear()

    data = utils.load_cached()

    check_dict(data)


def test_user_agent():
    clear()
    assert not utils.exist()

    ua = UserAgent(cache=False)

    assert not ua.ie is None
    assert not ua.msie is None
    assert not ua.internetexplorer is None
    assert not ua.internet_explorer is None
    assert not ua['internet explorer'] is None
    assert not ua.google is None
    assert not ua.chrome is None
    assert not ua.googlechrome is None
    assert not ua.google_chrome is None
    assert not ua['google chrome'] is None
    assert not ua.firefox is None
    assert not ua.ff is None
    assert not ua.ie is None
    assert not ua.safari is None
    assert not ua.random is None
    assert not ua['random'] is None

    assert ua.non_existing is None
    assert ua['non_existing'] is None

    data1 = ua.data

    ua.update()

    data2 = ua.data

    assert data1 == data2
    assert not data1 is data2

    clear()
    del ua

    ua = UserAgent()

    assert utils.exist()

    data1 = ua.data

    clear()

    ua.update()

    assert utils.exist()

    data2 = ua.data

    assert data1 == data2
    assert not data1 is data2
