from flask import Flask
from flask_restful import Api, Resource, reqparse
from params import params
from utils import tokenValidator
from resources.dataService.utils import getColType
import glob
import logging

# app = Flask(__name__)
# api = Api(app)

param=params()

class getColumn(Resource):
    def post(self):
        '''
        @ fileUid: file id
        @ type: num/cv/nlp 
        @ tokenstr: keypair1
        @ tokenint: keypair2
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('fileUid', type=str,required=True)
        parser.add_argument('type',type=str,required=True)
        parser.add_argument('tokenstr',type=str,required=True)
        parser.add_argument('tokenint',type=int,required=True)
        args = parser.parse_args()
        logging.debug(f"[getColumn] args: {args}")
        fid=args['fileUid']
        dataType=args['type']
        tokenstr=args['tokenstr']
        tokenint=args['tokenint']

        
        #check token
        if not tokenValidator(tokenstr,tokenint):
            return {"status":"error","msg":"token error","data":{}},201
        
        pft=param.dataFileType
        #check project type
        if dataType not in pft:
            return {"status":"error","msg":"data type not supported","data":{}},201
        
        folderPaths=glob.glob(param.filepath+"/"+fid)
        filePaths=glob.glob(param.filepath+"/"+fid+".*")

        if len(folderPaths)!=0:
            filepath=folderPaths[0]
        else:
            filepath=filePaths[0]

        gct=getColType(filepath,dataType).get()
        return gct,201