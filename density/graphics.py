from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
import pandas as pd
from pandas import PeriodIndex, DataFrame, Series
PANTONE_292 = (105, 179, 231)
# def create_figure(building, predictions):
#   script, div = create_prediction_plot(predictions.index, predictions)
    
def create_all_buildings(df):
    
    #  building = index of row (String)
    #  predictions = Series of columns with predictions (double va)
    all_divs = ""
    all_scripts = ""
    for building, predictions in df.iterrows():
        script, div = create_prediction_plot(predictions.index, predictions) 
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
    print(pd.DataFrame(d))
    return pd.DataFrame(d)


def create_prediction_plot(time, prediction):
    output_file("line.html")
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
    #  show(p)
    script, div = components(p)
    return (script, div)
create_all_buildings(phony_data())
