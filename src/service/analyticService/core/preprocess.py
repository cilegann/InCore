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
            fid,self.dataType,self.path,self.numFile,status=getFileInfo(self.fid)[0]
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
            #missing value filtering
            from service.analyticService.core.preprocessAlgo.missingFiltering import missingFiltering
            data=[]
            colType=[]
            for k,v in self.data.items():
                if v['missingFiltering']=='1':
                    data.append(v['data'])
                    colType.append(v['colType'])
            retainIndex=missingFiltering().getRetainIndex(data,colType,self.path)
            dataLen=0
            for k,v in self.data.items():
                v['data']=v['data'][retainIndex]
                if v['colType']=='int':
                    v['data']=v['data'].astype(np.int64)
                dataLen=len(v['data'])

            # outlier filtering
            retainIndex=np.asarray([True for i in range(dataLen)])
            for k,v in self.data.items():
                if v['outlierFiltering']!="0" and v['colType']!='string' and v['colType']!='path':
                    module=importlib.import_module(f"service.analyticService.core.preprocessAlgo.outlierFilteringAlgo.{v['outlierFiltering']}")
                    algo=getattr(module,v['outlierFiltering'])
                    ri=algo(v['data']).getRetainIndex()
                    retainIndex=np.logical_and(retainIndex,ri)
            for k,v in self.data.items():
                v['data']=v['data'][retainIndex]
                dataLen=len(v['data'])

            for k,v in self.data.items():
                if v['normalize']!="0" and v['colType']!='string' and v['colType']!='path':
                    module=importlib.import_module(f"service.analyticService.core.preprocessAlgo.normalizeAlgo.{v['normalize']}")
                    algo=getattr(module,v['normalize'])
                    v['data']=algo(v['data']).do()
            
            for k,v in self.data.items():
                if v['stringCleaning']!='0' and v['colType']=='string':
                    act=json.loads(v['stringCleaning'])
                    for a in act:
                        module=importlib.import_module(f"service.analyticService.core.preprocessAlgo.stringCleaningAlgo.{v['stringCleaning']}")
                        algo=getattr(module,v['stringCleaning'])
                        v['data']=algo(v['data']).do()

            uid=fileUidGenerator().uid
            logging.info(f"[Preprocess Do] New UID: {uid}")
            newdata={k:v['data'] for k,v in self.data.items()}
            colNames=self.df.columns.tolist()
            newDf=pd.DataFrame(newdata,columns=colNames)

            if self.dataType!='cv':
                fileType=self.numFile[self.numFile.rfind("."):]
                newNumFile=os.path.join(self.params.filepath,uid+fileType)
                logging.debug(newNumFile)
                newPath=newNumFile
                if fileType=='.tsv':
                    newDf.to_csv(newNumFile,sep='\t',index=False)
                if fileType=='.csv':
                    newDf.to_csv(newNumFile,index=False)
            else:
                oldNumFileName=self.numFile[self.numFile.rfind("/")+1:]
                numFileType=self.numFile[self.numFile.find("."):]
                newNumFile=os.path.join(self.params.filepath,uid,oldNumFileName)
                newPath=os.path.join(self.params.filepath,uid)
                shutil.copytree(self.path,newPath)
                newDf.to_csv(newNumFile,index=False)
            
            db=sql()
            db.cursor.execute(f"insert into files (`fid`,`dataType`,`path`,`numFile`,`inuse`) values ('{uid}','{self.dataType}','{newNumFile}','{newPath}',False);")
            db.conn.commit()
            return uid

        except Exception as e:
            import traceback
            raise Exception(f"[Preprocess Do]{traceback.format_exc()}")