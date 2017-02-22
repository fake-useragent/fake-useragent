from __future__ import absolute_import, unicode_literals

import os
import unittest2

from fake_useragent import settings


settings.HTTP_TIMEOUT = 2

settings.HTTP_RETRIES = 1

settings.HTTP_DELAY = 0


class BaseTestCase(
    unittest2.TestCase,
):
    db = settings.DB

    def clear_db(self, path=db):
        try:
            os.remove(path)
        except OSError:
            pass
