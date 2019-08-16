import numpy as np
import pandas as pd
import os

class missingFiltering():
    def getNumMissing(self,data,length):
        try:
            if len(data)==0:
                return [False for i in range(length)]
            total=np.sum(data,axis=0)
            return np.isnan(total)
        except Exception as e:
            raise Exception(f'[getNumMissing]{e}')

    def getPathMissing(self,data,length,pathBase):
        try:
            if pathBase==None or len(data)==0:
                return np.asarray([False for i in range(length)])
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

    def getStrMissing(self,data,length):
        try:
            if len(data)==0:
                return np.asarray([False for i in range(length)])
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
            nonNans=np.logical_and(~self.getNumMissing(numData,len(data[0])),np.logical_and(~self.getPathMissing(pathData,len(data[0]),pathBase),~self.getStrMissing(strData,len(data[0]))))
            for i in range(len(data)):
                data[i]=data[i][nonNans]
                if coltype[i]=='int':
                    data[i]=data[i].astype(np.int64)
            return data
        except Exception as e:
            raise Exception(f'[filtCols]{e}')

    def getIndex(self,data,coltype,doList,pathBase=None):
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
            nonNans=np.logical_and(~self.getNumMissing(numData,len(data[0])),np.logical_and(~self.getPathMissing(pathData,len(data[0]),pathBase),~self.getStrMissing(strData,len(data[0]))))
            return nonNans
        except Exception as e:
            raise Exception(f'[filtCols]{e}')