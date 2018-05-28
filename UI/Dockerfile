# start from base
FROM ubuntu

# install system-wide deps for python and node
RUN apt-get -yqq update
RUN apt-get -yqq install python-pip python-dev
RUN apt-get -yqq install nodejs npm

# copy our application code
ADD . /app
WORKDIR /app


RUN pip install -r requirements.txt

# expose port
EXPOSE 5000/tcp

# start app
CMD [ "python", "./server.py" ]
