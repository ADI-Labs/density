#!/usr/bin/env bash

# installs the package passed in if it's not installed
install () {
    package=$1
    dpkg-query -l $package &> /dev/null
    if [ $? -ne 0 ]; then
        apt-get -y install $package 
    fi
}

# install git
install git-core
install git


# install python
install python
install python-pip
install python-dev
install python-software-properties
install libpq-dev
pip install flake8  # for local testing
pip install -r /vagrant/config/requirements.txt


# install postgres
install postgresql
sudo -u postgres psql -c "create schema public;"
# TODO: setup database and insert any data that is necessary


# install redis
install redis-server
# TODO: necessary setups for dev with Redis


# install vim
install vim


# set up supervisord
install supervisord


if [ ! -a /etc/supervisor/conf.d/data.conf ]; then
    cat > /etc/supervisor/conf.d/data.conf << EOF
[program:data]
directory=/vagrant/
command=/vagrant/scripts/start_server_supervisor.sh /vagrant/config/settings.dev
autostart=true
autorestart=true
EOF
fi

service supervisor stop
sleep 3
service supervisor start

exit 0
