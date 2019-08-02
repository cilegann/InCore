from flask import Flask
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from params import params
from utils import tokenValidator
import glob
import uuid
from resources.dataService.utils import fileChecker,fileUidGenerator
import logging

# app = Flask(__name__)
# api = Api(app)

param=params()

class Upload(Resource):
    def post(self):
        '''
        @ type: num/cv/nlp
        @ file: a file
        @ tokenstr: keypair1
        @ tokenint: keypair2
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files',required=True)
        parser.add_argument('type',type=str,required=True)
        # parser.add_argument('user',type=str,required=True)
        parser.add_argument('tokenstr',type=str,required=True)
        parser.add_argument('tokenint',type=int,required=True)
        args = parser.parse_args()
        logging.debug(f"[Upload] args: {args}")
        file = args['file']
        dataType=args['type']
        # user=args['user']
        tokenstr=args['tokenstr']
        tokenint=args['tokenint']

        
        #check token
        if not tokenValidator(tokenstr,tokenint):
            return {"status":"error","msg":"token error","data":{}},201
        
        pft=param.dataFileType
        #check project type
        if dataType not in pft:
            return {"status":"error","msg":"project type not supported","data":{}},201
        
        #check filetype
        
        filename=file.filename
        filetype=filename[filename.rfind("."):]
        logging.debug("[Upload] File type:{filetype}")
        if filetype not in pft[dataType]:
            return {"status":"error","msg":"file type error","data":{}},201

        #generate file UID and save
        uid=fileUidGenerator().uid
        logging.debug(f'[Upload] file UID:{uid}')
        savedPath=param.filepath+"/"+uid+filetype
        try:
            file.save(savedPath)
        except Exception as e:
            return {"status":"error","msg":f"file error:{e}","data":{}},201

        '''
        @ check file content
        '''
        fileCheck=fileChecker(savedPath,dataType).check()
        if fileCheck['status']!='success':
            return {"status":"error","msg":fileCheck['msg'],"data":{}},201
        logging.info(f"[Upload] OK with file uid {uid}")
        return {"status":"success","msg":"","data":{"fileUid":uid}},201