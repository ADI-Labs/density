# use Docker's provided python image
FROM continuumio/miniconda
MAINTAINER Alan Du <ahd2125@columbia.edu>

# install all packages
COPY ./config/environment.yml /environment.yml
RUN conda env update --name root --file /environment.yml

# add the application directories
COPY ./density /density
WORKDIR /density

# expose the port and start the server
EXPOSE 6002
CMD gunicorn density:app \
    --bind 0.0.0.0:6002 \
    --log-file /opt/logs/gunicorn.log \
    --log-level debug
