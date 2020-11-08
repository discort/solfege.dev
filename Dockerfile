FROM python:3.8-slim-buster

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get -y dist-upgrade && apt-get install -y git \
    && apt-get -y install gcc libpq-dev ffmpeg libsndfile-dev nginx && rm -rf /var/lib/apt /var/cache/apt

WORKDIR /wheels
ADD ./requirements.txt /wheels

RUN pip install -r /wheels/requirements.txt \
                       -f /wheels \
        && rm -rf /wheels \
        && rm -rf /root/.cache/pip/*

RUN pip install uwsgi

WORKDIR /opt
COPY . /opt

ADD support/default.conf /etc/nginx/conf.d/default.conf
ADD support/start.sh /usr/local/bin/start.sh
RUN chmod 755 /usr/local/bin/start.sh

CMD ["/usr/local/bin/start.sh"]
