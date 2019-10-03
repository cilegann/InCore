from flask import Flask
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from params import params
from utils import tokenValidator,sql
import glob
import uuid
from service.dataService.utils import fileChecker,fileUidGenerator
import logging
import jwt

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
        fName='[Upload]'
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files',required=True)
        parser.add_argument('type',type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        
        file = args['file']
        dataType=args['type']
        token=args['token']
        
        #check token
        if not tokenValidator(token):
            return {"status":"error","msg":"token error","data":{}},401
        args.pop('token')
        logging.debug(f"[API_Upload] args: {args}")
        pft=param.dataExtensionType
        #check project type
        if dataType not in pft:
            return {"status":"error","msg":"project type not supported","data":{}},400
        
        #check filetype
        
        filename=file.filename
        filetype=filename[filename.rfind("."):]
        logging.debug("[API_Upload] File type:{filetype}")
        if filetype not in pft[dataType]:
            return {"status":"error","msg":"file type error","data":{}},400

        #generate file UID and save
        uid=fileUidGenerator().uid
        logging.debug(f'[API_Upload] file UID:{uid}')
        savedPath=param.filepath+"/"+uid+filetype
        try:
            file.save(savedPath)
        except Exception as e:
            return {"status":"error","msg":f"file error:{e}","data":{}},400

        '''
        @ check file content
        '''
        try:
            fileChecker(savedPath,dataType).check()
        except Exception as e:
            logging.error(f'{fName}{e}')
            return {"status":"error","msg":str(e),"data":{}},400
        if filetype=='.zip':
            savedPath=savedPath[:savedPath.rfind(".")]
            numFilePath=glob.glob((savedPath+"/*.csv"))[0].replace("\\","/")
        try:
            db=sql()
            if filetype=='.zip':
                db.cursor.execute(f"insert into files (`fid`,`dataType`,`path`,`numFile`,`inuse`) values ('{uid}','{dataType}','{savedPath}','{numFilePath}',False);")
            else:
                db.cursor.execute(f"insert into files (`fid`,`dataType`,`path`,`numFile`,`inuse`) values ('{uid}','{dataType}','{savedPath}','{savedPath}',False);")
            db.conn.commit()
        except Exception as e:
            db.conn.rollback()
        finally:
            db.conn.close()
        logging.info(f"[API_Upload] OK with file uid {uid}")
        return {"status":"success","msg":"","data":{"fileUid":uid}},201