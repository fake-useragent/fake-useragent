import json

import scrapy


class UserAgentSpider(scrapy.Spider):
    name = "useragent"
    allowed_domains = ["useragentstring.com"]
    # We use the Google Web Cache, to go around Cloudflare
    start_urls = [
        "https://webcache.googleusercontent.com/search?q=cache:https%3A%2F%2Ftechblog.willshouse.com%2F2012%2F01%2F03%2Fmost-common-user-agents%2F",
    ]

    def parse(self, response):
        # Retrieve the JSON textarea content
        data = response.css("textarea.get-the-list::text")[1].get()
        # Convert JSON to Python object
        agents = json.loads(data)

        for agent in agents:
            try:
                [browser, version, os] = agent["system"].split()
                # Remove percentage icon & convert to float
                agent["percent"] = float(agent["percent"][:-1])
                # Add additional fields
                agent["browser"] = browser.lower()  # To lower-case
                agent["version"] = float(version)  # Convert to float
                agent["os"] = os.lower()  # To lower-case
                # Yield each agent object at the time
                yield agent
            except ValueError:
                # Ignore user-agent strings that could not be parsed (eg. bot agent strings)
                pass
