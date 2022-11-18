import logging

from fake_useragent import settings

logging.basicConfig(level=logging.DEBUG)

settings.HTTP_DELAY = 0
