import pytest
import pandas as pd

from pandas import PeriodIndex, DataFrame, Series
from density import graphics

def fake_data_multiple_buildings():
	# made up data for lerner 1, 2, 3 and butler 1, 2, 3
    d = {'1' : pd.Series([1, 2, 3, 4, 5, 1], index=['lerner 1', 'lerner 2', 'lerner 3', 'butler 1', 'butler 2', 'butler 3']),
        '2' : pd.Series([2, 4, 3, 4, 5, 2], index=['lerner 1', 'lerner 2', 'lerner 3', 'butler 1', 'butler 2', 'butler 3']),
        '3' : pd.Series([3, 6, 3, 4, 5, 3], index=['lerner 1', 'lerner 2', 'lerner 3', 'butler 1', 'butler 2', 'butler 3']),
        '4' : pd.Series([4, 8, 3, 4, 5, 4], index=['lerner 1', 'lerner 2', 'lerner 3', 'butler 1', 'butler 2', 'butler 3']), }

    return pd.DataFrame(d)

def fake_data_one_building():
	# made up data for one building over a 24 hour period 
	time = []

	for x in range(0, 24):
		time.append(x*10)

	time_index = []
	for x in range(0, 24):
		time_index.append(str(x))

	seriesTime = pd.Series(time, index=time_index)
	return (pd.PeriodIndex(time_index), seriesTime)

def test_create_prediction_plot():
	time, predictions = fake_data_one_building()

	plot = graphics.create_prediction_plot(time, predictions)

def test_create_all_buildings():
	all_buildings = fake_data_multiple_buildings()

	script, divs = create_all_buldings()

	assert len(divs) == 6 # makes all div files