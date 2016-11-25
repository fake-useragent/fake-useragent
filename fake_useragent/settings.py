from __future__ import absolute_import, unicode_literals

import os
import tempfile

__version__ = '0.1.4'

DB = os.path.join(
    tempfile.gettempdir(),
    'fake_useragent_{version}.json'.format(
        version=__version__,
    ),
)

CACHE_SERVER = 'https://fake-useragent.herokuapp.com/browsers/{version}'.format(  # noqa
    version=__version__,
)

BROWSERS_STATS_PAGE = 'http://www.w3schools.com/browsers/browsers_stats.asp'

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
    'google': 'chrome',
    'googlechrome': 'chrome',
    'ff': 'firefox',
}

OVERRIDES = {
    'IE': 'Internet Explorer',
}

HTTP_TIMEOUT = 3

HTTP_RETRIES = 2

HTTP_DELAY = 0.1
