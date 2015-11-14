try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO
import gzip
import json
try:
    from urllib.error import HTTPError
    from urllib.parse import urlencode
    from urllib.request import urlopen, Request
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError


class Request_(object):

    def __init__(self, url, params):
        self.url = url
        self.params = params

    def execute(self):
        try:
            request = Request(
                '{0}?{1}'.format(self.url, urlencode(self.params)))
            request.add_header('Accept-encoding', 'gzip')
            response = urlopen(request, timeout=5)
        except HTTPError as e:
            response = e
        if response.info().get('Content-Encoding') == 'gzip':
            buf = BytesIO(response.read())
            response = gzip.GzipFile(fileobj=buf)
        return response.read().decode('utf-8')


class SOError(Exception):
    pass


class SORequest(Request_):

    def __init__(self, path, params):
        params.update({
            'site': 'stackoverflow'
        })
        super(SORequest, self).__init__(
            'https://api.stackexchange.com/2.2/{0}'.format(path), params)

    def execute(self):
        result = json.loads(super(SORequest, self).execute())
        if 'error_message' in result:
            raise SOError(str(result))
        return result
