import numpy as np
from PIL import Image

def XYdataGenerator(fileList,yList,height,width,batchSize):
    trainIndex=0
    while(1):
        lowerBound=trainIndex
        if lowerBound+batchSize>len(fileList)-1:
            upperBound=len(fileList)
            trainIndex=0
        else:
            upperBound=lowerBound+batchSize
            trainIndex=upperBound
        todo_fileList=fileList[lowerBound:upperBound]
        y=yList[lowerBound:upperBound]
        x=[]
        for f in todo_fileList:
            img=Image.open(f[0])
            try:
                img=img.resize((width,height))
            except:
                pass
            img=np.asarray(img)
            if len(img.shape)==2 or img.shape[2]==1: #add support for grey scale image
                img=np.stack((img,img,img),axis=2)
            if img.shape[2]>3:
                img=img[:,:,:3]
            img=img.astype('float64')
            img/=255.
            x.append(img)
        x=np.asarray(x)
        yield x,y

def XdataGenerator(fileList,height,width,batchSize):
    trainIndex=0
    while(1):
        lowerBound=trainIndex
        if lowerBound+batchSize>len(fileList)-1:
            upperBound=len(fileList)
            trainIndex=0
        else:
            upperBound=lowerBound+batchSize
            trainIndex=upperBound
        todo_fileList=fileList[lowerBound:upperBound]
        x=[]
        for f in todo_fileList:
            img=Image.open(f[0])
            try:
                img=img.resize((width,height))
            except:
                pass
            img=np.asarray(img)
            if len(img.shape)==2 or img.shape[2]==1: #add support for grey scale image
                img=np.stack((img,img,img),axis=2)
            if img.shape[2]>3:
                img=img[:,:,:3]
            img=img.astype('float64')
            img/=255.
            x.append(img)
        x=np.asarray(x)
        yield x