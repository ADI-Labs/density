# Density

[![Build
Status](https://travis-ci.org/ADI-Labs/density.svg?branch=master)](https://travis-ci.org/ADI-Labs/density)

[Density](https://density.adicu.com) estimates how full different parts of
Columbia are, based on the number of devices connected to the WiFi (data
graciously provided by CUIT in coordination with ESC).


## Contributing

## Local Dev

We recommend using [Vagrant](https://www.vagrantup.com) for development
environment set-up. If you have Vagrant, running `vagrant up` should set-up
and provision the virtual machine for you.

Inside the virtual machine, run:

```bash
cd /vagrant
source config/settings.dev
flask run --host=0.0.0.0
```

and go to https://localhost:5000. You should see your own local Density app!

### Dependencies

Density is build with Python 3.6 and Flask. We use a [conda](https://conda.io)
environment, defined via `config/environment.yml`, for dependency management.
When you run `source config/settings.dev`, the appropriate conda environment
will automatically be activated.

Density runs on Postgres 9.6. To access the database, you can just run:

```
sudo -u postgres psql density
```

You can find a copy of the database schema in `config/schema.sql`.

### Testing

We use `py.test` for testing and `flake8` for linting. All tests are defined
in `density/tests`. To run tests locally, in the app root directory you should
run:

```bash
source config/settings.dev
py.test
flake8
```

We have [Travis CI](https://travis-ci.org/ADI-Labs/density/) set-up to enforce
passing tests.

### Deployment

Density is currently deployed on ADI's server via Docker (defined in the
`Dockerfile`). To build the Docker image locally, install Docker and run:

```bash
docker build -t density .
docker run --net=host -d density
```

### Project Layout

```
.
├── config
│   ├── bootstrap.sh      -- bootstrap script for Vagrant
│   ├── dump.sql          -- a database dump for local development
│   ├── environment.yml   -- a file defining our conda environment
│   ├── schema.sql        -- our database schema
│   └── settings.dev      -- various configuration settings for development
├── density
│   ├── config.py         -- loads configuration from environment variables
│   ├── data.py           -- stores various constants
│   ├── db.py             -- app interface to the Postgres database
│   ├── __init__.py       -- the bulk of the app logic
│   ├── predict.py        -- in-progress work for data science work
│   ├── static/
│   ├── templates/
│   └── tests/
├── API.md                -- API documentation
├── Dockerfile            -- Dockerfile for production
├── README.md
├── run.py                -- File for Flask to run
├── setup.cfg
└── Vagrantfile
```
