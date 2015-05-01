import unittest

from density import calculate_capacity


class TestCalculateCapacity(unittest.TestCase):

    # testing logic in calulate_capacity()
    def test_calculate_capacity(self):

        # test version of cap_data
        cap_test = [
            {'capacity': 100, 'group_name': 'Butler Library 6',
             'parent_id': 103, 'parent_name': 'Butler'},
            # test stk ->stacks
            {'capacity': 255, 'group_name': 'Butler Library stk',
             'parent_id': 103, 'parent_name': 'Butler'},
            {'capacity': 75, 'group_name': "JJ's Place",
             'parent_id': 75, 'parent_name': 'John Jay'},
            {'capacity': 150, 'group_name': 'Starr East Asian Library',
             'parent_id': 62, 'parent_name': 'East Asian Library'}
        ]

        # test version of cur_data
        cur_test = [
            {'client_count': 78, 'group_name': 'Butler Library 6'},
            {'client_count': 80, 'group_name': "JJ's Place"},  # test > 100%
            {'client_count': 15, 'group_name': 'Starr East Asian Library'},
            {'client_count': 100, 'group_name': 'Butler Library stk'}
        ]

        # test (expected) version of locations
        loc_accurate = [
            {'name': 'Butler Library 6', 'fullness': 78,
             'parentId': 103, 'parentName': 'Butler'},
            {'name': 'Butler Library Stacks', 'fullness': 39,
             'parentId': 103, 'parentName': 'Butler'},
            {'name': "JJ's Place", 'fullness': 100,
             'parentId': 75, 'parentName': 'John Jay'},
            {'name': 'Starr East Asian Library', 'fullness': 10,
             'parentId': 62, 'parentName': 'East Asian Library'}
        ]

        loc_test = calculate_capacity(cap_test, cur_test)

        # need to add test for parent_id and parent_name
        for i in range(len(loc_accurate)):
            self.assertEqual(loc_accurate[i]['name'], loc_test[i]['name'])
            self.assertEqual(loc_accurate[i]['fullness'],
                             loc_test[i]['fullness'])
            self.assertEqual(loc_accurate[i]['parentId'],
                             loc_test[i]['parentId'])
            self.assertEqual(loc_accurate[i]['parentName'],
                             loc_test[i]['parentName'])
