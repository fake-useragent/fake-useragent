# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import tempfile
from pathlib import Path

__version__ = '0.1.13'

DB = os.path.join(
    tempfile.gettempdir(),
    'fake_useragent_{version}.json'.format(
        version=__version__,
    ),
)

FALLBACK_PATH = str(Path(__file__).resolve().parent
                    .joinpath('data', 'fallback.json')
                    )

BROWSERS_STATS_PAGE = 'https://www.w3schools.com/browsers/default.asp'

BROWSER_BASE_PAGE = 'https://user-agents.net/browsers/{browser}/'

BROWSER_HOST = 'https://user-agents.net'

BROWSERS_COUNT_LIMIT = 70

BROWSERS_OS_COUNT_LIMIT = 20

REPLACEMENTS = {
    ' ': '',
    '_': '',
}
BROWSERS_NAMES = ['chrome', 'edge', 'firefox', 'safari', 'opera']

BROWSERS_OS = {
    'chrome': ['win10', 'win8-1', 'win8', 'linux', 'macos'],
    'edge': ['win10', 'win8-1', 'win7', 'macos'],
    'firefox': ['win10', 'ubuntu', 'macos', 'linux'],
    'safari': ['macos', 'macosx', 'win8-1', 'linux'],
    'opera': ['win10', 'linux', 'macos', 'win8-1']
    }

SHORTCUTS = {
    'edge': 'edge',
    'google': 'chrome',
    'googlechrome': 'chrome',
    'ff': 'firefox',
}

HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        }

HTTP_TIMEOUT = 15

HTTP_RETRIES = 2

HTTP_DELAY = 0.1
