import template
import json
import density


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

    def test_annotate_fullness_percentage(self):
        cur_data = [{
            "client_count": 5,
            "dump_time": "Sat, 01 Nov 2014 19:45:00 GMT",
            "group_id": 147,
            "group_name": "Architectural and Fine Arts Library 1",
            "parent_id": 146,
            "parent_name": "Avery"
        }]
        # Extract capacity of lib from FULL_CAP_DATA
        AFALibrary1_capacity = 0
        for cap in density.FULL_CAP_DATA:
            if cap['group_id'] == 147:
                AFALibrary1_capacity = cap['capacity']
                break
        result_percent = 5.0 / AFALibrary1_capacity * 100
        result_data = [{
            "client_count": 5,
            "dump_time": "Sat, 01 Nov 2014 19:45:00 GMT",
            "group_id": 147,
            "group_name": "Architectural and Fine Arts Library 1",
            "parent_id": 146,
            "parent_name": "Avery",
            "percent_full": result_percent
        }]
        self.assertEqual(result_data, density.annotate_fullness_percentage(
            cur_data))
