from flask import Flask
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from params import params
from utils import tokenValidator
import glob
import uuid

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
        savedPath='./'+param.filepath+"/"+uid+filetype
        file.save(savedPath)

        '''
        @ check file content
        '''
        if filetype=='.csv':
            pass
            #TODO call csv checker
        if filetype=='.tsv':
            pass
            #TODO call tsv checker
        if filetype=='.zip':
            import zipfile
            with zipfile.ZipFile(savedPath, 'r') as zip_ref:
                zip_ref.extractall('./'+param.filepath+'/'+uid)
            csvFiles=glob.glob(r(param.filepath+"/"+uid+"/*.csv"))
            if len(csvFiles)!=1:
                return {"status":"error","msg":"zip should contains only 1 csv file","data":{}},201
            # TODO call zip checker

        
        return file.name, 201