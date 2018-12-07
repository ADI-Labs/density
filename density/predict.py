import datetime

import numpy as np
import pandas as pd


SELECT = """
    SELECT d.client_count, d.dump_time,
           r.id AS group_id, r.name AS group_name,
           b.id AS parent_id, b.name AS building_name
    FROM density_data d
    JOIN routers r ON r.id = d.group_id
    JOIN buildings b ON b.id = r.building_id"""

FULL_CAP_DATA = {
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
    'Uris/Watson Library': 1046,
}


def db_to_pandas(cursor):
    """ Return occupancy data as pandas dataframe
    column dtypes:
        building_name: string
        group_id: int64
        group_name: category
        parent_id: category
        client_count: int64
        time_point: string
    index: DateTimeIndex -- dump_time
    Parameters
    ----------
    cursor: cursor for our DB
        Connection to db
    Returns
    -------
    pandas.DataFrame
        Density data in a Dataframe
    """
    today = datetime.datetime.today()
    day_of_week = today.weekday()
    week_of_year = today.isocalendar()[1]

    # construct SQL query to fetch only the data we need
    query = ' WHERE extract(WEEK from d.dump_time) = ' + \
            '{} AND extract(DOW from d.dump_time) = '.format(week_of_year) + \
            '{}'.format(day_of_week)
    cursor.execute(SELECT + query)
    raw_data = cursor.fetchall()

    # convert fetched data to a pandas dataframe
    df = pd.DataFrame(raw_data) \
           .set_index("dump_time") \
           .assign(group_name=lambda df: df["group_name"].astype('category'),
                   parent_id=lambda df: df["parent_id"].astype('category'))

    # add a new time point column to the datafram
    time_points = zip(df.index.hour, df.index.minute)
    time_points = ["{}:{}".format(x[0], x[1]) for x in time_points]
    df["time_point"] = time_points

    return df

def predict_today(past_data):
    """Return a dataframes of predicted counts for today
    where the indexs are timestamps of the day and columns are locations
    Parameters
    ----------
    past_data: pandas.DataFrama
        a dictionary of dataframes of density data where the keys are
        days of the week
    Returns
    -------
    pandas.DataFrame
        Dataframe containing predicted counts for 96 today's timepoints
    """
    results, locs = [], []

    for group in np.unique(past_data["group_name"]):
        locs.append(group)

        # gets all rows for unique 'group'
        group_data = past_data[past_data["group_name"] == group]

        # get only client count and time point for each 'group' for all 4 years
        group_data = group_data[["client_count", "time_point"]]

        # average counts by time for each location
        group_result = group_data.groupby("time_point").mean()

        # convert capacity count to percentage
        group_result = np.divide(group_result, FULL_CAP_DATA[group])

        results.append(group_result.transpose())

    result = pd.concat(results)  # combine the data for all locations
    result.index = locs
    result = result.transpose()  # time points indexes and locations columns

    old_indexes = result.index
    new_indexes = []

    # make sure all time index has the same string format
    for index in old_indexes:
        splited = index.split(":")
        leading, trailing = splited[0], splited[1]
        if len(leading) == 1:
            leading = "0" + leading
        if trailing == "0":
            trailing = "00"
        new_index = "{}:{}".format(leading, trailing)
        new_indexes.append(new_index)

    result.index = new_indexes
    result = result.sort_index()

    return result

