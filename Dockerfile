FROM ubuntu:bionic
MAINTAINER daniel.quilitzsch@mhp.com

RUN apt update && apt install -y python3 python3-venv apache2 libapache2-mod-wsgi-py3 
RUN a2enmod proxy && a2enmod proxy_http

#python venv builded via pip in separate ubuntu:bionic container :)
ADD venv /venv
ADD app /app
RUN chown -R www-data:www-data /app
RUN chmod +rx /app/webapisrv.py
RUN chmod +rx /app/davsrv.py
RUN chmod +rx /app/globals.py

#-Old!!!----
#ADD venv/lib64/python3.6/site-packages/ /usr/lib/python3/dist-packages/ 
#-----------

COPY a2conf/000-default.conf /etc/apache2/sites-enabled/000-default.conf

CMD . /venv/bin/activate && apachectl -D FOREGROUND
