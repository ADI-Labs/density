#!/bin/sh

ssh -T travis@adicu.com <<'ENDSSH'
echo   "=================================="
echo   "Deployment Starting"
echo   "----------------------------------"
echo   "Progress:"
printf "Deploying density.adicu.com          "

cd /srv/density/www
git fetch && git reset --hard origin/deploy

docker build -t density .
docker kill density
docker rm density
docker run \
    --net=host \
    --restart=always \
    -v /srv/density/www/../logs:/opt/logs \
    -d --name="density" density

printf "Done\n"
exit
ENDSSH
