import os
import tempfile


DB = os.path.join(
    tempfile.gettempdir(), 'fake_useragent.json'
)

BROWSERS_STATS_PAGE = 'http://www.w3schools.com/browsers/browsers_stats.asp'

BROWSER_BASE_PAGE = 'http://useragentstring.com/pages/%s/'

BROWSERS_COUNT_LIMIT = 30
