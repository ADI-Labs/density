# Density

[![Build
Status](https://travis-ci.org/ADI-Labs/density.svg?branch=master)](https://travis-ci.org/ADI-Labs/density)

[Density](https://density.adicu.com) estimates how full different parts of
Columbia are, based on the number of devices connected to the WiFi (data
graciously provided by CUIT in coordination with ESC).


## Contributing

### Local Development

Density currently runs on Python 3.6.3 and PostgreSQL 9.6. Our Python
dependencies are managed via [Pipenv](https://docs.pipenv.org/). If you
have Python 3.6 already installed, just run:

```bash
pip install -U pipenv
pipenv install --dev
./scripts/bootstrap.sh
```

### Vagrant

If you don't know how to install Python 3.6.3 and PostgreSQL 9.6
yourself, we also have a [Vagrant](https://www.vagrantup.com/) setup. Go
to [Vagrant Downloads](https://www.vagrantup.com/downloads.html) to
download Vagrant, and then in the terminal run:

```bash
vagrant up
vagrant ssh
```

This should `ssh` you into `vagrant@vagrant` virtualmachine. Go to
`/vagrant` and then run `pipenv install --dev`.

### Environment variables

We use `.env` file (automatically loaded by `pipenv`) to handle
configuration. This should automatically be created for you when you run
`./scripts/bootstrap.sh` (or when Vagrant provisions itself).

In production, we use a different set of environment variables.

## Running the Server

```
pipenv run flask run
```

to start the server. If you're using Vagrant, you'll have to run:

```
pipenv run flask run --host=0.0.0.0
```

### Testing

We use `py.test` for testing and `flake8` for linting. All tests are defined
in `density/tests`. To run tests locally, in the app root directory you should
run:

```bash
pipenv run flake8
pipenv run py.test
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
├── API.md              -- API documentation
├── density
│   ├── config.py       -- Load configuration from `.env` file
│   ├── data.py         -- Raw data for rooms
│   ├── db.py           -- Handle all database access
│   ├── __init__.py     -- Bulk of the app logic
│   ├── predict.py      -- WIP (unused) file for predictions
│   ├── static/         -- static assets for Flask
│   ├── templates       -- Jinja2 templates for Flask
│   └── tests/          -- various tests
├── Dockerfile
├── Pipfile             -- List of Python dependencies
├── Pipfile.lock
├── README.md
├── scripts
│   ├── bootstrap.sh    -- Set-up PostgreSQL logic and `.env`
│   ├── dump.sql        -- dump of database for development
│   ├── schema.sql      -- database schema (for reference)
│   └── vagrant.sh      -- script to setup Vagrant
├── setup.cfg           -- Setup for CI
└── Vagrantfile
```
