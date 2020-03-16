#!/usr/bin/python3

#apt install python3 python3-pip libnfs-dev
#pip3 install libnfs
#https://twisted.readthedocs.io/en/twisted-16.3.0/web/howto/using-twistedweb.html
#https://wsgidav.readthedocs.io/en/latest/index.html

#nfs = libnfs.NFS('nfs://192.168.10.20/nfsdev')
#a = nfs.open('/test.txt', mode='w+')
#a.write(dateTime)
#a.close()

#fileList = nfs.listdir('/')
#print(fileList)

#-Import needed modules---------------------------------------------------
import os
import sys
import time
import threading


#-Global Vars-------------------------------------------------------------
from globals import dataPath
from globals import scriptDir


#-Import custom modules-------
from webapi import start_apisrv
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

