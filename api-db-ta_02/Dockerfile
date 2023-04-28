#Dockerfile

FROM python:3.8

MAINTAINER AV

ADD . /app

WORKDIR /app

#new
ENV PYTHONPATH=/app

# Set environment variable for database host
ENV DB_HOST=timescale

RUN apt-get update && apt-get install -y build-essential redis-server sqlite3 \
    curl software-properties-common libpq-dev

# install nodejs and wscat websocket client
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -

RUN apt-get install -y nodejs && npm install wscat

# download and build TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install

RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz

RUN python -m pip install --upgrade pip

# install popular Python packages
RUN pip3 install -r requirements.txt

RUN pip install asyncpg

RUN pip install psycopg2-binary

RUN pip install python-multipart

RUN pip install alembic

COPY entrypoint.sh /usr/src/app/entrypoint.sh

RUN chmod +x entrypoint.sh

RUN pip install uvicorn

