from __future__ import absolute_import, unicode_literals

import os
import tempfile

__version__ = '0.1.2'

DB = os.path.join(tempfile.gettempdir(), 'fake_useragent_{version}.json'.format(  # noqa
    version=__version__,
))

BROWSERS_STATS_PAGE = 'https://web.archive.org/web/http://www.w3schools.com/browsers/browsers_stats.asp'  # noqa

BROWSER_BASE_PAGE = 'https://web.archive.org/web/http://useragentstring.com/pages/useragentstring.php?name={browser}'  # noqa

BROWSERS_COUNT_LIMIT = 50

REPLACEMENTS = {
    ' ': '',
    '_': '',
}

SHORTCUTS = {
    'internet explorer': 'internetexplorer',
    'ie': 'internetexplorer',
    'msie': 'internetexplorer',
    'google': 'chrome',
    'googlechrome': 'chrome',
    'ff': 'firefox',
}

OVERRIDES = {
    'IE': 'Internet Explorer',
}

HTTP_TIMEOUT = 20

HTTP_RETRIES = 5

HTTP_DELAY = 5

HOTFIX = True
