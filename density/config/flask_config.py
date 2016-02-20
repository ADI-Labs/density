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
    'HOST': '0.0.0.0',
    'PORT': None,
    'SECRET_KEY': None,
    'PG_USER': None,
    'PG_PASSWORD': None,
    'PG_DB': None,
    'PG_HOST': None,
    'PG_PORT': None,
    'GOOGLE_CLIENT_ID': None,
    'DEBUG': None
}

try:  # use local settings
    for env_key, value in config.iteritems():
        if not value:
            config[env_key] = os.environ[env_key]

except KeyError as e:
    """ Throw an error if a setting is missing """
    print "ERR MSG: {}".format(e.message)
    print ("Some of your settings aren't in the environment."
           "You probably need to run:"
           "\n\n\tsource config/<your settings file>")
    sys.exit(1)

config['DEBUG'] = (config['DEBUG'] == 'TRUE')

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
