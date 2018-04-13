#!/usr/bin/env bash
createuser --superuser adi
createdb -E UTF8 -T template0 -O adi local_density
psql -d local_density <<EOL
ALTER ROLE adicu WITH PASSWORD 'password';
EOL
psql local_density < scripts/dump.sql

echo
echo

tee .env <<EOL
FLASK_DEBUG=true
FLASK_APP=density/__init__.py

DB_URI="postgresql://adi:password@localhost:5432/local_density"

GOOGLE_CLIENT_ID="859795907220-57lf7t8m19a1i3huaogqg546u5efjk8j.apps.googleusercontent.com"
SECRET_KEY="abc123"
UPLOAD_KEY="12345abcde"
EOL
