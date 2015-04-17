
# Density

[![Build Status](https://travis-ci.org/adicu/density.svg?branch=master)](https://travis-ci.org/adicu/density)


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




## Routes

Supported routes currently include:

```
/       : Density homepage with "fullness" graphic
/latest : APi endpoint providing the latest data available
/home   : future API homepage that allows a user to obtain an API token
```




## Data Sources

Data for density is provided by CUIT in coordination with ESC.




## Style guide

Make sure to conform to [AirBnb's brilliant style guide](https://github.com/airbnb/javascript) when writing javascript.



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



# Changelog

0.1.1: Datetime formatting changed to ISO 8601.
0.1.0: Basic API up and stable.




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
