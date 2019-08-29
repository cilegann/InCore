from flask import Flask,make_response
from flask_restful import Api, Resource
from params import params
import logging
import json
import importlib

param=params()

class getDataProjectType(Resource):
    def get(self):
        try:
            logging.info("[API_getDataProjectType]")
        except Exception as e:
            logging.error(f'[API_getDataProjectType] {e}')
            return  {'status':'error','msg':f'[getDataProjectType] {e}','data':{}},500
        return {'status':'success','msg':'','data':param.dataProjectType},200

class getDataFileType(Resource):
    def get(self):
        try:
            logging.info("[API_getDataFileType]")
        except Exception as e:
            logging.error(f'[API_getDataFileType] {e}')
            return  {'status':'error','msg':f'[getDataFileType] {e}','data':{}},500
        return {'status':'success','msg':'','data':param.dataFileType},200

