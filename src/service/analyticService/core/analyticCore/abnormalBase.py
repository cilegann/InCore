from service.analyticService.core.analyticCore.analyticBase import analytic
from service.analyticService.core.analyticCore.evaluateTools import classificationReport
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

'''
prediction result should be saved to self.result['label'] as a 1D np array which composed of -1 and 1
'''

class abnormal(analytic):
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
            self.d2c={"label":{"-1":1,"1":0}} # data to category mapping
            self.c2d={"label":{"0":1,"1":-1}} # category to data mapping
            self.model=None #model
            self.result={} # A outputData liked structure
            self.vizRes={} # {"figname":{"div":"bokehDiv","script":"scriptDiv"}}
            self.txtRes="" # "string"
            self.customObj={} #other to-saved variable should place here e.g. text tokenization {"objName":obj}
            if action=='test':
                if not testLabel:
                    raise Exception("test label must be given under abnormal testing mode")
                self.outputDict={"label":testLabel}
                self.paramDef["output"]=[{"name":"label","type":"classifiable"}]
            if action=='predict':
                self.outputDict={"label":"label"}
                self.paramDef["output"]=[{"name":"label","type":"classifiable"}]
            self.getParams()
            if action=='test' or action=='predict':
                self.loadModel()
            self.colType={c["name"]:{"type":c["type"],"classifiable":c["classifiable"]} for c in getColType(self.numFile,self.dataType).get()}
            self.getData()
        except Exception as e:
            raise Exception(f'[{self.algoName}][init]{traceback.format_exc()}')

    def predict(self):
        self.clearSession()
        self.dataDf['label']=self.result['label']
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
        if self.action=='test':
            self.clearSession()
        if self.action=='train':
            self.txtRes=""
        elif self.action=="test":
            self.txtRes += f"label:\n"
            realTmp=self.outputData["label"]
            predicted=self.result["label"]
            real=[]
            for r in realTmp:
                real.append(self.c2d["label"][str(np.argmax(r))])
            label=[-1,1]
            self.txtRes += f"  Report:\n{classificationReport(real,predicted,label=label)}"
        self.visualize()
        return {"text": self.txtRes, "fig": self.vizRes}

    def projectVisualize(self):
        figs={}
        if self.action=='test':
            real=[]
            for r in self.outputData["label"]:
                real.append(str(self.c2d["label"][str(np.argmax(r))]))
            predicted=[str(i) for i in self.result["label"]]
            label=["-1","1"]
            cmx=confusion_matrix(real,predicted,labels=label)
            cmx=cmx.astype('float')/cmx.sum(axis=1)[:,np.newaxis]
            df=pd.DataFrame(cmx,columns=label)
            algo=heatmap(df,f"confusion matrix of label",color='blue',xName='predict',yName='real')
            algo.doBokehViz()
            algo.getComp()
            figs[f"confusion matrix of label"]=algo.component
        allInput={}
        for k,v in self.inputDict.items():
            for col in v:
                if self.colType[col]['type']=='float' or self.colType[col]['type']=='int':
                    allInput[col]=self.dataDf[col]
        algo=abnormalDot(allInput,self.result["label"],"preview")
        algo.doBokehViz()
        algo.getComp()
        figs["Preview"]=algo.component
        return figs
    