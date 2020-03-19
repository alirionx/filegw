#-Import needed modules----------------------
import os
from cheroot import wsgi
from wsgidav.wsgidav_app import WsgiDAVApp


#-Global and Env Vars------------------------
from globals import dataPath
from globals import scriptDir

print(dataPath)

#--------------------

commonConf = {
    "host": "0.0.0.0",
    "port": 8080,
    "simple_dc":{
        "user_mapping": {"*": True}
    },
    "provider_mapping": {
        "/": dataPath,
    },
    "verbose": 1,
}

#-The WebDav Service------------------------

app = WsgiDAVApp(commonConf)

def start_davsrv(config=False):
    if config == False:
        config = commonConf

    app = WsgiDAVApp(config)

    server_args = {
        "bind_addr": (config["host"], config["port"]),
        "wsgi_app": app,
    }
    server = wsgi.Server(**server_args)
    server.start()

#--------------------------------------------

