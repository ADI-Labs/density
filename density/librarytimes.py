import datetime

OPENING_TIME_WEEKDAY = {
    'Architectural and Fine Arts Library 1': [[900, 2300]],
    'Architectural and Fine Arts Library 2': [[900, 2300]],
    'Architectural and Fine Arts Library 3': [[900, 2300]],
    'Butler Library 2': [[0, 2400]],
    'Butler Library 3': [[0, 2400]],
    'Butler Library 4': [[0, 2400]],
    'Butler Library 301': [[0, 2400]],
    'Butler Library 5': [[900, 2300]],
    'Butler Library 6': [[900, 2300]],
    'Butler Library stk': [[900, 2300]],
    "JJ's Place": [[1200, 2400], [0, 1000]],
    'John Jay Dining Hall': [[930, 2100]],
    'Lehman Library 2': [[900, 1200]],
    'Lehman Library 3': [[900, 1200]],
    'Lerner 1': [[730, 2400], [0, 100]],
    'Lerner 2': [[730, 2400], [0, 100]],
    'Lerner 3': [[730, 2400], [0, 100]],
    'Lerner 4': [[730, 2400], [0, 100]],
    'Lerner 5': [[730, 2400], [0, 100]],
    'Roone Arledge Auditorium': [[730, 2400], [0, 100]],
    'Science and Engineering Library': [[900, 2400], [0, 300]],
    'Starr East Asian Library': [[900, 2300]],
    'Uris/Watson Library': [[800, 2400]],
}

OPENING_TIME_THURSDAY = {
    'Architectural and Fine Arts Library 1': [[900, 2300]],
    'Architectural and Fine Arts Library 2': [[900, 2300]],
    'Architectural and Fine Arts Library 3': [[900, 2300]],
    'Butler Library 2': [[0, 2400]],
    'Butler Library 3': [[0, 2400]],
    'Butler Library 4': [[0, 2400]],
    'Butler Library 301': [[0, 2400]],
    'Butler Library 5': [[900, 2300]],
    'Butler Library 6': [[900, 2300]],
    'Butler Library stk': [[900, 2300]],
    "JJ's Place": [[1200, 2400], [0, 1000]],
    'John Jay Dining Hall': [[930, 2100]],
    'Lehman Library 2': [[900, 1200]],
    'Lehman Library 3': [[900, 1200]],
    'Lerner 1': [[730, 2400], [0, 300]],
    'Lerner 2': [[730, 2400], [0, 300]],
    'Lerner 3': [[730, 2400], [0, 300]],
    'Lerner 4': [[730, 2400], [0, 300]],
    'Lerner 5': [[730, 2400], [0, 300]],
    'Roone Arledge Auditorium': [[730, 2400], [0, 300]],
    'Science and Engineering Library': [[900, 2400], [0, 300]],
    'Starr East Asian Library': [[900, 2300]],
    'Uris/Watson Library': [[800, 2200]],
}

OPENING_TIME_FRIDAY = {
    'Architectural and Fine Arts Library 1': [[900, 2100]],
    'Architectural and Fine Arts Library 2': [[900, 2100]],
    'Architectural and Fine Arts Library 3': [[900, 2100]],
    'Butler Library 2': [[0, 2400]],
    'Butler Library 3': [[0, 2400]],
    'Butler Library 4': [[0, 2400]],
    'Butler Library 301': [[0, 2400]],
    'Butler Library 5': [[900, 2100]],
    'Butler Library 6': [[900, 2100]],
    'Butler Library stk': [[900, 2100]],
    "JJ's Place": [[1200, 2400], [0, 1000]],
    'John Jay Dining Hall': [],
    # [] will return "NOT OPEN TODAY", size == 0
    'Lehman Library 2': [[900, 1900]],
    'Lehman Library 3': [[900, 1900]],
    'Lerner 1': [[730, 2400], [0, 300]],
    'Lerner 2': [[730, 2400], [0, 300]],
    'Lerner 3': [[730, 2400], [0, 300]],
    'Lerner 4': [[730, 2400], [0, 300]],
    'Lerner 5': [[730, 2400], [0, 300]],
    'Roone Arledge Auditorium': [[730, 2400], [0, 300]],
    'Science and Engineering Library': [[900, 2400], [0, 100]],
    'Starr East Asian Library': [[900, 1900]],
    'Uris/Watson Library': [[800, 2100]],
}

