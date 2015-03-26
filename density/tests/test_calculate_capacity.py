import unittest

from density import calculate_capacity


class TestCalculateCapacity(unittest.TestCase):

    # testing logic in calulate_capacity()
    def test_calculate_capacity(self):
        # test version of cap_data
        cap_test = [{'capacity': 100, 'group_name': 'Butler Library 6'},
        {'capacity': 255, 'group_name': 'Butler Library stk'},  # test stk ->stacks
        {'capacity': 75, 'group_name': "JJ's Place"},
        {'capacity': 150, 'group_name': 'Starr East Asian Library'}]
        # test version of cur_data
        cur_test = [{'client_count': 78, 'group_name': 'Butler Library 6'},
        {'client_count': 80, 'group_name': "JJ's Place"},  # test > 100%
        {'client_count': 15, 'group_name': 'Starr East Asian Library'},
        {'client_count': 100, 'group_name': 'Butler Library stk'}]  # and out of order -- is this necessary?
        # test (expected) version of locations
        loc_accurate = [{'name': 'Butler Library 6', 'fullness': 78},
        {'name': 'Butler Library Stacks', 'fullness': 39},
        {'name': "JJ's Place", 'fullness': 100},
        {'name': 'Starr East Asian Library', 'fullness': 10}]

        loc_test = calculate_capacity(cap_test, cur_test)

	for i in range(len(loc_accurate)):
            self.assertEqual(loc_accurate[i]['name'], loc_test[i]['name'])
            self.assertEqual(loc_accurate[i]['fullness'], loc_test[i]['fullness'])
