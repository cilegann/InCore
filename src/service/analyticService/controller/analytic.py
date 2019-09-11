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
from service.analyticService.utils import getModelInfo,changeModelStatus
from service.analyticService.core.preprocess import preprocess as preprocessCore
from service.dataService.utils import getFileInfo,unlockFile
import threading
import ctypes
import pickle
import shutil

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
            if not os.path.exists(param.analyticServiceRoot+f"core/analyticCore/{args['dataType']}/{args['projectType']}/{args['algoName']}.json"):
                return {"status":"error","msg":f"[API_getAnalyticAlgoParam] {args['dataType']}.{args['projectType']}.{args['algoName']} not exists","data":{}},400
            with open(param.analyticServiceRoot+f"core/analyticCore/{args['dataType']}/{args['projectType']}/{args['algoName']}.json") as file:
                reg=json.load(file)
            return {"status":"success","msg":"","data":reg}
        except Exception as e:
            logging.error(f"[API_getAnalyticAlgoList] {traceback.format_exc()}")
            return {"status":"error","msg":f"[API_getAnalyticAlgoParam] {traceback.format_exc()}","data":{}},400

class doModelTrain(Resource):
    def post(self):
        try:
            logging.info('[API_doModelTrain]')
            parser=reqparse.RequestParser()
            parser.add_argument('token',type=str,required=True)
            parser.add_argument('fileUid',type=str,required=True)
            parser.add_argument('dataType',type=str,required=True)
            parser.add_argument('projectType',type=str,required=True)
            parser.add_argument('algoName',type=str,required=True)
            parser.add_argument('param',type=str,required=True)
            parser.add_argument('input',type=str,required=True)
            parser.add_argument('output',type=str,required=True)
            args=parser.parse_args()
            logging.debug(f'[API_doModelTrain]{args}')
            if not tokenValidator(args['token']):
                return {"status":"error","msg":"token error","data":{}},401
            fid=args['fileUid']
            dataType=args['dataType']
            projectType=args['projectType']
            algoName=args['algoName']
            algoParam=args['param']
            algoInput=args['input']
            algoOutput=args['output']
            with open(param.analyticAlgoReg) as file:
                reg=json.load(file)
            if dataType not in reg:
                return {"status":"error","msg":f"Analytic service currently not support dataType {dataType}","data":{}},400
            if projectType not in reg[dataType]:
                return {"status":"error","msg":f"Analytic service currently not support projectType {projectType} with dataType {dataType}","data":{}},400
            if algoName not in reg[dataType][projectType]:
                return {"status":"error","msg":f"Algo {algoName} not found in {dataType}.{projectType}","data":{}},400
            algoInfo={'dataType':dataType,'projectType':projectType,'algoName':algoName,'param':algoParam,'input':algoInput,'output':algoOutput}
            module=importlib.import_module(f"service.analyticService.core.analyticCore.{dataType}.{projectType}.{algoName}")
            attr=getattr(module,algoName)
            algo=attr(algoInfo,fid,'train')
            mid=algo.train()
            logging.info(f'[API_doModelTrain] ModelUid: {mid}')
            return {"status":"success","msg":"","data":{"modelUid":mid}},200
        except Exception as e:
            logging.error(f"[API_doModelTrain]{traceback.format_exc()}")
            return {"status":"error","msg":str(traceback.format_exc()),"data":{}},400

class stopTraining(Resource):
    def delete(self):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('token',type=str,required=True)
            parser.add_argument('modelUid',type=str,required=True)
            args=parser.parse_args()
            logging.info(f'[API_stopTraining] args:{args}')
            if not tokenValidator(args['token']):
                return {"status":"error","msg":"token error","data":{}},401
            mid=args['modelUid']
            _,_,_,_,_,status,_,_=getModelInfo(mid)[0]
            if status!='train':
                return {"status":"error","msg":f"model {mid} is not training","data":{}},400
            res=0
            for t in threading.enumerate():
                if t.name==mid:
                    print(t)
                    print(t.ident)
                    tid=ctypes.c_long(t.ident)
                    res=ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(SystemExit))
            if res==0:
                logging.info(f'[API_stopTraining] model {mid} not found in thread')
                return {"status":"error","msg":f"model {mid} not found in thread","data":{}},400
            elif res!=1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
                logging.info(f'[API_stopTraining] something went wrong, can\'t stop training')
                return {"status":"error","msg":f"something went wrong, can't stop training","data":{}},400
            try:
                db=sql()
                db.cursor.execute(f"UPDATE `models` SET `status`='fail',`failReason`='user stopped' WHERE `mid`='{mid}';")
                db.conn.commit()
            except Exception as e:
                db.conn.rollback()
                raise Exception(e)
            finally:
                db.conn.close()
            return {"status":"success","msg":"","data":{}},200
        except Exception as e:
            logging.error(f"[API_stopTraining]{traceback.format_exc()}")
            return {"status":"error","msg":str(traceback.format_exc()),"data":{}},400

