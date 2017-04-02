# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class FakeUserAgentError(Exception):
    pass


# common alias
UserAgentError = FakeUserAgentError
