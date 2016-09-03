from who_data.tests import IntegrationTestBase


class SearchViewTests(IntegrationTestBase):

    def test_json_structure(self):
        self.TestApp.get('/search/ping', status=200)
