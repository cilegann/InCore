from params import params
from flask import Flask,make_response
from flask_restful import Api, Resource, reqparse
import uuid
from utils import tokenValidator,sql
import logging
import json
import importlib
import traceback
import os

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
            if args['dataType'] not in reg:
                return {"status":"error","msg":f"{args['dataType']} is not a valid dataType","data":{}},400
            if args['projectType'] not in reg[args['dataType']]:
                return {"status":"error","msg":f"{args['projectType']} is not a valid projectType","data":{}},400
            return {"status":"success","msg":"","data":reg[args['dataType']][args['projectType']]}
        except Exception as e:
            logging.error(f"[API_getAnalyticAlgoList] {traceback.format_exc()}")
            return {"status":"error","msg":f"[API_getAnalyticAlgoList] {traceback.format_exc()}","data":{}},400

class getAnalyticAlgoParam(Resource):
    def get(self):
        try:
            logging.info('[API_getAnalyticAlgoParam]')
            parser=reqparse.RequestParser()
            parser.add_argument('dataType',type=str,required=True)
            parser.add_argument('projectType',type=str,required=True)
            parser.add_argument('algoName',type=str,required=True)
            args = parser.parse_args()
            if not os.path.exists(param.analyticServiceRoot+f"core/analyticAlgo/{args['dataType']}/{args['projectType']}/{args['algoName']}.json"):
                return {"status":"error","msg":f"[API_getAnalyticAlgoParam] {args['dataType']}.{args['projectType']}.{args['algoName']} not exists","data":{}},400
            with open(param.analyticServiceRoot+f"core/analyticAlgo/{args['dataType']}/{args['projectType']}/{args['algoName']}.json") as file:
                reg=json.load(file)
            return {"status":"success","msg":"","data":reg}
        except Exception as e:
            logging.error(f"[API_getAnalyticAlgoList] {traceback.format_exc()}")
            return {"status":"error","msg":f"[API_getAnalyticAlgoParam] {traceback.format_exc()}","data":{}},400
            