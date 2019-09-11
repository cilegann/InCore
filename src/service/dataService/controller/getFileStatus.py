from flask import Flask
from flask_restful import Api, Resource, reqparse
from params import params
from utils import tokenValidator,sql
from service.dataService.utils import getColType,getFileInfo
import glob
import logging
import json

# app = Flask(__name__)
# api = Api(app)

param=params()

class getFileStatus(Resource):
    def post(self):
        '''
        @ fileUids: file id
        @ tokenstr: keypair1
        @ tokenint: keypair2
        '''
        fName='getFileStatus'
        parser = reqparse.RequestParser()
        parser.add_argument('fileUids', type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        #logging.info(f"[API_getFileStatus] args: {args}")
        fids=args['fileUids']
        token=args['token']

        fids=json.loads(fids)
        logging.debug(f'[API_getFileStatus]{fids}')
        #check token
        if not tokenValidator(token):
            return {"status":"error","msg":"token error","data":{}},401
        try:
            fileInfo=[getFileInfo(fid)[0] for fid in fids]
        except Exception as e:
            logging.error(f'[API_{fName}]{e}')
            return {'status':'error','msg':str(e),'data':{}},400
        fileInfo=[f[4] for f in fileInfo]
        #logging.debug(f"{fileInfo}")
        #logging.debug(f'[API_{fName}]{json.dumps(fileInfo)}')
        return {"status":"success","msg":"","data":{"status":fileInfo}},200