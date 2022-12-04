import scrapy

from urllib.parse import urlparse


class UserAgentSpider(scrapy.Spider):
    name = "useragent"
    allowed_domains = ["useragentstring.com"]
    start_urls = [
        "https://useragentstring.com/pages/Chrome/",
        "https://useragentstring.com/pages/Opera/",
        "https://useragentstring.com/pages/Firefox/",
        "https://useragentstring.com/pages/Safari/",
        "https://useragentstring.com/pages/Edge/",
        "https://useragentstring.com/pages/Internet Explorer/",
    ]

    def parse(self, response):
        # Retrieve last section from the URL path (first strip the last slash)
        browserName = urlparse(response.url).path.rstrip("/").split("/")[-1]
        # Lowercase
        browserName = browserName.lower()
        # Replace space (%20) with a real space if present
        browserName = browserName.replace("%20", " ")
        # Retrieve all useragent strings from hyperlinks on the website
        agents = response.css("#liste li a::text").getall()
        # Remove all whitespaces of each element
        agents = [s.strip() for s in agents]
        # Push data
        yield {browserName: agents}
