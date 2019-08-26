from params import params
from service.dataService.utils import getFileInfo,getDf,getColType,fileUidGenerator
from utils import sql
import logging
import json
import numpy as np
import pandas as pd
import importlib

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
            raise Exception(f"[Preprocess Init]{e}")

    def do(self):
        try:
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
                dataLen=len(v['data'])

            retainIndex=np.asarray([True for i in range(dataLen)])
            for k,v in self.data.items():
                if v['outlierFiltering']!="0" and v['colType']!='string' and v['colType']!='path':
                    module=importlib.import_module(f"service.analyticService.core.preprocessAlgo.outlierFiltering.{v['outlierFiltering']}")
                    algo=getattr(module,v['outlierFiltering'])
                    ri=algo(v['data'],v['outlierFiltering']).getRetainIndex
                    retainIndex=np.logical_and(retainIndex,ri)
            for k,v in self.data.items():
                v['data']=v['data'][retainIndex]
                dataLen=len(v['data'])

            for k,v in self.data.items():
                if v['normalize']!="0" and v['colType']!='string' and v['colType']!='path':
                    module=importlib.import_module(f"service.analyticService.core.preprocessAlgo.normalize.{v['normalize']}")
                    algo=getattr(module,v['normalize'])
                    v['data']=algo(v['data'],v['normalize']).do()
            
            for k,v in self.data.items():
                if v['stringCleaning']!='0' and v['colType']=='string':
                    act=json.loads(v['stringCleaning'])
                    for a in act:
                        module=importlib.import_module(f"service.analyticService.core.preprocessAlgo.stringCleaning.{v['stringCleaning']}")
                        algo=getattr(module,v['stringCleaning'])
                        v['data']=algo(v['data'],v['stringCleaning']).do()
            uid=fileUidGenerator().uid
            newdata={k:v['data'] for k,v in self.data.items()}
            colNames=data.columns.tolist()
            newDf=pd.DataFrame(newdata,columns=colNames)
            db=sql()
            #TODO insert to db
            if self.dataType!='cv':
                fileType=self.numFile[self.numFile.find("."):]
                if fileType=='tsv':
                    newDf.to_csv(os.path.join(self.params.filepath,uid+fileType),sep='\t')
                if fileType=='csv':
                    newDf.to_csv(os.path.join(self.params.filepath,uid+fileType))
            else:
                pass
                #TODO handle cv folder copying
            
            #TODO return uid
        except Exception as e:
            raise Exception(f"[Preprocess Do]{e}")