OPENING_TIME_SATURDAY = {
    'Architectural and Fine Arts Library 1': [[1000, 2100]],
    'Architectural and Fine Arts Library 2': [[1000, 2100]],
    'Architectural and Fine Arts Library 3': [[1000, 2100]],
    'Butler Library 2': [[0, 2400]],
    'Butler Library 3': [[0, 2400]],
    'Butler Library 4': [[0, 2400]],
    'Butler Library 301': [[0, 2400]],
    'Butler Library 5': [1100, 1800],
    'Butler Library 6': [1100, 1800],
    'Butler Library stk': [1100, 1800],
    "JJ's Place": [[1200, 2400], [0, 1000]],
    'John Jay Dining Hall': [],
    'Lehman Library 2': [1000, 1800],
    'Lehman Library 3': [1000, 1800],
    'Lerner 1': [[800, 2400], [0, 300]],
    'Lerner 2': [[800, 2400], [0, 300]],
    'Lerner 3': [[800, 2400], [0, 300]],
    'Lerner 4': [[800, 2400], [0, 300]],
    'Lerner 5': [[800, 2400], [0, 300]],
    'Roone Arledge Auditorium': [[800, 2400], [0, 300]],
    'Science and Engineering Library': [[1000, 2300]],
    'Starr East Asian Library': [[1200, 1900]],
    'Uris/Watson Library': [[1000, 1800]],
}

OPENING_TIME_SUNDAY = {
    'Architectural and Fine Arts Library 1': [[1200, 2200]],
    'Architectural and Fine Arts Library 2': [[1200, 2200]],
    'Architectural and Fine Arts Library 3': [[1200, 2200]],
    'Butler Library 2': [[0, 2400]],
    'Butler Library 3': [[0, 2400]],
    'Butler Library 4': [[0, 2400]],
    'Butler Library 301': [[0, 2400]],
    'Butler Library 5': [1200, 2300],
    'Butler Library 6': [1200, 2300],
    'Butler Library stk': [1200, 2300],
    "JJ's Place": [[1200, 2400], [0, 1000]],
    'John Jay Dining Hall': [[930, 2100]],
    'Lehman Library 2': [[1100, 2300]],
    'Lehman Library 3': [[1100, 2300]],
    'Lerner 1': [[800, 2400], [0, 100]],
    'Lerner 2': [[800, 2400], [0, 100]],
    'Lerner 3': [[800, 2400], [0, 100]],
    'Lerner 4': [[800, 2400], [0, 100]],
    'Lerner 5': [[800, 2400], [0, 100]],
    'Roone Arledge Auditorium': [[800, 2400], [0, 100]],
    'Science and Engineering Library': [[1100, 2400], [0, 300]],
    'Starr East Asian Library': [[1200, 2200]],
    'Uris/Watson Library': [[1000, 2300]],
}

OPENING_TIME = [OPENING_TIME_WEEKDAY,
                OPENING_TIME_WEEKDAY,
                OPENING_TIME_WEEKDAY,
                OPENING_TIME_THURSDAY,
                OPENING_TIME_FRIDAY,
                OPENING_TIME_SATURDAY,
                OPENING_TIME_SUNDAY, ]


def dict_for_time():
    # get library opening times according to today's day in a week
    today = datetime.datetime.today()
    weekday = today.weekday()
    library_times = OPENING_TIME[weekday]

    # get the current hour and minute in the format HHMM
    current_time = (datetime.datetime.now().hour * 100) + \
                   (datetime.datetime.now().minute)

    message = {}

    for group_name in library_times.keys():
        open_time = library_times[group_name]
        message[group_name] = get_opening_time(current_time, open_time)

    return message


def get_opening_time(current_time, interval):
    # get closing time
    if (time_is_in_interval(current_time, interval)):
        # if the library is open 24/7
        if (interval == [[0, 2400]]):
            output = " (Opens 24 hrs) "

        # if the library's closing hour goes beyond midnight
        elif (len(interval) == 2):
            close_hour = int(interval[1][1] / 100)
            output = " (Closes at " + str(close_hour) + "AM)"

        # if the library closes before midnight
        else:
            close_hour = int(interval[0][1] / 100)
            output = " (Closes at " + str(close_hour - 12) + "PM)"

    # get opening time
    else:
        if (len(interval) == 0):
            output = " (Closed Today)"
        else:
            open_hour = int(interval[0][0] / 100)
            output = " (Opens at " + str(open_hour) + "AM)"

    return output


def time_is_in_interval(time, interval):
    if len(interval) == 0:
        return False
    elif len(interval) == 1:
        if (time < interval[0][0]) or (time > interval[0][1]):
            return False
        else:
            return True
    else:
        if (time > interval[1][1]) and (time < interval[0][0]):
            return False
        else:
            return True
