import datetime

import numpy as np
import pandas as pd
from .data import FULL_CAP_DATA, COMBINATIONS

SELECT = """
    SELECT d.client_count, d.dump_time,
           r.id AS group_id, r.name AS group_name,
           b.id AS parent_id, b.name AS building_name
    FROM density_data d
    JOIN routers r ON r.id = d.group_id
    JOIN buildings b ON b.id = r.building_id"""


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

def new_multi_predict(clusters):

    

    results, locs = [], []

    for group in np.unique(cluster1["group_name"]):

        locs.append(group)

        deviations = []
        means = []

        for elem in clusters:

            group_data = elem[elem["group_name"] == group]
            group_data = group_data[["client_count", "time_point"]]
            deviations.append(group_data.groupby("time_point").std())
            means.append(group_data.groupby("time_point").mean())

        group_result_std = deviations[0]

        temp_df = group_result_std.copy(deep=True)

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

    print(result)
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
        print("group_result_std")
        print(group_result_std)
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

    print(result)
    return result

def to_percentage(group, name):
    return np.divide(group, FULL_CAP_DATA[name])

def normalize_dump_times(raw_data):
    """ Return a list of dicts of each data point in db

    Parameters
    ----------
    raw_data: list of dicts
    Returns
    -------
    list of dicts
        the 'dump_time' for each element in raw_data has minutes set to 0, 15, 30, 45

    """
    for point_entry in raw_data:
        minute = point_entry["dump_time"].minute
        if (minute > 45 and minute < 60):
            point_entry["dump_time"] = point_entry["dump_time"].replace(minute = 45, second =0, microsecond = 0)
        elif(minute > 30 and minute < 45):
            point_entry["dump_time"] = point_entry["dump_time"].replace(minute = 30, second =0, microsecond = 0)
        elif(minute > 15 and minute < 30):
            point_entry["dump_time"] = point_entry["dump_time"].replace(minute = 15, second =0, microsecond = 0)
        elif(minute > 0 and minute < 15):
            point_entry["dump_time"] = point_entry["dump_time"].replace(minute = 0, second =0, microsecond = 0)

    return raw_data

def get_query(combination, week_of_year, day_of_week, week_delta_back, week_delta_forward):

    if not combination:
        combination = [day_of_week] # default 

    if(week_of_year > 53 or week_of_year < 0):
        return "ERROR: week_of_year parameter must be 0-53. week_of_year = "+str(week_of_year)

    if(day_of_week > 6 or day_of_week < 0):
        return "ERROR: day_of_week parameter must be 0-6. day_of_week = "+str(day_of_week)

    if(week_delta_back < 0):
        week_delta_back = 0 # default

    if(week_delta_forward < 0):
        week_delta_forward = 0 # default


    query = ' WHERE extract(WEEK from d.dump_time) = ' + \
            '{} AND extract(DOW from d.dump_time) = '.format(week_of_year) + \
            '{}'.format(day_of_week)

    for week_delta in range(week_delta_back+1):
        for elem in combination:
            if(day_of_week != elem or ((day_of_week == elem) and (week_delta != 0) )):
                query += \
                 ' OR (extract(WEEK from d.dump_time) = ' + \
                 '{}'.format(week_of_year - week_delta) + \
                 ' AND extract(DOW from d.dump_time) = {}) '.format(elem)

    for week_delta in range(week_delta_forward+1):
        for elem in combination:
            if(week_delta != 0):
                query += \
                 ' OR (extract(WEEK from d.dump_time) = ' + \
                 '{}'.format(week_of_year + week_delta) + \
                 ' AND extract(DOW from d.dump_time) = {}) '.format(elem)

    return query


def categorize_data(cursor, query):

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

    # retrieve data from database using selected cluster
    cursor.execute(SELECT + query)

    raw_data = cursor.fetchall()
    raw_data = normalize_dump_times(raw_data)

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
