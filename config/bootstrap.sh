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

# install postgresql-9.3
PG_REPO_APT_SOURCE=/etc/apt/sources.list.d/pgdg.list
if [ ! -f "$PG_REPO_APT_SOURCE" ]
then
    echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > "$PG_REPO_APT_SOURCE"
    wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
    apt-get update
fi

apt-get -y install postgresql-9.3
sudo -u postgres psql < /vagrant/config/density_dump.sql

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

exit 0
