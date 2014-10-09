
import unittest
import json


class TestingTemplate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """ Instantiates a test instance of the app before each test """
        self.app = data.app.test_client()
        # TODO: any db standardization

    @classmethod
    def tearDownClass(self):
        """ clean up databases """
        # TODO: any db sanitization
        pass

