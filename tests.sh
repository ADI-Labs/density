#!/bin/bash

source /vagrant/config/settings.dev
export TESTING=TRUE

echo '--------------------------------------'
echo '              Linting'
echo '--------------------------------------'

flake8

echo '--------------------------------------'
echo '             Unit Tests'
echo '--------------------------------------'
cd density && PYTHONPATH=. py.test --verbose
