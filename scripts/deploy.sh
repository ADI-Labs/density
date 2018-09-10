#!/bin/bash

set -ex

echo   "=================================="
echo   "Deployment Starting"
echo   "----------------------------------"
echo   "Progress:"
printf "Deploying density.adicu.com          "

ssh -T travis@adicu.com -o StrictHostKeyChecking=no <<'ENDSSH'
cd /srv/density/www
git fetch && git reset --hard origin/master

docker build -t density .
docker kill density
docker rm density
docker run \
    --net=host \
    --restart=always \
    -v /srv/density/www/../logs:/opt/logs \
    -d --name="density" density
exit
ENDSSH

printf "Done\n"
