from flask import Flask
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from params import params
from utils import tokenValidator
import glob
import uuid
from resources.dataService.fileChecker import fileChecker

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
        file = args['file']
        prjtype=args['type']
        # user=args['user']
        tokenstr=args['tokenstr']
        tokenint=args['tokenint']
        '''
        @ check token
        '''
        if not tokenValidator(tokenstr,tokenint):
            return {"status":"error","msg":"token error","data":{}},201
        
        '''
        @ check filetype
        '''
        pft=param.projectFileType
        filename=file.filename
        filetype=filename[filename.rfind("."):]
        if filetype!=pft[prjtype]:
            return {"status":"error","msg":"file type error","data":{}},201

        '''
        @ generate file UID and save
        '''
        uid=uuid.uuid1()
        while len(glob.glob(r(param.filepath+"/"+uid+"*")))!=0:
            uid=uuid.uuid1()
        savedPath=param.filepath+"/"+uid+filetype
        try:
            file.save(savedPath)
        except Exception as e:
            return {"status":"error","msg":"file error","data":{}},201

        '''
        @ check file content
        '''
        fileCheck=fileChecker(savedPath)
        if fileCheck['status']!='success':
            return {"status":"error","msg":fileCheck['msg'],"data":{}},201

        return {"status":"success","msg":"","data":{"fileUid":uid}},201