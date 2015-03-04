
[![Build Status](https://travis-ci.org/adicu/density.svg?branch=master)](https://travis-ci.org/adicu/density)

Density
---

Density is a project to provide easy access to the Wireless Density data from Columbia.
For more details on the project, please view the [spec](SPEC.md).




## Local Dev

This is the recommend means of setting up Density for development.
Next, install [vagrant](http://www.vagrantup.com/).
Once vagrant is installed, you can run `vagrant up`, and vagrant will provision the virtual machine for you.

To run the app, follow the these steps:

```bash
vagrant ssh
cd /vagrant
source config/settings.dev
cd density
python density.py
```





## Importing Dev Data

We use a partial dump of our data for quick-and-easy development.
This gets loaded on VM provision by our Vagrant setup scripts.
It contains a small subset and is not updated frequently, but is sufficient for most feature development and bug squashing.

Be sure to also insert the [Oauth table](config/oauth_dev_dump.sql) so that you can make authenticated requests against the API.






## Docker

The Docker container requires that either the port for the Postgres instance is forward or that the host is set to an exact IP or domain.

Using Docker:

```bash
# enter the project directory
cd density

# builds a Docker image
#   -t dictates that the image is tagged as 'density'
docker build -t density .

# runs a docker container tagged as 'density'
#   --net=host forwards all ports from the host to the container
#       this allows docker to access the Postres port, 5432
#   -e allows setting environment variables within the container
#   -d detaches the process and runs the container like a daemon
docker run --net=host -e SECRET_KEY=abc -d density

# ps shows all docker containers currently running
docker ps
```





## Consul

[Consul](https://consul.io/) is a distributed key/value store that we are using to configure Density in production.
You should not need to intereact with Consul unless you are attempting to deploy it.

Consul is installed within the Vagrant VM automatically.
It can be started with the script at `config/run_consul.sh`.
The web UI is located at [port 8500](http://localhost:8500).








## Routes

Supported routes currently include:

```
/       : Density homepage with "fullness" graphic
/latest : APi endpoint providing the latest data available
/home   : future API homepage that allows a user to obtain an API token
```



## Data Sources

TODO

# app structure

```
|-- config/ (config settings and install scripts)
|-- README.md (This file)
|-- density/
    \
    |-- density.py  (the executable for this application)
    |-- static/     (your static files, such as js, css, imgs)
    |-- tests/      (unittest scripts that should be used during development)
```


# List of Developers

- Brian Zeng
- David Hao
- Sungwoo Bae
- Nate Brennand
- Benjamin Low
- Jessica Forde
- Jessica Valarezo
- Maclyn Brandwein
- Jackie Ho
- Dan Schlosser
- Terra Blevins
- Evan Tarrh
- Raymond Xu
