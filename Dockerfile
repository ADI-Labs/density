# use Docker's provided python image
FROM python:2.7
MAINTAINER natebrennand <natebrennand@gmail.com>

# install all packages
COPY ./config/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# add the application directories
ADD ./density /density
WORKDIR /density

# expose the port and start the server
EXPOSE 5000
CMD gunicorn density:app -b 0.0.0.0:5000 --log-level debug
