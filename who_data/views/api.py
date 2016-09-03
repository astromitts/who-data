from pyramid.response import Response  # noqa
from pyramid.view import view_config
from collections import OrderedDict
import math
from pyramid.httpexceptions import HTTPNotFound
from who_data.models.who import Country, WHODiseaseReport


class APIBase(object):
    _valid_versions = {
        'v1': 1,
    }

    def __init__(self, request):
        self.request = request
        self.api_version = self._valid_versions.get(
            request.matchdict['api_version']
        )

        # bail if unknown version
        if not self.api_version:
            raise HTTPNotFound


class APISearchablePage(APIBase):
    """
    Base class for API pages that accept search parameters and pagination
    """
    _per_page_limit = None
    model = None

    def __init__(self, request):
        super(APISearchablePage, self).__init__(request)

        # bet base URL for use in metadata links
        self._link_base = self.request.host_url + self.request.path

        # determine the page and offset, default to 1
        self._page = int(self.request.GET.get('_page', '1'))
        if self._per_page_limit:
            self._offset = (self._page - 1) * self._per_page_limit

        self.return_dict = OrderedDict()

        # all searches should return the following properties:
        self.return_dict['meta'] = OrderedDict([
            ('self_link', self.request.url),
            ('next_link', None),
            ('prev_link', None),
            ('api_version', self.api_version)
        ])
        self.return_dict['results'] = OrderedDict([
            ('total_items', 0),
            ('total_pages', 0),
            ('total_page_items', 0),
            ('page', self._page),
            ('items', []),
        ])

    def __call__(self):
        self.__fetch_items__()
        self.__set_result_meta__()
        return self.return_dict

    def __set_result_meta__(self):
        total_items = self.return_dict['results']['total_items']
        if self._per_page_limit:
            total_pages = math.ceil(total_items / self._per_page_limit)
            total_page_items = len(self.return_dict['results']['items'])
        else:
            total_pages = 1
            total_page_items = self.return_dict['results']['total_items']
        self.return_dict['results']['total_pages'] = total_pages
        self.return_dict['results']['total_page_items'] = total_page_items

        # set previous link
        if self._page > 1:
            self.return_dict['meta']['prev_link'] = (
                self._link_base + '?_page=%s' % (self._page - 1)
            )

        # set next link
        if self._page < total_pages:
            self.return_dict['meta']['next_link'] = (
                self._link_base + '?_page=%s' % (self._page + 1)
            )

    def __format_results__(self, result_rows):
        """
        Format result rows and add them to api return structure
        By default, just append the rows as-is
        Override this function for resource specific formatting
        """
        for row in result_rows:
            self.return_dict['results']['items'].append(row)

    def __fetch_items__(self):
        count, rows = self.model.search(
            limit=self._per_page_limit,
            offset=self._offset,
        )
        self.return_dict['results']['total_items'] = count
        self.__format_results__(rows)


@view_config(route_name='api_v1_ping', renderer='json')
class APIPing(APISearchablePage):

    def __fetch_items__(self):
        pass


@view_config(route_name='api_v1_country_search', renderer='json')
class APICountryLanding(APISearchablePage):
    _per_page_limit = 25
    model = Country

    def __format_results__(self, result_rows):
        """
        Override result format function
        """
        for row in result_rows:
            self.return_dict['results']['items'].append(
                {
                    'name': row['name'],
                    'link': self.request.route_url(
                        'api_v1_country_resource',
                        api_version='v%s' % self.api_version,
                        url_name=row['url_name']
                    )
                }
            )


class APIResourcePage(APIBase):
    """
    Base class for API pages that represent a resource - these should point
    to a single instance of an object type, it is not searchable or paginated
    """
    def __init__(self, request):
        super(APIResourcePage, self).__init__(request)

        # all resources should return the following properties:
        self.return_dict = OrderedDict()
        self.return_dict['meta'] = OrderedDict([
            ('self_link', self.request.url),
            ('api_version', self.api_version)
        ])
        self.return_dict['resource'] = OrderedDict()

    def __call__(self):
        return self.return_dict


@view_config(route_name='api_v1_country_resource', renderer='json')
class APICountryResource(APIResourcePage):

    def __call__(self):
        url_name = self.request.matchdict['url_name']
        resource = Country.fetch_first(url_name=url_name)
        if resource:
            self.return_dict['resource']['country'] = {
                'name': resource['name'],
                'alias': resource['alias'],
                'id': resource['id'],
            }
            report_rows = WHODiseaseReport.get_for_country(
                country_id=resource['id']
            )
            report_dicts = OrderedDict()
            for report in report_rows:
                report_dicts[report.id] = report_dicts.get(
                    report.id,
                    OrderedDict([
                        ('disease', {
                            'name': report.name,
                        }),
                        ('reports', []),
                    ])
                )
                report_dicts[report.id]['reports'].append(
                    {
                        'year': report.year,
                        'count': report.report_count,
                    }
                )
            self.return_dict['resource']['disease_reports'] = []
            for key, rd in report_dicts.items():
                self.return_dict['resource']['disease_reports'].append(rd)
        else:
            raise HTTPNotFound

        return self.return_dict
