#!/usr/bin/env bash


# add swap if DNE
# swap is necessary for using Docker
if [ $(sudo swapon -s | wc -l) -eq 1 ]
then
    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
fi


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

install postgresql-9.3
install libpg-dev
sudo -u postgres psql < /vagrant/config/density_dump.sql
sudo -u postgres psql < /vagrant/config/oauth_dev_dump.sql

# install python
install python
install python-pip
install python-dev
install python-software-properties

pip install -r /vagrant/config/requirements.txt
pip install flake8  # for local testing

# install vim
install vim

# install docker
install docker.io
service restart docker

exit 0