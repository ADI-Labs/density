
import unittest
import density


class TestingTemplate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """ Instantiates a test instance of the app before each test """
        self.app = density.app.test_client()
        # TODO: any db standardization

    @classmethod
    def tearDownClass(self):
        """ clean up databases """
        # TODO: any db sanitization
        pass
