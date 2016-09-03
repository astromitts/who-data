""" Tests for search views in the WHO Data Pyramid App
"""

from who_data.tests import IntegrationTestBase


class APITests(IntegrationTestBase):

    def invalid_version(self):
        page = self.TestApp.get('/who-data/api/v2/ping', status=404)

    def ping(self):
        '''
        Test that the basic search JSON logic works and has expected structure
        '''
        page = self.TestApp.get('/who-data/api/v1/ping', status=200)
        self.assertTrue('meta' in page.json)
        self.assertTrue('self_link' in page.json['meta'])
        self.assertTrue('next_link' in page.json['meta'])
        self.assertTrue('prev_link' in page.json['meta'])
        self.assertTrue('api_version' in page.json['meta'])
        self.assertTrue('results' in page.json)
        self.assertTrue('total_items' in page.json['results'])
        self.assertTrue('total_pages' in page.json['results'])
        self.assertTrue('page' in page.json['results'])
        self.assertTrue('items' in page.json['results'])

    def country_landing_page(self):
        page = self.TestApp.get('/who-data/api/v1/countries', status=200)
        self.assertTrue(page.json['results']['total_items'] > 0)
