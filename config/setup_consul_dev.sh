#!/bin/sh

curl -X PUT -d '5000' http://localhost:8500/v1/kv/density/flask_port
curl -X PUT -d 'TRUE' http://localhost:8500/v1/kv/density/flask_debug
curl -X PUT -d '859795907220-57lf7t8m19a1i3huaogqg546u5efjk8j.apps.googleusercontent.com' http://localhost:8500/v1/kv/density/google_client_id
curl -X PUT -d 'density' http://localhost:8500/v1/kv/density/postgres_database
curl -X PUT -d 'localhost' http://localhost:8500/v1/kv/density/postgres_host
curl -X PUT -d 'adi' http://localhost:8500/v1/kv/density/postgres_password
curl -X PUT -d '5432' http://localhost:8500/v1/kv/density/postgres_port
curl -X PUT -d 'adi' http://localhost:8500/v1/kv/density/postgres_user
curl -X PUT -d 'abc123' http://localhost:8500/v1/kv/density/secret_key