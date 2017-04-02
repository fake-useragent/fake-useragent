# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
from functools import partial

import mock
import pytest

from fake_useragent import (VERSION, FakeUserAgent, FakeUserAgentError,
                            UserAgent, settings)
from tests.utils import _request


def setup_function(function):
    try:
        os.remove(settings.DB)
    except OSError:
        pass


def teardown_function(function):
    try:
        os.remove(settings.DB)
    except OSError:
        pass


def _probe(ua):
    ua.ie
    ua.msie
    ua.internetexplorer
    ua.internet_explorer
    ua['internet explorer']
    ua.edge
    ua.google
    ua.chrome
    ua.googlechrome
    ua.google_chrome
    ua['google chrome']
    ua.firefox
    ua.ff
    ua.safari
    ua.random
    ua['random']
    ua.edge


def test_fake_user_agent_browsers():
    ua = UserAgent(cache=False, use_cache_server=False)

    _probe(ua)

    with pytest.raises(FakeUserAgentError):
        ua.non_existing

    with pytest.raises(FakeUserAgentError):
        ua['non_existing']

    data1 = ua.data

    ua.update()

    data2 = ua.data

    assert data1 == data2

    assert data1 is not data2


def test_fake_user_agent_path(path):
    assert not os.path.isfile(path)

    ua = UserAgent(path=path, cache=True, use_cache_server=False)

    assert path == ua.path

    assert os.path.isfile(path)


def test_fake_default_path():
    assert not os.path.isfile(settings.DB)

    ua = UserAgent(cache=True, use_cache_server=False)

    assert settings.DB == ua.path

    assert os.path.isfile(settings.DB)


def test_fake_fallback():
    fallback = 'Foo Browser'

    denied_urls = [
        'https://www.w3schools.com/browsers/browsers_stats.asp',
        'http://useragentstring.com/pages/useragentstring.php',
        settings.CACHE_SERVER,
    ]

    with mock.patch(
        'fake_useragent.utils.Request',
        side_effect=partial(_request, denied_urls=denied_urls),
    ):
        ua = UserAgent(cache=False, use_cache_server=False, fallback=fallback)

    assert ua.random == fallback

    assert ua.ie == fallback


def test_fake_no_fallback():
    denied_urls = [
        'https://www.w3schools.com/browsers/browsers_stats.asp',
        'http://useragentstring.com/pages/useragentstring.php',
        settings.CACHE_SERVER,
    ]

    with mock.patch(
        'fake_useragent.utils.Request',
        side_effect=partial(_request, denied_urls=denied_urls),
    ):
        with pytest.raises(FakeUserAgentError):
            UserAgent(cache=False, use_cache_server=False)


def test_fake_update():
    ua = UserAgent(cache=False, use_cache_server=False)

    ua.update()

    _probe(ua)


def test_fake_update_cache(path):
    assert not os.path.isfile(path)

    ua = UserAgent(path=path, cache=False, use_cache_server=False)

    assert not os.path.isfile(path)

    with pytest.raises(AssertionError):
        ua.update(cache='y')

    ua.update(cache=True)

    assert os.path.isfile(path)

    _probe(ua)


def test_fake_update_use_cache_server():
    ua = UserAgent(cache=False, use_cache_server=True)

    denied_urls = [
        'https://www.w3schools.com/browsers/browsers_stats.asp',
        'http://useragentstring.com/pages/useragentstring.php',
    ]

    with mock.patch(
        'fake_useragent.utils.Request',
        side_effect=partial(_request, denied_urls=denied_urls),
    ):
        ua.update()

        _probe(ua)

    denied_urls = [
        'https://www.w3schools.com/browsers/browsers_stats.asp',
        'http://useragentstring.com/pages/useragentstring.php',
        settings.CACHE_SERVER,
    ]

    with mock.patch(
        'fake_useragent.utils.Request',
        side_effect=partial(_request, denied_urls=denied_urls),
    ):
        with pytest.raises(FakeUserAgentError):
            ua.update()


def test_fake_not_use_cache_server():
    denied_urls = [
        'https://www.w3schools.com/browsers/browsers_stats.asp',
        'http://useragentstring.com/pages/useragentstring.php',
    ]

    with mock.patch(
        'fake_useragent.utils.Request',
        side_effect=partial(_request, denied_urls=denied_urls),
    ):
        with pytest.raises(FakeUserAgentError):
            UserAgent(cache=False, use_cache_server=False)


def test_fake_update_not_use_cache_server():
    ua = UserAgent(cache=False, use_cache_server=False)

    denied_urls = [
        'https://www.w3schools.com/browsers/browsers_stats.asp',
        'http://useragentstring.com/pages/useragentstring.php',
    ]

    with mock.patch(
        'fake_useragent.utils.Request',
        side_effect=partial(_request, denied_urls=denied_urls),
    ):
        with pytest.raises(FakeUserAgentError):
            ua.update()


def test_fake_use_cache_server():
    denied_urls = [
        'https://www.w3schools.com/browsers/browsers_stats.asp',
        'http://useragentstring.com/pages/useragentstring.php',
    ]

    with mock.patch(
        'fake_useragent.utils.Request',
        side_effect=partial(_request, denied_urls=denied_urls),
    ):
        ua = UserAgent(cache=False, use_cache_server=True)

    _probe(ua)


def test_fake_cache_boolean():
    with pytest.raises(AssertionError):
        UserAgent(cache='y')


def test_fake_use_cache_server_boolean():
    with pytest.raises(AssertionError):
        UserAgent(use_cache_server='y')


def test_fake_path_str_types():
    with pytest.raises(AssertionError):
        UserAgent(path=10)


def test_fake_fallback_str_types():
    with pytest.raises(AssertionError):
        UserAgent(fallback=True)


def test_fake_safe_attrs_iterable_str_types():
    with pytest.raises(AssertionError):
        UserAgent(safe_attrs={})

    with pytest.raises(AssertionError):
        UserAgent(safe_attrs=[66])


def test_fake_safe_attrs():
    ua = UserAgent(safe_attrs=('__injections__',))

    with pytest.raises(AttributeError):
        ua.__injections__


def test_fake_version():
    assert VERSION == settings.__version__


def test_fake_aliases():
    assert FakeUserAgent is UserAgent
