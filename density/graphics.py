from bokeh.plotting import figure
import pandas as pd
from pandas import PeriodIndex, DataFrame, Series

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

create_all_buildings(phony_data())
print(phony_data())