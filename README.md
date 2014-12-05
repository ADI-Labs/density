
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

    vagrant ssh
    cd /vagrant
    source config/settings.dev
    cd density
    python density.py





## Importing Dev Data

TODO

We use a partial dump of our data for quick-and-easy development.
This gets loaded on VM provision by our Vagrant setup scripts.
It contains a small subset and is not updated frequently, but is sufficient for most feature development and bug squashing.





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
- Jessica Forde
- Jessica Valarezo
