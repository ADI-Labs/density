import datetime
from . import librarytimes

LOCATION_AUX_DATA = {
    'Architectural and Fine Arts Library 1': {
        'nickname': 'Avery 1',
        'type': 'library'
    },
    'Architectural and Fine Arts Library 2': {
        'nickname': 'Avery 2',
        'type': 'library'
    },
    'Architectural and Fine Arts Library 3': {
        'nickname': 'Avery 3',
        'type': 'library'
    },
    'Butler Library 2': {
        'nickname': '',
        'type': 'library'
    },
    'Butler Library 3': {
        'nickname': '',
        'type': 'library'
    },
    'Butler Library 4': {
        'nickname': '',
        'type': 'library'
    },
    'Butler Library 301': {
        'nickname': '',
        'type': 'library'
    },
    'Butler Library 5': {
        'nickname': '',
        'type': 'library'
    },
    'Butler Library 6': {
        'nickname': '',
        'type': 'library'
    },
    'Butler Library stk': {
        'nickname': 'Stacks',
        'type': 'library'
    },
    "JJ's Place": {
        'nickname': 'JJs',
        'type': 'dining'
    },
    'John Jay Dining Hall': {
        'nickname': '',
        'type': 'dining'
    },
    'Lehman Library 2': {
        'nickname': '',
        'type': 'library'
    },
    'Lehman Library 3': {
        'nickname': '',
        'type': 'library'
    },
    'Lerner 1': {
        'nickname': '',
        'type': 'center'
    },
    'Lerner 2': {
        'nickname': '',
        'type': 'center'
    },
    'Lerner 3': {
        'nickname': 'Ferris',
        'type': 'center'
    },
    'Lerner 4': {
        'nickname': '',
        'type': 'center'
    },
    'Lerner 5': {
        'nickname': '',
        'type': 'center'
    },
    'Roone Arledge Auditorium': {
        'nickname': '',
        'type': 'center'
    },
    'Science and Engineering Library': {
        'nickname': 'NoCo',
        'type': 'library'
    },
    'Starr East Asian Library': {
        'nickname': 'Kent',
        'type': 'library'
    },
    'Uris/Watson Library': {
        'nickname': '',
        'type': 'library'
    },
}

def get_location_aux_data():
    output = {}
    times = librarytimes.dict_for_time()    

    for group_name in LOCATION_AUX_DATA.keys():
        data = LOCATION_AUX_DATA[group_name]
        data['open'] = librarytimes.is_open(group_name)
        output[group_name] = data

    return output