import datetime
import psycopg2
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

MAX_STD = 1000




def predict_from_dataframes(clusters):
    """ 
        Calculate predictions for one day for each time_point for each building given clusters

    Parameters
    ----------
    list clusters: list of pandas.core.frame.DataFrame, each with all client_counts for each cluster

    Returns
    -------
    pandas.core.frame.DataFrame results: dataframe with mean prediction for corresponding index time_point and column group_name
    """

    results = []

    if not clusters:
        return "Clusters parameter passed empty"

    # list of strings with each unique group_name
    group_names = list(FULL_CAP_DATA.keys())

    indeces_to_del = []
    # Check that each cluster has the same unique group_names
    for cluster_index in range(len(clusters)):

        # list with all unique group_names found in this cluster
        cluster_group_names = np.unique(clusters[cluster_index]["group_name"])

        # iterate through all group_names in this cluster and compare to group_names in FULL_CAP_DATA
        for group_index in range(len(cluster_group_names)):

            # if the group_names don't match, delete the cluster
            if(group_names[group_index] != cluster_group_names[group_index]):
                indeces_to_del.append(cluster_index)
                print("Expected group name: "+str(group_names[group_index])+" but got: "+str(cluster_group_names[group_index]))
                print("Removed cluster with index "+str(cluster_index)+" from available clusters")

    for i in indeces_to_del:
        del clusters[i]

    if not clusters:
        return "Clusters parameter is empty after removing cluster(s) due to non-expected group_name"


    # for each unique group_name (str with building name) found in cluster_template. That is, each unique graph to be created
    for group in group_names:

        # list of tables (one per cluster)
        # key: time_point  
        # value: standard deviation of the set composed by all client_counts at that time_point in the cluster
        deviations = []

        # same as deviations but with the mean of each set
        means = []

        for cluster in clusters:

            # Select only this building for all clusters and all times
            group_data = cluster[cluster["group_name"] == group]
            # Get rid of all other columns except client_count and time_point
            group_data = group_data[["client_count", "time_point"]]
            # key: time_point
            # item: list of client_counts
            group_data = group_data.groupby("time_point")
            
            # Dismiss cluster if it is empty
            if(len(group_data.groups.keys()) != 0):
                deviations.append(group_data.std())
                means.append(group_data.mean())

        if not deviations:
            return "deviations is empty, probably because no data could be groupby(time_point)"

        deviations_template = deviations[0]

        group_result = deviations_template.copy(deep=True)

        # for every row in deviations_template (that is, for every time_point)  (every dataframe in deviations
        # should have the same number of time_points)
        for time_point_index in range(len(deviations_template.index)):
            
            # time_point (type str) for row time_point_index in deviations_template
            time_point = deviations_template.iloc[time_point_index].name

            min_std = MAX_STD
            cluster_with_min_std = 0
            
            for i in range(len(deviations)):

                row = deviations[i].iloc[time_point_index]
                # make sure row in deviation refers to same time_point as row in deviations_template
                if(row.name == time_point):
                    std_for_time_point = row[0]
                    if(std_for_time_point <= min_std):
                        min_std = std_for_time_point
                        cluster_with_min_std = i    

            group_result.iloc[time_point_index] = means[cluster_with_min_std].iloc[time_point_index]

        # convert client_count to percentage
        group_result = np.divide(group_result, FULL_CAP_DATA[group])

        results.append(group_result.transpose())
  
    result = pd.concat(results)  # combine the data for all locations
    result.index = group_names
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

    """ 
        Get query to execute and fetch data for predictions. one query returned = one cluster

    Parameters
    ----------
    int[] combination: list with days_of_week to cluster together
    int week_of_year: int 0-53
    int day_of_week: 0 (Sunday) - 6 (Saturday)
    int week_delta_back: number of weeks back to include in cluster
    int week_delta_forward: number of weeks forward to include in cluster

    Returns
    -------
    str query: to execute cursor.execute(SELECT+query)
    """

    if not combination:
        print("ERROR: combination is empty. Set to [day_of_week]")
        combination = [day_of_week] # default 

    # can't continue if week_of_year or day_of_week are invalid
    if(week_of_year > 53 or week_of_year < 0):
        return "ERROR: week_of_year parameter must be 0-53. week_of_year = "+str(week_of_year)
    if(day_of_week > 6 or day_of_week < 0):
        return "ERROR: day_of_week parameter must be 0-6. day_of_week = "+str(day_of_week)

    if(week_delta_back < 0):
        print("ERROR: week_delta_back must be positive. Set to 0")
        week_delta_back = 0 # default

    if(week_delta_forward < 0):
        print("ERROR: week_delta_forward must be positive. Set to 0")
        week_delta_forward = 0 # default

    # adds the basic query
    query = ' WHERE extract(WEEK from d.dump_time) = ' + \
            '{} AND extract(DOW from d.dump_time) = '.format(week_of_year) + \
            '{}'.format(day_of_week)

    # for each week back
    for week_delta in range(week_delta_back+1):

        # elem is each cluster combination of days_of_weel
        for elem in combination:

            # make sure we don't add the day and week already added at the beginning of query
            if(day_of_week != elem or ((day_of_week == elem) and (week_delta != 0))):
                query += \
                 ' OR (extract(WEEK from d.dump_time) = ' + \
                 '{}'.format(week_of_year - week_delta) + \
                 ' AND extract(DOW from d.dump_time) = {}) '.format(elem)

    # for each week forward
    for week_delta in range(week_delta_forward+1):
        for elem in combination:

            # only add for week_delta > 0 so we don't add the same ones again
            if(week_delta != 0):
                query += \
                 ' OR (extract(WEEK from d.dump_time) = ' + \
                 '{}'.format(week_of_year + week_delta) + \
                 ' AND extract(DOW from d.dump_time) = {}) '.format(elem)

    return query

