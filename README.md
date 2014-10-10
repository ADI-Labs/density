
[![Build Status](https://travis-ci.org/adicu/density.svg?branch=master)](https://travis-ci.org/adicu/density)

Density
---

This is the recommend means of setting up Density for development.
Next, install [vagrant](http://www.vagrantup.com/).
Once vagrant is installed, you can run `vagrant up`, and vagrant will provision the virtual machine for you.
The app will run automatically under [Supervisor](http://supervisord.org/).
You can point your browser to [http://localhost:5000](http://localhost:5000) to see the running app.

If anything is wrong, the following commands will help you diagnose the app:

    vagrant ssh
    sudo service supervisor stop
    cd /vagrant
    source config/settings.dev
    cd density
    python density.py

Take a look at the logs, in `/var/log/supervisor` as well.



## Importing Dev Data

TODO

We use a partial dump of our data for quick-and-easy development. This gets
loaded on VM provision by our Vagrant setup scripts. It contains a small subset
and is not updated frequently, but is sufficient for most feature development
and bug squashing.





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