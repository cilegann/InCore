from params import params
from service.dataService.utils import getFileInfo,getDf,getColType
from flask import Flask,make_response
from flask_restful import Api, Resource, reqparse
import uuid
from utils import tokenValidator,sql
import logging
import json
import importlib
import traceback
from service.analyticService.core.correlationAlgo.correlationBase import NoDataException
params=params()


class getCorrelationAlgoList(Resource):
    def get(self):
        try:
            logging.info('[API_getCorrelationAlgoList]')
            with open(params.correlationAlgoReg) as file:
                j=file.read()
            return {'status':'success','msg':'','data':json.loads(j)},200
        except Exception as e:
            logging.error(f'[API_getCorrelationAlgoList]{e}')
            return {'status':'error','msg':str(e),'data':{}},400


class doCorrelation(Resource):
    def post(self):
        fName='API_correlation'
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('token',type=str,required=True)
            parser.add_argument('fileUid',type=str,required=True)
            parser.add_argument('algoname',type=str,required=True)
            args = parser.parse_args()
            logging.info(f"[{fName}] args: {args}")
            fid=args['fileUid']
            algoName=args['algoname']
            token=args['token']
            if not tokenValidator(token):
                return {"status":"error","msg":"token error","data":{}},401
            module=importlib.import_module(f"service.analyticService.core.correlationAlgo.{algoName}")
            algo=getattr(module,algoName)
            result=algo(fid).do()
            fig={"div":result['div'],"script":result['script']}
            response=make_response(json.dumps({'status':'success','msg':'','data':fig}))
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
        except NoDataException as e:
            logging.info(f"[{fName}]{e}")
            return {"status":"success","msg":"","data":"None"},200
        except Exception as e:
            logging.error(f"[{fName}]{traceback.format_exc()}")
            return {"status":"error","msg":str(traceback.format_exc()),"data":{}},400