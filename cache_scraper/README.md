# User-agent web scraper

This is an user-agent web scraper for [useragentstring.com](https://useragentstring.com). Which helps me to create a cache file in [**JSON Lines** format](https://jsonlines.org/) (**note:** which is just NOT just 'normal' JSON file, for a good reason).

The JSON Lines [cache.json file](https://useragent.melroy.org/cache.json) is currently hosted on the useragent.melroy.org domain and used within the `fake-useragent` Python package as fallback URL. Thus only used if other sources are down or something breaks during HTML content parsing.
