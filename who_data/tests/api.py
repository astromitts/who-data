""" Tests for search views in the WHO Data Pyramid App
"""

from who_data.tests import IntegrationTestBase


class APITests(IntegrationTestBase):

    def invalid_version(self):
        self.TestApp.get('/api/v2/ping', status=404)

    def ping(self):
        '''
        Test that the basic search JSON logic works and has expected structure
        '''
        page = self.TestApp.get('/api/v1/ping', status=200)
        self.assertTrue('meta' in page.json)
        self.assertTrue('self_link' in page.json['meta'])
        self.assertTrue('next_link' in page.json['meta'])
        self.assertTrue('prev_link' in page.json['meta'])
        self.assertTrue('api_version' in page.json['meta'])
        self.assertTrue('results' in page.json)
        self.assertTrue('total_items' in page.json['results'])
        self.assertTrue('total_pages' in page.json['results'])
        self.assertTrue('total_page_items' in page.json['results'])
        self.assertTrue('page' in page.json['results'])
        self.assertTrue('items' in page.json['results'])

    def country_search_page(self):
        page = self.TestApp.get('/api/v1/countries', status=200)
        self.assertTrue(page.json['results']['total_items'] > 0)
        self.assertEquals(
            page.json['meta']['self_link'],
            'http://localhost/api/v1/countries'
        )
        self.assertEquals(
            page.json['meta']['next_link'],
            'http://localhost/api/v1/countries?_page=2'
        )
        self.assertEquals(
            page.json['meta']['prev_link'],
            None
        )

        page = self.TestApp.get(
            '/api/v1/countries?_page=%s' % (
                page.json['results']['total_pages']
            ),
            status=200
        )
        self.assertEquals(
            page.json['meta']['self_link'],
            'http://localhost/api/v1/countries?_page=%s' % (
                page.json['results']['total_pages']
            )
        )
        self.assertEquals(
            page.json['meta']['prev_link'],
            'http://localhost/api/v1/countries?_page=%s' % (
                page.json['results']['total_pages'] - 1
            )
        )
        self.assertEquals(
            page.json['meta']['next_link'],
            None
        )

    def country_resource_page(self):
        page = self.TestApp.get(
            '/api/v1/countries/brunei-darussalam',
            status=200
        )
        self.assertTrue('meta' in page.json)
        self.assertTrue('self_link' in page.json['meta'])
        self.assertTrue('api_version' in page.json['meta'])
        self.assertTrue('resource' in page.json)
        self.assertEquals(
            page.json['resource']['country']['name'],
            'Brunei Darussalam'
        )
        self.assertTrue('disease_reports' in page.json['resource'])
        self.assertTrue(
            len(page.json['resource']['disease_reports']) >= 3
        )

    def country_resource_notfound(self):
        self.TestApp.get(
            '/api/v1/countries/narnia',
            status=404
        )

    def disease_search_logic(self):
        def test_results(items):
            '''
            verify that returned items are within requested params
            '''
            for item in items:
                self.assertTrue(item['count'] >= 5000)
                self.assertTrue(item['year'] >= 1989)
                self.assertTrue(item['year'] <= 1995)

        # verify a searches for a range of matches on number fields
        page = self.TestApp.get(
            '/api/v1/diseases/guinea-worm/search?year=1989:1995&count=5000:',
            status=200
        )
        self.assertEquals(
            page.json['meta']['next_link'],
            'http://localhost/api/v1/diseases/guinea-worm/'
            'search?year=1989:1995&count=5000:&_page=2'
        )
        test_results(page.json['results']['items'])

        page = self.TestApp.get(
            '/api/v1/diseases/guinea-worm/search?year='
            '1989:1995&count=5000:&_page=2',
            status=200
        )
        self.assertEquals(
            page.json['meta']['prev_link'],
            'http://localhost/api/v1/diseases/guinea-worm/'
            'search?year=1989:1995&count=5000:'
        )
        test_results(page.json['results']['items'])

        # verify a search for an exact match on a number field
        page = self.TestApp.get(
            '/api/v1/diseases/guinea-worm/search?year='
            '1989:1995&count=5029',
            status=200
        )

        for item in page.json['results']['items']:
            self.assertTrue(item['count'] == 5029)
