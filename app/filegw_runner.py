#!/usr/bin/python3

#-Install on local system-------------------------
# apt install python3 python3-pip python3-flask python3-cheroot 
# pip3 install wsgidav # läuft auf collections_abc fehler (Lösung: import collections.abc as collections_abc)


#-Install in virtenv (runs also in docker)--------
# apt update && apt install -y python3 python3-venv
# python3 -m venv /myapp
# source /myapp/bin/activate   oder   . /myapp/bin/activate
# pip install flask cheroot wsgidav
# 
# Howto:https://www.codementor.io/@abhishake/minimal-apache-configuration-for-deploying-a-flask-app-ubuntu-18-04-phu50a7ft


#-Create a docker nfs volume--------------------
# docker volume create --driver local \
#    --opt type=nfs \
#    --opt o=addr=192.168.10.20,rw \
#    --opt device=:/test \
#    test


#-Import needed modules---------------------------------------------------
import os
import sys
import time
import threading


#-Global Vars-------------------------------------------------------------
from globals import dataPath
from globals import scriptDir


#-Import custom modules-------
from webapisrv import start_apisrv
from davsrv import start_davsrv

#-Sub Process Handler-----------------------------------------------------

#_thread.start_new_thread(start_srv, tuple())
davThread = threading.Thread(target=start_davsrv, args=())
davThread.daemon = True
davThread.start()

apiThread = threading.Thread(target=start_apisrv, args=())
apiThread.daemon = True
apiThread.start()

while True:
    time.sleep(1)

#-The Flask Part----------------------------------------------------------

