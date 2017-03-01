from __future__ import absolute_import, unicode_literals

import io
import json
import os
from functools import partial
try:  # Python 2 # pragma: no cover
    from urllib2 import Request
except ImportError:  # Python 3 # pragma: no cover
    from urllib.request import Request

import mock
import pytest

from fake_useragent import errors, settings, utils

from tests.utils import _request, find_unused_port


def test_utils_get():
    assert utils.get('http://google.com') is not None


def test_utils_get_retries():
    def __request(*args, **kwargs):  # noqa
        __request.attempt += 1

        if __request.attempt < settings.HTTP_RETRIES:
            return Request('http://0.0.0.0:{port}'.format(
                port=find_unused_port(),
            ))

        return Request(*args, **kwargs)
    __request.attempt = 0

    with mock.patch(
        'fake_useragent.utils.Request',
        side_effect=__request,
    ):
        assert utils.get('http://google.com') is not None

    assert __request.attempt == 2


def test_utils_get_cache_server():
    body = utils.get(settings.CACHE_SERVER).decode('utf-8')

    data = json.loads(body)

    expected = {
        'randomize': mock.ANY,
        'browsers': {
            'chrome': mock.ANY,
            'firefox': mock.ANY,
            'opera': mock.ANY,
            'safari': mock.ANY,
            'internetexplorer': mock.ANY,
        },
    }

    assert expected == data


def test_utils_get_browsers():
    browsers = utils.get_browsers()

    assert len(browsers) == 5

    expected = [
        'Firefox',
        'Opera',
        'Chrome',
        'Internet Explorer',
        'Safari',
    ]

    browser_names = [browser[0] for browser in browsers]

    assert set(expected) == set(browser_names)

    total = 100

    for _, percentage in browsers:
        total -= float(percentage)

    assert round(total, 0) <= 1


def test_utils_get_browser_versions():
    browser_names = [browser[0] for browser in utils.get_browsers()]

    for browser in browser_names:
        count = len(utils.get_browser_versions(browser))
        assert count == settings.BROWSERS_COUNT_LIMIT


def test_utils_load(path):
    _load = utils.load

    with mock.patch(
        'fake_useragent.utils.load',
        side_effect=_load,
    ) as mocked:
        data = utils.load(use_cache_server=False)

        mocked.assert_called()

    expected = {
        'randomize': mock.ANY,
        'browsers': {
            'chrome': mock.ANY,
            'firefox': mock.ANY,
            'opera': mock.ANY,
            'safari': mock.ANY,
            'internetexplorer': mock.ANY,
        },
    }

    assert expected == data


def test_utils_write(path):
    data = {'foo': 'bar'}

    utils.write(path, data)

    with io.open(path, mode='rt', encoding='utf-8') as fp:
        expected = json.loads(fp.read())

    assert expected == data


def test_utils_read(path):
    data = {'foo': 'bar'}

    with io.open(path, mode='wt', encoding='utf-8') as fp:
        dumped = json.dumps(data)

        if not isinstance(dumped, utils.text):  # Python 2
            dumped = dumped.decode('utf-8')

        fp.write(dumped)

    expected = utils.read(path)

    assert expected == data


def test_utils_exist(path):
    assert not os.path.isfile(path)

    assert not utils.exist(path)

    with io.open(path, mode='wb') as fp:
        fp.write(b'\n')

    assert os.path.isfile(path)

    assert utils.exist(path)


def test_utils_rm(path):
    assert not os.path.isfile(path)

    with io.open(path, mode='wb') as fp:
        fp.write(b'\n')

    assert os.path.isfile(path)

    utils.rm(path)

    assert not os.path.isfile(path)


def test_utils_update(path):
    utils.update(path, use_cache_server=False)

    mtime = os.path.getmtime(path)

    _load = utils.load

    with mock.patch(
        'fake_useragent.utils.load',
        side_effect=_load,
    ) as mocked:
        utils.update(path, use_cache_server=False)

        mocked.assert_called()

    assert os.path.getmtime(path) != mtime


def test_utils_load_cached(path):
    _load = utils.load

    with mock.patch(
        'fake_useragent.utils.load',
        side_effect=_load,
    ) as mocked:
        data = utils.load_cached(path, use_cache_server=False)

        mocked.assert_called()

    expected = {
        'randomize': mock.ANY,
        'browsers': {
            'chrome': mock.ANY,
            'firefox': mock.ANY,
            'opera': mock.ANY,
            'safari': mock.ANY,
            'internetexplorer': mock.ANY,
        },
    }

    assert expected == data

    expected = data

    with mock.patch('fake_useragent.utils.load') as mocked:
        data = utils.load_cached(path, use_cache_server=False)

        mocked.assert_not_called()

    assert expected == data


def test_utils_load_no_use_cache_server(path):
    denied_urls = [
        'http://www.w3schools.com/browsers/browsers_stats.asp',
        'http://useragentstring.com/pages/useragentstring.php',
    ]

    with mock.patch(
        'fake_useragent.utils.Request',
        side_effect=partial(_request, denied_urls),
    ):
        with pytest.raises(errors.FakeUserAgentError):
            utils.load(use_cache_server=False)

        with pytest.raises(errors.FakeUserAgentError):
            utils.load_cached(path, use_cache_server=False)

        with pytest.raises(errors.FakeUserAgentError):
            utils.update(path, use_cache_server=False)


def test_utils_load_use_cache_server(path):
    denied_urls = [
        'http://www.w3schools.com/browsers/browsers_stats.asp',
        'http://useragentstring.com/pages/useragentstring.php',
    ]

    with mock.patch(
        'fake_useragent.utils.Request',
        side_effect=partial(_request, denied_urls),
    ):
        data = utils.load(use_cache_server=True)

        expected = {
            'randomize': mock.ANY,
            'browsers': {
                'chrome': mock.ANY,
                'firefox': mock.ANY,
                'opera': mock.ANY,
                'safari': mock.ANY,
                'internetexplorer': mock.ANY,
            },
        }

        assert expected == data


def test_utils_load_use_cache_server_down(path):
    denied_urls = [
        'http://www.w3schools.com/browsers/browsers_stats.asp',
        'http://useragentstring.com/pages/useragentstring.php',
        settings.CACHE_SERVER,
    ]

    with mock.patch(
        'fake_useragent.utils.Request',
        side_effect=partial(_request, denied_urls),
    ):
        with pytest.raises(errors.FakeUserAgentError):
            utils.load(use_cache_server=True)
