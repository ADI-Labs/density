import density
import unittest
import re


class TestAuth(unittest.TestCase):

    def test_email_regex(self):
        """ Tests the regex used to filter Oauth applicants """
        cases = [
            ('nsb2142@columbia.edu', True),
            ('nsb2142@columbia.eduABC', False),
            ('@@nsb2142@columbia.edu', False),
            ('jae@cs.columbia.edu', True),
            ('nsb2142@barnard.edu', True),
            ('nsb2142@yale.edu', False),
        ]

        for email, res in cases:
            self.assertEqual(
                bool(re.match(density.CU_EMAIL_REGEX, email)),
                res)
