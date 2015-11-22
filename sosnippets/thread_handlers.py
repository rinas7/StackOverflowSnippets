import sublime

from .question_ranker import QuestionRanker
from .snippet_parser import SnippetParser
from .threads import SOAnswersThread, SOQuestionsThread
from .utils import unescape


class AbstractThreadHandler(object):

    def __init__(self, data):
        self.data = data
        self.thread = self.new_thread()

    def new_thread(self):
        raise NotImplementedError

    def start(self):
        self.thread.start()
        self.handle()

    def handle(self):
        if self.thread.is_alive():
            self.on_in_progress()
            sublime.set_timeout(self.handle, 100)
        else:
            self.on_finish()
            if self.thread.error:
                self.on_error(self.thread.error)
            else:
                self.on_success(self.thread.result)

    def on_in_progress(self):
        pass

    def on_finish(self):
        pass

    def on_error(self, error):
        pass

    def on_success(self, result):
        pass


class AbstractSublimeThreadHandler(AbstractThreadHandler):

    loading_bar_width = 5

    def __init__(self, view, data):
        super(AbstractSublimeThreadHandler, self).__init__(data)
        self.view = view
        self.progress_dot_count = 0

    def on_in_progress(self):
        self.view.show_status('Loading {0}{1}'.format(
            '.' * self.progress_dot_count,
            ' ' * (self.loading_bar_width - self.progress_dot_count)))
        self.progress_dot_count += 1
        self.progress_dot_count %= self.loading_bar_width

    def on_finish(self):
        self.view.hide_status()

    def on_error(self, error):
        sublime.error_message(
            '{0}: {1}'.format(error.__class__.__name__, error))


class AbstractSORequestHandler(AbstractSublimeThreadHandler):

    def on_success(self, result):
        super(AbstractSORequestHandler, self).on_success(result)
        if not self.thread.from_cache:
            self.view.show_status('Remaining Quota: {0}/{1}'.format(
                result['quota_remaining'], result['quota_max']), 10000)


class SOQuestionsHandler(AbstractSORequestHandler):

    def new_thread(self):
        return SOQuestionsThread(self.data)

    def on_success(self, result):
        super(SOQuestionsHandler, self).on_success(result)
        if result['items']:
            questions = self.rerank_questions(result['items'])
            self.view.show_quick_panel(
                [unescape(q['title']) for q in questions],
                lambda i: self.on_question_selected(questions[i]))
        else:
            sublime.error_message('No results found')

    def rerank_questions(self, questions):
        return QuestionRanker(self.data, questions).get_sorted_questions()

    def on_question_selected(self, question):
        SOAnswersHandler(self.view, question['question_id']).start()


class SOAnswersHandler(AbstractSORequestHandler):

    lines_per_snippet = 5

    def new_thread(self):
        return SOAnswersThread(self.data)

    def on_success(self, result):
        super(SOAnswersHandler, self).on_success(result)
        snippets = self.snippets_from_items(result['items'])
        if snippets:
            self.view.show_quick_panel(
                self.format_quick_panel_snippets(snippets),
                lambda i: self.on_snippet_selected(snippets[i]))
        else:
            sublime.error_message('No snippets found')

    def format_quick_panel_snippets(self, snippets):
        result = []
        for snippet in snippets:
            lines = self.remove_blank_lines(snippet.splitlines())
            if len(lines) > self.lines_per_snippet:
                lines = lines[:self.lines_per_snippet-1] + ['...']
            else:
                lines.extend(['']*(self.lines_per_snippet - len(lines)))
            result.append(lines)
        return result

    def remove_blank_lines(self, lines):
        return [l for l in lines if l.strip() != '']

    def snippets_from_items(self, items):
        snippets = []
        for item in items:
            snippets.extend(SnippetParser(item['body']).get_snippets())
        return snippets

    def on_snippet_selected(self, snippet):
        print(snippet)
        self.view.sublime_view.run_command(
            "insert_snippet", {
                "contents": self.escape_sublime_snippet(snippet)})

    def escape_sublime_snippet(self, snippet):
        return snippet.replace('\\', '\\\\').replace('$', '\\$')
