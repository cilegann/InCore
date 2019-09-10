from service.analyticService.core.analyticCore.analyticBase import analytic
from params import params
from service.analyticService.utils import modelUidGenerator
from service.dataService.utils import getFileInfo,getColType,categoricalConverter,getDf,lockFile,fileUidGenerator
import json
import traceback
import os
import shutil
from utils import sql
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd
from service.visualizeService.core.analyticVizAlgo.heatmap import heatmap
from service.visualizeService.core.analyticVizAlgo.abnormalDot import abnormalDot

class clustering(analytic):
    def __init__(self,algoInfo,fid,action='train',mid=None,testLabel=None):
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
            self.outputData={}
            self.d2c={} # data to category mapping
            self.c2d={} # category to data mapping
            self.model=None #model
            self.result={} # A outputData liked structure
            self.vizRes=None # {"figname":{"div":"bokehDiv","script":"scriptDiv"}}
            self.txtRes=None # "string"
            self.customObj={} #other to-saved variable should place here e.g. text tokenization {"objName":obj}
            self.getParams()
            if action=='test' or action=='predict':
                self.loadModel()
            self.colType={c["name"]:{"type":c["type"],"classifiable":c["classifiable"]} for c in getColType(self.numFile,self.dataType).get()}
            self.getData()
        except Exception as e:
            raise Exception(f'[{self.algoName}][init]{traceback.format_exc()}')

    def predict(self):
        self.dataDf['clust']=self.result['clust']
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
    
    def test(self):
        self.visualize()
        return {"text": self.txtRes, "fig": self.vizRes}

    def projectVisualize(self):
        figs={}
        allInput={}
        for k,v in self.inputDict.items():
            for col in v:
                if self.colType[col]['type']=='float' or self.colType[col]['type']=='int':
                    allInput[col]=self.dataDf[col]
        algo=abnormalDot(allInput,self.result["clust"],"preview")
        algo.doBokehViz()
        algo.getComp()
        figs["Preview"]=algo.component
    