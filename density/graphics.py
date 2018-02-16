from bokeh.plotting import figure, output_file, show
import pandas as pd
from pandas import PeriodIndex, DataFrame, Series

PANTONE_292 = (105, 179, 231)

def create_figure(building, predictions):

	for time, prediction in predictions.iteritems():
		print("building:", building, "time:", time, "prediction:", prediction)


def create_all_buildings(df):
    
    #  building = index of row (String)
    #  predictions = Series of columns with predictions (double va)

    index = 0
    for building, predictions in df.iterrows():
    	create_figure(building, predictions)
    	index = index + 1

def phony_data():
	d = {'12am' : pd.Series([1, 2, 3, 4, 5, 6], index=['lerner 1', 'lerner 2', 'lerner 3', 'butler 1', 'butler 2', 'butler 3']),
		'1am' : pd.Series([2, 4, 3, 4, 5, 6], index=['lerner 1', 'lerner 2', 'lerner 3', 'butler 1', 'butler 2', 'butler 3']),
		'2am' : pd.Series([3, 6, 3, 4, 5, 6], index=['lerner 1', 'lerner 2', 'lerner 3', 'butler 1', 'butler 2', 'butler 3']),
		'3am' : pd.Series([4, 8, 3, 4, 5, 6], index=['lerner 1', 'lerner 2', 'lerner 3', 'butler 1', 'butler 2', 'butler 3']), }

	return pd.DataFrame(d)


def create_prediction_plot():

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
    p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=2)

    show(p)


create_all_buildings(phony_data())
print(phony_data())
create_prediction_plot()
