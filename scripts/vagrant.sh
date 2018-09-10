#!/usr/bin/env bash
PG_REPO_APT_SOURCE=/etc/apt/sources.list.d/pgdg.list
if [ ! -f "$PG_REPO_APT_SOURCE" ]
then
    echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" > "$PG_REPO_APT_SOURCE"
    wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
fi

apt-get update
apt-get install --yes postgresql-9.6

if [ ! -d "/opt/anaconda" ]; then
    wget --quiet --no-clobber https://repo.continuum.io/miniconda/Miniconda3-4.5.11-Linux-x86_64.sh
    bash Miniconda3-4.5.11-Linux-x86_64.sh -b -p "/opt/anaconda"
    echo 'export PATH="/opt/anaconda/bin:$PATH"' >> /home/vagrant/.bashrc
fi

export PATH="/opt/anaconda/bin:$PATH"
conda install --yes python=3.6.6 pip virtualenv
pip install -U pipenv
chown -R vagrant:vagrant /opt/anaconda

cd /vagrant/ && ./scripts/bootstrap.sh
