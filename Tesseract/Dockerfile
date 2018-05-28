# start from base
FROM ubuntu

# install system-wide deps for python and node
RUN apt-get -yqq update
RUN apt-get -yqq install python-pip python-dev
RUN apt-get -yqq install nodejs npm
#RUN ln -s /usr/bin/nodejs /usr/bin/node

RUN apt-get update
RUN apt-get install -y g++ # or clang++ (presumably)
RUN apt-get install -y autoconf automake libtool
RUN apt-get install -y autoconf-archive
RUN apt-get install -y pkg-config
RUN apt-get install -y libpng-dev
RUN apt-get install -yqq libturbojpeg
RUN apt-get install -y libtiff5-dev
RUN apt-get install -y zlib1g-dev
#RUN apt-get install -y --reinstall build-essential
#RUN apt-get install -y gcc
# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org Flask requests
RUN apt-get install -y libleptonica-dev
RUN apt install -y tesseract-ocr

# copy our application code
ADD . /app
WORKDIR /app

# fetch app specific deps



# expose port
EXPOSE 9200/tcp

# start app
CMD [ "python", "./server.py" ]
