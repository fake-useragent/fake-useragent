import os
import tempfile
import uuid

import pytest


@pytest.fixture
def path(request):
    path = os.path.join(tempfile.gettempdir(), uuid.uuid1().hex)

    try:
        os.remove(path)
    except OSError:
        pass

    yield path

    try:
        os.remove(path)
    except OSError:
        pass
