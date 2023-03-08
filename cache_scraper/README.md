# User-agent web scraper

This is an user-agent web scraper for [useragentstring.com](https://useragentstring.com). Which helps me to create a cache file in [**JSON Lines** format](https://jsonlines.org/) (**note:** which is just NOT just 'normal' JSON file, for a good reason).

You could host your own cache server using [Docker](Dockerfile), we use to host our own cache server. However, this server was overloaded with requests.

We are now using the web scraper to add the data locally within the `fake-useragent` PyPi package. Meaning that it won't require Internet connection after the package is installed in order to contain a list of user agent strings.

## Running

You should use & execute the [`update_data_file.sh`](../update_data_file.sh) script in the root folder of this project.

Alternatively, use a Python virtual environment (virtualenv).  
After which you can install the Python dependencies, using: `pip install -r requirements.txt`.

Then start the spider using:

```sh
./start_spider.py
```

Then copy the file to the correct location:

```sh
cp website/cache.json ../src/fake_useragent/data/browsers.json
```
