import pandas as pd
import numpy as np
import datetime
import psycopg2
from matplotlib import pyplot as plt

conn = psycopg2.connect(dbname="local_density", user="adicu", password="password")

SELECT = """
    SELECT d.client_count, d.dump_time,
           r.id AS group_id, r.name AS group_name,
           b.id AS parent_id, b.name AS building_name
    FROM density_data d
    JOIN routers r ON r.id = d.group_id
    JOIN buildings b ON b.id = r.building_id"""

FULL_CAP_DATA = {
    'Architectural and Fine Arts Library 1': 22,
    'Architectural and Fine Arts Library 2': 272,
    'Architectural and Fine Arts Library 3': 133,
    'Butler Library 2': 573,
    'Butler Library 3': 413,
    'Butler Library 4': 346,
    'Butler Library 301': 282,
    'Butler Library 5': 157,
    'Butler Library 6': 220,
    'Butler Library stk': 80,
    "JJ's Place": 129,
    'John Jay Dining Hall': 200,
    'Lehman Library 2': 178,
    'Lehman Library 3': 570,
    'Lerner 1': 138,
    'Lerner 2': 224,
    'Lerner 3': 248,
    'Lerner 4': 243,
    'Lerner 5': 206,
    'Roone Arledge Auditorium': 497,
    'Science and Engineering Library': 154,
    'Starr East Asian Library': 197,
    'Uris/Watson Library': 992,
}


def db_to_pandas(cursor):
    """ Return occupancy data as pandas dataframe
    column dtypes:
        group_id: int64
        group_name: category
        parent_id: int64
        parent_name: category
        client_count: int64
        week: int64
        weekday: int64
        time_point: string
    index: DateTimeIndex -- dump_time
    Parameters
    ----------
    conn: psycopg2.extensions.connection
        Connection to db
    Returns
    -------
    pandas.DataFrame
        Density data in a Dataframe
    """
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    day_of_week = tomorrow.weekday()
    week_of_year = tomorrow.isocalendar()[1]
    query = " WHERE extract(WEEK from d.dump_time) = {} AND extract(DOW from d.dump_time) = {}".format(week_of_year, day_of_week)
    cursor.execute(SELECT + query)
    raw_data = cursor.fetchall()
    df = pd.DataFrame(raw_data) \
    	   .set_index("dump_time") \
    	   .assign(group_name=lambda df: df["group_name"].astype('category'),
                   parent_id=lambda df: df["parent_id"].astype('category'))

    time_points = zip(df.index.hour, df.index.minute)
    time_points = ["{}:{}".format(x[0], x[1]) for x in time_points]
    df["time_point"] = time_points # get time of the day (HH:mm) for a given timestamp

    return df


def predict_tomorrow(past_data):
    """Return a dataframes of predicted counts for tomorrow 
    where the indexs are timestamps of the day and columns are locations
    Parameters
    ----------
    day_dict: Dictionary
        a dictionary of dataframes of density data where the keys are days of the week
    Returns
    -------
    pandas.DataFrame
        Dataframe containing predicted counts for 96 tomorrow's timepoints
    """
    
    results, locs = [], []
    for group in np.unique(past_data["group_name"]):
        locs.append(group)
        group_data = past_data[past_data["group_name"] == group]
        group_data = group_data[["client_count", "time_point"]]
        group_result = group_data.groupby("time_point").mean()  # average counts by time for each location
        group_result = np.divide(group_result, FULL_CAP_DATA[group])  # convert capacity count to percentage
        results.append(group_result.transpose())
    result = pd.concat(results)  # combine the data for all locations
    result.index = locs
    result = result.transpose()  # make time points indexes and locations columns
    
    old_indexes = result.index
    new_indexes = []

    # make sure all time index has the same string format
    for index in old_indexes:
        splited = index.split(":")
        leading, trailing = splited[0], splited[1]
        if len(leading) == 1:
            leading = "0" + leading
        new_index = "{}:{}".format(leading, trailing)
        new_indexes.append(new_index)

    result.index = new_indexes
    result = result.sort_index()
    
    return result

