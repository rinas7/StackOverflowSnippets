try:
    from .sosnippets.requests import SORequest
except (ImportError, SystemError, ValueError):
    from sosnippets.requests import SORequest


def get_tags_from_so():
    tags = []
    for page in range(1, 10):
        print('page {}'.format(page))
        result = SORequest('tags', {
            'order': 'desc',
            'sort': 'popular',
            'page': page,
            'pagesize': 100
        }).execute()
        tags.extend([t['name'] for t in result['items']])
    return tags


if __name__ == '__main__':
    print('gettings tags from stack overflow')
    tags = get_tags_from_so()
    print('writing tags to sosnippets/so_tags.py')
    with open('sosnippets/so_tags.py', 'w') as f:
        f.write('so_tags = [\n    ')
        f.write(',\n    '.join(["'{0}'".format(t) for t in tags]))
        f.write(']\n')
