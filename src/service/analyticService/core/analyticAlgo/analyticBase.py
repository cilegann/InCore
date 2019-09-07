import pandas as pd
import numpy as np
from service.dataService.utils import getFileInfo,getColType,categoricalConverter,getDf,lockFile,fileUidGenerator
from service.analyticService.utils import modelUidGenerator
from utils import sql
from params import params
import threading
import traceback
import json
from datetime import datetime
import os
import pickle
from keras.models import load_model
from keras.utils import to_categorical
import shutil

class analytic():
    def __init__(self,algoInfo,fid,action='train',mid=None):
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
            if not mid:
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
                                [col1-row1,col2-row1,....,colN-row1],
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

            ** Note that if the output is a classifiable one by algo's definition, it will be one-hot encoding format i.e [[0,1,0],[1,0,0]] instead of [1,0]
            '''
            self.d2c={} # data to category mapping
            self.c2d={} # category to data mapping
            self.model=None
            self.result=None
            self.vizRes=None
            self.txtRes=None
            self.getParams()
            if action=='test' or action=='train':
                self.loadModel()
            self.colType={c["name"]:{"type":c["type"],"classifiable":c["classifiable"]} for c in getColType(self.numFile,self.dataType)}
            self.getData()
            # the convertion of classifiable data should be implemented in each PROJECT D-class __init__
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
            return self.mid
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
        self.vizRes=self.projectVisualize()
        algoGraphs=self.algoVisualize()
        if len(algoGraphs)!=0:
            #TODO: save np.array to image, generate imgBokeh, add to self.vizRes
            pass

    # inherit in PROJECT to add feature
    def predict(self):
        for param in self.paramDef['output']:
            if param['type']=='classifiable':
                v=self.result[param['name']]
                v=np.argmax(v,axis=1)
                v=[self.c2d[self.outputDict[param['name']]][str(i)] for i in v]
                self.dataDf[self.outputDict[param['name']]]=np.asarray(v)
            else:
                self.dataDf[self.outputDict[param['name']]]=self.result[param['name']]
        for k,v in self.result.items():
            self.dataDf[k]=v
        uid=fileUidGenerator().uid
        if self.dataType=='cv':
            oldNumFileName=self.numFile[self.numFile.rfind("/")+1:]
            numFileType=self.numFile[self.numFile.find("."):]
            newNumFile=os.path.join(self.sysparam.filepath,uid,oldNumFileName)
            newPath=os.path.join(self.sysparam.filepath,uid)
            actionFile=os.path.join(self.sysparam.filepath,uid+'.json')
            shutil.copytree(self.path,newPath)
            self.dataDf.to_csv(newNumFile,index=False)
        else:
            fileType=self.numFile[self.numFile.rfind("."):]
            newNumFile=os.path.join(self.sysparam.filepath,uid+fileType)
            newPath=newNumFile
            if fileType=='.tsv':
                self.dataDf.to_csv(newNumFile,sep='\t',index=False)
            if fileType=='.csv':
                self.dataDf.to_csv(newNumFile,index=False)
        if self.preprocessActionFile:
            actionFile=os.path.join(self.sysparam.filepath,uid+'.json')
            shutil.copyfile(self.preprocessActionFile,actionFile)
        try:
            db=sql()
            if self.preprocessActionFile:
                db.cursor.execute(f"insert into files (`fid`,`dataType`,`path`,`numFile`,`inuse`,`preprocessAction`) values ('{uid}','{self.dataType}','{newPath}','{newNumFile}',False,'{actionFile}','{actionFile}');")
            else:
                db.cursor.execute(f"insert into files (`fid`,`dataType`,`path`,`numFile`,`inuse`) values ('{uid}','{self.dataType}','{newPath}','{newNumFile}',False,'{actionFile}');")
            db.conn.commit()
        except Exception as e:
            raise Exception(e)
        finally:
            db.conn.close()
        return uid
    
    # implement in PROJECT
    def test(self):
        '''
        implement in PROJECT
        call predictAlgo
        call visualize
        generate text to self.txtRes
        '''
        raise NotImplementedError("test not implemented")

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

    def getData(self):
        rawDf=getDf(self.numFile,self.dataType)
        colType=self.colType

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
                    d=rawDf[col]
                if param["type"]=='classifiable':
                    if colType[col]['classifiable']!="1":
                        raise Exception(f'[getData] input {param["name"]} column {col} should be classifiable')
                    d=rawDf[col]
                    if col not in self.d2c:
                        self.d2c[col],self.c2d[col]=categoricalConverter(d,colType[col]['type'])
                    d=np.asarray([self.d2c[col][str(i)] for i in d])
                    d=to_categorical(d)
                if param["type"]=='string':
                    if colType[col]['type']!='string':
                        raise Exception(f'[getData] input {param["name"]} column {col} should be string')
                    d=rawDf[col]
                if param["type"]=='path':
                    if colType[col]['type']!='path':
                        raise Exception(f'[getData] input {param["name"]} column {col} should be path')
                    d=rawDf[col]
                self.inputData[param["name"]].append(d)
            if param['type']=='classifiable':
                self.inputData[param['name']]=self.inputData[param['name']].transpose(1,0,2)
            else:
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
                    d=rawDf[col]
                if param["type"]=='classifiable':
                    if colType[col]['classifiable']!="1":
                        raise Exception(f'[getData] output {param["name"]} column {col} should be classifiable')
                    d=rawDf[col]
                    if col not in self.d2c:
                        self.d2c[col],self.c2d[col]=categoricalConverter(d,colType[col]['type'])
                    d=np.asarray([self.d2c[col][str(i)] for i in d])
                    d=to_categorical(d)
                if param["type"]=='string':
                    if colType[col]['type']!='string':
                        raise Exception(f'[getData] output {param["name"]} column {col} should be string')
                    d=rawDf[col]
                if param["type"]=='path':
                    if colType[col]['type']!='path':
                        raise Exception(f'[getData] output {param["name"]} column {col} should be path')
                    d=rawDf[col]
                self.outputData[col]=d
        self.dataDf=rawDf
    
    # inherit in PROJECT or ALGO to add feature
    def saveModel(self):
        if self.model==None:
            raise Exception(f"[{self.algoName}] Model is none. Abort.")
        try:
            os.mkdir(os.path.join(self.sysparam.modelpath,self.mid))
        except:
            pass
        if self.lib=='keras':
            self.model.save(os.path.join(self.sysparam.modelpath,self.mid,"model.h5"))
            jStr=self.model.to_json()
            with open(os.path.join(self.sysparam.modelpath,self.mid,"model.json"),'w') as file:
                file.write(jStr)
        elif self.lib=='sklearn':
            with open(os.path.join(self.sysparam.modelpath,self.mid,"model.pkl"),'wb') as file:
                pickle.dump(self.model,file)
        with open(os.path.join(self.sysparam.modelpath,self.mid,"algoInfo.pkl"),'wb') as file:
            pickle.dump(self.algoInfo,file)
        with open(os.path.join(self.sysparam.modelpath,self.mid,"preview.pkl"),'wb') as file:
            pickle.dump({"text":self.txtRes,"fig":self.vizRes})
        with open(os.path.join(self.sysparam.modelpath,self.mid,"d2c.json"),'w') as file:
            json.dump(self.d2c,file)
        with open(os.path.join(self.sysparam.modelpath,self.mid,"c2d.json"),'w') as file:
            json.dump(self.c2d,file)

    # inherit in PROJECT or ALGO to add feature
    def loadModel(self):
        if self.lib=='keras':
            self.model=load_model(os.path.join(self.sysparam.modelpath,self.mid,"model.h5"))
        elif self.lib=='sklearn':
            with open(os.path.join(self.sysparam.modelpath,self.mid,"model.pkl"),'rb') as file:
                self.model=pickle.load(file)
        with open(os.path.join(self.sysparam.modelpath,self.mid,"d2c.json")) as file:
            self.d2c=json.load(file)
        with open(os.path.join(self.sysparam.modelpath,self.mid,"c2d.json")) as file:
            self.c2d=json.load(file)
    
    # implement in PROJECT
    def projectVisualize(self):
        '''
        implement in PROJECT
        return [{div,script},{div,script},{div,script}]
        '''
        raise NotImplementedError("projectVisulize not implemented")

    # implement in ALGO
    def trainAlgo(self):
        '''
        implement in ALGO
        save model to self.model
        save report string to self.txtRes
        save result to self.result like OUTPUT DATA
        '''
        raise NotImplementedError(f"{self.algoName} trainAlgo Not implemented")
    
    # implement in ALGO
    def predictAlgo(self):
        '''
        implement in ALGO
        use self.dataDf and self.dataDict to predict
        save result to self.result like OUTPUT DATA
        if the output is classifiable, you should save the "probabily" instead of label i.e [[0.3,0.6,0.1],[0.8,0.05,0.15]] instead of [1,0]
        '''
        raise NotImplementedError(f"{self.algoName} predictAlgo Not implemented")

    # implement in ALGO if needed
    def algoVisualize(self):
        '''
        implement in ALGO if needed
        each visualized image should be converted to a 3D np.array
        return [array1, array2, ..., array3]
        '''
        return []