class getModelPreview(Resource):
    def get(self):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('token',type=str,required=True)
            parser.add_argument('modelUid',type=str,required=True)
            args=parser.parse_args()
            logging.info(f'[API_getModelPreview] args:{args}')
            if not tokenValidator(args['token']):
                return {"status":"error","msg":"token error","data":{}},401
            mid=args['modelUid']
            _,_,_,_,_,status,_,_=getModelInfo(mid)[0]
            if status!='success':
                return {"status":"error","msg":f"model {mid} is still training or failed. Can't provide preview","data":{}},400
            with open(os.path.join(param.modelpath,mid,'preview.pkl'),'rb') as file:
                preview=pickle.load(file)
            return {"status":"success","msg":"","data":preview}
        except Exception as e:
            logging.error(f"[API_getModelPreview]{traceback.format_exc()}")
            return {"status":"error","msg":str(traceback.format_exc()),"data":{}},400

class doModelTest(Resource):
    def post(self):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('token',type=str,required=True)
            parser.add_argument('modelUid',type=str,required=True)
            parser.add_argument('fileUid',type=str,required=True)
            parser.add_argument('label',type=str)
            args=parser.parse_args()
            logging.info(f'[API_doModelTest] args:{args}')
            if not tokenValidator(args['token']):
                return {"status":"error","msg":"token error","data":{}},401
            mid=args['modelUid']
            fid=args['fileUid']
            _,_,_,_,_,status,_,_=getModelInfo(mid)[0]
            if status!='success':
                return {"status":"error","msg":f"model {mid} is still training or failed. Can't test","data":{}},400
            with open(os.path.join(param.modelpath,mid,'algoInfo.pkl'),'rb') as file:
                algoInfo=pickle.load(file)
            module=importlib.import_module(f"service.analyticService.core.analyticCore.{algoInfo['dataType']}.{algoInfo['projectType']}.{algoInfo['algoName']}")
            attr=getattr(module,algoInfo['algoName'])
            if algoInfo['projectType']=='abnormal':
                algo=attr(algoInfo,fid,'test',mid=mid,testLabel=args['label'])
            else:
                algo=attr(algoInfo,fid,'test',mid=mid)
            algo.predictAlgo()
            result=algo.test()
            return {"status":"success","msg":"","data":result},200
        except Exception as e:
            logging.error(f"[API_doModelTest]{traceback.format_exc()}")
            return {"status":"error","msg":str(traceback.format_exc()),"data":{}},400

class doModelPredict(Resource):
    def post(self):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('token',type=str,required=True)
            parser.add_argument('modelUid',type=str,required=True)
            parser.add_argument('fileUid',type=str,required=True)
            parser.add_argument('preprocess',type=bool,required=True)
            args=parser.parse_args()
            logging.info(f'[API_doModelPredict] args:{args}')
            if not tokenValidator(args['token']):
                return {"status":"error","msg":"token error","data":{}},401
            mid=args['modelUid']
            fid=args['fileUid']
            _,modelFid,_,_,_,status,_,_=getModelInfo(mid)[0]
            if status!='success':
                return {"status":"error","msg":f"model {mid} is still training or failed. Can't predict","data":{}},400
            preprocessedFid="None"
            if args['preprocess']:
                _,_,_,_,_,preprocessActionFile=getFileInfo(modelFid)[0]
                if preprocessActionFile:
                    with open(preprocessActionFile) as file:
                        action=json.load(file)
                    preprocessedFid=preprocessCore(fid,action)
                    fid=preprocessedFid
            with open(os.path.join(param.modelpath,mid,'algoInfo.pkl'),'rb') as file:
                algoInfo=pickle.load(file)
            module=importlib.import_module(f"service.analyticService.core.analyticCore.{algoInfo['dataType']}.{algoInfo['projectType']}.{algoInfo['algoName']}")
            attr=getattr(module,algoInfo['algoName'])
            algo=attr(algoInfo,fid,'predict',mid=mid)
            algo.predictAlgo()
            predictedFid=algo.predict()
            return {"status":"success","msg":"","data":{"preprocessedFileUid":preprocessedFid,"predictedFileUid":predictedFid}},200
        except Exception as e:
            logging.error(f"[API_doModelPredict]{traceback.format_exc()}")
            return {"status":"error","msg":str(traceback.format_exc()),"data":{}},400

