import numpy as np
import pandas as pd

# import psycopg2
# import psycopg2.extras
# import psycopg2.pool
from sklearn.linear_model import LinearRegression


# This method is not currently used by __init__ ; just a substitute method 
# in case you guys need it in the future
def get_percentage_dict(cursor):
    """Return a dictionary of group_ids and corresponding regression models
    Parameters
    ----------
    cursor: Psycopg2.cursor 
    Returns
    -------
    Dictionary
        Dictionary containing group_ids as keys and regression models as values
    """
    query = "SELECT DISTINCT group_id FROM feedback_data"
    cursor.execute(query)
    group_ids = [id['group_id'] for id in cursor.fetchall()]
    print("This is the group ids")
    print(group_ids)
    models = {}
    for group_id in group_ids:
        df = get_feedback_data(cursor, group_id)
        models[group_id] = build_reg_model(df)

    return models


def get_feedback_data(cursor, group_id):
    """Return a DataFrame that contains the new percentage and raw count for a specific location
    Parameters
    ----------
    cursor: Psycopg2.cursor
    group_id: int
        Group_id for each location
    Returns
    -------
    pandas.DataFrame
        A DataFrame that contains the percentage and raw count from user feedback
    """
    query = """ SELECT raw_count, percentage_change
                FROM feedback_data
                WHERE group_id = %s;"""
    cursor.execute(query, [group_id])
    df = pd.DataFrame(cursor.fetchall())   
    return df

# Change return value to model.coef_ for debugging
def build_reg_model(df):
    """Return a Linear Regression model to calculate the new percentage based on a raw count
    Parameters
    ----------
    df: pandas.DataFrame
        DataFrame that contains the new percentage and raw count from user feedback for a specific location
    Returns
    -------
    sklearn.linear_model.model
        A Linear Regression model to calculate the new percentage based on a raw count
    """
    # sort the DataFrame by raw count (Very important to generate correct data!)
    df = df.sort_values(by=['raw_count'])
    x = df['raw_count'].values[:, None]
    y = df['percentage_change'].values[:, None]

    # Calculate linear coefficients for x, x^2, x^3, x^4 to build the model
    x_new = np.hstack([x, x**2, x**3, x**4])
    model = LinearRegression()
    model.fit(x_new, y)

    return model.coef_

"""
The way to use the regression model
z = 100
z_new = np.hstack([z, z**2,z**3,z**4]).reshape(1,4)
p = model.predict(z_new)[0][0]
# p will return a y value for the x value inputted as z
"""