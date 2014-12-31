import template
import json


class TestLatestRoute(template.TestingTemplate):

    def test_number_rooms(self):
        resp = self.app.get('/latest')
        self.assertEqual(200, resp.status_code)

        json_resp = json.loads(resp.data)
        self.assertEqual(22, len(json_resp['data']))


    def test_number_empty_rooms(self):
        resp = self.app.get('/latest')
        self.assertEqual(200, resp.status_code)

        json_resp = json.loads(resp.data)
        self.assertEqual(2, len([r for r in json_resp['data'] if not r['client_count']]))

