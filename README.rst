fake-useragent
==============

:info: Up to date simple useragent faker with real world database

.. image:: https://travis-ci.org/hellysmile/fake-useragent.svg?branch=master
    :target: https://travis-ci.org/hellysmile/fake-useragent

.. image:: https://coveralls.io/repos/hellysmile/fake-useragent/badge.png?branch=master
    :target: https://coveralls.io/r/hellysmile/fake-useragent?branch=master

.. image:: https://pypip.in/download/fake-useragent/badge.svg?period=month
    :target: https://pypi.python.org/pypi/fake-useragent

.. image:: https://pypip.in/version/fake-useragent/badge.svg
    :target: https://pypi.python.org/pypi/fake-useragent

.. image:: https://landscape.io/github/hellysmile/fake-useragent/master/landscape.png
   :target: https://landscape.io/github/hellysmile/fake-useragent/master

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

if you want to update saved database just

.. code-block:: python

    from fake_useragent import UserAgent
    ua = UserAgent()
    ua.update()

if you dont want cache database or no writable file system:

.. code-block:: python

    from fake_useragent import UserAgent
    ua = UserAgent(cache=False)


Tests
-----

.. code-block:: console

    pip install tox
    tox
