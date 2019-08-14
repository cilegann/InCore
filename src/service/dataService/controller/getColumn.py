from flask import Flask
from flask_restful import Api, Resource, reqparse
from params import params
from utils import tokenValidator,sql
from service.dataService.utils import getColType,getFileInfo
import glob
import logging

# app = Flask(__name__)
# api = Api(app)

param=params()

class getColumn(Resource):
    def post(self):
        '''
        @ fileUid: file id
        @ tokenstr: keypair1
        @ tokenint: keypair2
        '''
        fName='[getCol]'
        parser = reqparse.RequestParser()
        parser.add_argument('fileUid', type=str,required=True)
        parser.add_argument('tokenstr',type=str,required=True)
        parser.add_argument('tokenint',type=int,required=True)
        args = parser.parse_args()
        logging.info(f"[getColumn] args: {args}")
        fid=args['fileUid']
        tokenstr=args['tokenstr']
        tokenint=args['tokenint']

        
        #check token
        if not tokenValidator(tokenstr,tokenint):
            return {"status":"error","msg":"token error","data":{}},401
        
        try:
            fileInfo=getFileInfo(fid)
        except Exception as e:
            logging.error(f'{fName}{e}')
            return {'status':'error','msg':str(e),'data':{}},400
        fileInfo=fileInfo[0]

        filePath=fileInfo[2]
        dataType=fileInfo[1]
        try:
            gct=getColType(filePath,dataType).get()
        except Exception as e:
            logging.error(f'{fName}{e}')
            return {'status':'error','msg':str(e),'data':{}},400
        return {'status':'success','msg':'','data':{"cols":gct}},200