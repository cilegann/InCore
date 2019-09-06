from flask import Flask,make_response
from flask_restful import Api, Resource, reqparse
from params import params
import logging
import json
import importlib
import traceback

param=params()

class getDataProjectType(Resource):
    def get(self):
        try:
            logging.info("[API_getDataProjectType]")
            return {'status':'success','msg':'','data':param.dataProjectType},200
        except Exception as e:
            logging.error(f'[API_getDataProjectType] {traceback.format_exc()}')
            return  {'status':'error','msg':f'[getDataProjectType] {traceback.format_exc()}','data':{}},400
        

class getDataExtensionType(Resource):
    def get(self):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('datatype',type=str,required=True)
            args = parser.parse_args()
            datatype=args['datatype']
            logging.info(f"[API_getDataExtensionType] args:{args}")
        except Exception as e:
            logging.error(f'[API_getDataExtensionType] {e}')
            return  {'status':'error','msg':f'[getDataExtensionType] {e}','data':{}},400
        if datatype not in param.dataExtensionType:
            return {'status':'error','msg':f'[getDataExtensionType] dataType {datatype} not valid','data':{}},400
        return {'status':'success','msg':'','data':param.dataExtensionType[datatype]},200

