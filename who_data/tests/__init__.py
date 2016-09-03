import unittest
from pyramid import testing


class IntegrationTestBase(unittest.TestCase):
    """
    Base class for tests that require fully integrated
    Pyramid application stack
    """

    def setUp(self):
        from who_data import main
        from webtest import TestApp
        import configparser

        config_ini = configparser.ConfigParser()
        config_ini.read('development.ini')
        self.config = testing.setUp()
        self.app = main({}, settings=config_ini._sections)
        self.TestApp = TestApp(self.app)

    def tearDown(self):
        testing.tearDown()
