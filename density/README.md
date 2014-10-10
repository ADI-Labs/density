
#Overview

### `density.py`

This is the executable file for the project.


###lib

This contains the SQL query generator.
Some legacy code has been left until we reimplement it.


###housing

Contains logic for the `/housing` endpoints.
The endpoints are part of a blueprint in the `housing/housing.py` file.


###errors

Contains logic for creating errors.
Routes are given the `catch_error` decorator and look for an AppError to be thrown.
This then returns the defined error.

All errors are defined in `errors/definitions.json`.
This will be very useful when we start building the documentation.


###rate limiting

Defined in `auth/`.

A user is given a set number of API requests per hour.
These are split between `SPLIT_FACTOR` parts of an hour (i.e., `SPLIT_FACTOR=4`, 15 minute increments).

For testing purposes, use the token `12345`.


###config

Contains the logic that pulls app settings from environment variables.

