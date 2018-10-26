from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
import numpy as np
import pandas

PANTONE_292 = (105, 179, 231)

def create_all_buildings(df):
    """
    Generates html/javascript code for graphs of all buildings

    :param df: DataFrame that contains predictions of traffic
    for each building over 24 hour period
    :return: tuple of script and div of plot prediction for all buildings
    :rtype: tuple of string, string
    """

    building_divs = {}

    for building, predictions in df.iterrows():
        #  create plot prediction for each building and add to dictionary
        # mins = np.asarray([time.split(':')[1] for time in predictions.index])
        # hours = np.where(mins == "00")[0]
        time = pandas.to_datetime(predictions.index)

        building_divs[building] = create_prediction_plot(
            time, predictions.iloc[0:predictions.size] * 100)

    #  create script and div from dictionary
    script, div = components(building_divs)

    return (script, div)


def create_prediction_plot(time, prediction):
    """
    Create prediction plot for one building

    :param time: pandas Index object with time of today's 24 hours
    :param prediction: pandas Series object with predictions corresponding
    to today's 24 hours
    :return: bokeh Figure that with plot prediction of one building
    :rtype: bokeh Figure
    """

    p = figure(x_axis_type="datetime", y_range=(0, 100), 
               tools='pan,wheel_zoom,xbox_select,reset', toolbar_location="right", 
               toolbar_sticky=False,plot_width=1800, plot_height=600, sizing_mode="scale_width")


    #  set format for x axis
    p.xaxis.axis_label = "Time of Day"
    p.xaxis.axis_line_width = 3
    p.xaxis.axis_line_color = PANTONE_292
    p.xaxis.major_label_text_color = PANTONE_292
    p.xaxis.axis_label_text_font_size = "13pt"
    #  set format for y axis
    p.yaxis.axis_label = "Predicted Capacity"
    p.yaxis.axis_line_color = PANTONE_292
    p.yaxis.axis_label_text_font_size = "13pt"
    p.yaxis.major_label_text_color = PANTONE_292
    p.yaxis.major_label_orientation = "vertical"
    p.yaxis.axis_line_width = 3

    # use ColumnDataSource to parse in data to enable tooltips
    source = ColumnDataSource(data={
    'time'      : time,
    'capacity'    : prediction,
    })

    #  add a line renderer
    p.line(x='time', y='capacity', source = source)

    p.add_tools(HoverTool(
    tooltips=[
        ( 'capacity', '@capacity %'  ),
    ],
    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline'
    ))

    return p
