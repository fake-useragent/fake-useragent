fake-useragent
==============

:info: Up to date simple useragent faker with real world database

.. image:: https://img.shields.io/travis/hellysmile/fake-useragent.svg
    :target: https://travis-ci.org/hellysmile/fake-useragent

.. image:: https://img.shields.io/coveralls/hellysmile/fake-useragent.svg
    :target: https://coveralls.io/r/hellysmile/fake-useragent

.. image:: https://landscape.io/github/hellysmile/fake-useragent/master/landscape.svg?style=flat
    :target: https://landscape.io/github/hellysmile/fake-useragent/master

.. image:: https://img.shields.io/pypi/v/fake-useragent.svg
    :target: https://pypi.python.org/pypi/fake-useragent

Features
********

* grabs up to date ``useragent`` from `useragentstring.com <http://useragentstring.com/>`_
* randomize with real world statistic via `w3schools.com <http://www.w3schools.com/browsers/browsers_stats.asp>`_

Installation
------------

.. code-block:: shell

    pip install fake-useragent

Usage
-----

.. code-block:: python

    from fake_useragent import UserAgent
    ua = UserAgent()

    ua.ie
    # Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);
    ua.msie
    # Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)'
    ua['Internet Explorer']
    # Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)
    ua.opera
    # Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11
    ua.chrome
    # Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
    ua.google
    # Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13
    ua['google chrome']
    # Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11
    ua.firefox
    # Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1
    ua.ff
    # Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1
    ua.safari
    # Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25

    # and the best one, random via real world browser usage statistic
    ua.random

Notes
-----

``fake-useragent`` store collected data at your os temp dir, like ``/tmp``

If You want to update saved database just:

.. code-block:: python

    from fake_useragent import UserAgent
    ua = UserAgent()
    ua.update()

If You dont want cache database or no writable file system:

.. code-block:: python

    from fake_useragent import UserAgent
    ua = UserAgent(cache=False)

In very rare case, if cache server and sources will be
unavailable ``fake-useragent`` wont be able to download data: (version 0.1.3 added)

.. code-block:: python

    from fake_useragent import UserAgent
    ua = UserAgent()

    # Traceback (most recent call last):
    #   ...
    # fake_useragent.errors.FakeUserAgentError

    # You can catch it via

    from fake_useragent import FakeUserAgentError

    try:
        ua = UserAgent()
    except FakeUserAgentError:
        pass

If You will try to get unknown browser: (version 0.1.3 changed)

.. code-block:: python

    from fake_useragent import UserAgent
    ua = UserAgent()
    ua.best_browser
    # Traceback (most recent call last):
    #   ...
    # fake_useragent.errors.FakeUserAgentError

You can completely disable ANY annoying exception with adding ``fallback``: (version 0.1.4 added)

.. code-block:: python

    import fake_useragent

    ua = fake_useragent.UserAgent(fallback='Your favorite Browser')
    # in case if something went wrong, one more time it is REALLY!!! rare case
    ua.random == 'Your favorite Browser'

Want to control location of data file? (version 0.1.4 added)

.. code-block:: python

    import fake_useragent

    # I am STRONGLY!!! recommend to use version suffix
    location = '/home/user/fake_useragent%s.json' % fake_useragent.VERSION

    ua = fake_useragent.UserAgent(path=location)
    ua.random

If you need to safe some attributes from overriding them in UserAgent by ``__getattr__`` method
use ``safe_attrs`` you can pass there attributes names.
At least this will prevent you from raising FakeUserAgentError when attribute not found.

For example, when using fake_useragent with `injections <https://github.com/tailhook/injections>`_ you need to:

.. code-block:: python

    import fake_useragent

    ua = fake_useragent.UserAgent(safe_attrs=('__injections__',))

Please, do not use if you don't understand why you need this.
This is magic for rarely extreme case.

Experiencing issues???
----------------------

Make sure that You using latest version!!!

.. code-block:: shell

    pip install -U fake-useragent

Check version via python console: (version 0.1.4 added)

.. code-block:: python

    import fake_useragent

    print(fake_useragent.VERSION)

And You are always welcome to post `issues <https://github.com/hellysmile/fake-useragent/issues>`_

Please do not forget mention version that You are using

Tests
-----

.. code-block:: console

    pip install tox
    tox

Changelog
---------

* 0.1.4 December 14, 2016
    - Added custom data file location support
    - Added ``fallback`` browser support, in case of unavailable data sources
    - Added alias ``fake_useragent.FakeUserAgent`` for ``fake_useragent.UserAgent``
    - Added alias ``fake_useragent.UserAgentError`` for ``fake_useragent.FakeUserAgentError``
    - Reduced fake_useragent.settings.HTTP_TIMEOUT to 3 seconds
    - Started migration to new data file format
    - Simplified a lot 4+ years out of date code
    - Better thread/greenlet safety
    - Added verbose logging
    - Added ``safe_attrs`` for prevent overriding by ``__getattr__``

* 0.1.3 November 24, 2016
    - Added hosted data file, when remote services is unavailable
    - Raises ``fake_useragent.errors.FakeUserAgentError`` in case when there is not way to download data
    - Raises ``fake_useragent.errors.FakeUserAgentError`` instead of ``None`` in case of unknown browser
    - Added ``gevent.sleep`` support in ``gevent`` patched environment when trying to download data

* X.X.X xxxxxxx xx, xxxx
    - xxxxx ?????

Authors
-------

You can visit `authors page <https://github.com/hellysmile/fake-useragent/blob/master/AUTHORS>`_
