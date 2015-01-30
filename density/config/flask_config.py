
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

    # oauth settings
    GOOGLE_CLIENT_ID = environ['GOOGLE_CLIENT_ID']

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_DEFAULT_SENDER = 'densitylogger@gmail.com'
    MAIL_USERNAME = 'densitylogger@gmail.com'
    MAIL_PASSWORD = 'adicudensity'

    # administrator list
    ADMINS = ['thebrianzeng@gmail.com',
        'dzh2101@columbia.edu',
        'jgv2108@columbia.edu',
        'sb3657@columbia.edu',
        'maclyn@maclyn.me',
        'jzf2101@columbia.edu',
        'benlowkh@gmail.com']

except KeyError as e:
    """ Throw an error if a setting is missing """
    print "ERR MSG: {}".format(e.message)
    print ("Some of your settings aren't in the environment."
           "You probably need to run:"
           "\n\n\tsource config/<your settings file>")
    exit(1)
