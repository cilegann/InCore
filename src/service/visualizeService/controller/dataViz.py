from flask import Flask,make_response
from flask_restful import Api, Resource, reqparse
from params import params
from utils import tokenValidator,sql
import logging
import json
import importlib

param=params()

class getDataVizAlgoList(Resource):
    def get(self):
        try:
            reg=json.load(open(param.dataVizAlgoReg))
            logging.debug(f'[getDataVizAlgo] reg list: {reg}')
        except Exception as e:
            logging.error(f'[getDataVizAlgo] {e}')
            return  {'status':'error','msg':f'[getDataVizAlgo] {e}','data':{}},500
        return {'status':'success','msg':'','data':reg},200

class doDataViz(Resource):
    def post(self):
        fName='doDataViz'
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('tokenstr',type=str,required=True)
            parser.add_argument('tokenint',type=int,required=True)
            parser.add_argument('fileUid',type=str,required=True)
            parser.add_argument('algoname',type=str,required=True)
            parser.add_argument('datacol',type=str,required=True)
            args = parser.parse_args()
            logging.debug(f"[{fName}] args: {args}")
            fid=args['fileUid']
            algoName=args['algoname']
            try:
                datacol=json.loads(args['datacol'])
            except Exception as e:
                return {"status":"error","msg":"can't parse datacol json","data":{}},401
            if not tokenValidator(args['tokenstr'],args['tokenint']):
                return {"status":"error","msg":"token error","data":{}},401
            
            module=importlib.import_module(f"service.visualizeService.core.dataVizAlgo.{algoName}")
            algo=getattr(module,algoName)
            reg=json.load(open(param.dataVizAlgoReg))
            for a in reg['algos']:
                if a['algoname']==algoName:
                    algoInfo=a
                    break
            if algoInfo==None:
                return {"status":"error","msg":f"algo {algoName} not found","data":{}},401
            v=algo(algoInfo,datacol,fid)
            if algoInfo['lib']=='bokeh':
                v.doBokehViz()
            elif algoInfo['lib']=='matplotlib':
                v.doMatpltViz()
                v.saveimg()
                v.img2bokeh()
            v.getComp()

        except Exception as e:
            logging.error(f'[doDataViz]{e}')
            return {'status':'error','msg':f'[doDataViz]{e}','data':{}},400
        # return {'status':'success','msg':'','data':v.component},201
        response=make_response(json.dumps({'status':'success','msg':'','data':v.component}))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response