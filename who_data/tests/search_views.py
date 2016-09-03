from who_data.tests import IntegrationTestBase


class SearchViewTests(IntegrationTestBase):

    def test_json_structure(self):
        '''
        Test that the basic search JSON logic works and has expected structure
        '''
        page = self.TestApp.get('/search/ping', status=200)
        self.assertTrue('meta' in page.json)
        self.assertTrue('self_link' in page.json['meta'])
        self.assertTrue('next_link' in page.json['meta'])
        self.assertTrue('prev_link' in page.json['meta'])
        self.assertTrue('results' in page.json)
        self.assertTrue('total_items' in page.json['results'])
        self.assertTrue('total_pages' in page.json['results'])
        self.assertTrue('page' in page.json['results'])
        self.assertTrue('items' in page.json['results'])
