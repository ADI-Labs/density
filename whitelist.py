# Because vulture only performs static analysis, this file is used
# by vulture as a whitelist module and passed as a parameter when
# running vulture so that it'll know that certain methods are being
# used.

from density import density
from bokeh import figure

# Ignore bokeh figure attribute assignment
figure.xaxis.axis_label
figure.xaxis.axis_line_width
figure.xaxis.axis_line_color
figure.xaxis.major_label_text_color
figure.yaxis.axis_label
figure.yaxis.axis_line_color
figure.yaxis.major_label_text_color
figure.yaxis.major_label_orientation
figure.yaxis.axis_line_width

# Ignore Flask app attribute assignment
density.app.json_encoder

# Ignore all Flask routes
density.get_connections
density.log_outcome
density.page_not_found
density.internal_error
density.home
density.about
density.predict
density.docs
density.building_info
density.auth
density.redirect_uri
density.get_day_group_data
density.get_day_building_data
density.get_window_group_data
density.get_window_building_data
density.map
