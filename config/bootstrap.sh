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
apt-get install --yes docker.io git vim

# install postgresql-9.3
PG_REPO_APT_SOURCE=/etc/apt/sources.list.d/pgdg.list
if [ ! -f "$PG_REPO_APT_SOURCE" ]
then
    echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > "$PG_REPO_APT_SOURCE"
    wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
    apt-get update
fi

apt-get install --yes postgresql-9.3
sudo -u postgres psql < /vagrant/config/density_dump.sql
sudo -u postgres psql < /vagrant/config/oauth_dev_dump.sql

if [ ! -d "/opt/conda" ]; then
    wget --no-clobber http://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
    bash Miniconda2-latest-Linux-x86_64.sh -b -p "/opt/conda"
    echo 'export PATH="/opt/conda/bin:$PATH"' >> /home/vagrant/.bashrc
    export PATH="/opt/conda/bin:$PATH"

    conda update --yes conda
    conda env update --name root --file /vagrant/config/environment.yml
fi

exit 0
