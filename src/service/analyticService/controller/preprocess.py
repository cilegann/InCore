from params import params
from service.dataService.utils import getFileInfo,getDf,getColType
from flask import Flask,make_response
from flask_restful import Api, Resource, reqparse
import uuid
from utils import tokenValidator,sql
import logging
import json
import importlib
from service.analyticService.core.preprocess import preprocess as core
import traceback
params=params()

class getPreprocessAlgoList(Resource):
    def get(self):
        try:
            logging.info('[API_getPreprocessAlgoList]')
            with open(params.dataPreprocessAlgoReg) as file:
                j=file.read()
            return {'status':'success','msg':'','data':json.loads(j)},200
        except Exception as e:
            logging.error(f'[API_getPreprocessAlgoList]{e}')
            return {'status':'error','msg':str(e),'data':{}},400

class doPreprocess(Resource):
    def post(self):
        fName='API_doPreprocess'
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('token',type=str,required=True)
            parser.add_argument('fileUid',type=str,required=True)
            parser.add_argument('action',type=str,required=True)
            args = parser.parse_args()
            logging.info(f"[{fName}] args: {args}")
            fid=args['fileUid']
            token=args['token']
            if not tokenValidator(token):
                return {"status":"error","msg":"token error","data":{}},401
            try:
                action=json.loads(args['action'])
            except Exception as e:
                return {"status":"error","msg":"can't parse action json","data":{}},400
            uid=core(fid,action).do()
            return {"status":"success","msg":"","data":{"fileUid":uid}}
        except Exception as e:
            logging.error(f"[{fName}] {traceback.format_exc()}")
            return {"status":"error","msg":str(e),"data":{}},400

class previewPreprocess(Resource):
    pass