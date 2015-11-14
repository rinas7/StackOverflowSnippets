import sublime, sublime_plugin

try:
    from .sosnippets.so_query_generator import SOQueryGenerator
    from .sosnippets.thread_handlers import SOQuestionsHandler
    from .sosnippets.view import View
except (ImportError, SystemError, ValueError):
    from sosnippets.so_query_generator import SOQueryGenerator
    from sosnippets.thread_handlers import SOQuestionsHandler
    from sosnippets.view import View


class SosnippetsCommand(sublime_plugin.TextCommand):

    last_query = ''

    def __init__(self, *args, **kwargs):
        super(SosnippetsCommand, self).__init__(*args, **kwargs)
        self._view = View(self.view)
        self.query_generator = SOQueryGenerator(self.view)

    def run(self, edit):
        sublime.active_window().show_input_panel(
            'Search Stack Overflow:',
            self.last_query, self.on_search, None, None)

    def on_search(self, query):
        self.last_query = query
        SOQuestionsHandler(
            self._view, self.query_generator.generate(query)).start()
