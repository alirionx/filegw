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
        newPath = request.args.get('path')
        if newPath.endswith('../'):
            newPath = newPath.replace('../', '')
            pathSplit = newPath.split('/')
            if len(pathSplit) > 0:
                pathSplit = pathSplit[:-1]
            davPath = '/'.join(pathSplit)

            return redirect('?path='+davPath, code=302)
        else:
            davPath += newPath

    davPath = davPath.replace('//', '/')

    if not os.path.isdir(davPath):
        return 'Bad Request', 400 

    dirObj = []
    dirAry = os.listdir(davPath)
    dirAry.sort()
    
    if davPath not in ['', '/']:
        dirObj = [{
            "path":'../',
            "type":"dir",
            "lnk":davPath+"../"
        }]

    for val in dirAry:
        isPath = (davPath + '/' + val).replace('//', '/')
        if os.path.isdir(isPath):
            toAdd = { 
                "path":val, 
                "type":"dir",
                "lnk":isPath
            }
            dirObj.append(toAdd)

    for val in dirAry:
        isPath = (davPath + '/' + val).replace('//', '/')
        if os.path.isfile(isPath):
            toAdd = { 
                "path":val, 
                "type":"file",
                "lnk":""
            }
            dirObj.append(toAdd)

    #dirJson = json.dumps(dirAry, indent=2)
    #return '<pre>'+dirJson+'</pre>'

    return render_template(
        'browse.html', 
        view='browse',
        davPath=davPath,
        dirAry=dirAry,
        dirObj=dirObj
    )




#-------------------------------------------------------------------------

def start_apisrv():
    flPath = os.path.realpath(__file__)
    print(flPath)
    os.system("python3 " + flPath)  


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
   
#-------------------------------------------------------------------------