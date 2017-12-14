"""
Collects settings from the environment and adds them to the app configuration.

Flask specific settings will be set here and we can store additional settings
in the config object as well.
"""

import os
import datetime as dt

from flask.json import JSONEncoder

# dictionary the flask app configures itself from
config = {
    'DB_URI': None,
    'GOOGLE_CLIENT_ID': None,
    'SECRET_KEY': None,
    'UPLOAD_KEY': None
}

try:
    for env_key, value in config.items():
        if not value:
            config[env_key] = os.environ[env_key]
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
