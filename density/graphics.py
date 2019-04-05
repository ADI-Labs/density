from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
import numpy as np
import pandas

PANTONE_292 = (105, 179, 231)

def create_all_buildings(df):
    """
    Generates html/javascript code for graphs of all buildings

    Parameters
    ----------
    df: DataFrame that contains predictions of traffic
    for each building over 24 hour period
    Returns
    -------
    tuple of string, string: script and div of plot prediction for all buildings
    """

    building_divs = {}

    # predictions is df with index time_point and value prediction percentage
    for building, predictions in df.iterrows():
        
        time = pandas.to_datetime(predictions.index)

        building_divs[building] = create_prediction_plot(
            time, predictions.iloc[0:predictions.size] * 100)

    #  create script and div from dictionary
    script, div = components(building_divs)

    return (script, div)


def create_prediction_plot(time, prediction):
    """
        Create prediction plot for one building

    Parameters
    ----------
    time: pandas Index object with time of today's 24 hours
    prediction: pandas Series object with predictions corresponding
    to today's 24 hours

    Returns
    -------
    bokeh Figure: plot prediction of one building
    """
    p = figure(x_axis_type="datetime", y_range=(0, 100), 
               tools='pan,wheel_zoom,reset', toolbar_location="right", active_drag="pan", active_scroll="wheel_zoom",
               toolbar_sticky=False, sizing_mode="stretch_both")
    p.toolbar.logo = None
    p.toolbar_location = None


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
        ( 'capacity', '<span style="color: black;">@capacity % </span>'),
    ],
    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline'
    ))

    return p
