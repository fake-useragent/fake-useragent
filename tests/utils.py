from __future__ import absolute_import, unicode_literals

import socket
try:  # Python 2 # pragma: no cover
    from urllib2 import Request
except ImportError:  # Python 3 # pragma: no cover
    from urllib.request import Request

_used_ports = set()


def find_unused_port():
    while True:
        service = socket.socket()

        try:
            service.bind(('127.0.0.1', 0))

            _, port = service.getsockname()

            if port not in _used_ports:
                break
        finally:
            service.close()

    return port


def _request(denied_urls, *args, **kwargs):
    requested_url = args[0]

    for url in denied_urls:
        if url in requested_url:
            return Request('http://0.0.0.0:{port}'.format(
                port=find_unused_port(),
            ))

    return Request(*args, **kwargs)
