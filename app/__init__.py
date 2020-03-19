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
from globals import tmpPath
from globals import scriptDir

app = Flask(__name__)
#template_dir = os.path.dirname(os.path.realpath(__file__)) + '/templates'
#app = Flask(__name__, template_folder=template_dir)

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
    
    #-set real and virt Path
    virtPath = request.args.get('path')
    if virtPath == "": virtPath = "/"
    realPath = davPath + request.args.get('path')
    
    #-handle folder up requests------
    pathSplit = virtPath.split('/')
    if virtPath.endswith('../'):
        virtPath = virtPath.replace('../', '')
        pathSplit = virtPath.split('/')
        if len(pathSplit) > 1:
            pathSplit = pathSplit[:-1]
        davPath = '/'.join(pathSplit)

        return redirect('?path='+davPath, code=302)
    #else:
    #    realPath = davPath += virtPath

    #-Format realPath and check if exists-----
    realPath = realPath.replace('//', '/')
    if not os.path.isdir(realPath):
        return 'Bad Request', 400 

    #-Build the file and folder Ary-----
    dirObj = []
    dirAry = os.listdir(realPath)
    dirAry.sort()
    
    #-Add folder Up option if virtPath is NOT virt root path---
    if virtPath not in ['', '/']:
        dirObj = [{
            "path":'../',
            "type":"dir",
            "lnk":virtPath+"../"
        }]

    #-Build files and folder object for webUI file browser--- 
    #-for Folders---
    for val in dirAry:
        isVirtPath = (virtPath + '/' + val).replace('//', '/')
        isRealPath = (davPath + '/' + isVirtPath).replace('//', '/')
        if os.path.isdir(isRealPath):
            toAdd = { 
                "path":val, 
                "type":"dir",
                "lnk":isVirtPath
            }
            dirObj.append(toAdd)
    
    #-for Files--- -> DQ: DAS IST ABSICHTLICH DOPPELT!!!
    for val in dirAry:
        isVirtPath = (virtPath + '/' + val).replace('//', '/')
        isRealPath = (davPath + '/' + isVirtPath).replace('//', '/')
        if os.path.isfile(isRealPath):
            toAdd = { 
                "path":val, 
                "type":"file",
                "lnk":isVirtPath
            }
            dirObj.append(toAdd)


    #-The path line navigator Ary for webUI file browser----
    pathObj = [{"dir":"", "lnk":"/"}]
    pathSplit = virtPath.split('/')[1:]
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
        virtPath=virtPath,
        pathObj=pathObj,
        dirObj=dirObj
    )

#--------------------------------
@app.route('/mkdir', methods=['GET']) 
def html_make_dir():

    #-Check if path GET arg is given, else error--- 
    if request.args.get('path') == None:
        return 'parameter path not set', 400

    #-define real and virt Path---
    virtPath = request.args.get('path')
    realPath = (dataPath + '/' + virtPath).replace('//', '/')
    
    #-Exit if realPath does not exist--
    if not os.path.isdir(realPath):
        return 'path does not exist ', 400

    #-Render HTML Template---
    return render_template(
        'make_dir.html', 
        view='make_dir',
        path=virtPath,
        backTo='/?path='+virtPath
    )


#--------------------------------
@app.route('/file/upload', methods=['GET']) 
def html_file_upload():
    #-Check if path GET arg is given, else error--- 
    if request.args.get('path') == None:
        return 'parameter path not set', 400

    #-define real and virt Path---
    virtPath = request.args.get('path')
    realPath = (dataPath + '/' + virtPath).replace('//', '/')

    #-Exit if realPath does not exist--
    if not os.path.isdir(realPath):
        return 'path does not exist ', 400

    #-Render HTML Template---
    return render_template(
        'upload_file.html', 
        view='file_upload',
        path=virtPath,
        backTo='/?path='+virtPath
    )