def get_db_queries(day_of_week, week_of_year, max_week_delta, combinations_day_of_week):
    '''
        Gets the db queries to execute to get data for each cluster
        Clusters are formed combining days_of_week for every week_delta < max_week_delta
        One cluster per combination of days_of_week found in combinations_day_of_week
        
        Parameters
        ----------
            int day_of_week: 0 (Sunday) - 6 (Saturday)
            int week_of_year: 0-53
            int max_week_delta: number of weeks to go back and forward from current week to form clusters
            int[][] combinations_day_of_week: each int array contains days_of_week to combine to form cluster
        Returns
        ---------
            str[] queries: list of queries to execute
    '''
    queries = []

    # Iterate through all weeks 0-max_week_delta, both back and forward
    for i in range(max_week_delta):

        for j in range(max_week_delta):

            # for each combination in combinations_day_of_week: get query and fetch data
            for cluster in range(len(combinations_day_of_week)):

                # combination is int array with week_days to cluster together
                combination = combinations_day_of_week[cluster]
                if not combination:
                    print("ERROR combinations_day_of_week[cluster] is empty. cluster = " + str(cluster))
                    combination = [day_of_week] # default 
                    print("combination set to: "+str(combination))
                    
                # returns query  for specific cluster
                query = get_query(combination, week_of_year, day_of_week, i, j)
                if("ERROR" in query):
                    print("get_query returned ERROR: "+query)
                    # set to default query
                    query = ' WHERE extract(WEEK from d.dump_time) = ' + \
                            '{} AND extract(DOW from d.dump_time) = '.format(week_of_year) + \
                            '{}'.format(day_of_week)
                    print("query set to: "+query)

                queries.append(query)

    return queries

def categorize_data(cursor, query):

    """ 
        Return data as pandas dataframe

        index: DateTimeIndex -- dump_time
    
    Parameters
    ----------
    cursor: cursor for our DB
        Connection to db
    query: str
        query to execute w/o SELECT

    Returns
    -------
    pandas.DataFrame
        Density data in a Dataframe
    """
    try:
        # retrieve data from database using selected cluster
        cursor.execute(SELECT+query)

    except (psycopg2.ProgrammingError, psycopg2.InternalError) as e:
        return "ERROR: cursor.execute failed. "+str(e)+" \nQuery: "+query

    raw_data = cursor.fetchall()
    if not raw_data:
        return "ERROR : cursor.fetchall() did not return any data"
    raw_data = normalize_dump_times(raw_data)

    # convert fetched data to a pandas dataframe
    df = pd.DataFrame(raw_data) \
           .set_index("dump_time") \
           .assign(group_name=lambda df: df["group_name"].astype('category'),
                   parent_id=lambda df: df["parent_id"].astype('category'))

    # add a new time point column to the dataframe
    time_points = zip(df.index.hour, df.index.minute)
    
    time_points = ["{}:{:02d}".format(x[0], x[1]) for x in time_points]
    df["time_point"] = time_points

    # To print ALL of the dataframe uncomment this 
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(df)

    return df
