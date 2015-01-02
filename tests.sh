#!/bin/bash

source /vagrant/config/settings.dev
export TESTING=TRUE

echo '--------------------------------------'
echo '    pep 8 complicance testing'
echo '--------------------------------------'

flake8 density/tests
flake8 density/density.py

echo '--------------------------------------'
echo '    unit testing'
echo '--------------------------------------'
nosetests -sv density/tests/


