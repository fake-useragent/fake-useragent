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

OS_REPLACEMENTS = {
    "windows": ["win10", "win7"],
}

SHORTCUTS = {
    "microsoft edge": "edge",
    "google": "chrome",
    "googlechrome": "chrome",
    "ff": "firefox",
}
