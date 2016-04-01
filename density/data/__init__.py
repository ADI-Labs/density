from bokeh.plotting import figure
from pandas import PeriodIndex

import pandas as pd


PANTONE_292 = (105, 179, 231)

def db_to_pandas(conn):
    """ Return occupancy data as pandas dataframe

    column dtypes:
        group_id: int64
        group_name: category
        parent_id: int64
        parent_name: category
        client_count: int64
    index: DateTimeIndex -- dump_time

    Parameters
    ----------
    conn: psycopg2.extensions.connection

    Returns
    _______

    pandas.DataFrame

    """

    df = pd.read_sql('SELECT * FROM density_data', conn) \
           .set_index("dump_time") \
           .assign(group_name=lambda df: df["group_name"].astype('category'),
                   parent_name=lambda df: df["parent_name"].astype('category'))

    return df


def plot_prediction_point_estimate(series, predictor):

    future_dts = PeriodIndex(start=series.index[-1], freq='15T',
                             periods=24 * 4)
    predictions = pd.Series(predictor(future_dts),
                            index=future_dts.to_datetime())

    p = figure(x_axis_type="datetime")
    p.line(series.index, series, color="dodgerblue", line_width=3,
           line_cap="round")
    p.line(predictions.index, predictions, color="crimson", line_width=3,
           line_dash="dashed", line_cap="round")

    p.xaxis.axis_label = "Time of Day"
    p.xaxis.axis_line_width = 3
    p.xaxis.axis_line_color = PANTONE_292
    p.xaxis.major_label_text_color = PANTONE_292

    p.yaxis.axis_label = "Capacity"
    p.yaxis.axis_line_color = PANTONE_292
    p.yaxis.major_label_text_color = PANTONE_292
    p.yaxis.major_label_orientation = "vertical"
    p.yaxis.axis_line_width = 3

    return p
