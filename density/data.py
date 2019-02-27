# The max historical capacity of each building Density has recorded
FULL_CAP_DATA_MAX_HISTORY = {
    'Architectural and Fine Arts Library 1': 27,
    'Architectural and Fine Arts Library 2': 362,
    'Architectural and Fine Arts Library 3': 220,
    'Butler Library 2': 729,
    'Butler Library 3': 438,
    'Butler Library 4': 414,
    'Butler Library 301': 292,
    'Butler Library 5': 236,
    'Butler Library 6': 255,
    'Butler Library stk': 245,
    "JJ's Place": 185,
    'John Jay Dining Hall': 319,
    'Lehman Library 2': 213,
    'Lehman Library 3': 700,
    'Lerner 1': 168,
    'Lerner 2': 362,
    'Lerner 3': 357,
    'Lerner 4': 354,
    'Lerner 5': 373,
    'Roone Arledge Auditorium': 923,
    'Science and Engineering Library': 234,
    'Starr East Asian Library': 257,
    'Uris/Watson Library': 1046
}

# Global variable used in other files
"""
    key: str building_name
    value: int max_capacity
"""
FULL_CAP_DATA = {}

# Global variable used in other files
"""
    type: list of list of list of ints
    COMBINATIONS[day][cluster]: int list with days_of_week to use for day #day (Monday = 0) and cluster #cluster (varies by day)
                                days in the array are ints (0-Sunday, 6-Saturday)
"""
COMBINATIONS = []
COMBINATIONS.append([[1], [1,2], [1,3], [1,2,3], [1,2,3,4], [1,2,3,4,5]]) # Monday
COMBINATIONS.append([[2], [2,1], [2,3], [1,2,3], [1,2,3,4], [1,2,3,4,5]]) # Tuesday
COMBINATIONS.append([[3], [3,1], [3,2], [1,2,3], [1,2,3,4], [1,2,3,4,5]]) # Wednesday
COMBINATIONS.append([[4], [4,5], [3,4], [3,4,5], [1,2,3,4,5]]) # Thursday
COMBINATIONS.append([[5], [5,6], [4,5], [5,0], [5,6,0]]) # Friday
COMBINATIONS.append([[6], [6,0], [5,6], [5,6,0]]) # Saturday
COMBINATIONS.append([[0], [6,0], [5,0], [5,6,0]]) # Sunday

def resize_full_cap_data(percentage):
    """
        Resizes dict FULL_CAP_DATA used as global variable for all buildings' max capacity
        :param int percentage: percentage to multiply each FULL_CAP_DATA value by
        :return: error message
        :rtype: str
    """
    if (percentage < 0 or percentage > 1):
        return "parameter must be between 0 and 1"

    for key, value in FULL_CAP_DATA_MAX_HISTORY.items():
        FULL_CAP_DATA[key] = int(value*percentage)

    return "0"


    