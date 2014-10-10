 
"""
Collects settings from the environment and adds them to the app configuration.

Flask specific settings will be set here and we can store additional settings
in the config object as well.
"""


from os import environ
from sys import exit


try:
    # flask settings
    HOST = environ['HOST']
    PORT = environ['PORT']
    SECRET_KEY = environ['SECRET_KEY']
    DEBUG = True if environ['DEBUG'] == 'TRUE' else False

    # postgres settings
    PG_USER = environ['PG_USER']
    PG_PASSWORD = environ['PG_PASSWORD']
    PG_DB = environ['PG_DB']
    PG_HOST = environ['PG_HOST']
    PG_PORT = environ['PG_PORT']
    PG_PAGE_LIMIT = environ['PG_PAGE_LIMIT']
    PG_DEFAULT = environ['PG_DEFAULT']

    environ['RATE_LIMIT'] # check for existance

except KeyError as e:
    """ Throw an error if a setting is missing """
    print "ERR MSG: {}".format(e.message)
    print ("Some of your settings aren't in the environment."
           "You probably need to run:\n\n\tsource config/<your settings file>")
    exit(1)
