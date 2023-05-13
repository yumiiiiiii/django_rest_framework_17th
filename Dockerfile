#FROM python:3.8.3-alpine
FROM python:3.8.3-slim-buster
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

# dependencies for psycopg2-binary
#RUN apk add --no-cache mariadb-connector-c-dev
#RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base


# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel # 오류해결...-> Could not build wheels for backports.zoneinfo, which is required to install pyproject.toml-based projects
RUN pip install pyproject.toml

RUN apt-get update && apt-get install -y sudo
RUN adduser --disabled-password --gecos "" user  \
    && echo 'user:user' | chpasswd \
    && adduser user sudo \
    && echo 'user ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers



RUN apt-get -y install python3-dev default-libmysqlclient-dev build-essential

RUN sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

RUN pip install -r requirements.txt
#RUN pip install --upgrade pip # upgrade

# Now copy in our code, and run it
COPY . /app/