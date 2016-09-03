from pyramid.response import Response  # noqa
from pyramid.view import view_config
from collections import OrderedDict
from pyramid.httpexceptions import HTTPNotFound
from who_data.models.who import Country


class APIViewBase(object):
    valid_versions = {
        'v1': 1,
    }

    def __init__(self, request):
        self.request = request
        self.api_version = self.valid_versions.get(
            request.matchdict['api_version']
        )
        if not self.api_version:
            raise HTTPNotFound

        self.return_dict = OrderedDict()

        # all searchers should return the following properties:
        self.return_dict['meta'] = OrderedDict([
            ('self_link', None),
            ('next_link', None),
            ('prev_link', None),
            ('api_version', self.api_version)
        ])
        self.return_dict['results'] = OrderedDict([
            ('total_items', 0),
            ('total_pages', 0),
            ('page', None),
            ('items', []),
        ])

    def __call__(self):
        self.__fetch_items__()
        return self.return_dict

    def __fetch_items__(self):
        raise NotImplementedError()


@view_config(route_name='api_v1_ping', renderer='json')
class APIPing(APIViewBase):

    def __fetch_items__(self):
        pass


@view_config(route_name='api_v1_country_landing', renderer='json')
class APICountryLanding(APIViewBase):

    def __fetch_items__(self):
        count, rows = Country.search()
        self.return_dict['results']['total_items'] = count
