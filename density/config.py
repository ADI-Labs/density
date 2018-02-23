"""
Collects settings from the environment and adds them to the app configuration.

Flask specific settings will be set here and we can store additional settings
in the config object as well.
"""

import datetime as dt
import os

from flask.json import JSONEncoder

# dictionary the flask app configures itself from
keys = {'DB_URI', 'GOOGLE_CLIENT_ID', 'SECRET_KEY', 'UPLOAD_KEY'}

try:
    config = {key: os.environ[key] for key in keys}
except KeyError as e:
    """ Throw an error if a setting is missing """
    print(f"ERR MSG: {e}")
    print("Some of your settings aren't in the environment. "
          "You probably need to create a `.env` file")
    raise


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
