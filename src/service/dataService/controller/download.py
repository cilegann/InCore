from flask import Flask,make_response,abort
from flask_restful import Api,Resource,reqparse
from params import params
from utils import tokenValidator,sql
import glob
from pathlib import Path
import logging
import zipfile
import os
import shutil
from service.dataService.utils import getFileInfo

param=params()

class Download(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('fileUid', type=str,required=True)
            # parser.add_argument('fileName',type=str)
            # parser.add_argument('tokenstr',type=str,required=True)
            # parser.add_argument('tokenint',type=int,required=True)
            args = parser.parse_args()
            logging.info(f"[API_Download] args: {args}")
            fileUid = args['fileUid']
            # fileName=args['fileName']
            # tokenstr=args['tokenstr']
            # tokenint=args['tokenint']

            # #check token
            # if not tokenValidator(tokenstr,tokenint):
            #     return {"status":"error","msg":"token error","data":{}},201
            
            try:
                fileInfo=getFileInfo(fileUid)
            except Exception as e:
                logging.error(f'[API_Download]{e}')
                return {'status':'error','msg':str(e),'data':{}},400
            #fileInfo=fileInfo[0]
            logging.debug(f'[API_Download] FileInfo: {fileInfo}')
            if len(fileInfo)==0:
                logging.debug("[API_Download] file not found")
                abort(404)
            

            table=fileInfo[0]
            if table[1]=='cv':
                filepath=table[2]+'.zip'
                shutil.make_archive(table[2], 'zip', table[2])
                filetype='.zip'
            else:
                filepath=table[2]
                filetype=filepath[filepath.rfind('.'):]

            with open(filepath,'rb') as file:
                data=file.read()

            if filetype=='.zip':
                os.remove(filepath)
            headers={}
            # if fileName==None:
            #     fileName=fileUid
            headers['Content-Type']='application/octet-stream'
            # headers['Content-Disposition'] = 'attachment; filename='+fileName+filetype
            # return {"status":"success","msg":"","data":data},200
            return make_response(data,200,headers)
        except Exception as e:
            logging.error(f'[API_Download]{e}')
            return {"status":"error","msg":str(e),"data":{}},400
        
        
