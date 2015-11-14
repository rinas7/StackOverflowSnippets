import re

from .utils import unescape


class SnippetParser(object):

    code_start_tag = '<pre><code>'
    code_end_tag = '</code></pre>'

    def __init__(self, text):
        self.text = text

    def get_snippets(self):
        snippets = []
        i = 0
        while True:
            start = self.text.find(self.code_start_tag, i)
            if start == -1:
                break
            end = self.text.find(
                self.code_end_tag, start + len(self.code_start_tag))
            if end == -1:
                break
            r = re.compile(r'^(>{3}|>|\.{3}) ', flags=re.M)
            snippet = unescape(self.text[start+len(self.code_start_tag):end])
            snippet = r.sub('', snippet)
            snippets.append(snippet)
            i = end
        return snippets
