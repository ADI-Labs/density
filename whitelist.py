# Because vulture only performs static analysis, this file is used
# by vulture as a whitelist module and passed as a parameter when
# running vulture so that it'll know that certain methods are being
# used.

from density import density
from bokeh import figure

app = density.app

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
app.json_encoder

# Ignore all Flask routes
routes = [app.view_functions[rule.endpoint] for rule in
          app.url_map.iter_rules()]
