from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

import pandas as pd

from pandas import PeriodIndex, DataFrame, Series

PANTONE_292 = (105, 179, 231)

def create_all_buildings(df):
    """
    Generates html/javascript code for graphs of all buildings 

    :param df: DataFrame that contains predictions of traffic for each building over 24 hour period
    :return: tuple of scripts for all buildings and divs for all buildings
    :rtype: tuple of string, string
    """
    
    #  building = index of row (String)
    #  predictions = Series of columns with predictions 

    all_divs = ""
    all_scripts = ""

    for building, predictions in df.iterrows():
        #  create prediction plot for one building
        script, div = create_prediction_plot(predictions.index, predictions) 

        #  add div and script to other div and scripts 
        all_divs += (div + "\n")
        all_scripts += (script + "\n")

    print(all_divs)
    print(all_scripts)
    return (all_scripts, all_divs)


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
    :return: tuple of script and div for one plot
    :rtype: tuple of string, string 
    """

    p = figure(plot_width=400, plot_height=400)

    #set format for x axis
    p.xaxis.axis_label = "Time of Day"
    p.xaxis.axis_line_width = 3
    p.xaxis.axis_line_color = PANTONE_292
    p.xaxis.major_label_text_color = PANTONE_292

    #set format for y axis
    p.yaxis.axis_label = "Predicted Capacity"
    p.yaxis.axis_line_color = PANTONE_292
    p.yaxis.major_label_text_color = PANTONE_292
    p.yaxis.major_label_orientation = "vertical"
    p.yaxis.axis_line_width = 3

    # add a line renderer
    p.line(time, prediction, line_width=2)

    #  get script and div of plot
    script, div = components(p)
    return (script, div)

#   create_all_buildings(phony_data())
