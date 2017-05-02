"""
Collects settings from the environment and adds them to the app configuration.

Flask specific settings will be set here and we can store additional settings
in the config object as well.
"""

import os
import sys
import datetime as dt

from flask.json import JSONEncoder

# dictionary the flask app configures itself from
config = {
    'SECRET_KEY': None,
    'PG_USER': None,
    'PG_PASSWORD': None,
    'PG_DB': None,
    'PG_HOST': None,
    'PG_PORT': None,
    'GOOGLE_CLIENT_ID': None,
    'UPLOAD_KEY': None
}

try:  # use local settings
    for env_key, value in config.items():
        if not value:
            config[env_key] = os.environ[env_key]

except KeyError as e:
    """ Throw an error if a setting is missing """
    print("ERR MSG: {}".format(e.message))
    print("Some of your settings aren't in the environment."
          "You probably need to run:"
          "\n\n\tsource config/<your settings file>")
    sys.exit(1)

# Mail settings
config['MAIL_SERVER'] = 'smtp.gmail.com'
config['MAIL_PORT'] = 465
config['MAIL_USE_SSL'] = True
config['MAIL_USE_TLS'] = False
config['MAIL_DEFAULT_SENDER'] = 'densitylogger@gmail.com'
config['MAIL_USERNAME'] = 'densitylogger@gmail.com'

# TODO: set config["MAIL_PASSWORD"]

# administrator list
config['ADMINS'] = [
    'bz2231@columbia.edu',
    'dan@adicu.com',
    'mjp2220@columbia.edu'
]

class ISO8601Encoder(JSONEncoder):
    """ JSON encoder for ISO8601 datetime strings

    See http://flask.pocoo.org/snippets/119/ """

    def default(self, obj):
        try:
            if isinstance(obj, dt.datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
