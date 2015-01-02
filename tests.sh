#!/bin/bash

source /vagrant/config/settings.dev
export TESTING=TRUE

echo '--------------------------------------'
echo '    pep 8 complicance testing'
echo '--------------------------------------'

flake8 density/
flake8 density/tests

echo '--------------------------------------'
echo '    unit testing'
echo '--------------------------------------'
cd density && nosetests


