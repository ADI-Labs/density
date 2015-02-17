
import template
import json


class TestDateFormatChecker(template.TestingTemplate):

    def test_bad_date(self):
        resp = self.authenticated_get('/day/23/group/85')

        self.assertEqual(400, resp.status_code)

        body = json.loads(resp.data)
        self.assertIn('error', body)
        self.assertIn('YYYY-MM-DD', body.get('error'))

    def test_good_date(self):
        resp = self.authenticated_get('/day/2014-10-23/group/85')

        self.assertEqual(200, resp.status_code)

        body = json.loads(resp.data)
        self.assertEqual(len(body['data']), 96)
