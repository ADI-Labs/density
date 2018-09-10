#!/usr/bin/env bash
sudo -u postgres createuser --superuser adi
sudo -u postgres createdb -E UTF8 -l en_US.UTF8 -T template0 -O adi density
sudo -u postgres psql -d density <<EOL
ALTER ROLE adi WITH PASSWORD 'password';
EOL
sudo -u postgres psql density < scripts/dump.sql

echo
echo

tee .env <<EOL
FLASK_DEBUG=true
FLASK_APP=density/__init__.py
DB_URI="postgresql://adi:password@localhost:5432/density"
GOOGLE_CLIENT_ID="859795907220-57lf7t8m19a1i3huaogqg546u5efjk8j.apps.googleusercontent.com"
SECRET_KEY="abc123"
UPLOAD_KEY="12345abcde"
EOL
