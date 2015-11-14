import sublime


class View(object):

    def __init__(self, sublime_view):
        self.sublime_view = sublime_view
        self.active_status_count = 0

    def show_status(self, message, timeout=None):
        self.sublime_view.set_status(
            'sosnippets', 'Stack Overflow Snippets: {0}'.format(message))
        if timeout is not None:
            self.active_status_count += 1
            sublime.set_timeout(self.on_status_timeout, timeout)

    def on_status_timeout(self):
        if self.active_status_count > 0:
            self.active_status_count -= 1
        if self.active_status_count == 0:
            self.hide_status()

    def hide_status(self):
        self.sublime_view.erase_status('sosnippets')

    def show_quick_panel(self, messages, callback):
        self.sublime_view.window().show_quick_panel(
            messages, lambda i: self.on_message_selected(i, callback),
            sublime.MONOSPACE_FONT)

    def on_message_selected(self, message_index, callback):
        if message_index != -1:
            callback(message_index)
