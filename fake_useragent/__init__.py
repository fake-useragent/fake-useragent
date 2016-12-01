from __future__ import absolute_import, unicode_literals

import logging

from fake_useragent.errors import FakeUserAgentError, UserAgentError  # noqa # isort:skop
from fake_useragent.fake import FakeUserAgent, UserAgent  # noqa # isort:skop
from fake_useragent.settings import __version__ as VERSION  # noqa # isort:skip


logging.basicConfig(level=logging.INFO)
