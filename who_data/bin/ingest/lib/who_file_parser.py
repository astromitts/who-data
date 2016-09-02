'''
Class for a standard WHO Data file for a tropical disease cases reported
CSV File

This class should take in an absolute filepath to a CSV and parse the file,
storing the information in a dictionary
'''

import csv
from who_data.bin.ingest.lib.file_hash import file_hash

class WHOFileParser(object):

    def __init__(self, pkey, file_path):
        self.pkey = pkey
        self._file_path = file_path
        self.file_hash = file_hash(file_path)
        self.header_years = []
        self.data = []

    def _parse_header_years(self, header_row):
        '''
        Take in a list of file headers and parse out the year, returning
        only a list of the years as the headers

        Luckily, we know for now that each WHO file header is in the same
        format: "something something something; YYYY" so just grab the last
        4 characters of each header
        '''
        parsed_header = [int(i[-4:]) for i in header_row]
        return parsed_header


    def parse(self):
        '''
        Do the actual file parsing here
        This function should return a list of dictionaries which represents
        reported cases by year, where each entry looks like:
        {
            'country': 'country-name',
            'reports_by_year':{
                1990: 123,
                1991: 176,
                [...]
            }
        }
        '''
        file = open(self._file_path, 'r')
        reader = csv.reader(file)
        raw_header = reader.__next__()
        raw_header.remove('Country')

        self.header_years = self._parse_header_years(raw_header)

        result_rows = []
        for row in reader:
            country = row[0]
            reports_by_year = {}
            position = 1
            for year in self.header_years:
                try:
                    reports_by_year[year] = int(row[position])
                except Exception:
                    reports_by_year[year] = None
                position += 1
            result_rows.append(
                {
                    'country': country,
                    'reports_by_year': reports_by_year
                }
            )
        self.data = result_rows
