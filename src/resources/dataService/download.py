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
from resources.dataService.utils import getFileInfo

param=params()

class Download(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('fileUid', type=str,required=True)
            parser.add_argument('fileName',type=str)
            # parser.add_argument('tokenstr',type=str,required=True)
            # parser.add_argument('tokenint',type=int,required=True)
            args = parser.parse_args()
            logging.debug(f"[Download] args: {args}")
            fileUid = args['fileUid']
            fileName=args['fileName']
            # tokenstr=args['tokenstr']
            # tokenint=args['tokenint']

            # #check token
            # if not tokenValidator(tokenstr,tokenint):
            #     return {"status":"error","msg":"token error","data":{}},201
            table=getFileInfo(fileUid)
            if table['status']!='success':
                return {"status":"error","msg":table['msg'],"data":{}},412
            table=table['data']
            logging.debug(f'[Download] {table}')
            if len(table)==0:
                logging.debug("[Download] file not found")
                abort(404)
            

            table=table[0]
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
            if fileName==None:
                fileName=fileUid
            headers['Content-Type']='application/octet-stream; charset=utf-8'
            headers['Content-Disposition'] = 'attachment; filename='+fileName+filetype
            return make_response(data,200,headers)
        except Exception as e:
            logging.error(e)
            return {"status":"error","msg":str(e),"data":{}},412
        
        
