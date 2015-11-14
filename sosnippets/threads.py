import threading
import traceback

from .cache import Cache
from .requests import SORequest


class AbstractCachedThread(threading.Thread):

    caches = {}
    cache_size = 0

    def __init__(self, data):
        super(AbstractCachedThread, self).__init__()
        self.data = data
        self.result = None
        self.error = None
        self.from_cache = False

    def run(self):
        cached = self.get_cache().get(self.data)
        if cached is not None:
            self.from_cache = True
            self.result = cached
        else:
            self.from_cache = False
            self._run()
        self.get_cache().add(self.data, self.result)

    def get_cache(self):
        class_ = self.__class__
        if class_ not in self.caches:
            self.caches[class_] = Cache(self.cache_size)
        return self.caches[class_]

    def _run(self):
        try:
            self.result = self.execute()
        except Exception as e:
            traceback.print_exc()
            self.error = e
            return

    def execute(self):
        raise NotImplementedError


class SOQuestionsThread(AbstractCachedThread):

    cache_size = 25

    def execute(self):
        params = {
            'order': 'desc',
            'sort': 'votes',
            'q': self.data,
            'answers': 1,
            'pagesize': 25
        }
        return SORequest('search/advanced', params).execute()


class SOAnswersThread(AbstractCachedThread):

    cache_size = 100

    def execute(self):
        params = {
            'order': 'desc',
            'sort': 'votes',
            'pagesize': 7,
            'filter': 'withbody'
        }
        path = 'questions/{0}/answers'.format(self.data)
        return SORequest(path, params).execute()
