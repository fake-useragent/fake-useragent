"""General library settings."""

try:
    from importlib import metadata

    __version__ = metadata.version("fake-useragent")
except ImportError:
    __version__ = "unknown"

REPLACEMENTS = {
    " ": "",
    "_": "",
}

SHORTCUTS = {
    "microsoft edge": "edge",
    "google": "chrome",
    "googlechrome": "chrome",
    "ff": "firefox",
}
