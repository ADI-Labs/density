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

apt-get update

# install git
apt-get install --yes git

# install postgresql-9.3
PG_REPO_APT_SOURCE=/etc/apt/sources.list.d/pgdg.list
if [ ! -f "$PG_REPO_APT_SOURCE" ]
then
    echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > "$PG_REPO_APT_SOURCE"
    wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
    apt-get update
fi

apt-get install --yes postgresql-9.3 \
    libpq-dev
sudo -u postgres psql < /vagrant/config/density_dump.sql
sudo -u postgres psql < /vagrant/config/oauth_dev_dump.sql

# install python
apt-get install --yes python \
    python-pip \
    python-dev \
    python-software-properties

pip install -r /vagrant/config/requirements.txt
pip install flake8  # for local testing

# install vim
apt-get install --yes vim

# install docker
apt-get install --yes docker.io
service restart docker

exit 0