#--------------------------------
@app.route('/zip/upload', methods=['GET']) 
def html_zip_upload():
    #-Check if path GET arg is given, else error--- 
    if request.args.get('path') == None:
        return 'parameter path not set', 400

    #-define real and virt Path---
    virtPath = request.args.get('path')
    realPath = (dataPath + '/' + virtPath).replace('//', '/')

    #-Exit if realPath does not exist--
    if not os.path.isdir(realPath):
        return 'path does not exist ', 400

    #-Render HTML Template---
    return render_template(
        'upload_zip.html', 
        view='zip_upload',
        path=virtPath,
        backTo='/?path='+virtPath
    )

#--------------------------------
@app.route('/data/delete', methods=['GET']) 
def html_folder_delete():
    #-Check if path GET arg is given, else error--- 
    if request.args.get('path') == None or request.args.get('path') == '/':
        return 'parameter path not set', 400

    #-define real, virt Path and backto Path---
    virtPath = request.args.get('path')
    realPath = (dataPath + '/' + virtPath).replace('//', '/')
    btPath = virtPath.split('/')[:-1]
    btPath = '/'.join(btPath)

    #-Exit if realPath does not exist--
    if not os.path.isdir(realPath) and not os.path.isfile(realPath):
        return 'path does not exist ', 400
    
    #-Render HTML Template---
    msg = 'Wollen Sie "'+virtPath+'" wirklich löschen?' 

    return render_template(
        'confirm.html', 
        view='data_delete',
        msg=msg,
        path=virtPath,
        backTo='/?path='+btPath
    )



#-API Section---------------------------------------------------------------------

@app.route('/api/mkdir', methods=['POST']) 
def api_make_dir():

    #-Check if all required POST args are given---
    try: 
        path = request.form['path']
        mkdir = request.form['mkdir']
        mkdir = ''.join(e for e in mkdir if e.isalnum())
        tgtPath = dataPath + '/' + path 
        tgtPath = tgtPath.replace('//', '/')
        mkPath = tgtPath + '/' + mkdir
        mkPath = mkPath.replace('//', '/')
    except: 
        return 'Bad Request', 400
    
    #-Check if custom redirect is gives---
    try: backTo =  request.form['backto'].replace('//', '/')
    except: backTo = False

    #-Check Access and try to create new directory---
    chkAccess = os.access(tgtPath, os.W_OK)
    if chkAccess == True:
        try: os.mkdir(mkPath)
        except: return 'Something went wrong.', 400
    else:
        return 'Missing rights to create a folder here...', 400


    #-Redirect if set-------
    if backTo != False:
        return redirect(backTo, code=302)
    else:
        return mkdir


#--------------------------------
@app.route('/api/file/download', methods=['GET']) 
def api_file_download():
    #-Check if path GET arg is given, else error--- 
    if request.args.get('path') == None:
        return 'parameter path not set', 400
    
    path = request.args.get('path')
    tgtPath = dataPath + '/' + path
    
    if not os.path.isfile(tgtPath):
        return 'file does not exist or is unreadable', 404

    #-Try to load and send file---    
    try:
        return send_file(tgtPath, as_attachment=True)
    except FileNotFoundError:
        abort(404)

#-------------------

@app.route('/api/zip/download', methods=['GET']) 
def api_zip_download():
    #-Check if path GET arg is given, else error--- 
    if request.args.get('path') == None:
        return 'parameter path not set', 400

    path = request.args.get('path')
    tgtPath = dataPath + '/' + path

    #-If source path is directory: Zip and download----
    if os.path.isdir(tgtPath):
        fName = tgtPath.split('/')[-1]
        fName = ''.join(e for e in fName if e.isalnum())
        fPath = '/tmp/'+fName

        shutil.make_archive(fPath, 'zip', tgtPath)
        try:
            return send_file(fPath+'.zip', as_attachment=True)
        except FileNotFoundError:
            abort(404)
    
    #-If source path is file: Zip and download----
    elif os.path.isfile(tgtPath):
        fSrc = tgtPath.split('/')[:-1]
        fSrc = '/'.join(fSrc)
        fName = tgtPath.split('/')[-1]
        fPath = '/tmp/'+fName

        shutil.make_archive(fPath, 'zip', fSrc, fName)
        try:
            return send_file(fPath+'.zip', as_attachment=True)
        except FileNotFoundError:
            abort(404)
    else:
        return 'Bad Request', 400


