[![Test & Deploy fake-useragent](https://github.com/fake-useragent/fake-useragent/actions/workflows/action.yml/badge.svg?branch=main)](https://github.com/fake-useragent/fake-useragent/actions/workflows/action.yml?query=branch%3Amain)
[![Ruff linter](https://github.com/fake-useragent/fake-useragent/actions/workflows/ruff.yml/badge.svg?branch=main)](https://github.com/fake-useragent/fake-useragent/actions/workflows/ruff.yml?query=branch%3Amain)
[![CodeQL](https://github.com/fake-useragent/fake-useragent/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/fake-useragent/fake-useragent/actions/workflows/codeql.yml?query=branch%3Amain)

# fake-useragent

Up-to-date simple useragent faker with real world database.

## Features

- Data is pre-downloaded & post-processed from [Intoli LLC](https://github.com/intoli/user-agents/tree/main/src) and the data is part of the package itself
- The data consists of a wide range of browser agents and various browsers
- Retrieves user-agent strings (both of type: `desktop`, `tablet` and/or `mobile` UAs)
- Retrieve user-agent Python dictionary (aka object), with fields like `useragent`, `percent`, `type`, `device_brand`, `browser`, `browser_version`, `os`, `os_version` and `platform`
- Supports Python 3.x

### Installation

```sh
pip install fake-useragent
```

Or if you have multiple Python / pip versions installed, use `pip3`:

```sh
pip3 install fake-useragent
```

### Usage

Simple usage examples below, see also next chapters in this readme for more advanced usages:

```py
from fake_useragent import UserAgent
ua = UserAgent()

# Get a random browser user-agent string
print(ua.random)
# Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0

# Or get user-agent string from a specific browser
print(ua.chrome)
# Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
print(ua.google)
# Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) GSA/343.0.695551749 Mobile/15E148 Safari/604.1
print(ua['Chrome'])
# Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
print(ua.firefox)
# Mozilla/5.0 (Android 14; Mobile; rv:133.0) Gecko/133.0 Firefox/133.0
print(ua.ff)
# Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0
print(ua.safari)
# Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1 Ddg/17.6
print(ua.opera)
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0
print(ua.edge)
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
```

#### Additional usage

Additional features that fake-useragent now offers since v1.2.0.

If you want to specify your own browser list, you can do that via the `browsers` argument (default is: `["Google", "Chrome", "Firefox", "Edge", "Opera"," Safari", "Android", "Yandex Browser", "Samsung Internet", "Opera Mobile", "Mobile Safari", "Firefox Mobile", "Firefox iOS", "Chrome Mobile", "Chrome Mobile iOS", "Mobile Safari UI/WKWebView", "Edge Mobile", "DuckDuckGo Mobile", "MiuiBrowser", "Whale", "Twitter", "Facebook", "Amazon Silk"]`).  
This example will only return random user-agents from Edge and Chrome:

```py
from fake_useragent import UserAgent
ua = UserAgent(browsers=['Edge', 'Chrome'])
ua.random
```

_Note:_ Fakeuser-agent knowns about browsers: Chrome, Edge, Firefox, Safari, Opera, Android, Opera Mobile, Mobile Safari, Firefox Mobile, Firefox iOS, Chrome Mobile, Chrome Mobile iOS and more (see again full list above).  
_Note #2:_ Since fakeuser-agent v2.0.0 the browser names are case-sensitive!

---

If you want to specify your own operating systems, you can do that via the `os` argument (default is: `["Windows", "Linux", "Ubuntu", "Chrome OS", "Mac OS X", "Android", "iOS"]`).  
In this example you will only get Linux user-agents back:

```py
from fake_useragent import UserAgent
ua = UserAgent(os='Linux')
ua.random
```

_Note:_ Since fakeuser-agent v2.0.0 the OS names are case-sensitive!

---

You can also specify the type of platforms you want to use, you can do that via the `platforms` argument (default is `["desktop", "mobile", "tablet"]`.
This example will only return random user-agents from a mobile device:

```py
from fake_useragent import UserAgent
ua = UserAgent(platforms='mobile')
ua.random
```

And a random user-agent from a desktop device:

```py
from fake_useragent import UserAgent
ua = UserAgent(platforms='desktop')
ua.random
```

---

If you want to return more recent user-agent strings, you can play with the `min_version` argument (default is: `0.0`, meaning all user agents will match).  
In this example you get only user agents that have a minimum version of 120.0:

```py
from fake_useragent import UserAgent
ua = UserAgent(min_version=120.0)
ua.random
```

---

For backwards compatibility, a minimum usage percentage can still be specified with the `min_percentage` argument. However, the current list of user agents does
not contain this statistic. Therefore all of the user-agents will match.

---

_Hint:_ Of-course you can **combine all those arguments** to you liking!

#### User-agent Python Dictionary

Since version 1.3.0 we now also offer you the following "get" properties which return the whole Python dictionary of the UA, instead of only the user-agent string:

> **Warning**
> Raw JSON objects (in a Python dictionaries) are returned "as is".
> Meaning, this data structure could change in the future!
>
> Be aware that these "get" properties below might not return the same key/value pairs in the future.
> Use `ua.random` or alike as mentioned above, if you want to use a stable interface.

```py
from fake_useragent import UserAgent
ua = UserAgent()

# Random user-agent dictionary (object)
ua.getRandom
# {'percent': 0.8, 'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76', 'system': 'Edge 116.0 Win10', 'browser': 'edge', 'version': 116.0, 'os': 'win10'}

# More get properties:
ua.getFirefox
# {'percent': 0.3, 'useragent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/118.0', 'system': 'Firefox 118.0 Win10', 'browser': 'firefox', 'version': 118.0, 'os': 'win10'}
ua.getChrome
ua.getSafari
ua.getEdge

# And a method with an argument.
# This is exactly the same as using: ua.getFirefox
ua.getBrowser('firefox')
```

### Notes

You can override the fallback string using the `fallback` parameter, in very rare cases something failed:

```py
from fake_useragent import UserAgent

ua = UserAgent(fallback='your favorite Browser')
# in case if something went wrong, one more time it is REALLY!!! rare case
ua.random == 'your favorite Browser'
```

If you will try to get unknown browser:

```py
from fake_useragent import UserAgent
ua = UserAgent()
print(ua.unknown)
#Error occurred during getting browser: randm, but was suppressed with fallback.
#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0
```

If you need to safe some attributes from overriding them in UserAgent by `__getattr__` method
use `safe_attrs` you can pass there attributes names.
At least this will prevent you from raising FakeUserAgentError when attribute not found.

For example, when using fake*useragent with `injections <https://github.com/tailhook/injections>`* you need to:

```py
from fake_useragent import UserAgent

ua = UserAgent(safe_attrs=('__injections__',))
```

Please, do not use if you don't understand why you need this.
This is magic for rarely extreme case.

### Experiencing issues?

Make sure that you using latest version!

```sh
pip install --upgrade fake-useragent
```

Or if that isn't working, try to install the latest package version like this (`2.0.3` is an example, check what the [latest version is on PyPi](https://pypi.org/project/fake-useragent/#history)):

```sh
pip install fake-useragent==2.0.3
```

Check version via the Python console:

```py
import fake_useragent

print(fake_useragent.__version__)
```

And you are always welcome to post [issues](https://github.com/fake-useragent/fake-useragent/issues).

Please do not forget to mention the version that you are using.

### For Developers

#### User-agent Data

The user-agent data we retrieve from [user-agents.net](https://user-agents.net). Data is stored in [JSONlines](https://jsonlines.org/) format. File is located in the: `src/fake_useragent/data` directory.

We are currently working on a new automation script (see issue [#333](https://github.com/fake-useragent/fake-useragent/issues/333)) to fetch user-agent scripts from user-agents.net and up date the user-agents once in a while.

The data JSON file is part of the Python package, see [pyproject.toml](pyproject.toml). Read more about [Data files support](https://setuptools.pypa.io/en/latest/userguide/datafiles.html).

#### Python Virtual Environment

We encourage to use Python virtual environment before installing Pip packages, like so:

```sh
python -m virtualenv env
source env/bin/activate
```

#### Local Install

```sh
pip install -e .
```

#### Tests

```sh
pip install -r requirements.txt
tox
```

#### Linting

To fix imports using ruff:

```sh
pip install -r requirements.txt
ruff check --select="I" --fix .
```

Fix black code formatting errors:

```sh
pip install -r requirements.txt
black .
```

_Note:_ When ruff v1.0 releases, we most likely move fully towards `ruff` instead of `black`.

### Changelog

- 2.0.2 & 2.0.3 December 10, 2024

  -  Fix project dependencies toml file & sync docs

- 2.0.1 December 7, 2024 (my birthday)

  - Add requires-python to toml config

- 2.0.0 December 4, 2024

  - Switch to new data source (again again)
  - Possible browser options: `"Google", "Chrome", "Firefox", "Edge", "Opera"," Safari", "Android", "Yandex Browser", "Samsung Internet", "Opera Mobile",
"Mobile Safari", "Firefox Mobile", "Firefox iOS", "Chrome Mobile", "Chrome Mobile iOS", "Mobile Safari UI/WKWebView",
"Edge Mobile", "DuckDuckGo Mobile", "MiuiBrowser", "Whale", "Twitter", "Facebook", "Amazon Silk"`
  - Possible OS options: `"Windows", "Linux", "Ubuntu", "Chrome OS", "Mac OS X", "Android", "iOS"`
  - Possible type options: `"desktop", "mobile", "tablet"`
  - Update fake.py to handle the new data key/value objects
  - Updated the README
  - Renamed browsers.json to browsers.jsonl. And other refactors.

- 1.5.1 March 16, 2024

  - Remove trailing spaces in user agent strings

- 1.5.0 March 8, 2024

  - Migrated to new user-agent data source (thanks @BoudewijnZwart), backwards compatible API.
  - Update all pip package dependencies to latest stable versions

- 1.4.0 November 24, 2023

  - Update all PIP packages
  - Support Python 3.12 (thanks @vladkens)
  - Fix package conflict in cache scraper
  - Improve ruff CLI calls

- 1.3.0 October 2, 2023

  - Introducing new `ua.getRandom`, `ua.getFirefox`, `ua.getChrome`, `ua.getSafari`. And a generic method: `ua.getBrowser(..)` (eg. `getBrowser('firefox')`)
    - These new properties above allows you to retrieve the whole raw Python dictionary, instead of only the UA string.
    - These properties might return different key/values pairs in the future!
  - Fix the `os` argument 'windows' to check for both `win10`and `win7` values (previously only checking on `win10`), thus returning more UAs
  - Improved user-agent scraper (now also containing Safari browser again)
  - Updated browsers.json data file

- 1.2.1 August 2, 2023

  - Small improvements in the `min_percentage` check
  - Update all Pip package dependencies

- 1.2.0 August 2, 2023

  - Updated browser useragent data
  - Allow filters on browser, OS and usage percentage
  - Update the cache scraper to scape the new data source for user-agent strings
  - Adapted the code to work with the new JSON data format
  - Parameter `use_external_data=True` and `verify_ssl` are **removed**. If you use those parameters, just remove it in your code!

- 1.1.3 March 20, 2023

  - Update dependencies

- 1.1.2 February 8, 2023

  - Security fixes

- 1.1.1 December 4, 2022

  - Remove whitespaces from user agent strings, this is a patch release

- 1.1.0 November 26, 2022

  - Add `pkg_resource` as fallback mechanism in trying to retrieve the local JSON data file

- 1.0.1 November 10, 2022

  - Add `importlib-metadata` & `importlib-resources` as dependencies
  - Check on specific Python version regarding the importlib resources (python v3.10 or higher) in order to have `files()` working
  - `importlib_metadata` should now also work on Python version before 3.8
  - Remove obsolete `MANIFEST.in` file

- 1.0.0 November 17, 2022

  - Make the JSON Lines data file part of the Python package, data is retrieved locally
    - Extend the `myproject.toml` file with `package-data` support
  - Remove centralized caching server implementation
  - Make real unit-tests which should run reliable, fast, independent and without Internet connection

- 0.1.14 November 5, 2022

  - Improve code quality standards using modern Python >=3.7 syntax
  - Migrated to `pyproject.toml` build system format + syntax check
  - Add additional classifiers to the toml file
  - Improved `tox.ini` file
  - Improved GitHub Actions job using pip cache
  - And various small fixes

- 0.1.13 October 21, 2022

  - Implement `browsers` argument, allowing you to override the browser names you want to use
  - Fix browser listing of Internet Explorer and Edge
  - Don't depend on w3schools.com anymore
  - Clean-up data (temp) file format
  - Update fallback cache server URL / use JSON Lines as file format
  - Move to GitHub Actions instead of Travis
  - Using [`black`](https://pypi.org/project/black/) Python formatter in favour of Flake

- 0.1.12 March 31, 2022

  - forked

- 0.1.11 October 4, 2018

  - moved `s3 + cloudfront` fallback to `heroku.com`, cuz someone from Florida did ~25M requests last month

- 0.1.10 February 11, 2018

  - Minor fix docs `cloudfront` url

- 0.1.9 February 11, 2018

  - fix `w3schools.com` renamed `IE/Edge` to `Edge/IE`
  - moved `heroku.com` fallback to `s3 + cloudfront`
  - stop testing Python3.3 and pypy

- 0.1.8 November 2, 2017

  - fix `useragentstring.com` `Can't connect to local MySQL server through socket`

- 0.1.7 April 2, 2017

  - fix broken README.rst

- 0.1.6 April 2, 2017

  - fixes bug `use_cache_server` do not affected anything
  - `w3schools.com <https://www.w3schools.com/browsers/browsers_stats.asp>`\_ moved to `https`
  - `verify_ssl` options added, by default it is `True` (`urllib.urlopen` ssl context for Python 2.7.9- and 3.4.3- is not supported)

- 0.1.5 February 28, 2017

  - added `ua.edge` alias to Internet Explorer
  - w3schools.com starts displaying `Edge` statistic
  - Python 2.6 is not tested anymore
  - `use_cache_server` option added
  - Increased `fake_useragent.settings.HTTP_TIMEOUT` to 5 seconds

- 0.1.4 December 14, 2016

  - Added custom data file location support
  - Added `fallback` browser support, in case of unavailable data sources
  - Added alias `fake_useragent.FakeUserAgent` for `fake_useragent.UserAgent`
  - Added alias `fake_useragent.UserAgentError` for `fake_useragent.FakeUserAgentError`
  - Reduced `fake_useragent.settings.HTTP_TIMEOUT` to 3 seconds
  - Started migration to new data file format
  - Simplified a lot 4+ years out of date code
  - Better thread/greenlet safety
  - Added verbose logging
  - Added `safe_attrs` for prevent overriding by `__getattr__`

- 0.1.3 November 24, 2016

  - Added hosted data file, when remote services is unavailable
  - Raises `fake_useragent.errors.FakeUserAgentError` in case when there is not way to download data
  - Raises `fake_useragent.errors.FakeUserAgentError` instead of `None` in case of unknown browser
  - Added `gevent.sleep` support in `gevent` patched environment when trying to download data

- X.X.X xxxxxxx xx, xxxx
  - xxxxx ?????

### Authors

You can visit [authors page](https://github.com/fake-useragent/fake-useragent/blob/main/AUTHORS).
