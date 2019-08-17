from params import params
from service.dataService.utils import getFileInfo,getDf,getColType
from flask import Flask,make_response
from flask_restful import Api, Resource, reqparse
import uuid
from utils import tokenValidator,sql
import logging
import json
import importlib
params=params()

class getPreprocessAlgoList(Resource):
    def get(self):
        try:
            with open(params.dataPreprocessAlgoReg) as file:
                j=file.read()
            return {'status':'success','msg':'','data':json.loads(j)},200
        except Exception as e:
            logging.error(f'[API_getPreprocessAlgoList]{e}')
            return {'status':'error','msg':str(e),'data':{}},400

class doPreprocess(Resource):
    pass

class previewPreprocess(Resource):
    pass