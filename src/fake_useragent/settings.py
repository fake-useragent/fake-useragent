from importlib import metadata

__version__ = metadata.version("fake-useragent")

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
