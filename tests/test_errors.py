import unittest

from fake_useragent import errors


class TestErrors(unittest.TestCase):
    def test_error_aliases(self):
        assert errors.FakeUserAgentError is errors.UserAgentError
