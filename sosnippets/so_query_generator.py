from .so_tags import so_tags


class SOQueryGenerator(object):

    def __init__(self, sublime_view):
        self.sublime_view = sublime_view
        self.so_tags = {}
        for t in so_tags:
            self.so_tags[t.lower()] = t

    def generate(self, query):
        syntax = self.get_syntax()
        if syntax in self.so_tags:
            query = '[{0}] {1}'.format(self.so_tags[syntax], query)
        else:
            query = '{0} {1}'.format(syntax, query)
        return query

    def get_syntax(self):
        syntax_file = self.sublime_view.settings().get('syntax')
        start = syntax_file.rfind('/')
        if start == -1:
            start = 0
        end = syntax_file.rfind('.')
        if end == -1:
            end = len(syntax_file)
        return syntax_file[start+1:end].lower()
