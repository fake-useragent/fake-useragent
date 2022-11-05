import logging

from fake_useragent import settings

logging.basicConfig(level=logging.DEBUG)

settings.HTTP_TIMEOUT = 10

# settings.HTTP_RETRIES = 3

settings.HTTP_DELAY = 0
