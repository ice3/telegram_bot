"""Utility functions."""
import re

pattern = ('http[s]?://'
           '(?:[a-zA-Z]|[0-9]|'
           '[$-_@.&+]|'
           '[!*\(\),]|'
           '(?:%[0-9a-fA-F][0-9a-fA-F]))+'
           )


def extract_urls_from_text(text):
    """Extract all URLs from a string and return an iterable with each."""
    urls = re.findall(pattern, text)
    return urls
