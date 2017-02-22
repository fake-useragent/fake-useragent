import os

import unittest2

from fake_useragent import settings


settings.HTTP_TIMEOUT = 2

settings.HTTP_RETRIES = 1

settings.HTTP_DELAY = 0


class BaseTestCase(unittest2.TestCase):
    db = settings.DB

    # maxDiff = None

    def clear_db(self, path=None):
        if path is None:
            path = self.db

        try:
            os.remove(path)
        except OSError:
            pass
