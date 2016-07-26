#!/bin/bash

source /vagrant/config/settings.dev
export TESTING=TRUE

echo '--------------------------------------'
echo '              Linting'
echo '--------------------------------------'

flake8
vulture ./

echo '--------------------------------------'
echo '             Unit Tests'
echo '--------------------------------------'
cd density && PYTHONPATH=. py.test --verbose
