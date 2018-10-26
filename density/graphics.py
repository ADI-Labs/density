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
    ind = ['00:00', '00:15', '00:30', '00:45', '01:00', '01:15', '01:30', '01:45',
       '02:00', '02:15', '02:30', '02:45', '03:00', '03:15', '03:30', '03:45',
       '04:00', '04:15', '04:30', '04:45', '05:00', '05:15', '05:30', '05:45',
       '06:00', '06:15', '06:30', '06:45', '07:00', '07:15', '07:30', '07:45',
       '08:00', '08:15', '08:30', '08:45', '09:00', '09:15', '09:30', '09:45',
       '10:00', '10:15', '10:30', '10:45', '11:00', '11:15', '11:30', '11:45',
       '12:00', '12:15', '12:30', '12:45', '13:00', '13:15', '13:30', '13:45',
       '14:00', '14:15', '14:30', '14:45', '15:00', '15:15', '15:30', '15:45',
       '16:00', '16:15', '16:30', '16:45', '17:00', '17:15', '17:30', '17:45',
       '18:00', '18:15', '18:30', '18:45', '19:00', '19:15', '19:30', '19:45',
       '20:00', '20:15', '20:30', '20:45', '21:00', '21:15', '21:30', '21:45',
       '22:00', '22:15', '22:30', '22:45', '23:00', '23:15', '23:30', '23:45']
    building_divs = {}

    for building, predictions in df.iterrows():
        #  create plot prediction for each building and add to dictionary
        # mins = np.asarray([time.split(':')[1] for time in predictions.index])
        # hours = np.where(mins == "00")[0]
        
        time = pandas.to_datetime(ind)

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
