from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

import pandas as pd

from pandas import PeriodIndex, DataFrame, Series

PANTONE_292 = (105, 179, 231)

def create_all_buildings(df):
    """
    Generates html/javascript code for graphs of all buildings 

    :param df: DataFrame that contains predictions of traffic for each building over 24 hour period
    :return: tuple of script and div of plot prediction for all buildings 
    :rtype: tuple of string, string
    """
    
    building_divs = {}

    #  building = index of row (String)
    #  predictions = Series of columns with predictions 

    for building, predictions in df.iterrows():
        #  create plot prediction for each building and add to dictionary
        building_divs[building] = create_prediction_plot(predictions.index, predictions)

    #  create script and div from dictionary
    script, div = components(building_divs)

    return (script, div)


def phony_data():

    d = {'1' : pd.Series([1, 2, 3, 4, 5, 1], index=['lerner 1', 'lerner 2', 'lerner 3', 'butler 1', 'butler 2', 'butler 3']),
        '2' : pd.Series([2, 4, 3, 4, 5, 2], index=['lerner 1', 'lerner 2', 'lerner 3', 'butler 1', 'butler 2', 'butler 3']),
        '3' : pd.Series([3, 6, 3, 4, 5, 3], index=['lerner 1', 'lerner 2', 'lerner 3', 'butler 1', 'butler 2', 'butler 3']),
        '4' : pd.Series([4, 8, 3, 4, 5, 4], index=['lerner 1', 'lerner 2', 'lerner 3', 'butler 1', 'butler 2', 'butler 3']), }

    return pd.DataFrame(d)


def create_prediction_plot(time, prediction):
    """
    Create prediction plot for one building  

    :param time: pandas Index object with time of next 24 hours
    :param prediction: pandas Series object with predictions corresponding to next 24 hours
    :return: bokeh Figure that with plot prediction of one building 
    :rtype: bokeh Figure 
    """

    p = figure(plot_width=400, plot_height=400)

    #  set format for x axis
    p.xaxis.axis_label = "Time of Day"
    p.xaxis.axis_line_width = 3
    p.xaxis.axis_line_color = PANTONE_292
    p.xaxis.major_label_text_color = PANTONE_292

    #  set format for y axis
    p.yaxis.axis_label = "Predicted Capacity"
    p.yaxis.axis_line_color = PANTONE_292
    p.yaxis.major_label_text_color = PANTONE_292
    p.yaxis.major_label_orientation = "vertical"
    p.yaxis.axis_line_width = 3

    #  add a line renderer
    p.line(time, prediction, line_width=2)

    #  return plot for one building
    return p

# create_all_buildings(phony_data())
