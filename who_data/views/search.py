from pyramid.response import Response  # noqa
from pyramid.view import view_config
from collections import OrderedDict


class SearchViewBase(object):

    def __init__(self, request):
        self.request = request
        self.return_dict = OrderedDict()

        # all searchers should return the following properties:
        self.return_dict['meta'] = OrderedDict([
            ('self_link', None),
            ('next_link', None),
            ('prev_link', None)
        ])
        self.return_dict['results'] = OrderedDict([
            ('total_items', None),
            ('total_pages', None),
            ('page', None),
            ('items', []),
        ])

    def __call__(self):
        self.__fetch_items__()
        return self.return_dict

    def __fetch_items__(self):
        raise NotImplementedError()


@view_config(route_name='search_ping', renderer='json')
class SearchBlank(SearchViewBase):

    def __fetch_items__(self):
        pass
