try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

def unescape(lst):
    return HTMLParser().unescape(lst)
