#-To Implement Feature List-----------------------------------------------
#--API Functions: Download, Upload, Delete, 
#--Folder ZIP Download, ZIP Upload
#--Action Menue in WebUI (oncontextmenue) for file and folder
#--Folder Path bar on top

#-Import needed modules---------------------------------------------------
import os
import sys
import shutil
import json
#import zipfile
from flask import Flask, request, redirect, url_for, send_from_directory, session, render_template, send_file

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

#-HTML Render Section-----------------------------------------------------

@app.route('/', methods=['GET']) 
def html_browser():
    davPath = dataPath
    pathSplit = []
    
    #-Forward to root path if no path is set-
    if request.args.get('path') == None:
        return redirect('?path=/', code=302)
    
    #-handle folder up requests
    newPath = request.args.get('path')
    pathSplit = newPath.split('/')
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

    #-Build the file and folder Ary-----
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


    #-The path line navigator Ary----
    pathObj = [{"dir":"", "lnk":"/"}]
    pathSplit = davPath.split('/')[1:]
    tmpSplit = []
    for entry in pathSplit:
        if entry != "":
            tmpSplit.append(entry)
            lnk = '/'.join(tmpSplit) 
            pathObj.append( {"dir":entry, "lnk":"/"+lnk} )

    #-Render HTML Template---
    return render_template(
        'browse.html', 
        view='browse',
        davPath=davPath,
        pathObj=pathObj,
        dirObj=dirObj
    )
#--------------------------------
@app.route('/folder/delete', methods=['GET']) 
def html_folder_delete():
    if request.args.get('path') == None or request.args.get('path') == '/':
        return 'parameter path not set', 400

    path = request.args.get('path')
    btPath = path.split('/')[:-1]
    btPath = '/'.join(btPath)
    msg = 'Wollen Sie "'+path+'" wirklich löschen?' 
    #-Render HTML Template---
    return render_template(
        'confirm.html', 
        view='folder_delete',
        msg=msg,
        path=path,
        backTo='/?path='+btPath
    )



#-API Section-------------------------------------------------------------
@app.route('/api/zip/download', methods=['GET']) 
def api_zip_download():
    if request.args.get('path') == None:
        return 'parameter path not set', 400

    path = request.args.get('path')
    fName = path.split('/')[-1]
    fName = ''.join(e for e in fName if e.isalnum())
    fPath = '/tmp/'+fName

    shutil.make_archive(fPath, 'zip', path)

    #zipf = zipfile.ZipFile(fName, 'w', zipfile.ZIP_DEFLATED)
    #zipdir('tmp/', zipf)
    #zipf.close()

    #return fPath
    #return send_file(fPath+'.zip', attachment_filename=fName+'.zip')
    try:
        return send_file(fPath+'.zip', as_attachment=True)
    except FileNotFoundError:
        abort(404)

#------------------

@app.route('/api/data/delete', methods=['POST']) 
def api_folder_delete():
    
    try: delPath = request.form['path'].replace('//', '/')
    except: return 'Bad Request', 400

    try: backTo =  request.form['backto'].replace('//', '/')
    except: backTo = '/'

    chk = False
    if os.path.isfile(delPath):
        try:
            os.remove(delPath)
            chk = True
        except:
            inf = 'unable to delete'
    
    if os.path.isdir(delPath):
        try:
            shutil.rmtree(delPath, ignore_errors=False)
            chk = True
        except:
            inf = 'unable to delete' + delPath
    
    if chk == False: 
        return inf, 400

    print(delPath + ' = deleted')

    return redirect(backTo, code=302)
    


#-------------------------------------------------------------------------

def start_apisrv():
    flPath = os.path.realpath(__file__)
    print(flPath)
    os.system("python3 " + flPath)  


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
   
#-------------------------------------------------------------------------