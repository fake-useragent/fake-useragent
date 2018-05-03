# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import tempfile

__version__ = '0.1.10'

DB = os.path.join(
    tempfile.gettempdir(),
    'fake_useragent_{version}.json'.format(
        version=__version__,
    ),
)

CACHE_SERVER = 'http://d2g6u4gh6d9rq0.cloudfront.net/browsers/fake_useragent_{version}.json'.format(  # noqa
    version=__version__,
)

BROWSERS_STATS_PAGE = 'https://www.w3schools.com/browsers/default.asp'

BROWSER_BASE_PAGE = 'https://developers.whatismybrowser.com/useragents/explore/software_name/'  # noqa

BROWSERS_COUNT_LIMIT = 50

REPLACEMENTS = {
    ' ': '',
    '_': '',
}

SHORTCUTS = {
    'internet explorer': 'internet-explorer',
    'ie': 'internet-explorer',
    'msie': 'internet-explorer',
    'edge': 'internet-explorer',
    'google': 'chrome',
    'googlechrome': 'chrome',
    'ff': 'firefox',
}

OVERRIDES = {
    'Edge/IE': 'Internet Explorer',
    'IE/Edge': 'Internet Explorer',
}

HTTP_TIMEOUT = 5

HTTP_RETRIES = 2

HTTP_DELAY = 0.1
