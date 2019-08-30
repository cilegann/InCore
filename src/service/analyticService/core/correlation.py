import pandas as pd
import numpy as np
from service.dataService.utils import getFileInfo,getDf,getColType,fileUidGenerator
import logging

class NoDataException(Exception):
    def __init__(self,msg):
        self.message=msg

class correlation():
    def __init__(self,fid,algoName):
        self.fid=fid
        self.algoName=algoName
        _,self.dataType,self.path,self.numFile,_,_=getFileInfo(self.fid)[0]
        colType=getColType(self.numFile,self.dataType).get()
        self.colType={}
        for d in colType:
            self.colType[d['name']]=d['type']
        self.df=getDf(self.numFile,self.dataType).get()
        toDrop=[]
        for k,v in self.colType.items():
            if v!='int' and v!='float':
                toDrop.append(k)
        self.df=self.df.drop(columns=toDrop)
        if len(self.df.columns.tolist())==0:
            raise NoDataException("[Correlation] No numerical columns in this file")
        self.corr=None
        self.component=None

    def do(self):
        self.calculate()
        self.plot()
        return self.component

    def calculate(self):
        raise NotImplementedError(f"[Correlation][{self.algoName}] Not implemented.")
        
    def plot(self):
        pass