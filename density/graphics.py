from bokeh.embed import components
from bokeh.plotting import figure

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

    #  building = index of row (String)
    #  predictions = Series of columns with predictions

    for building, predictions in df.iterrows():
        #  create plot prediction for each building and add to dictionary
        building_divs[building] = create_prediction_plot(
            predictions.index.tolist()[::4], predictions[::4] * 100)

    #  create script and div from dictionary
    script, div = components(building_divs)

    return (script, div)


def create_prediction_plot(time, prediction):
    """
    Create prediction plot for one building

    :param time: pandas Index object with time of next 24 hours
    :param prediction: pandas Series object with predictions corresponding
    to next 24 hours
    :return: bokeh Figure that with plot prediction of one building
    :rtype: bokeh Figure
    """

    p = figure(x_range=time, y_range=(0, 100), tools="wheel_zoom",
               plot_width=1800, plot_height=600, sizing_mode="scale_width")

    #  set format for x axis
    p.xaxis.axis_label = "Time of Day"
    p.xaxis.axis_line_width = 3
    p.xaxis.axis_line_color = PANTONE_292
    p.xaxis.major_label_text_color = PANTONE_292
    p.xaxis.axis_label_text_font_size = "18pt"
    p.xaxis.major_label_text_font_size = "10pt"

    #  set format for y axis
    p.yaxis.axis_label = "Predicted Capacity"
    p.yaxis.axis_line_color = PANTONE_292
    p.yaxis.axis_label_text_font_size = "18pt"
    p.yaxis.major_label_text_font_size = "10pt"
    p.yaxis.major_label_text_color = PANTONE_292
    p.yaxis.major_label_orientation = "vertical"
    p.yaxis.axis_line_width = 3

    #  add a line renderer
    p.vbar(x=time, top=prediction, width=0.3)
    # p.line(time, prediction, line_width=0.59)

    #  return plot for one building
    return p

# create_all_buildings(phony_data())
