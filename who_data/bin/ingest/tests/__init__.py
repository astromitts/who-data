import unittest

class TestBase(unittest.TestCase):
    ''' Base class for tests that do not require database connectvity
    '''
    def setUp(self):
        pass

    def tearDown(self):
        pass