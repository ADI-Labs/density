# use Docker's provided python image
FROM continuumio/miniconda
MAINTAINER Alan Du <ahd2125@columbia.edu>

# install all packages
COPY ./config/environment.yml /config/environment.yml
RUN conda env create --name density --file /config/environment.yml

# add the application directories
COPY ./config /config
COPY ./density /density
WORKDIR /density

# expose the port and start the server
EXPOSE 6002
CMD /bin/bash -c "source /config/settings.prod && \
    source activate density && \
    gunicorn density:app \
        --bind 0.0.0.0:6002 \
        --log-file /opt/logs/gunicorn.log \
        --log-level debug"
