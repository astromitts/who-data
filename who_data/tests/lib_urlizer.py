"""
Tests for who-data lib urlizer function
"""
import unittest


class urlizer(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        from who_data.lib.urlizer import urlize

        expected_results = {
            "United States": "united-states",
            "Cöte D'Ivore": "cote-d-ivore",
            "Congo (republic of)": "congo-republic-of",
        }

        for name_in, name_out in expected_results.items():
            url_name = urlize(name_in)
            self.assertEquals(name_out, url_name)

