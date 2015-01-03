import template
import json


class TestLatestRoute(template.TestingTemplate):

    def test_latest_data(self):
        resp = self.authenticated_get('/latest')
        self.assertEqual(200, resp.status_code)

        json_resp = json.loads(resp.data)

        # check number of responses
        self.assertEqual(22, len(json_resp['data']))

        # check number of empty rooms
        self.assertEqual(2, len([r for r in json_resp['data']
                                 if not r['client_count']]))
