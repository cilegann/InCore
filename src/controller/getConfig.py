from flask import Flask,make_response
from flask_restful import Api, Resource, reqparse
from params import params
import logging
import json
import importlib

param=params()

class getDataProjectType(Resource):
    def get(self):
        try:
            logging.debug("[API_getDataProjectType]")
        except Exception as e:
            logging.error(f'[API_getDataProjectType] {e}')
            return  {'status':'error','msg':f'[getDataProjectType] {e}','data':{}},400
        return {'status':'success','msg':'','data':param.dataProjectType},200

class getDataExtensionType(Resource):
    def get(self):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('datatype',type=str,required=True)
            args = parser.parse_args()
            datatype=args['datatype']
            logging.debug(f"[API_getDataExtensionType] args:{args}")
        except Exception as e:
            logging.error(f'[API_getDataExtensionType] {e}')
            return  {'status':'error','msg':f'[getDataExtensionType] {e}','data':{}},400
        if datatype not in param.dataExtensionType:
            return {'status':'error','msg':f'[getDataExtensionType] dataType {datatype} not valid','data':{}},400
        return {'status':'success','msg':'','data':param.dataExtensionType[datatype]},200

