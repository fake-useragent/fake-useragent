# User-agent web scraper

This is an user-agent web scraper for [useragentstring.com](https://useragentstring.com). Which helps me to create a cache file in [**JSON Lines** format](https://jsonlines.org/) (**note:** which is just NOT just 'normal' JSON file, for a good reason).

You could host your own cache server using [Docker](Dockerfile), we use to host our own cache server. However, this server was overloaded with requests.

We are now using the web scraper to add the data locally within the `fake-useragent` PyPi package. Meaning that it won't require Internet connection after the package is installed in order to contain a list of user agent strings.

## Running

You **should** use and execute the [`update_data_file.sh`](../update_data_file.sh) script in the **root folder** of this project. See also the README in the root directory.

---

Alternatively, use a Python virtual environment (virtualenv): `python -m virtualenv env && source env/bin/activate`  
After which you can install the Python dependencies, using: `pip install -r requirements.txt`.

Then start the spider using:

```sh
./start_spider.py
```

Then manually copy the file to the correct location:

```sh
cp website/cache.json ../src/fake_useragent/data/browsers.json
```

## Debugging

You could use `scrapy shell` for debugging the website/content within your terminal:

```sh
scrapy shell -s USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36' 'https://webcache.googleusercontent.com/search?q=cache:https%3A%2F%2Ftechblog.willshouse.com%2F2012%2F01%2F03%2Fmost-common-user-agents%2F'
```
