#!/usr/bin/env bash
sudo -u postgres createuser --superuser adi
sudo -u postgres createdb -E UTF8 -l en_US.UTF8 -T template0 -O adi density
sudo -u postgres psql -d density <<EOL
ALTER ROLE adi WITH PASSWORD 'password';
EOL
sudo -u postgres psql density < dump.sql