#------------------
@app.route('/api/file/upload', methods=['POST']) 
def api_file_upload():
    
    #Howto Curl: curl -X POST -F 'files[]=@/home/myuser/myfile.txt' -F 'path=/Downloads' http://localhost:5000/api/file/upload
    
    #-Check if all required POST args are given---
    try: 
        path = request.form['path']
        tgtPath = dataPath + '/' + path 
        tgtPath = tgtPath.replace('//', '/')
        fileList = request.files.getlist('files[]')
    except: 
        return 'Bad Request', 400

    #-Check if custom redirect is gives---
    try: backTo =  request.form['backto'].replace('//', '/')
    except: backTo = False

    #-Check Access Rights for file upload---
    chkAccess = os.access(tgtPath, os.W_OK)
    if chkAccess == False:
        return 'Missing rights to create a folder here...', 400
    
    #-Try to save uploaded files---
    chk = True
    uplOkAry = []
    for file in fileList:
        try:
            file.save(os.path.join(tgtPath, file.filename))
            uplOkAry.append(file.filename)
        except:
            chk = False
    if chk == False: 
        return 'Upload failed', 400
    
    #-Redirect if set-------
    if backTo != False:
        return redirect(backTo, code=302)
    else:
        return json.dumps(uplOkAry)


#------------------
@app.route('/api/zip/upload', methods=['POST']) 
def api_zip_upload():
    #-Check if all required POST args are given---
    try: 
        path = request.form['path']
        tgtPath = dataPath + '/' + path 
        tgtPath = tgtPath.replace('//', '/')
        fileList = request.files.getlist('files[]')
    except: 
        return 'Bad Request', 400

    #-Check if custom redirect is gives---
    try: backTo =  request.form['backto'].replace('//', '/')
    except: backTo = False

    #-Check Access Rights for file upload---
    chkAccess = os.access(tgtPath, os.W_OK)
    if chkAccess == False:
        return 'Missing rights to create a folder here...', 400

    #-Try to unzip uploaded archive-file---
    chk = True
    for file in fileList:
        try:
            file.save(os.path.join(tmpPath, file.filename))
            shutil.unpack_archive(tmpPath+'/'+file.filename, tgtPath, 'zip')
        except:
            chk = False
    if chk == False: 
        return 'Upload failed', 400
    
    #-Redirect if set-------
    if backTo != False:
        return redirect(backTo, code=302)
    else:
        return file.filename
    

#------------------
@app.route('/api/data/delete', methods=['POST']) 
def api_folder_delete():
     #-Check if all required POST args are given---
    try: 
        path = request.form['path'].replace('//', '/')
        delPath = dataPath + '/' + path 
    except: 
        return 'Bad Request', 400

    #-Check if custom redirect is gives---
    try: backTo =  request.form['backto'].replace('//', '/')
    except: backTo = False

    #-Check if path is file or folder and try to delete---
    chk = False
    inf = ''
    if os.path.isfile(delPath):
        try:
            os.remove(delPath)
            chk = True
        except:
            inf = 'unable to delete file: '+delPath
    
    if os.path.isdir(delPath):
        try:
            shutil.rmtree(delPath, ignore_errors=False)
            chk = True
        except:
            inf = 'unable to delete folder: ' + delPath
    
    if chk == False: 
        return inf, 400


    #-Redirect if set-------
    if backTo != False:
        return redirect(backTo, code=302)
    else:
        return delPath


#-----------------------------------------------------------------------------

def start_apisrv():
    flPath = os.path.realpath(__file__)
    print(flPath)
    os.system("python3 " + flPath)  


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
   
#-----------------------------------------------------------------------------