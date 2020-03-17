#-Import needed modules---------------------------------------------------
import os
import sys
import json
from flask import Flask, request, redirect, url_for, send_from_directory, session, render_template

#-Global and Session Vars-------------------------------------------------
from globals import dataPath
from globals import scriptDir

app = Flask(__name__)
app.secret_key = "changeit"
app.debug = True

#@app.before_first_request
#def start_dav():
#    thread.start()
#def init_sessions():
    #session['workdir'] = False
#    session.permanent = True

#-The Flask Thing (API)---------------------------------------------------

@app.route('/', methods=['GET']) 
def html_home():
    davPath = dataPath
    if request.args.get('path') != None:
        davPath += request.args.get('path')

    if not os.path.isdir(davPath):
        return 'Bad Request', 400 

    dirAry = os.listdir(davPath)
    dirJson = json.dumps(dirAry, indent=2)
    #return '<pre>'+dirJson+'</pre>'

    return render_template(
        'browse.html', 
        view='browse',
        dirAry=dirAry
    )




#-------------------------------------------------------------------------

def start_apisrv():
    flPath = os.path.realpath(__file__)
    print(flPath)
    os.system("python3 " + flPath)  


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
   
#-------------------------------------------------------------------------