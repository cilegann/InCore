import pandas as pd
import numpy as np
from service.dataService.utils import getFileInfo,getColType,categoricalConverter,getDf,lockFile,fileUidGenerator
from service.analyticService.utils import modelUidGenerator,changeModelStatus
from service.visualizeService.core.analyticVizAlgo.customImg import customImg
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
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
import logging

class analytic():
    def __init__(self,algoInfo,fid,action='train',mid=None):
        try:
            self.action=action # 'train' / 'preview' / 'test' / 'predict'
            self.algoInfo=algoInfo
            self.sysparam=params()
            self.dataType=self.algoInfo['dataType'] # 'num' / 'cv' / 'nlp'
            self.projectType=self.algoInfo['projectType'] # 'regression' / 'classification' .....
            self.algoName=self.algoInfo['algoName']
            self.fid=fid
            _,dataType,self.path,self.numFile,_,self.preprocessActionFile=getFileInfo(self.fid)[0]
            if dataType!=self.dataType:
                raise Exception(f'{self.fid} has dataType {dataType} but a {self.dataType} file is required')
            self.thread=None
            if not mid:
                self.mid=modelUidGenerator().uid
            else:
                self.mid=mid
            self.paramDef=json.load(open(self.sysparam.analyticServiceRoot+f'core/analyticCore/{self.dataType}/{self.projectType}/{self.algoName}.json'))
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
            self.model=None #model
            self.result={} # A outputData liked structure
            self.vizRes={} # {"figname":{"div":"bokehDiv","script":"scriptDiv"}}
            self.txtRes="" # "string"
            self.formRes={}
            self.customObj={} #other to-saved variable should place here e.g. text tokenization {"objName":obj}
            
            self.getParams()
            if action=='test' or action=='predict':
                self.loadModel()
            self.colType={c["name"]:{"type":c["type"],"classifiable":c["classifiable"]} for c in getColType(self.numFile,self.dataType).get()}
            self.getData()
        except Exception as e:
            raise Exception(f'[{self.algoName}][init]{traceback.format_exc()}')

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
                if not param['lowerBound']<=value<=param['upperBound']:
                    raise Exception(f'[getParam] Param {param["name"]} not in range {param["lowerBound"]}~{param["upperBound"]}')
            if param["type"]=='float':
                if not param['lowerBound']<=value<=param['upperBound']:
                    raise Exception(f'[getParam] Param {param["name"]} not in range {param["lowerBound"]}~{param["upperBound"]}')
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
        rawDf=getDf(self.numFile,self.dataType).get()
        colType=self.colType

        #check input columns
        #BUG: array shape when single
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
                    d=rawDf[col].tolist()
                if param["type"]=='classifiable':
                    if colType[col]['classifiable']!=1:
                        raise Exception(f'[getData] input {param["name"]} column {col} should be classifiable')
                    d=rawDf[col].tolist()
                    if col not in self.d2c:
                        self.d2c[col],self.c2d[col]=categoricalConverter(d,colType[col]['type'])
                    d=np.asarray([self.d2c[col][str(i)] for i in d])
                    d=[np.asarray(i) for i in to_categorical(d)]
                if param["type"]=='string':
                    if colType[col]['type']!='string':
                        raise Exception(f'[getData] input {param["name"]} column {col} should be string')
                    d=rawDf[col].tolist()
                if param["type"]=='path':
                    if colType[col]['type']!='path':
                        raise Exception(f'[getData] input {param["name"]} column {col} should be path')
                    d=rawDf[col].tolist()
                    for di in range(len(d)):
                        d[di]=os.path.join(self.path,d[di])
                self.inputData[param["name"]].append(d)
            if param["amount"]!="single":
                if param['type']=='classifiable':
                    self.inputData[param['name']]=np.asarray(self.inputData[param['name']])
                    try:
                        self.inputData[param['name']]=self.inputData[param['name']].transpose(1,0,2)
                    except:
                        self.inputData[param['name']]=self.inputData[param['name']].transpose()
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
                    d=rawDf[col].tolist()
                if param["type"]=='classifiable':
                    if colType[col]['classifiable']!=1:
                        raise Exception(f'[getData] output {param["name"]} column {col} should be classifiable')
                    d=rawDf[col].tolist()
                    if col not in self.d2c:
                        self.d2c[col],self.c2d[col]=categoricalConverter(d,colType[col]['type'])
                    d=np.asarray([self.d2c[col][str(i)] for i in d])
                    d=to_categorical(d)
                if param["type"]=='string':
                    if colType[col]['type']!='string':
                        raise Exception(f'[getData] output {param["name"]} column {col} should be string')
                    d=rawDf[col].tolist()
                if param["type"]=='path':
                    if colType[col]['type']!='path':
                        raise Exception(f'[getData] output {param["name"]} column {col} should be path')
                    d=rawDf[col].tolist()
                    for di in range(len(d)):
                        d[di]=os.path.join(self.path,d[di])
                self.outputData[param["name"]]=d
        self.dataDf=rawDf

    def train(self):
        try:
            try:
                db=sql()
                db.cursor.execute(f"INSERT INTO `models` (`mid`, `fid`, `dataType`, `projectType`,`algoName`,`status`,`startTime`) VALUES ('{self.mid}', '{self.fid}', '{self.dataType}', '{self.projectType}','{self.algoName}','train','{datetime.now()}');")
                db.conn.commit()
            except Exception as e:
                db.conn.rollback()
                raise Exception(e)
            finally:
                db.conn.close()
            lockFile(self.fid)
            self.thread=threading.Thread(target=self.trainWrapper)
            self.thread.start()
            self.thread.name=str(self.mid)
            return self.mid
        except Exception as e:
            raise Exception(f"[{self.algoName}][train] {traceback.format_exc()}")

    def trainWrapper(self):
        try:
            self.setSession()
            if self.lib=='keras':
                with self.session.as_default():
                    with self.graph.as_default():
                        self.trainAlgo()
            else:
                self.trainAlgo()
            if self.txtRes=="":
                self.predictWrapper()
                try:
                    self.test()
                except Exception:
                    pass
            self.saveModel()
            self.clearSession()
            changeModelStatus(self.mid,"success")
        except Exception as e:
            errormsg=str(e).replace("'","''")
            try:
                db=sql()
                db.cursor.execute(f"UPDATE `models` SET `status`='fail',`failReason`='{errormsg}' WHERE `mid`='{self.mid}';")
                db.conn.commit()
            except Exception as e:
                db.conn.rollback()
                raise Exception(e)
            finally:
                db.conn.close()
            raise Exception(f"{traceback.format_exc()}")
    
    def predictWrapper(self):
        try:
            if self.lib=='keras':
                with self.session.as_default():
                    with self.graph.as_default():
                        self.predictAlgo()
            else:
                self.predictAlgo()
        except Exception as e:
            raise Exception(f"{traceback.format_exc()}")

    def visualize(self):
        try:
            self.vizRes=self.projectVisualize()
        except Exception as e:
            raise Exception(f"[{self.algoName}] projectViz error: {traceback.format_exc()}")
        try:
            algoGraphs=self.algoVisualize()
            if len(algoGraphs)!=0:
                for k,v in algoGraphs.items():
                    if type(v)!=dict:
                        ci=customImg(v)
                        ci.convert()
                        comp=ci.component
                    else:
                        comp=v
                    if k in self.vizRes:
                        self.vizRes[f"{k}-1"]=comp
                    else:
                        self.vizRes[k]=comp
        except Exception as e:
            logging.error(f"[{self.algoName}] custom Viz error: {traceback.format_exc()}")

    # inherit in PROJECT to add feature
    def predict(self):
        self.clearSession()
        for param in self.paramDef['output']:
            if param['type']=='classifiable':
                v=self.result[param['name']]
                v=np.argmax(v,axis=1)
                v=[self.c2d[self.outputDict[param['name']]][str(i)] for i in v]
                self.dataDf[self.outputDict[param['name']]]=np.asarray(v)
            else:
                self.dataDf[self.outputDict[param['name']]]=self.result[param['name']]
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
            newPath=newPath.replace("\\","/")
            newNumFile=newNumFile.replace("\\","/")
            if self.preprocessActionFile:
                actionFile=actionFile.replace("\\","/")
                db.cursor.execute(f"insert into files (`fid`,`dataType`,`path`,`numFile`,`inuse`,`preprocessAction`) values ('{uid}','{self.dataType}','{newPath}','{newNumFile}',False,'{actionFile}');")
            else:
                db.cursor.execute(f"insert into files (`fid`,`dataType`,`path`,`numFile`,`inuse`) values ('{uid}','{self.dataType}','{newPath}','{newNumFile}',False);")
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
    
    # inherit in PROJECT or ALGO to add feature
    def saveModel(self):
        if self.model==None:
            raise Exception(f"[{self.algoName}] Model is none. Abort.")
        try:
            os.mkdir(os.path.join(self.sysparam.modelpath,self.mid))
        except:
            pass
        if self.lib=='keras':
            with self.session.as_default():
                with self.graph.as_default():
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
            pickle.dump({"text":self.txtRes,"fig":self.vizRes,"form":self.formRes},file)
        with open(os.path.join(self.sysparam.modelpath,self.mid,"d2c.json"),'w') as file:
            json.dump(self.d2c,file)
        with open(os.path.join(self.sysparam.modelpath,self.mid,"c2d.json"),'w') as file:
            json.dump(self.c2d,file)
        with open(os.path.join(self.sysparam.modelpath,self.mid,"customObj.pkl"),'wb') as file:
            pickle.dump(self.customObj,file)

    # inherit in PROJECT or ALGO to add feature
    def loadModel(self):
        self.setSession()
        if self.lib=='keras':
            self.model=load_model(os.path.join(self.sysparam.modelpath,self.mid,"model.h5"))
        elif self.lib=='sklearn':
            with open(os.path.join(self.sysparam.modelpath,self.mid,"model.pkl"),'rb') as file:
                self.model=pickle.load(file)
        with open(os.path.join(self.sysparam.modelpath,self.mid,"d2c.json")) as file:
            self.d2c=json.load(file)
        with open(os.path.join(self.sysparam.modelpath,self.mid,"c2d.json")) as file:
            self.c2d=json.load(file)
        with open(os.path.join(self.sysparam.modelpath,self.mid,"customObj.pkl"),'rb') as file:
            self.customObj=pickle.load(file)
    
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
        parameter: self.param
        input data : self.inputData
        output data: self.outputData
        save model to self.model
        save report string to self.txtRes
        save result to self.result like OUTPUT DATA
        '''
        raise NotImplementedError(f"{self.algoName} trainAlgo Not implemented")
    
    # implement in ALGO
    def predictAlgo(self):
        '''
        implement in ALGO
        the model is loaded as self.model
        use self.inputData to predict
        save result to self.result like OUTPUT DATA
        if the output is classifiable, you should save the "probabily" instead of label i.e [[0.3,0.6,0.1],[0.8,0.05,0.15]] instead of [1,0]
        '''
        raise NotImplementedError(f"{self.algoName} predictAlgo Not implemented")

    # implement in ALGO if needed
    def algoVisualize(self):
        '''
        implement in ALGO if needed
        each visualized figure should be converted to a dictionary with figure name as key and figure as value
        valid figure type: (1) Image as 3D np.array (2) Bokeh component {"div":"the div","script":"the script"}
        return example 
        {
            "figure 1 name": np.array,
            "figure 2 name": {
                "div": "the div",
                "script": "the script"
            }
        }
        '''
        return {}
    
    def clearSession(self):
        return 0
        if self.lib=='keras':
            self.session.close()
    
    def setSession(self):
        if self.lib=='keras':
            config = tf.ConfigProto()
            config.gpu_options.allow_growth=True
            self.session= tf.Session(config=config)
            KTF.set_session(self.session)
            # self.session=KTF.get_session()
            self.graph=tf.get_default_graph()
            # self.graph.finalize()
        
