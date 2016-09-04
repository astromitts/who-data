from pyramid.response import Response  # noqa
from pyramid.view import view_config
from collections import OrderedDict


@view_config(route_name='home', renderer='json')
def home_view(request):
    hello = OrderedDict()
    hello['message'] = (
        'Hello. some day, this page will be a pretty HTML document. '
        'Right now though, you can just use it to link to other pages '
        'in the app that are complete.'
    ),
    hello['links'] = [
        request.route_url('api_v1_country_search', api_version='v1'),
        request.route_url('api_v1_disease_search', api_version='v1'),
    ]
    return hello