def multi_predict(cluster,
                  cluster1,
                  cluster2,
                  cluster3,
                  cluster4,
                  cluster5,
                  cluster6):
    """Return a dataframe of predicted counts for today
    where the indeces are timestamps of the day and columns are locations
    Parameters
    ----------
    cluster: pandas.DataFrame
        a dictionary of dataframes of density data where the keys are
        days of the week
    .
    .
    .
    cluster n: pandas.DataFrame
        a dictionary of dataframes of density data where the keys are
        days of the week
    Returns
    -------
    pandas.DataFrame
        Dataframe containing predicted counts for 96 today's timepoints
    """
    results, locs = [], []

    for group in np.unique(cluster1["group_name"]):
        locs.append(group)

        # gets all rows for unique 'group' for every cluster
        group_data = cluster[cluster["group_name"] == group]
        group_data1 = cluster1[cluster1["group_name"] == group]
        group_data2 = cluster2[cluster2["group_name"] == group]
        group_data3 = cluster3[cluster3["group_name"] == group]
        group_data4 = cluster4[cluster4["group_name"] == group]
        group_data5 = cluster5[cluster5["group_name"] == group]
        group_data6 = cluster6[cluster6["group_name"] == group]

        # get only client count and time point for each 'group'
        group_data = group_data[["client_count", "time_point"]]
        group_data1 = group_data1[["client_count", "time_point"]]
        group_data2 = group_data2[["client_count", "time_point"]]
        group_data3 = group_data3[["client_count", "time_point"]]
        group_data4 = group_data4[["client_count", "time_point"]]
        group_data5 = group_data5[["client_count", "time_point"]]
        group_data6 = group_data6[["client_count", "time_point"]]
        


        # get all stds for every 15 min per location
        group_result_std = group_data.groupby("time_point").std()
        group_result_std1 = group_data1.groupby("time_point").std()
        group_result_std2 = group_data2.groupby("time_point").std()
        group_result_std3 = group_data3.groupby("time_point").std()
        group_result_std4 = group_data4.groupby("time_point").std()
        group_result_std5 = group_data5.groupby("time_point").std()
        group_result_std6 = group_data6.groupby("time_point").std()

        # calculate all the means but only select the rows with the smaller std
        group_data_mean = group_data.groupby("time_point").mean()
        group_data_mean1 = group_data1.groupby("time_point").mean()
        group_data_mean2 = group_data2.groupby("time_point").mean()
        group_data_mean3 = group_data3.groupby("time_point").mean()
        group_data_mean4 = group_data4.groupby("time_point").mean()
        group_data_mean5 = group_data5.groupby("time_point").mean()
        group_data_mean6 = group_data6.groupby("time_point").mean()

        # print(group_data.index)
        temp_df = group_result_std.copy(deep=True)
        #print(temp_df.index)


        # for every row, use the row with the lowest std from all clusters
        for x in range(len(group_result_std.index)):
            tempList = [group_result_std.iloc[x][0],
                        group_result_std1.iloc[x][0],
                        group_result_std2.iloc[x][0],
                        group_result_std3.iloc[x][0],
                        group_result_std4.iloc[x][0],
                        group_result_std5.iloc[x][0],
                        group_result_std6.iloc[x][0]]

            min_pos = tempList.index(min(tempList))
            if min_pos == 0:
                temp_df.iloc[x] = group_data_mean.iloc[x]

            elif min_pos == 1:
                temp_df.iloc[x] = group_data_mean1.iloc[x]
            elif min_pos == 2:
                temp_df.iloc[x] = group_data_mean2.iloc[x]
            elif min_pos == 3:
                temp_df.iloc[x] = group_data_mean3.iloc[x]
            elif min_pos == 4:
                temp_df.iloc[x] = group_data_mean4.iloc[x]
            elif min_pos == 5:
                temp_df.iloc[x] = group_data_mean5.iloc[x]
            elif min_pos == 6:
                temp_df.iloc[x] = group_data_mean6.iloc[x]

        group_result = temp_df

        # convert capacity count to percentage
        group_result = to_percentage(group_result, group)
        results.append(group_result.transpose())

    result = pd.concat(results)  # combine the data for all locations
    result.index = locs
    result = result.transpose()  # time points indexes and locations columns

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

def to_percentage(group, name):
    return np.divide(group, FULL_CAP_DATA[name])

