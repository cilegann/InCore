from params import params
from service.dataService.utils import getFileInfo,getDf,getColType
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
            # for k,v in self.data.items():
            #     if v['outlierFiltering']!="0":
            #         #TODO
            #         module=importlib.import_module(f"service.analyticService.core.preprocessAlgo.outlierFiltering.{v['outlierFiltering']}")
            #         algo=getattr(module,v['outlierFiltering'])
            #         
            #filt outlier row

            for c in self.data:
                pass # normalize
            
            for c in self.data:
                pass # clean string
            
            # generate uid
            
            # generate new df
            
            # write new df to uid file
            
            # return uid
        except Exception as e:
            raise Exception(f"[Preprocess Do]{e}")