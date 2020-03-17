FROM ubuntu:bionic
MAINTAINER daniel.quilitzsch@mhp.com

RUN apt update && apt install -y python3 python3-venv apache2 libapache2-mod-wsgi-py3 

#ADD venv /venv
ADD app /app
RUN chmod +rx /app/webapisrv.py
RUN chmod +rx /app/davsrv.py
RUN chmod +rx /app/globals.py

ADD venv/lib64/python3.6/site-packages/ /usr/lib/python3/dist-packages/

COPY a2conf/000-default.conf /etc/apache2/sites-enabled/000-default.conf
COPY docker_run.sh /docker_run.sh

RUN chmod +x docker_run.sh
#CMD /docker_run.sh

CMD apachectl -D FOREGROUND
