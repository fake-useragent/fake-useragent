# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from fake_useragent import errors


def test_error_aliases():
    assert errors.FakeUserAgentError is errors.UserAgentError
