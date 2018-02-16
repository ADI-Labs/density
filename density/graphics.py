from bokeh.plotting import figure
import pandas as pd
from pandas import PeriodIndex, DataFrame, Series

def create_figure(building, predictions):

    for time, prediction in predictions.iteritems():
    	print(time, ": ", predictions)

def create_all_buildings(df):
    
    #  building = index of row
    #  predictions = Series of columns with predictions
    for building, predictions in df.iterrows():
    	create_figure(building, predictions)

def phony_data():
	d = {'one' : pd.Series([1., 2., 3.], index=['a', 'b', 'c']),
		'two' : pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}

	return pd.DataFrame(d)

#  create_all_buildings(phony_data())
print(phony_data())