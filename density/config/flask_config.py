"""
Collects settings from the environment and adds them to the app configuration.

Flask specific settings will be set here and we can store additional settings
in the config object as well.
"""


from os import environ
from sys import exit
from datetime import datetime

from consul import Consul
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

# consul_configurations contains equivalent keys that will be used to extract
# configuration values from Consul.
consul_configurations = [  # consul key --> config key
    ('flask_port', 'PORT'),
    ('flask_debug', 'DEBUG'),
    ('secret_key', 'SECRET_KEY'),
    ('postgres_user', 'PG_USER'),
    ('postgres_password', 'PG_PASSWORD'),
    ('postgres_database', 'PG_DB'),
    ('postgres_host', 'PG_HOST'),
    ('postgres_port', 'PG_PORT'),
    ('google_client_id', 'GOOGLE_CLIENT_ID'),
]

if environ.get('USE_ENV_VARS') == 'TRUE':
    try:  # use local settings
        for env_key, value in config.iteritems():
            if not value:
                config[env_key] = environ[env_key]

    except KeyError as e:
        """ Throw an error if a setting is missing """
        print "ERR MSG: {}".format(e.message)
        print ("Some of your settings aren't in the environment."
               "You probably need to run:"
               "\n\n\tsource config/<your settings file>")
        exit(1)

else:  # use consul
    kv = Consul().kv  # initalize client to KV store

    for consul_key, config_key in consul_configurations:
        _, tmp = kv.get("density/{}".format(consul_key))
        val = tmp.get('Value')
        config[config_key] = val
        if not val:
            raise Exception(("no value found in Consul for key "
                             "density/{}").format(consul_key))

    # mail settings
    config.update({
        'MAIL_SERVER': 'smtp.googlemail.com',
        'MAIL_PORT': 465,
        'MAIL_USE_SSL': True,
        'MAIL_USE_TLS': False,
        'MAIL_DEFAULT_SENDER': 'densitylogger@gmail.com',
        'MAIL_USERNAME': 'densitylogger@gmail.com',
        'MAIL_PASSWORD': kv.get('density/mail_password')[1]
    })
    if not config['MAIL_PASSWORD']:
        raise Exception("No password for Mail found in Consul")

    # administrator list
    ADMINS = [
        'bz2231@columbia.edu',
        'dzh2101@columbia.edu',
        'jgv2108@columbia.edu',
        'sb3657@columbia.edu',
        'mgb2163@columbia.edu',
        'jzf2101@columbia.edu'
    ]

    config['ADMINS'] = ADMINS

config['DEBUG'] = (config['DEBUG'] == 'TRUE')

""" Creates a json encoder that returns ISO 8601 strings for datetimes
    http://flask.pocoo.org/snippets/119/ """


class ISO8601Encoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