class deleteModel(Resource):
    def post(self):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('token',type=str,required=True)
            parser.add_argument('modelUid',type=str,required=True)
            args=parser.parse_args()
            logging.info(f'[API_deleteModel] args:{args}')
            if not tokenValidator(args['token']):
                return {"status":"error","msg":"token error","data":{}},401
            mid=args['modelUid']
            _,modelFid,_,_,_,status,_,_=getModelInfo(mid)[0]
            if status=='train':
                return {"status":"error","msg":f"model {mid} is still training. Can't delete","data":{}},400
            try:
                shutil.rmtree(os.path.join(param.modelpath,mid))
            except FileNotFoundError:
                pass
            try:
                db=sql()
                db.cursor.execute(f"delete from `models` where `mid`='{mid}';")
                numOfresult=db.cursor.execute(f"select * from `models` where `fid`='{modelFid}';")
                if numOfresult==0:
                    unlockFile(modelFid)
                db.conn.commit()
            except Exception as e:
                db.conn.rollback()
                raise e
            finally:
                db.conn.close()
            return {"status":"success","msg":"","data":{}},200
        except Exception as e:
            logging.error(f"[API_deleteModel]{traceback.format_exc()}")
            return {"status":"error","msg":str(traceback.format_exc()),"data":{}},400
            

class getModelStatus(Resource):
    def get(self):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('token',type=str,required=True)
            parser.add_argument('modelUid',type=str,required=True)
            args=parser.parse_args()
            logging.info(f'[API_getModelStatus] args:{args}')
            if not tokenValidator(args['token']):
                return {"status":"error","msg":"token error","data":{}},401
            mid=args['modelUid']
            _,_,_,_,_,status,_,_=getModelInfo(mid)[0]
            return {"status":"success","msg":"","data":status},200
        except Exception as e:
            logging.error(f"[API_getModelStatus]{traceback.format_exc()}")
            return {"status":"error","msg":str(traceback.format_exc()),"data":{}},400

class getModelParameter(Resource):
    def get(self):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('token',type=str,required=True)
            parser.add_argument('modelUid',type=str,required=True)
            args=parser.parse_args()
            logging.info(f'[API_getModelParameter] args:{args}')
            if not tokenValidator(args['token']):
                return {"status":"error","msg":"token error","data":{}},401
            mid=args['modelUid']
            _,_,_,_,_,status,_,_=getModelInfo(mid)[0]
            if status!='success':
                return {"status":"error","msg":f"model {mid} is still training or failed. Can't get parameter","data":{}},400
            with open(os.path.join(param.modelpath,mid,'algoInfo.pkl'),'rb') as file:
                algoInfo=pickle.load(file)
            return {"status":"success","msg":"","data":algoInfo},200
        except Exception as e:
            logging.error(f"[API_getModelParameter]{traceback.format_exc()}")
            return {"status":"error","msg":str(traceback.format_exc()),"data":{}},400

class getModelFailReason(Resource):
    def get(self):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('token',type=str,required=True)
            parser.add_argument('modelUid',type=str,required=True)
            args=parser.parse_args()
            logging.info(f'[API_getModelFailReason] args:{args}')
            if not tokenValidator(args['token']):
                return {"status":"error","msg":"token error","data":{}},401
            mid=args['modelUid']
            _,_,_,_,_,status,_,reason=getModelInfo(mid)[0]
            if status!='fail':
                return {"status":"error","msg":f"No failure found","data":{}},400
            return {"status":"success","msg":"","data":reason},200
        except Exception as e:
            logging.error(f"[API_getModelFailReason]{traceback.format_exc()}")
            return {"status":"error","msg":str(traceback.format_exc()),"data":{}},400