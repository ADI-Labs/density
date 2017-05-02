#!/usr/bin/env bash

# install postgresql-9.3
PG_REPO_APT_SOURCE=/etc/apt/sources.list.d/pgdg.list
if [ ! -f "$PG_REPO_APT_SOURCE" ]
then
    echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" > "$PG_REPO_APT_SOURCE"
    wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
    apt-get update
fi

apt-get install --yes postgresql-9.6
source /vagrant/config/settings.dev

sudo -u postgres psql < /vagrant/config/dump.sql
sudo -u postgres psql -c "CREATE USER adi WITH PASSWORD 'adi';"
sudo -u postgres psql -c "CREATE DATABASE density;"
sudo -u postgres psql -c "GRANT CONNECT ON DATABASE density TO adi;"
sudo -u postgres psql -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO adi;"

if [ ! -d "/opt/conda" ]; then
    wget --quiet --no-clobber http://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
    bash Miniconda2-latest-Linux-x86_64.sh -b -p "/opt/conda"
    echo 'export PATH="/opt/conda/bin:$PATH"' >> /home/vagrant/.bashrc
fi

export PATH="/opt/conda/bin:$PATH"

conda update --yes conda
conda env create --name density --file /vagrant/config/environment.yml --quiet

chown -R vagrant:vagrant /opt/conda
exit 0
