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
        fName='[getFileStatus]'
        parser = reqparse.RequestParser()
        parser.add_argument('fileUids', type=str,required=True)
        parser.add_argument('tokenstr',type=str,required=True)
        parser.add_argument('tokenint',type=int,required=True)
        args = parser.parse_args()
        logging.debug(f"[getFileStatus] args: {args}")
        fids=args['fileUids']
        tokenstr=args['tokenstr']
        tokenint=args['tokenint']

        fids=json.loads(fids)
        logging.debug(f'[getFileStatus]{fids}')

        #check token
        if not tokenValidator(tokenstr,tokenint):
            return {"status":"error","msg":"token error","data":{}},401
        try:
            fileInfo=[getFileInfo(fid) for fid in fids]

        except Exception as e:
            logging.error(f'{fName}{e}')
            return {'status':'error','msg':str(e),'data':{}},400

        fileInfo=[f[4] for f in fileInfo]
        logging.debug(json.dumps(fileInfo))
        return {"status":"success","msg":"","data":{"status":fileInfo}},200