#!/usr/bin/env bash

# installs the package passed in if it's not installed
install () {
    package=$1
    dpkg-query -l $package &> /dev/null
    if [ $? -ne 0 ]; then
        apt-get -y install $package
    fi
}

apt-get update

# install git
install git-core
install git


# install postgres
install postgresql

# check if user adicu has been created
echo Check for adicu database user
echo \\dg | sudo -u postgres psql | grep adicu
if [ 0 -ne $? ]; then
    cat | sudo -u postgres psql <<EOF
CREATE USER adicu with password 'adicu';
EOF
fi

echo

# check if database has been created
echo Check for density database
echo \\l | sudo -u postgres psql | grep density
if [ 0 -ne $? ]; then
    cat | sudo -u postgres psql <<EOF
CREATE DATABASE density WITH
OWNER adicu
ENCODING 'UTF-8'
LC_CTYPE 'en_US.utf8'
LC_COLLATE 'en_US.utf8'
TEMPLATE template0;
-- Create the schema
\c density
CREATE SCHEMA schema;
ALTER SCHEMA schema OWNER TO adicu;
EOF
fi

# install python
apt-get install -y python \
    python-pip \
    python-dev \
    python-software-properties \
    libpq-dev
apt-get update
pip install -r /vagrant/config/requirements.txt
pip install flake8  # for local testing


# install vim
install vim


# set up supervisor
install supervisor


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
