from fake_useragent import errors


def test_error_aliases():
    assert errors.FakeUserAgentError is errors.UserAgentError
