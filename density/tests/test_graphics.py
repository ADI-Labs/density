import pytest
import pandas as pd

from pandas import PeriodIndex, DataFrame, Series
from density import graphics

def test_create_prediction_plot():
	time = []

	for x in range(0, 24):
		time.append(x*10)

	time_index = []
	for x in range(0, 24):
		time_index.append(str(x))

	seriesTime = pd.Series(time, index=time_index)

	time, predictions = (pd.PeriodIndex(time_index), seriesTime)

	plot = graphics.create_prediction_plot(time, predictions)

def test_create_all_buildings():
	d = {'1' : pd.Series([1, 2, 3, 4, 5, 1], index=['lerner 1', 'lerner 2', 'lerner 3', 'butler 1', 'butler 2', 'butler 3']),
        '2' : pd.Series([2, 4, 3, 4, 5, 2], index=['lerner 1', 'lerner 2', 'lerner 3', 'butler 1', 'butler 2', 'butler 3']),
        '3' : pd.Series([3, 6, 3, 4, 5, 3], index=['lerner 1', 'lerner 2', 'lerner 3', 'butler 1', 'butler 2', 'butler 3']),
        '4' : pd.Series([4, 8, 3, 4, 5, 4], index=['lerner 1', 'lerner 2', 'lerner 3', 'butler 1', 'butler 2', 'butler 3']), }

	all_buildings = pd.DataFrame(d)

	script, divs = create_all_buldings(all_buildings)

	assert len(divs) == 6 # makes all div files