def categorize_data(cursor, cluster, time):

    """ Return data as pandas dataframe

    index: DateTimeIndex -- dump_time
    Parameters
    ----------
    cursor: cursor for our DB
        Connection to db
    Returns
    -------
    pandas.DataFrame
        Density data in a Dataframe
    """
    #today = datetime.datetime.today()
    today = time


    # PostgreSQL's days do not match Python's
    if (today.weekday() + 1 == 7):
        day_of_week = 0
    else:
        day_of_week = today.weekday() + 1
    week_of_year = today.isocalendar()[1]

    # cluster 0 -> all datapoints for same day for 4 years
    query = ' WHERE extract(WEEK from d.dump_time) = ' + \
            '{} AND extract(DOW from d.dump_time) = '.format(week_of_year) + \
            '{}'.format(day_of_week)

    # cluster 1 -> all data points for same day and week ahead for 4 years
    query1 = ' WHERE (extract(WEEK from d.dump_time) = ' + \
             '{} AND extract(DOW from d.dump_time) = '.format(week_of_year) + \
             '{})'.format(day_of_week) + \
             ' OR (extract(WEEK from d.dump_time) = ' + \
             '{}'.format(week_of_year + 1) + \
             ' AND extract(DOW from d.dump_time) = {}) '.format(day_of_week)

    # cluster 2 -> all data points for same date and week before for 4 years
    query2 = ' WHERE (extract(WEEK from d.dump_time) = ' + \
             '{} AND extract(DOW from d.dump_time) = '.format(week_of_year) + \
             '{})'.format(day_of_week) + \
             ' OR (extract(WEEK from d.dump_time) = ' + \
             '{}'.format(week_of_year - 1) + \
             ' AND extract(DOW from d.dump_time) = {}) '.format(day_of_week)

    # cluster 3 -> all data point for same date, week before, and week after
    query3 = ' WHERE (extract(WEEK from d.dump_time) = ' + \
             '{} AND extract(DOW from d.dump_time) = '.format(week_of_year) + \
             '{})'.format(day_of_week) + \
             ' OR (extract(WEEK from d.dump_time) = ' + \
             '{}'.format(week_of_year + 1) + \
             ' AND extract(DOW from d.dump_time) = {}) '.format(day_of_week) +\
             ' OR (extract(WEEK from d.dump_time) = ' + \
             '{}'.format(week_of_year - 1) + \
             ' AND extract(DOW from d.dump_time) = {})'.format(day_of_week)

    # cluster 4 -> get all data point for same date, week before,
    # and 2 weeks before
    query4 = ' WHERE (extract(WEEK from d.dump_time) = ' + \
             '{} AND extract(DOW from d.dump_time) = '.format(week_of_year) + \
             '{})'.format(day_of_week) + \
             ' OR (extract(WEEK from d.dump_time) = ' + \
             '{}'.format(week_of_year - 1) + \
             ' AND extract(DOW from d.dump_time) = {}) '.format(day_of_week) +\
             ' OR (extract(WEEK from d.dump_time) = ' + \
             '{}'.format(week_of_year - 2) + \
             ' AND extract(DOW from d.dump_time) = {})'.format(day_of_week)

    # cluster 5 -> get all data point for same date, week after,
    # and 2 weeks after
    query5 = ' WHERE (extract(WEEK from d.dump_time) = ' + \
             '{} AND extract(DOW from d.dump_time) = '.format(week_of_year) + \
             '{})'.format(day_of_week) + \
             ' OR (extract(WEEK from d.dump_time) = ' + \
             '{}'.format(week_of_year + 1) + \
             ' AND extract(DOW from d.dump_time) = {}) '.format(day_of_week) +\
             ' OR (extract(WEEK from d.dump_time) = ' + \
             '{}'.format(week_of_year + 2) + \
             ' AND extract(DOW from d.dump_time) = {})'.format(day_of_week)

    # cluster 6 -> get all data point for same date, week before,
    # and 2 weeks before, week after, and two weeks after
    query6 = ' WHERE (extract(WEEK from d.dump_time) = ' + \
             '{} AND extract(DOW from d.dump_time) = '.format(week_of_year) + \
             '{})'.format(day_of_week) + \
             ' OR (extract(WEEK from d.dump_time) = ' + \
             '{}'.format(week_of_year - 1) + \
             ' AND extract(DOW from d.dump_time) = {}) '.format(day_of_week) +\
             ' OR (extract(WEEK from d.dump_time) = ' + \
             '{}'.format(week_of_year - 2) + \
             ' AND extract(DOW from d.dump_time) = {})'.format(day_of_week) + \
             ' OR (extract(WEEK from d.dump_time) = ' +\
             '{}'.format(week_of_year + 1) +\
             ' AND extract(DOW from d.dump_time) = {}) '.format(day_of_week) +\
             ' OR (extract(WEEK from d.dump_time) = ' +\
             '{}'.format(week_of_year + 2) +\
             ' AND extract(DOW from d.dump_time) = {}) '.format(day_of_week)

    # retrieve data from database using selected cluster
    if cluster == 0:
        cursor.execute(SELECT + query)
    elif cluster == 1:
        cursor.execute(SELECT + query1)
    elif cluster == 2:
        cursor.execute(SELECT + query2)
    elif cluster == 3:
        cursor.execute(SELECT + query3)
    elif cluster == 4:
        cursor.execute(SELECT + query4)
    elif cluster == 5:
        cursor.execute(SELECT + query5)
    else:
        cursor.execute(SELECT + query6)

    raw_data = cursor.fetchall()

    # convert fetched data to a pandas dataframe
    df = pd.DataFrame(raw_data) \
           .set_index("dump_time") \
           .assign(group_name=lambda df: df["group_name"].astype('category'),
                   parent_id=lambda df: df["parent_id"].astype('category'))
    #print(df.index)
    # add a new time point column to the datafram
    time_points = zip(df.index.hour, df.index.minute)

    time_points = ["{}:{:02d}".format(x[0], x[1]) for x in time_points]
    df["time_point"] = time_points

    return df
