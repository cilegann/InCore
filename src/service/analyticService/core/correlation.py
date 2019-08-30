import pandas as pd
import numpy as np
from service.dataService.utils import getFileInfo,getDf,getColType,fileUidGenerator
import logging
class correlation():
    def __init__(self,fid,algoName):
        self.fid=fid
        self.algoName=algoName
        _,self.dataType,self.path,self.numFile,_,_=getFileInfo(self.fid)[0]
        colType=getColType(self.numFile,self.dataType).get()
        self.colType={}
        for d in colType:
            self.colType[d['name']]=d['type']
        logging.debug(self.colType)
        self.df=getDf(self.numFile,self.dataType).get()
        self.corr=None
        self.component=None
    def calculate(self):
        raise NotImplementedError(f"[Correlation][{self.algoName}] Not implemented.")
    def plot(self):
        pass