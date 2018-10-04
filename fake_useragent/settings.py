# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import tempfile

__version__ = '0.1.11'

DB = os.path.join(
    tempfile.gettempdir(),
    'fake_useragent_{version}.json'.format(
        version=__version__,
    ),
)

CACHE_SERVER = 'https://fake-useragent.herokuapp.com/browsers/{version}'.format(
    version=__version__,
)

BROWSERS_STATS_PAGE = 'https://www.w3schools.com/browsers/default.asp'

BROWSER_BASE_PAGE = 'http://useragentstring.com/pages/useragentstring.php?name={browser}'  # noqa

BROWSERS_COUNT_LIMIT = 50

REPLACEMENTS = {
    ' ': '',
    '_': '',
}

SHORTCUTS = {
    'internet explorer': 'internetexplorer',
    'ie': 'internetexplorer',
    'msie': 'internetexplorer',
    'edge': 'internetexplorer',
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
