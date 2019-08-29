from params import params
from service.dataService.utils import getFileInfo,getDf,getColType,fileUidGenerator
from utils import sql
import logging
import json
import numpy as np
import pandas as pd
import importlib
import os
import shutil
import traceback

class preprocess():
    def __init__(self,fid,action):
        try:
            self.params=params()
            self.fid=fid
            self.action=action
            fid,self.dataType,self.path,self.numFile,status,actionFile=getFileInfo(self.fid)[0]
            self.colType=getColType(self.numFile,self.dataType).get()
            self.df=getDf(self.numFile,self.dataType).get()
            self.data={}
            for c in self.colType:
                self.data[c['name']]={'colType':c['type']}
                # self.data={"col1":{"type":"int","action":action,"data":data}}
            for c in self.action:
                self.data[c['col']]['missingFiltering']=c['missingFiltering']
                self.data[c['col']]['outlierFiltering']=c['outlierFiltering']
                self.data[c['col']]['normalize']=c['normalize']
                self.data[c['col']]['stringCleaning']=c['stringCleaning']
                self.data[c['col']]['data']=np.asarray(self.df[c['col']])
        except Exception as e:
            raise Exception(f"[Preprocess Init]{traceback.format_exc()}")

    def do(self):
        try:
            dataLen=0
            #missing value filtering
            from service.analyticService.core.preprocessAlgo.missingFiltering import missingFiltering
            for k,v in self.data.items():
                dataLen=len(v['data'])
            if dataLen!=0:
                data=[]
                colType=[]
                for k,v in self.data.items():
                    if v['missingFiltering']=='1':
                        data.append(v['data'])
                        colType.append(v['colType'])
                retainIndex=missingFiltering().getRetainIndex(data,colType,self.path)
                for k,v in self.data.items():
                    self.data[k]['data']=v['data'][retainIndex]
                    if v['colType']=='int':
                        self.data[k]['data']=v['data'].astype(np.int64)
                    dataLen=len(self.data[k]['data'])

            # outlier filtering
            if dataLen!=0:
                retainIndex=np.asarray([True for i in range(dataLen)])
                for k,v in self.data.items():
                    if v['outlierFiltering']!="0" and v['colType']!='string' and v['colType']!='path':
                        module=importlib.import_module(f"service.analyticService.core.preprocessAlgo.outlierFilteringAlgo.{v['outlierFiltering']}")
                        algo=getattr(module,v['outlierFiltering'])
                        ri=algo(v['data']).getRetainIndex()
                        retainIndex=np.logical_and(retainIndex,ri)
                for k,v in self.data.items():
                    self.data[k]['data']=v['data'][retainIndex]
                    dataLen=len(self.data[k]['data'])

            # normalize
            if dataLen!=0:
                for k,v in self.data.items():
                    if v['normalize']!="0" and v['colType']!='string' and v['colType']!='path':
                        module=importlib.import_module(f"service.analyticService.core.preprocessAlgo.normalizeAlgo.{v['normalize']}")
                        algo=getattr(module,v['normalize'])
                        self.data[k]['data']=algo(v['data']).do()
            if dataLen!=0:
                for k,v in self.data.items():
                    if v['stringCleaning']!='0' and v['colType']=='string':
                        act=json.loads(v['stringCleaning'])
                        for a in act:
                            module=importlib.import_module(f"service.analyticService.core.preprocessAlgo.stringCleaningAlgo.{a}")
                            algo=getattr(module,a)
                            self.data[k]['data']=algo(v['data']).do()

            uid=fileUidGenerator().uid
            logging.info(f"[Preprocess Do] New UID: {uid}")
            newdata={k:v['data'] for k,v in self.data.items()}
            colNames=self.df.columns.tolist()
            newDf=pd.DataFrame(newdata,columns=colNames)

            if self.dataType!='cv':
                fileType=self.numFile[self.numFile.rfind("."):]
                newNumFile=os.path.join(self.params.filepath,uid+fileType)
                newPath=newNumFile
                actionFile=os.path.join(self.params.filepath,uid+'.json')
                if fileType=='.tsv':
                    newDf.to_csv(newNumFile,sep='\t',index=False)
                if fileType=='.csv':
                    newDf.to_csv(newNumFile,index=False)
            else:
                oldNumFileName=self.numFile[self.numFile.rfind("/")+1:]
                numFileType=self.numFile[self.numFile.find("."):]
                newNumFile=os.path.join(self.params.filepath,uid,oldNumFileName)
                newPath=os.path.join(self.params.filepath,uid)
                actionFile=os.path.join(self.params.filepath,uid+'.json')
                shutil.copytree(self.path,newPath)
                newDf.to_csv(newNumFile,index=False)
            with open(actionFile,'w') as file:
                json.dump(self.action,file)
            newNumFile=newNumFile.replace("\\","/")
            newPath=newPath.replace("\\","/")
            actionFile=actionFile.replace("\\","/")
            db=sql()
            db.cursor.execute(f"insert into files (`fid`,`dataType`,`path`,`numFile`,`inuse`,`preprocessAction`) values ('{uid}','{self.dataType}','{newPath}','{newNumFile}',False,'{actionFile}');")
            db.conn.commit()
            return uid

        except Exception as e:
            import traceback
            raise Exception(f"[Preprocess Do]{traceback.format_exc()}")