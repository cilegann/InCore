from flask import Flask
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from params import params
from utils import tokenValidator,sql
import glob
import uuid
import logging
from service.dataService.utils import getFileInfo
import shutil
import os

# app = Flask(__name__)
# api = Api(app)

param=params()

class DeleteFile(Resource):
    def post(self):
        '''
        @ type: num/cv/nlp
        @ file: a file
        @ tokenstr: keypair1
        @ tokenint: keypair2
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('fileUid', type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.info(f"[API_DelFile] args: {args}")
        fid = args['fileUid']
        token=args['token']

        
        #check token
        if not tokenValidator(token):
            return {"status":"error","msg":"token error","data":{}},401
        try:
            fileInfo=getFileInfo(fid)
        except Exception as e:
            logging.error(f'[Delfile]{e}')
            return {'status':'error','msg':str(e),'data':{}},400

        fileInfo=fileInfo[0]

        if fileInfo[3]==1:
            logging.warning(f'[API_DelFile] file {fid} in use')
            return {"status":"error","msg":"The file is in-used","data":{}},400
        
        filePath=fileInfo[2]
        dataType=fileInfo[1]
        actionFile=fileInfo[5]
        if dataType=='cv':
            shutil.rmtree(filePath)
        else:
            os.remove(filePath)
        if actionFile:
            os.remove(actionFile)
        
        try:
            db=sql()
            db.cursor.execute(f"delete from files where fid='{fid}'")
            db.conn.commit()
        except Exception as e:
            logging.error(f"[API_DelFile] {e}")
        finally:
            db.conn.close()
        
        logging.info(f"[API_DelFile] OK with file uid {fid}")
        return {"status":"success","msg":"","data":{}},201