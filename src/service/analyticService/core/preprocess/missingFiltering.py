import numpy as np
import pandas as pd
import os

def getNumMissing(data,length):
    try:
        if len(data)==0:
            return [False for i in range(length)]
        total=np.sum(data,axis=0)
        return np.isnan(total)
    except Exception as e:
        raise Exception(f'[getNumMissing]{e}')

def getPathMissing(data,length,pathBase):
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

def getStrMissing(data,length):
    try:
        if len(data)==0:
            return np.asarray([False for i in range(length)])
        rawNan=pd.isnull(data)
        nan=np.any(rawNan,axis=0)
        return np.asarray(nan)
    except Exception as e:
        raise Exception(f'[getStrMissing]{e}')

def filtCols(data,coltype,pathBase=None):
    try:
        numData=[]
        pathData=[]
        strData=[]
        for d,t in zip(data,coltype):
            if t=="string":
                strData.append(d)
            elif t=="path":
                pathData.append(d)
            elif t=='int' or t =='float':
                numData.append(d)
        nonNans=np.logical_and(~getNumMissing(numData,len(data[0])),np.logical_and(~getPathMissing(pathData,len(data[0]),pathBase),~getStrMissing(strData,len(data[0]))))
        for i in range(len(data)):
            data[i]=data[i][nonNans]
            if coltype[i]=='int':
                data[i]=data[i].astype(np.int64)
        return data
    except Exception as e:
        raise Exception(f'[filtCols]{e}')