import pandas as pd
import numpy as np
from service.dataService.utils import getFileInfo,getColType,categoricalConverter,getDf,lockFile
from service.analyticService.utils import modelUidGenerator
from utils import sql
from params import params
import threading
import traceback
import json
from datetime import datetime

class analytic():
    def __init__(self,algoInfo,fid,action='train'):
        try:
            self.action=action # 'train' / 'preview' / 'test' / 'predict'
            self.algoInfo=algoInfo
            self.sysparam=params()
            self.dataType=self.algoInfo['dataType'] # 'num' / 'cv' / 'nlp'
            self.projectType=self.algoInfo['projectType'] # 'regression' / 'classification' .....
            self.algoName=self.algoInfo['algoname']
            self.fid=fid
            _,dataType,self.path,self.numFile,_,self.preprocessActionFile=getFileInfo(self.fid)[0]
            if dataType!=self.dataType:
                raise Exception(f'[]')
            self.thread=None
            self.mid=modelUidGenerator().uid
            self.paramDef=json.load(open(self.sysparam.analyticServiceRoot+f'analyticAlgo/{self.dataType}/{self.projectType}/{self.algoName}.json'))
            self.lib=self.paramDef["lib"]
            self.param=None # the input parameter
            self.inputDict=json.loads(algoInfo['input']) # input columns mapping
            self.outputDict=json.loads(algoInfo['output']) # output columns mapping
            self.dataDf=None # raw dataframe
            self.inputData={}    
            '''
            INPUT DATA STRUCTURE
            {
                "input1":
                        np.array(
                            [
                                [col1-row1,col2-row2,....,colN-row1],
                                ....,
                                [col1-rowM,col2-rowM,...,colN-rowM]
                            ]
                        )
                "input2":
                        np.array(
                            [
                                [col1-row1,col2-row2,....,colN-row1],
                                ....,
                                [col1-rowM,col2-rowM,...,colN-rowM]
                            ]
                        )
            }
            '''
            self.outputData={}
            '''
            OUTPUT DATA STRUCTURE
            {
                "output1":
                        np.array([col1-row1,col1-row2,....,col1-rowN])
                "output2":
                        np.array([col1-row1,col1-row2,....,col1-rowN])
            }
            '''
            self.model=None
            self.result=None
            self.vizRes=None
            self.txtRes=None
            self.getParams()
            if action=='test' or action=='train':
                self.loadModel()
            self.getData()
        except Exception as e:
            raise Exception(f'[{self.algoName}][init]{traceback.format_exc()}')
    
    def train(self):
        try:
            try:
                db=sql()
                db.cursor.execute(f"INSERT INTO `models` (`mid`, `fid`, `dataType`, `projectType`,`algoName`,`status`,`startTime`) VALUES ('{self.mid}', '{self.fid}', '{self.dataType}', '{self.projectType}','train','{datetime.now()}');")
                db.conn.commit()
            except Exception as e:
                db.conn.rollback()
                raise Exception(e)
            finally:
                db.conn.close()
            lockFile(self.fid)
            self.thread=threading.Thread(targert=self._trainWrapper)
            self.thread.start()
            self.thread.name=str(self.mid)
        except Exception as e:
            raise Exception(f"[{self.algoName}] {traceback.format_exc()}")

    def trainWrapper(self):
        try:
            self.trainAlgo()
            self.visualize()
            self.saveModel()
        except Exception as e:
            raise Exception(f"{traceback.format_exc()}")
    
    def visualize(self):
        self.vizRes=self.buildinVisualize()
        self.vizRes.extend(self.customVisualize())

    # implement in PROJECT
    def predict(self):
        '''
        implement in PROJECT
        call predictAlgo
        merge self.dataDf and self.result
        write out newDf
        return fid
        '''
        pass
    
    # implement in PROJECT
    def test(self):
        '''
        implement in PROJECT
        call predictAlgo
        call visualize
        generate text to self.txtRes
        '''
        pass

    def getParams(self):
        rawParam=json.loads(self.algoInfo['param'])
        #check parameter definition matching
        for param in self.paramDef["param"]:
            if param["name"] not in rawParam:
                raise Exception(f'[getParam] Param {param["name"]} not given')
            value=rawParam[param["name"]]
            if param["type"]=='int':
                if int(value)!=value:
                    raise Exception(f'[getParam] Param {param["name"]} should be int')
                if param['lowerbound']<=value<=param['upperbound']:
                    raise Exception(f'[getParam] Param {param["name"]} not in range {param["lowerbound"]}~{param["upperbound"]}')
            if param["type"]=='float':
                if param['lowerbound']<=value<=param['upperbound']:
                    raise Exception(f'[getParam] Param {param["name"]} not in range {param["lowerbound"]}~{param["upperbound"]}')
            if param["type"]=='bool':
                if value!=1 and value!=0:
                    raise Exception(f'[getParam] Param {param["name"]} sould be 0 or 1')
            if param["type"]=='enum':
                if value not in param["list"]:
                    raise Exception(f'[getParam] Param {param["name"]} not in options')
            if param["type"]=='string':
                pass
        self.param=rawParam
            pass

    def getData(self):
        rawDf=getDf(self.numFile,self.dataType)
        colType={c["name"]:{"type":c["type"],"classifiable":c["classifiable"]} for c in getColType(self.numFile,self.dataType)}

        #check input columns
        for param in self.paramDef["input"]:
            if param["name"] not in self.inputDict:
                raise Exception(f'[getData] input {param["name"]} not given')
            self.inputData[param["name"]]=[]
            if len(self.inputDict[param["name"]])==0:
                raise Exception(f'[getData] input {param["name"]} can\'t be empty')
            if param["amount"]=="single" and len(self.inputDict[param["name"]])>1:
                raise Exception(f'[getData] input {param["name"]} should contain only 1 column')
            for col in self.inputDict[param["name"]]:
                if col not in colType:
                    raise Exception(f'[getData] input {param["name"]} column {col} not in file')
                if param["type"]=='float':
                    if colType[col]['type']!='float' and colType[col]['type']!='int':
                        raise Exception(f'[getData] input {param["name"]} column {col} should be float or int')
                if param["type"]=='classifiable':
                    if colType[col]['classifiable']!="1":
                        raise Exception(f'[getData] input {param["name"]} column {col} should be classifiable')
                if param["type"]=='string':
                    if colType[col]['type']!='string':
                        raise Exception(f'[getData] input {param["name"]} column {col} should be string')
                if param["type"]=='path':
                    if colType[col]['type']!='path':
                        raise Exception(f'[getData] input {param["name"]} column {col} should be path')
                self.inputData[param["name"]].append(rawDf[col])
            self.inputData[param["name"]]=np.transpose(self.inputData[param["name"]])
    
        # check output columns if action is training or testing
        if self.action=='train' or self.action=='test':
            for param in self.paramDef["output"]:
                if param["name"] not in self.outputDict:
                    raise Exception(f'[getData] output {param["name"]} not given')
                col=self.outputDict[param["name"]]
                if col not in colType:
                    raise Exception(f'[getData] output {param["name"]} column {col} not in file')
                if param["type"]=='float':
                    if colType[col]['type']!='float' and colType[col]['type']!='int':
                        raise Exception(f'[getData] output {param["name"]} column {col} should be float or int')
                if param["type"]=='classifiable':
                    if colType[col]['classifiable']!="1":
                        raise Exception(f'[getData] output {param["name"]} column {col} should be classifiable')
                if param["type"]=='string':
                    if colType[col]['type']!='string':
                        raise Exception(f'[getData] output {param["name"]} column {col} should be string')
                if param["type"]=='path':
                    if colType[col]['type']!='path':
                        raise Exception(f'[getData] output {param["name"]} column {col} should be path')
                self.outputData[col]=rawDf[col]
        self.dataDf=rawDf
    
    #TODO: save model,algoInfo to ./model/mid/
    def saveModel(self):
        #TODO: save model,algoInfo to ./model/mid/
        if self.lib=='keras':
            pass
        elif self.lib=='sklearn':
            pass
        # save algoInfo
        # save resultTxt, result Fig
        self.customSaveModel()

    #TODO: load model,algoInfo
    def loadModel(self):
        #TODO: load model,algoInfo
        pass
    
    # implement in PROJECT
    def buildinVisualize(self):
        '''
        implement in PROJECT
        return [{div,script},{div,script},{div,script}]
        '''
        raise NotImplementedError("buildinVisulize not implemented")
        pass

    # implement in PROJECT if needed
    def customSaveModel(self):
        '''
        implement in PROJECT if needed
        e.g.: save categoricalMapping to ./model/mid/
        '''
        pass

    #implement in PROJECT if needed
    def customLoadModel(self):
        '''
        implement in PROJECT if needed
        e.g. : load categoricalMapping 
        '''
        pass

    #implement in ALGO
    def trainAlgo(self):
        '''
        implement in ALGO
        save model to self.model
        save report string to self.txtRes
        save result to self.result like OUTPUT DATA
        '''
        raise NotImplementedError(f"{self.algoName} Train algo Not implemented")
    
    #implement in ALGO
    def predictAlgo(self):
        '''
        implement in ALGO
        use self.dataDf and self.dataDict to predict
        save result to self.result like OUTPUT DATA
        '''
        raise NotImplementedError(f"{self.algoName} Predict algo Not implemented")
        pass

    # implement in ALGO if needed
    def customVisualize(self):
        '''
        implement in ALGO if needed
        return [{div,script},{div,script},{div,script}]
        '''
        return []
