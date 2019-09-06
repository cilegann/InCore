from params import params
from flask import Flask,make_response
from flask_restful import Api, Resource, reqparse
import uuid
from utils import tokenValidator,sql
import logging
import json
import importlib
import traceback

param=params()

class getAnalyticAlgoList(Resource):
    def get(self):
        try:
            logging.info('[API_getAnalyticAlgoList]')
            parser=reqparse.RequestParser()
            parser.add_argument('dataType',type=str,required=True)
            parser.add_argument('projectType',type=str,required=True)
            args = parser.parse_args()
            with open(param.analyticAlgoReg) as file:
                reg=json.load(file)
            return {"status":"error","msg":"","data":reg[args['dataType']][args['projectType']]}
        except Exception as e:
            logging.error(f"[API_getAnalyticAlgoList] {traceback.format_exc()}")
            return {"status":"error","msg":f"[API_getAnalyticAlgoList] {traceback.format_exc()}","data":{}}

class getAnalyticAlgoParam(Resource):
    def get(self):
        try:
            logging.info('[API_getAnalyticAlgoList]')
            parser=reqparse.RequestParser()
            parser.add_argument('dataType',type=str,required=True)
            parser.add_argument('projectType',type=str,required=True)
            parser.add_argument('algoname',type=str,required=True)
            args = parser.parse_args()
            with open(param.analyticServiceRoot+f"core/analyticAlgo/{args['dataType']}/{args['projectType']}/{args['algoname']}.json") as file:
                reg=json.load(file)
            return {"status":"error","msg":"","data":reg}
        except Exception as e:
            logging.error(f"[API_getAnalyticAlgoList] {traceback.format_exc()}")
            return {"status":"error","msg":f"[API_getAnalyticAlgoList] {traceback.format_exc()}","data":{}}
            