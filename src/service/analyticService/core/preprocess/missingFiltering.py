import numpy as np
import pandas as pd
import os

class missingFiltering():
    def getNumMissing(self,data):
        try:
            total=np.sum(data,axis=0)
            return np.isnan(total)
        except Exception as e:
            raise Exception(f'[getNumMissing]{e}')

    def getPathMissing(self,data,pathBase):
        try:
            if pathBase==None:
                raise Exception(f'[getPathMissing] pathBase cant be None')
            nan=[]
            for j in range(len(data[0])):
                nan.append(False)
                for i in range(len(data)):
                    if pd.isnull(data[i][j]):
                        nan[j]=True
                    elif not os.path.exists(os.path.join(pathBase,data[i][j])):
                        nan[j]=True
            return np.asarray(nan)
        except Exception as e:
            raise Exception(f'[getPathMissing]{e}')

    def getStrMissing(self,data):
        try:
            rawNan=pd.isnull(data)
            nan=np.any(rawNan,axis=0)
            return np.asarray(nan)
        except Exception as e:
            raise Exception(f'[getStrMissing]{e}')

    def filtCols(self,data,coltype,doList,pathBase=None):
        try:
            numData=[]
            pathData=[]
            strData=[]
            for d,t,do in zip(data,coltype,doList):
                if t=="string" and do:
                    strData.append(d)
                elif t=="path" and do:
                    pathData.append(d)
                elif (t=='int' or t =='float') and do:
                    numData.append(d)
            nonNans=np.asarray([True for i in range(len(data[0]))])
            if len(numData)!=0:
                nonNans=np.logical_and(nonNans,~self.getNumMissing(numData))
            if len(pathData)!=0:
                nonNans=np.logical_and(nonNans,~self.getPathMissing(pathData,pathBase))
            if len(strData)!=0:
                nonNans=np.logical_and(nonNans,~self.getStrMissing(strData))
            for i in range(len(data)):
                data[i]=data[i][nonNans]
                if coltype[i]=='int':
                    data[i]=data[i].astype(np.int64)
            return data
        except Exception as e:
            raise Exception(f'[filtCols]{e}')

    def getRetainIndex(self,data,coltype,pathBase=None):
        try:
            numData=[]
            pathData=[]
            strData=[]
            for d,t in zip(data,coltype):
                if t=="string":
                    strData.append(d)
                elif t=="path":
                    pathData.append(d)
                elif (t=='int' or t =='float'):
                    numData.append(d)
            nonNans=np.asarray([True for i in range(len(data[0]))])
            if len(numData)!=0:
                nonNans=np.logical_and(nonNans,~self.getNumMissing(numData))
            if len(pathData)!=0:
                nonNans=np.logical_and(nonNans,~self.getPathMissing(pathData,pathBase))
            if len(strData)!=0:
                nonNans=np.logical_and(nonNans,~self.getStrMissing(strData))
            return nonNans
        except Exception as e:
            raise Exception(f'[filtCols]{e}')