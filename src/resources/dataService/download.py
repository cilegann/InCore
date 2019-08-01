from flask import Flask,make_response
from flask_restful import Api,Resource,reqparse
from params import params
from utils import tokenValidator
import glob
from pathlib import Path
import logging
import zipfile
import os
import shutil

param=params()

class Download(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('fileUid', type=str,required=True)
            parser.add_argument('fileName',type=str)
            parser.add_argument('tokenstr',type=str,required=True)
            parser.add_argument('tokenint',type=int,required=True)
            args = parser.parse_args()
            logging.debug(f"[Download] args: {args}")
            fileUid = args['fileUid']
            fileName=args['fileName']
            # user=args['user']
            tokenstr=args['tokenstr']
            tokenint=args['tokenint']

            #check token
            if not tokenValidator(tokenstr,tokenint):
                return {"status":"error","msg":"token error","data":{}},201
            
            paths=glob.glob(param.filepath+"/"+fileUid)
            files=glob.glob(param.filepath+"/"+fileUid+".*")
            logging.debug(f'[Download] paths {paths}')
            logging.debug(f'[Download] files {files}')
            if len(paths)==0 and len(files)==0:
                from flask import abort

                logging.debug("[Download] file not found")
                abort(404)
            if len(files)==0:
                filepath=paths[0]+'.zip'
                shutil.make_archive(paths[0], 'zip', paths[0])
                filetype='.zip'
                pass
            else:
                filepath=files[0]
                filetype=filepath[filepath.rfind('.'):]

            with open(filepath,'rb') as file:
                data=file.read()

            if filetype=='.zip':
                os.remove(filepath)
            headers={}
            headers['Content-Type']='application/octet-stream; charset=utf-8'
            headers['Content-Disposition'] = 'attachment; filename='+fileName+filetype
            return make_response(data,201,headers)
        except Exception as e:
            return {"status":"error","msg":str(e),"data":{}},201
        
        
