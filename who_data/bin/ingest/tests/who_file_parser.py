'''
Tests for the WHOFileParser class
'''

from who_data.bin.ingest.tests import TestBase


class WHOFileParser(TestBase):
    def parse(self):
        from who_data.bin.ingest.lib.who_file_parser import WHOFileParser
        test_file_path = (
            'who_data/bin/ingest/tests/who-sample-file.csv'
        )
        parsed_data = WHOFileParser('test', test_file_path)
        parsed_data.parse()
        # there are 6 rows of data in the sample file
        self.assertTrue(len(parsed_data.data) == 6)
        test_row = parsed_data.data[3]

        # the 4th data row should be Cote d'Ivoire
        self.assertTrue(test_row['country'] == "Cote d'Ivoire")

        # there should be the following years in the test row:
        for i in range(1989, 2011):
            self.assertTrue(i in test_row['reports_by_year'])
        self.assertTrue(test_row['reports_by_year'][2004] == 21)
